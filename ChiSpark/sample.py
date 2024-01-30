import json
import dictan
from mylog import MyLogger

#def print_readable_dict(input_dict):
#    print(json.dumps(input_dict, indent=4))



my_dict = {'__name__': '__main__',
           '__doc__': None,
           '__package__': None,
           '__loader__': '<_frozen_importlib_external.SourceFileLoader object at 0x00000219B04689A0>',
            '__spec__': None,
            '__annotations__': {},
            '__builtins__': "<module 'builtins' (built-in)>",
            '__file__': 'C:\\Users\\user\\documents\\pro\\chicago_spark\\ChiSpark\\dicsco.py',
            '__cached__': None,
            'dictan': '<dictan.DictAnalyzer object at 0x00000219B0537730>',
            'MyLogger': "<class 'mylog.MyLogger'>",
            'dicscolog': "<MyLogger dicscolog (INFO)>",
            'dlev': 30,
            'locals_dict_1':
                {'__name__': '__main__',
                 '__doc__': None,
                 '__package__': None,
                 '__loader__': "<_frozen_importlib_external.SourceFileLoader object at 0x00000219B04689A0>",
                 '__spec__': None,
                 '__annotations__': {},
                 '__builtins__': "<module 'builtins' (built-in)>",
                 '__file__': 'C:\\Users\\user\\documents\\pro\\chicago_spark\\ChiSpark\\dicsco.py',
                 '__cached__': None,
                 'MyLogger': "<class 'mylog.MyLogger'>",
                 'dicscolog': "<MyLogger dicscolog (INFO)>",
                 'dlev': 30
                },
            'globals_dict_1':
                    {'__name__': '__main__',
                     '__doc__': None,
                     '__package__': None,
                     '__loader__': "<_frozen_importlib_external.SourceFileLoader object at 0x00000219B04689A0>",
                     '__spec__': None,
                     '__annotations__': {},
                     '__builtins__': "<module 'builtins' (built-in)>",
                     '__file__': 'C:\\Users\\user\\documents\\pro\\chicago_spark\\ChiSpark\\dicsco.py',
                     '__cached__': None,
                     'dictan': "<dictan.DictAnalyzer object at 0x00000219B0537730>",
                     'MyLogger': "<class 'mylog.MyLogger'>",
                     'dicscolog': "<MyLogger dicscolog (INFO)>",
                     'dlev': 30,
                     'locals_dict_1':
                        {'__name__': '__main__',
                         '__doc__': None,
                         '__package__': None,
                         '__loader__': "<_frozen_importlib_external.SourceFileLoader object at 0x00000219B04689A0>",
                         '__spec__': None,
                         '__annotations__': {},
                         '__builtins__': "<module 'builtins' (built-in)>",
                         '__file__': 'C:\\Users\\user\\documents\\pro\\chicago_spark\\ChiSpark\\dicsco.py',
                         '__cached__': None,
                         'dictan': "<dictan.DictAnalyzer object at 0x00000219B0537730>",
                         'MyLogger': "<class 'mylog.MyLogger'>",
                         'dicscolog': "<MyLogger dicscolog (INFO)>",
                         'dlev': 30
                        }
                    }
            }

        
#my_dict = {'a':1,'b':{'c':3,'d':{'e':5,'f':6}}}

dicscolog = MyLogger('dicscolog')
dlev = 30 # level for msg

da = dictan.DictAnalyzer(dicscolog)

#da.dict_info(my_dict,True)

da.print_dict(my_dict)

da.print_dict(dict(globals()))