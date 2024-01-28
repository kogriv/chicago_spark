class DictAnalyzer:
    """
    A class for analyzing and comparing dictionaries.
    """

    def __init__(self, logger, llev=30):
        """
        Initialize a DictAnalyzer object.

        Args:
            logger: An instance of a logger object.
            llev (int, optional): Logging level. Defaults to 30.
        """
        self.logger = logger
        self.llev = llev

    def dict_info(self, dictionary, verbose=False):
        """
        Generate information about the keys and values of a dictionary.

        Args:
            dictionary (dict): The dictionary to analyze.
            verbose (bool, optional): If True, print verbose information. Defaults to True.

        Returns:
            dict: A dictionary containing information about keys and values.
        """
        info_dict = {}
        if verbose:
            self.logger.mylev(self.llev, "----------------------------")
        for key, value in dictionary.items():
            key_info = {
                'value': value,
                'key_repr': repr(key),
                'value_repr': repr(value),
                'key_id': id(key),
                'key_type': type(key).__name__,
                'key_hash': hash(key), #if isinstance(key, (int, str, tuple, frozenset)) else None,
                'value_id': id(value),
                'value_type': type(value).__name__
            }
            info_dict[key] = key_info

            if verbose:
                self.logger.mylev(self.llev, f"    '{key}': {key_info},")
        if verbose:
            self.logger.mylev(self.llev, "----------------------------")
        return info_dict

    def compare_dicts_info(self, dict1, dict2, compare_type='direct'):
        """
        Compare two dictionaries and identify matching,
        similar, and unique elements.

        Args:
            dict1 (dict): The first dictionary for comparison.
            dict2 (dict): The second dictionary for comparison.
            compare_type (str, optional): The method of comparison. Can be 'direct', 'by_name', or 'by_hash'.
                Defaults to 'direct'.

            structure for dicts defined in dict_info() function:
                info_dict[key] = key_info
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

        Returns:
            tuple: A tuple containing four dictionaries:
                - Matching keys and values (kv).
                - Matching keys but differing values (k).
                - Unique elements from the first dictionary (d1).
                - Unique elements from the second dictionary (d2).
        """
        kv = {} # matching pairs by key and value
        k = {}  # matching keys, but not in kv keys
        d1 = {} # unique part of the 1st dictionary where keys are not in kv or k
        d2 = {} # unique part of the 2nd dictionary

        if compare_type == 'direct':
            """
            comparing keys directly from dictionaries,
            comparing values for 'value' elements
            """
            for key1, info1 in dict1.items():
                if key1 in dict2:
                    info2 = dict2[key1]
                    if info1['value'] == info2['value']:
                        kv[key1] = {'info1': info1, 'info2': info2}
                    else:
                        k[key1] = {'info1': info1, 'info2': info2}
                else:
                    d1[key1] = info1

            for key2, info2 in dict2.items():
                if key2 not in kv and key2 not in k:
                    d2[key2] = info2

        if compare_type == 'by_name':
            """
            comparing keys for 'key_repr' elements,
            comparing values for 'value_repr' elements
            """
            for key1, info1 in dict1.items():
                key2_matched = False
                for key2, info2 in dict2.items():
                    if info1['key_repr'] == info2['key_repr']:
                        key2_matched = True
                        if info1['value_repr'] == info2['value_repr']:
                            kv[key1] = {'info1': info1, 'info2': info2}
                        else:
                            k[key1] = {'info1':info1,'info2':info2}
                
                if not key2_matched:
                    d1[key1] = info1
                    
            
            for key2, info2 in dict2.items():
                key1_matched = False
                for key1, info1 in dict1.items():
                    if info2['key_repr'] == info1['key_repr']:
                        key1_matched = True
                if not key1_matched:
                    d2[key2] = info2

        elif compare_type == 'by_hash':
            """
            comparing keys for 'key_hash' elements,
            comparing values for 'value_id' elements
            """
            for key1, info1 in dict1.items():
                key2_matched = False
                for key2, info2 in dict2.items():
                    if info1['key_hash'] == info2['key_hash']:
                        key2_matched = True
                        if info1['value_id'] == info2['value_id']:
                            kv[key1] = {'info1': info1, 'info2': info2}
                        else:
                            k[key1] = {'info1':info1,'info2':info2}
                
                if not key2_matched:
                    d1[key1] = info1
            
            for key2, info2 in dict2.items():
                key1_matched = False
                for key1, info1 in dict1.items():
                    if info2['key_hash'] == info1['key_hash']:
                        key1_matched = True
                if not key1_matched:
                    d2[key2] = info2

        return kv, k, d1, d2


