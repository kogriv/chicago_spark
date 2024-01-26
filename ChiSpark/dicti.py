d1 = {1:1,2:2}
d2 = {1:2,2:2,3:3}
d3 = {2:2,'j':'d'}

def dict_info(dictionary, verbose=True):
    info_dict = {}
    if verbose:
        print("----------------------------")
    for key, value in dictionary.items():
        key_info = {
            'value': value,
            'key_repr': repr(key),
            'value_repr': repr(value),
            'key_id': id(key),
            'key_type': type(key).__name__,
            'key_hash': hash(key) if isinstance(key, (int, str, tuple, frozenset)) else None,
            'value_id': id(value),
            'value_type': type(value).__name__
        }
        info_dict[key] = key_info

        if verbose:
            #print("attempt to do iterate inside loop")
            print(f"    '{key}': {key_info},")
    if verbose:
        print("----------------------------")
    return info_dict

inf1 = dict_info(d1)
inf2 = dict_info(d2)
inf3 = dict_info(d3)

def compare_dicts_info(dict1, dict2, compare_type='direct'):
    kv = {} # совпадающие пары по ключу и по значению
    k = {}  # ключ совпадает, но не входит в ключи словаря kv
    d1 = {} # уникальная часть 1-го словаря, где ключи не вошли ни в kv ни в k
    d2 = {} # уникальная часть 2-го словаря

    if compare_type == 'direct':
        """
        сравнение ключей производится для
        непосредственно ключей словарей,
        сравнение значений - для элементов 'value'
        """
        for key1, info1 in dict1.items():
            if key1 in dict2:
                info2 = dict2[key1]
                if info1['value'] == info2['value']:
                    kv[key1] = info1['value']
                else:
                    k[key1] = {'val1': info1['value'], 'val2': info2['value']}
            else:
                d1[key1] = info1['value']

        for key2, info2 in dict2.items():
            if key2 not in kv and key2 not in k:
                d2[key2] = info2['value']

    if compare_type == 'by_name':
        """
        сравнение ключей производится
        для элементов 'key_repr',
        сравнение значений - для 
        элементов 'value_repr'
        """
        for key1, info1 in dict1.items():
            key2_matched = False
            for key2, info2 in dict2.items():
                if info1['key_repr'] == info2['key_repr']:
                    key2_matched = True
                    if info1['value_repr'] == info2['value_repr']:
                        kv[info1['key_repr']] = info1['value_repr']
                    else:
                        k[info1['key_repr']] =\
                        {'val1':info1['value_repr'],'val2':info2['value_repr']}
            
            if not key2_matched:
                d1[info1['key_repr']] = info1['value_repr']
                
        
        for key2, info2 in dict2.items():
            key1_matched = False
            for key1, info1 in dict1.items():
                if info2['key_repr'] == info1['key_repr']:
                    key1_matched = True
            if not key1_matched:
                d2[info2['key_repr']] = info2['value_repr']

    elif compare_type == 'by_hash':
        """
        сравнение ключей производится
        для элементов 'key_hash',
        сравнение значений - для элементов 'value_id'
        """
        for key1, info1 in dict1.items():
            key2_matched = False
            for key2, info2 in dict2.items():
                if info1['key_hash'] == info2['key_hash']:
                    key2_matched = True
                    if info1['value_id'] == info2['value_id']:
                        kv[info1['key_hash']] = info1['value_id']
                    else:
                        k[info1['key_hash']] =\
                        {'val1':info1['value_id'],'val2':info2['value_id']}
            
            if not key2_matched:
                d1[info1['key_hash']] = info1['value_id']
        
        for key2, info2 in dict2.items():
            key1_matched = False
            for key1, info1 in dict1.items():
                if info2['key_hash'] == info1['key_hash']:
                    key1_matched = True
            if not key1_matched:
                d2[info2['key_hash']] = info2['value_id']

    return kv, k, d1, d2

# Пример использования:
# Сравниваем результаты функции dict_info для двух словарей
for t in ['direct','by_name','by_hash']:
    compare_type=t
    kv, k, d1, d2 = compare_dicts_info(inf1, inf3, compare_type)
    print("comparing type:",compare_type)
    print("Common keys and values:", kv)
    print("Common keys but different values:", k)
    print("Unique keys and values for dict1:", d1)
    print("Unique keys and values for dict2:", d2)
    print("----------------------------")
