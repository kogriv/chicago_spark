def counter(start=0):
    def step():
        nonlocal start
        start += 1
        return start
 
    return step

c1 = counter(10)
c2 = counter()
print(c1(), c2())
print(c1(), c2())
print(c1(), c2())

def say_name(name):
    
    print(c1(), c2())
    print("----------------------------------")
    print("Inside outer function say_name:")
    print("Global scope:", globals())
    print("Local scope:", locals())

    def say_goodbye():

        print(c1(), c2())
        print("----------------------------------")
        print("Inside outer function say_name:")
        print("Global scope:", globals())
        print("Local scope:", locals())

        print("Don't say me goodbye, " + name + "!")
 
    return say_goodbye

root_global_scope = globals()
root_local_scope = locals()
"""
print("----------------------------------")
print("Inside root:")
print("Global scope:", root_global_scope)
print("----------------------------------")
print("Local scope:", root_local_scope)
print("----------------------------------")
"""
def compare_scopes(global_scope, local_scope):
    inside_var = "INSIDE_COMPARE_FUNCTION_VAR"
    
    def inside_func():
        print('local function name:', inside_func.__name__)
        print("inside_var value:", inside_var)
    
    inside_func()
    
    if global_scope == 1 and local_scope == 1:
        # Получаем словари для globals() и locals()
        temp_global_scope = globals()
        temp_local_scope = locals()
        scope_type = "inside function scope"
    else:
        temp_global_scope = global_scope
        temp_local_scope = local_scope
        scope_type = "outer function scope"

    print("----------------------------------")
    print("looking for: ", scope_type)
    print("globals():")
    print(temp_global_scope)
    print()
    print("-----")
    print("locals():")
    print(temp_local_scope)
    print()
    print("-----")
    common_elements ={}
    common_keys = {}
    different_elements = {}
    # Сравнение словарей и вывод результатов
    for k in set(temp_global_scope.keys()):
        if k in set(temp_local_scope.keys()):
            print("equal key: ",k)
            if temp_global_scope[k] == temp_local_scope[k]:
                common_elements[k] = temp_global_scope[k]
            else: common_keys[k] = [temp_global_scope[k],temp_local_scope[k]]
        else:
            print("different key: ",k)
            different_elements[k] = temp_global_scope[k]
    for k in set(temp_local_scope.keys()):
        if k in set(common_elements.keys()) or k in set(common_keys.keys()):
            ...
        else:
            different_elements[k] = temp_local_scope[k]
    

    # common_keys = set(temp_global_scope.keys()) & set(temp_local_scope.keys())
    # common_elements = {key: (temp_global_scope[key], temp_local_scope[key]) for key in common_keys}
    
    # different_keys = set(temp_global_scope.keys()) ^ set(temp_local_scope.keys())
    # different_elements = {key: (temp_global_scope.get(key, None), temp_local_scope.get(key, None)) for key in different_keys}

    
    print("common_elements for scopes are:")
    print(common_elements)
    print()
    print("-----")
    print("different_elements for scopes are")
    print(different_elements)
    print()
    print("-----")

    return common_elements, different_elements

# Пример использования
compare_scopes(1, 1)


global_scope_defined = \
{'__name__': '__main__',
 '__doc__': None,
 '__package__': None,
 '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x00000243178E89A0>,
 '__spec__': None, '__annotations__': {},
 '__builtins__': <module 'builtins' (built-in)>,
 '__file__': 'C:\\Users\\user\\documents\\pro\\chicago_spark\\ChiSpark\\envi_subprocess.py',
 '__cached__': None,
 'counter': <function counter at 0x0000024317D4D1B0>,
 'c1': <function counter.<locals>.step at 0x0000024317D4D240>,
 'c2': <function counter.<locals>.step at 0x0000024317D4D2D0>,
 'say_name': <function say_name at 0x0000024317D4D360>,
 'root_global_scope': {...},
 'root_local_scope': {...},
 'compare_scopes': <function compare_scopes at 0x0000024317D4D3F0>}


"""
print("----------------------------------")
print("Общие элементы видимости внутри функции:")
print(common)
print("----------------------------------")

print("\nРазличающиеся элементы видимости внутри функции:")
print(different)
print("----------------------------------")


common, different = compare_scopes(root_global_scope, root_local_scope)

print("----------------------------------")
print("Общие элементы в корне программы:")
print(common)
print("----------------------------------")

print("\nРазличающиеся элементы в корне программы:")
print(different)
print("----------------------------------")


print("Creating instatnce: f = say_name(\"Ivan\")")
f = say_name("Ivan")

# Используем dir() для просмотра области видимости переменной f
print("Scope of variable 'f':", dir(f))
"""

