"""Static analysis endpoint behind the "Check Dominance" page.

Uploads here are untrusted input, so the analysis is static: pylint for code
quality and detect_secrets for leaked credentials. Running an upload, either
through node (Naked) or in-process (js2py), is gated behind
settings.DOMINANCE_ALLOW_JS_EXECUTION, which is off by default; the endpoint
is unauthenticated, so with execution on it is remote code execution for
anyone who can reach it.
"""

import os
import shutil
import tempfile
import time
import zipfile
from io import StringIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings
from pylint.lint import Run
from pylint.reporters.text import TextReporter


# Limits applied before any work is done on an upload.
ALLOWED_SUFFIXES = ('.js', '.py', '.zip')
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_ZIP_MEMBERS = 200
MAX_ZIP_TOTAL_BYTES = 20 * 1024 * 1024


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def js_execution_enabled():
    return bool(getattr(settings, 'DOMINANCE_ALLOW_JS_EXECUTION', False))


def reject_upload(upload):
    """Return a reason to refuse this upload, or None to accept it."""
    name = os.path.basename(upload.name or '')
    if not name:
        return "file has no name"
    if not name.lower().endswith(ALLOWED_SUFFIXES):
        return f"{name}: only {', '.join(ALLOWED_SUFFIXES)} files are accepted"
    if upload.size is not None and upload.size > MAX_UPLOAD_BYTES:
        return f"{name}: larger than the {MAX_UPLOAD_BYTES // (1024 * 1024)}MB limit"
    return None


def save_upload(upload, workdir):
    """Save one upload inside workdir and return its full path.

    The stored name is basename()d before it reaches storage, so a name like
    '../../settings.py' cannot write outside workdir.
    """
    fs = FileSystemStorage(location=workdir)
    stored = fs.save(os.path.basename(upload.name), upload)
    return os.path.join(workdir, stored)


def optimize_code(path):
    data = {'errors': None, 'time': 0}
    pylint_output = StringIO()  # Custom open stream
    reporter = TextReporter(pylint_output)
    start = time.time()
    Run(['--enable=all', path], reporter=reporter, exit=False)
    end = time.time()
    data['errors'] = pylint_output.getvalue()
    data['time'] = end - start
    return data


def detect_secrets_in(path):
    secrets = SecretsCollection()
    with default_settings():
        secrets.scan_file(path)
    res = secrets.json()
    findings = res.get(path) if res else None
    if findings:
        return {'lineNo': findings[0]['line_number']}
    return None


def optimization_response(path):
    response = optimize_code(path)
    display_name = os.path.basename(path)
    response_dict = {'optimization': {}, 'rated': None,
                     'time': response['time'],
                     'fileName': display_name,
                     'visualization_data': {'text': display_name, 'value': response['time']},
                     'secret_data': None}
    index = 1
    for res in response['errors'].split("\n"):
        if 'rated' in res:
            response_dict['rated'] = res.strip()
            continue
        if ':' not in res:
            continue
        actual_res = res.split(':')
        if len(actual_res) >= 5:
            response_dict['optimization'][index] = actual_res[4] + ' LINE NO.' + actual_res[1]
            index += 1

    response_dict['secret_data'] = detect_secrets_in(path)
    return response_dict


def is_js_file(filename):
    return filename.lower().endswith(('.js', '.py'))


def is_zipped_file(filename):
    return filename.lower().endswith('.zip')


def safe_extract(zip_path, dest):
    """Extract zip_path into dest, refusing members that escape it.

    zipfile.extractall() honours '../' and absolute paths in member names, so
    an uploaded archive could previously write anywhere the server user could
    write (Zip Slip). Member count and total expanded size are capped too.
    """
    dest_real = os.path.realpath(dest)
    with zipfile.ZipFile(zip_path) as archive:
        members = [m for m in archive.infolist() if not m.is_dir()]
        if len(members) > MAX_ZIP_MEMBERS:
            raise ValueError(f"archive holds more than {MAX_ZIP_MEMBERS} files")
        if sum(m.file_size for m in members) > MAX_ZIP_TOTAL_BYTES:
            raise ValueError("archive expands to more than the permitted size")

        for member in members:
            target = os.path.realpath(os.path.join(dest_real, member.filename))
            if target != dest_real and not target.startswith(dest_real + os.sep):
                raise ValueError(
                    f"refusing archive member outside the target directory: {member.filename}")
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with archive.open(member) as src, open(target, 'wb') as dst:
                shutil.copyfileobj(src, dst)


def optimize_zip(zip_path, workdir):
    response = {}
    extract_root = os.path.join(workdir, 'extracted')
    os.makedirs(extract_root, exist_ok=True)
    safe_extract(zip_path, extract_root)

    for path, _subdirs, files in os.walk(extract_root):
        for name in files:
            if name.endswith('.js') and not name.endswith(('.json', '.map')):
                full = os.path.join(path, name)
                # keyed by the path inside the archive, not the server's temp dir
                response[os.path.relpath(full, extract_root)] = optimization_response(full)
    return response


