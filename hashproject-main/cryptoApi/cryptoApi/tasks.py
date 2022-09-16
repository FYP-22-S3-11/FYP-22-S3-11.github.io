import celery
import importlib


class CustomClsTask(celery.Task):

    def delay(self, *args, **kwargs):
        try:
            return super(CustomClsTask, self).delay(*args, **kwargs)
        except Exception:
            # module = __import__('.'.join(
            # self.__class__.name.split('.')[0:-1]))
            # func = getattr(module, self.__class__.name.split('.')[-1])
            # func(*args, **kwargs)
            mymethod = getattr(
                importlib.import_module(
                    '.'.join(self.__class__.name.split('.')[0:-1])
                ),
                self.__class__.name.split('.')[-1]
            )
            mymethod(*args, **kwargs)
            return True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
