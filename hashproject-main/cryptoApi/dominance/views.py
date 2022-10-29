
from re import sub
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.core.files.storage import FileSystemStorage
from io import StringIO
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import time
import shutil
import zipfile
import json

from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings

# from requests_html import HTML

import js2py
from Naked.toolshed.shell import execute_js, muterun_js


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def optimize_code(filename):
    data = {'errors': None,'time':0}
    pylint_output = StringIO()  # Custom open stream
    reporter = TextReporter(pylint_output)
    start = time.time()
    Run(['--enable=all',filename], reporter=reporter, exit=False)
    end = time.time()    
    data['errors'] = pylint_output.getvalue()
    data['time'] = end - start
    return data

def optimization_response(filename, name= None, folder = None):
    response = optimize_code(filename)
    opt_response = []
    response_dict = {'optimization': {},'rated':None, 
                    'time':response['time'],
                    'fileName': filename,
                    'visualization_data' : {'text': filename.rsplit('/')[-1], 'value': response['time']  },
                    'secret_data': None}
    response = response['errors'].split("\n")
    index = 1
    for res in response:
        if ':' in res:
            actual_res = res
            actual_res = actual_res.split(':')
            if len(actual_res) >=4:
                response_dict['optimization'][index] = actual_res[4] + ' LINE NO.' + actual_res[1]
                index+=1
            elif 'rated' in res:
                response_dict['rated'] = res
            opt_response.append(actual_res)

    response_dict['secret_data'] = detectSecrets(name, folder)
    return response_dict

def isJsFile(filename):
    if '.js' in filename:
        return True
    elif '.py' in filename:
        return True
    else:
        return False

def isZippedFile(filename):
    if '.zip' in filename:
        return True
    else:
        return False

def optimize_zip(filename,folder):
    response = {}
    with zipfile.ZipFile(folder+filename, 'r') as zip_ref:
        zip_ref.extractall(folder)

    for path, subdirs, files in os.walk(folder):
        for name in files:
            if '.js' in name and '.json' not in name and '.map' not in name:
                # print("--------path", path)
                # print("------- subdir", subdirs)
                if len(path) > 10:
                    res = optimization_response(path+ '/' + name, name, path)
                    response[path+ '/' + name] = res
                else:
                    res = optimization_response(path+name, name, path)
                    response[path+name] = res

                
    # return

    ## openeing all files
    # for f in os.listdir(folder):
    #     if '.js' in f:
    #         res = optimization_response(folder+f)
    #         response[f] = res
    # print("-----------------------response",response)
    return response

def detectSecrets(filename, folder):   
    secrets = SecretsCollection()
    with default_settings():
        if(folder[len(folder)-1] != '/'):
            secrets.scan_file(folder+'/'+filename)
        else:
            secrets.scan_file(folder+filename)
    res = secrets.json()
    if res:
        if(folder[len(folder)-1] != '/'):
            return {'lineNo': res[folder+'/'+filename][0]['line_number']}
        else:
            return {'lineNo': res[folder+filename][0]['line_number']}
    else:
        return None


def getTimeExecution():
    time = {}
    return time

def optimizeCompleteCode(folder, filename):
    data = {}
    file1 = open(folder+filename, 'r')

    ## Getting all functions and results
    lines = file1.read()
    # result = muterun_js(folder+filename)
    # print("-------lines", lines)
    startTime = time.time()
    result = execute_js(folder+filename)
    endTime = time.time()
    # print("-------1111result", result)
    # if result:
    #     print("------true")
    # print("-------1111result", result.__dir__())
    
    return data


def findDominancy(data):
    new_data = data
    max = data[0]['time']
    new_data[0]['dominant'] = True
    index = 0
    for dt in data:
        if max < dt['time']:
            print("------yes")
            new_data['dominant'] = True
        else:
            new_data['dominant'] = False
        index+=1
        
    return new_data