def optimize_methods(path):
    """Time each function in an uploaded script by running it.

    Off unless DOMINANCE_ALLOW_JS_EXECUTION is set: this evaluates code that
    an unauthenticated caller supplied.
    """
    if not js_execution_enabled():
        return []

    import js2py  # imported lazily so the default path never loads it

    data = []
    with open(path, 'r') as handle:
        lines = handle.readlines()

    method_def = []
    method_calls = []
    func = False
    block = ''
    block_def = ''
    for line in lines:
        if 'function' in line:
            func = True

        if '}' in line:
            block += line.replace('\n', '')
            block_def += line
            func = False
            method_def.append(block_def)
            block = ''
            block_def = ''
            continue
        block += line.replace('\n', '')
        block_def += line

        if not func and '(' in line and ')' in line:
            method_calls.append(line.strip())

    for index, method in enumerate(method_calls):
        if index >= len(method_def):
            break
        js = method_def[index] + '\n' + method
        startTime = time.time()
        result = js2py.eval_js(js.replace("document.write", "return "))
        endTime = time.time()
        data.append({'method': method, 'time': endTime - startTime})
    return data


def optimize_complete_code(path):
    """Run a whole uploaded script through node and time it.

    Off unless DOMINANCE_ALLOW_JS_EXECUTION is set, for the same reason as
    optimize_methods: this executes caller-supplied code.
    """
    if not js_execution_enabled():
        return {}

    from Naked.toolshed.shell import execute_js  # imported lazily

    startTime = time.time()
    execute_js(path)
    endTime = time.time()
    return {'time': endTime - startTime}


class CheckFile(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        result = {"method": 'get'}
        return Response(result)

    def post(self, request, format=None):
        """
        get file and check
        """
        result = {'warning': {'count': 0,
                              'details': []},
                  'error': {'count': 0,
                            'details': []},
                  'dominace': {'count': 0,
                               'details': []},
                  'optimization': [],
                  'time': 0,
                  'fileType': None,
                  'fileName': None,
                  'visualization_data': {'text': None, 'value': None},
                  'secret_data': [],
                  'methods': [],
                  'class_methods': [],
                  'max': 0,
                  }
        uploads = request.FILES.getlist('file', [])
        if not uploads:
            return Response({'detail': 'no file uploaded'},
                            status=status.HTTP_400_BAD_REQUEST)

        for upload in uploads:
            reason = reject_upload(upload)
            if reason:
                return Response({'detail': reason}, status=status.HTTP_400_BAD_REQUEST)

        # A per-request directory, rather than one shared folder emptied on
        # every call: concurrent requests no longer delete each other's
        # uploads, and nothing is left on disk afterwards.
        workdir = tempfile.mkdtemp(prefix='dominance-')
        try:
            if len(uploads) == 1:
                upload = uploads[0]
                path = save_upload(upload, workdir)
                name = os.path.basename(path)

                try:
                    result['methods'] = optimize_methods(path)
                    if result['methods']:
                        result['max'] = max(result['methods'], key=lambda x: x['time'])
                except Exception as err:
                    print("optimize_methods failed:", err)

                try:
                    result['class_methods'] = optimize_complete_code(path)
                except Exception as err:
                    print("optimize_complete_code failed:", err)

                if is_js_file(name):
                    result['fileType'] = 'js'
                    result['fileName'] = name
                    res = optimization_response(path)
                    result['optimization'] = res['optimization']
                    result['rated'] = res['rated']
                    # the page reads 'rate'; kept in step with 'rated'
                    result['rate'] = res['rated']
                    result['time'] = res['time']
                    result['visualization_data']['text'] = name
                    result['visualization_data']['value'] = res['time']
                    result['secret_data'] = detect_secrets_in(path)

                if is_zipped_file(name):
                    result['fileType'] = 'zip'
                    try:
                        result['optimization'] = optimize_zip(path, workdir)
                    except (ValueError, zipfile.BadZipFile) as err:
                        return Response({'detail': str(err)},
                                        status=status.HTTP_400_BAD_REQUEST)
                    result['visualization_data'] = [
                        v['visualization_data'] for v in result['optimization'].values()]
            else:
                result['fileType'] = 'multi'
                complete_res = []
                visualizationData = []

                for upload in uploads:
                    response = {}
                    path = save_upload(upload, workdir)
                    name = os.path.basename(path)

                    if is_js_file(name):
                        response['fileType'] = 'js'
                        response['fileName'] = name
                        res = optimization_response(path)
                        response['optimization'] = res['optimization']
                        response['rated'] = res['rated']
                        response['rate'] = res['rated']
                        response['time'] = res['time']
                        response['secret_data'] = res['secret_data']
                        visualizationData.append({'text': name, 'value': res['time']})

                    if is_zipped_file(name):
                        response['fileType'] = 'zip'
                        try:
                            response['optimization'] = optimize_zip(path, workdir)
                        except (ValueError, zipfile.BadZipFile) as err:
                            return Response({'detail': str(err)},
                                            status=status.HTTP_400_BAD_REQUEST)
                        for v in response['optimization'].values():
                            visualizationData.append(v['visualization_data'])

                    complete_res.append(response)
                result['optimization'] = complete_res
                result['visualization_data'] = visualizationData
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

        return Response({'result': result})
