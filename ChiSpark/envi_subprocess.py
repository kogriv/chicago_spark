
    
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