def optimizeMethods(folder, filename):
    data = []
    file1 = open(folder+filename, 'r')
    ## Getting all functions and results
    methods = []
    method_def = []
    method_names = []
    method_calls = []
    method_execution_time = []
    lines = file1.readlines()
    func = False
    str = ''
    str_def = ''
    for line in lines:
        if 'function' in line:
            func= True
            ln = line.split('function ')[1]
            ln = ln.split('(')[0]
            method_names.append(ln)

        if '}' in line:
            str+=line.replace('\n','')
            str_def+=line
            func = False
            methods.append(str)
            method_def.append(str_def)
            str =''
            continue
        str+=line.replace('\n','')
        str_def+=line

        ##getting method calls
        if not func and '(' in line and ')' in line:
            method_calls.append(line.strip())
    index = 0
    for method in method_calls:
        dt = {}
        method_definition = method_def[index]
        startTime = time.time()
        js = method_definition + '\n'+ method
        result = js2py.eval_js(js.replace("document.write", "return "))
        endTime = time.time()
        execTime = endTime - startTime
        index+=1
        dt ={'method': method, 'time': execTime}
        data.append(dt)
    return data

class CheckFile(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        result = {"method":'get'}     
        return Response(result)

    def post(self, request, format=None):
        """
        get file and check
        """
        result = {'warning': {'count':0,
                            'details': [] },
                'error': {'count': 0,
                            'details':[] },
                'dominace' : {'count' : 0,
                            'details' :[] },
                'optimization': [],
                'time': 0,
                'fileType': None,
                'fileName': None,
                'visualization_data' : {'text': None, 'value': None},         
                'secret_data' : [],
                'methods' : [],
                'class_methods' : [],
                'max': 0,
                }
        file_obj = request.FILES.getlist('file',[])
        # dir = '/home/crytopcompare/cryptoApi/my_folder/'
        dir = 'my_folder/'

        ##delete previous/extra files
        try:
            for f in os.listdir(dir):
                try:
                    os.remove(os.path.join(dir, f))
                except:
                    shutil.rmtree(os.path.join(dir, f))
        except Exception as e:
            print("error",e)


        ### check if multiple files
        if len(file_obj) == 1:
            file_obj = file_obj[0]
            
            ## saving file
            fs = FileSystemStorage(location=dir)
            filename = fs.save(file_obj.name, file_obj)

            ###testing
            try:
                result['methods'] = optimizeMethods(dir, file_obj.name)
                result['max'] = max(result['methods'], key=lambda x:x['time'])
            except Exception as e:
                print("error 275")

            try:
                result['class_methods'] = optimizeCompleteCode(dir, file_obj.name)
            except Exception as e:
                print("error 280", e)
            ### testing ends



            ## getting upload type
            if isJsFile(file_obj.name):
                result['fileType'] = 'js'
                result['fileName'] = filename
                ## optimization starts
                res = optimization_response(dir+filename, filename, dir)
                result['optimization'] = res['optimization']
                result['rated'] = res['rated'] 
                result['time'] = res['time']
                result['visualization_data']['text'] = filename
                result['visualization_data']['value'] = res['time']
                result['secret_data'] = detectSecrets(filename, dir)
                ## optimization ends  
            
            if isZippedFile(file_obj.name):
                result['fileType'] = 'zip'         
                result['optimization'] = optimize_zip(file_obj.name,dir)
                visualizationData = []
                for k,v in result['optimization'].items():
                    visualizationData.append(v['visualization_data'])
                result['visualization_data'] = visualizationData
        else:
            result['fileType'] = 'multi'
            complete_res = [] 
            visualizationData = []  

            ##saving files
            for obj in file_obj:
                response = {}
                
                ## saving file
                fs = FileSystemStorage(location=dir)
                filename = fs.save(obj.name, obj)

                ## getting upload type
                if isJsFile(obj.name):
                    response['fileType'] = 'js'
                    response['fileName'] = obj.name
                    ## optimization starts
                    res = optimization_response(dir+filename)
                    response['optimization'] = res['optimization']
                    response['rated'] = res['rated'] 
                    response['time'] = res['time']
                    # response['visualization_data']['text'] = obj.name
                    # response['visualization_data']['value'] = res['time']
                    visualizationData.append({'text': obj.name, 'value': res['time']})
                    ## optimization ends  
                
                if isZippedFile(obj.name):
                    response['fileType'] = 'zip'           
                    response['optimization'] = optimize_zip(obj.name,dir)                    
                    for k,v in response['optimization'].items():
                        visualizationData.append(v['visualization_data'])

                complete_res.append(response)
            result['optimization'] = complete_res
            result['visualization_data'] = visualizationData 

            
        
        # print("------get secrets start")
        
        # secrets = SecretsCollection()
        # with default_settings():
        #     secret_used = secrets.scan_file('dominance/views.py')
        # print("--------secr", secret_used)
        # import json
        # print(json.dumps(secrets.json(), indent=2))

        # print("-------secret ends")            

        return Response({'result':result})