if __name__ == '__main__':
    from mylog import MyLogger

    envilog = MyLogger('envilog', 30)

    # Создание экземпляра класса DictAnalyzer с передачей логгера и уровня логирования
    dictan = DictAnalyzer(envilog)

    print("sample sample of sample dicts")
    d01 = {'a': 1, 'b': 2, 'c': 3}
    d02 = {'b': 2, 'c': 4, 'd': 5}
    # Пример использования методов класса DictAnalyzer
    dict1 = dictan.dict_info(d01)
    dict2 = dictan.dict_info(d02)
    """
    envilog.mylev(30,"dict1:")
    envilog.mylev(30,dict1)

    envilog.mylev(30,"dict2:")
    envilog.mylev(30,dict2)
    """

    kv, k, d1, d2 = dictan.compare_dicts_info(dict1, dict2)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,d01)
    envilog.mylev(30,d02)
    envilog.mylev(30,"-----------direct comparison------------")
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"kv:")
    envilog.mylev(30,kv)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"k:")
    envilog.mylev(30,k)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"d1:")
    envilog.mylev(30,d1)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"d2:")
    envilog.mylev(30,d2)

    print("------------------------------------------")
    print("example of a dictionary with complex objects")
    class Dummy:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            # return f'{self.name}'
            return 'dummy_class'

        def __repr__(self):
            #return 'dummy_class'
            return f'{self.name}'

        def __hash__(self):
            # return hash(self.name)
            # Сравниваем объекты по длине имени
            if 1 <= len(self.name) <= 10:
                return hash('ten_letters')
            elif 11 <= len(self.name):
                return hash('twenty_letters')
            elif len(self.name) >= 21:
                return hash('over_twenty_letters')
            return hash('hash')

        def __eq__(self, other):
            # Определяем логику сравнения
            if isinstance(other, Dummy):
                # Сравниваем объекты по длине имени
                if 1 <= len(self.name) <= 10 and 1 <= len(other.name) <= 10:
                    return True
                elif 11 <= len(self.name) <= 20 and 11 <= len(other.name) <= 20:
                    return True
                elif len(self.name) >= 21 and len(other.name) >= 21:
                    return True
            return False
    
    obj1 = Dummy('first')
    obj2 = Dummy('second')
    obj3 = Dummy('more_ten_letters')
    obj4 = Dummy('more_than_twenty_letters')
    obj4 = Dummy('another_one_long_letters')

    d01 = {obj1: 1, obj2: 2, obj3: 3}
    d02 = {obj2: 2, obj3: 4, obj4: 5}
    # Пример использования методов класса DictAnalyzer
    dict1 = dictan.dict_info(d01)
    dict2 = dictan.dict_info(d02)

    kv, k, d1, d2 = dictan.compare_dicts_info(dict1, dict2)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"--------represent using logging---------")
    envilog.mylev(30,d01)
    envilog.mylev(30,d02)
    print("--------represent using print---------")
    print(d01)
    print(d02)
    envilog.mylev(30,"-----------direct comparison------------")
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"kv:")
    envilog.mylev(30,kv)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"k:")
    envilog.mylev(30,k)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"d1:")
    envilog.mylev(30,d1)
    envilog.mylev(30,"----------------------------------------")
    envilog.mylev(30,"d2:")
    envilog.mylev(30,d2)