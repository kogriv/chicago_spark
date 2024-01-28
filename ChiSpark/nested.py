def get_parameter_names(func):
    parameter_names = {}
    for i in range(func.__code__.co_argcount):
        parameter_names[f"var_func_{func.__name__}_{i}"] = func.__code__.co_varnames[i]
    return parameter_names

def head(name, age):
    def clos():
        print("Name:", name)
        print("Age:", age)

    return clos

f = head("Alice", 30)

parameter_names_dict = get_parameter_names(f.__closure__[0].cell_contents)
print(parameter_names_dict)
