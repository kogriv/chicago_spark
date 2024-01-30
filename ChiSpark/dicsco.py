import dictan
from mylog import MyLogger

dicscolog = MyLogger('dicscolog')
dlev = 30 # level for msg

dictan = dictan.DictAnalyzer(dicscolog)

#dicscolog.mylev(dlev,'---dict(globals())-origin---------------------')
#dicscolog.mylev(dlev,dict(globals()))
dicscolog.mylev(dlev,'---dict(globals())-serial---------------------')
dictan.print_dict(dict(globals()))
dicscolog.mylev(dlev,'---dict(locals())--serial---------------------')
#dicscolog.mylev(dlev,dict(locals()))
dictan.print_dict(dict(locals()))


locals_dict_1 = dict(locals())
globals_dict_1 = dict(globals())
#locinfo = dictan.dict_info(dict(locals()),True)
#glo = dict(globals())
# gloinfo, locinfo = 
#dictan.dict_info(dict(globals()),True),\
# dictan.dict_info(dict(locals()),True)


# Для глобальных переменных
# print("local_scope_defined = \\")
dicscolog.mylev(dlev,"----------------------------------------------")
dicscolog.mylev(dlev,"------- ---- ------- ----------- -------------")
dicscolog.mylev(dlev,"------- ---- ------- ----------- -------------")
dicscolog.mylev(dlev,"----------------------------------------------")

#kv, k, d1, d2 = 
dictan.compare_dicts_info(dictan.dict_info(dict(globals()),False),
                          dictan.dict_info(dict(locals()),False),
                          False,
                          'direct',
                          True)


dicscolog.mylev(dlev,'---dict(globals())-----------------------------')
#dicscolog.mylev(dlev,dict(globals()))
dictan.print_dict(dict(globals()))
dicscolog.mylev(dlev,'---dict(locals())-----------------------------')
#dicscolog.mylev(dlev,dict(locals()))
dictan.print_dict(dict(locals()))
# gloinfo, locinfo = 
#dictan.dict_info(dict(globals()),True),\
#dictan.dict_info(dict(locals()),True)
"""
dicscolog.mylev(dlev,"---kv-----------------------------------------")
dicscolog.mylev(dlev,kv)
dicscolog.mylev(dlev,"---k------------------------------------------")
dicscolog.mylev(dlev,k)
dicscolog.mylev(dlev,"---d1-----------------------------------------")
dicscolog.mylev(dlev,d1)
dicscolog.mylev(dlev,"---d2-----------------------------------------")
dicscolog.mylev(dlev,d2)



# Сравниваем результаты функции dict_info для двух словарей


for t in ['direct',
          #'by_name',
          #'by_hash'
          ]:
    compare_type=t
    kv, k, d1, d2 = compare_dicts_info(glodict, locdict, compare_type)
    print("comparing type:",compare_type)
    print("Common keys and values:", kv)
    print("Common keys but different values:", k)
    print("Unique keys and values for dict1:", d1)
    print("Unique keys and values for dict2:", d2)
    print("----------------------------")


# Для локальных переменных
print("local_scope_defined = \\")
print("{")
for key, value in loc.items():
    key_id = id(key)
    key_type = type(key).__name__
    value_id = id(value)
    value_type = type(value).__name__
    key_hash = hash(key) if isinstance(key, (int, str, tuple, frozenset)) else None
    print(f"    '{key}': {{'value': {repr(value)}, 'key_id': {key_id}, 'key_type': '{key_type}', 'key_hash': {key_hash}, 'value_id': {value_id}, 'value_type': '{value_type}'}},")
print("}")
"""