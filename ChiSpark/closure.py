import dictan
from mylog import MyLogger

lg = MyLogger('scopylogger','INFO')
ll = 30

da = dictan.DictAnalyzer(lg,ll)

globals_dict_core, \
locals_dict_core = dict(globals()), dict(locals())
print("Global scope dict globals():")
da.print_dict(globals_dict_core,0,False,False)
print('------------------------------------------')
print("Local scope dict locals():")
da.print_dict(locals_dict_core,0,False,False)
print('------------------------------------------')
#print("Local scope list dir():", dir())
#print('------------------------------------------')

def outer_func(name,old,weight):
    nested_var_in_outer_func = 'nested_var_in_OUTER_func_value'
    lg.mylev(ll,"outer_func for: " + str(name) + ", " +\
             str(old) + ", weight: "+ str(weight))
    lg.mylev(ll,"------------------------------------------")
    globals_dict_before_closure, \
    locals_dict_before_closure = dict(globals()), dict(locals())
    lg.mylev(ll,"-----comparing-globals-core-vs-globals-in-outer-func---------")
    da.compare_dicts_info(
                        da.dict_info(globals_dict_core),
                        da.dict_info(globals_dict_before_closure),
                        False,'direct',True
                        )

    lg.mylev(ll,"------locals-core-----------------------------")
    da.print_dict(locals_dict_core)
    lg.mylev(ll,"------locals-in-outer-before-closure--------------")
    da.print_dict(locals_dict_before_closure)
    lg.mylev(ll,"-----comparing-locals-core-vs-locals-in-outer-func---------")
    da.compare_dicts_info(
                        da.dict_info(locals_dict_core),
                        da.dict_info(locals_dict_before_closure),
                        False,'direct',True
                        )


    def nested_func():
        nested_var_in_nested_func = 'nested_var_in_NESTED_func_value'
        lg.mylev(ll,"Name, " + name + ", old: " + old)
        nested_var_in_outer_func_modified_in_nested = \
            nested_var_in_outer_func + "_modified"
        
        globals_dict_in_closure, \
        locals_dict_in_closure = dict(globals()), dict(locals())

        lg.mylev(ll,"-----comparing-globals-in-outer-vs-globals-in-nested-func---------")
        da.compare_dicts_info(da.dict_info(globals_dict_before_closure),
                              da.dict_info(globals_dict_in_closure),
                              False,'direct',True)
        
        lg.mylev(ll,"-----comparing-locals-outer-vs-locals-in-nested-func---------")
        da.compare_dicts_info(da.dict_info(locals_dict_before_closure),
                              da.dict_info(locals_dict_in_closure),
                              False,'direct',True)


    return nested_func


lg.mylev(30,'------------------------------------------')
lg.mylev(30,'----f = outer_func("Ivan","30",80)--------')
f = outer_func("Ivan","30",80)

lg.mylev(30,'------------------------------------------')
lg.mylev(30,'----f()-----------------------------------')
f()

def check_closured(func):
    if '__closure__' in dir(func):
        return True
    return False

def get_func_code_dict(func):
    code_dict = {}
    if '__code__' in dir(func):
        for i in dir(func.__code__):
            code_dict[i] = eval("func.__code__."+i)
            print(i,':',eval("func.__code__."+i))
    else: code_dict['empty_code_for'] = func
    return code_dict

"""
print("Global scope dict globals():", globals())
print('------------------------------------------')
print("Local scope dict locals():", locals())
print('------------------------------------------')
print("Local scope list dir():", dir())
print('------------------------------------------')
print("Scope list of variable 'f':", dir(f))
print('------------------------------------------')

print("Closure f.__closure__:", f.__closure__)
print('------------------------------------------')
print("Local variables f.__code__.co_varnames:", f.__code__.co_varnames)
print('------------------------------------------')
print("Globals f.__globals__:", f.__globals__)
print('------------------------------------------')

"""