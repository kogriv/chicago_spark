def get_parameter_names(func):
    parameter_names = {}

    print(func.__code__)
    for i in range(func.__code__.co_argcount):
        parameter_names[f"var_func_{func.__name__}_{i}"] = func.__code__.co_varnames[i]
    return parameter_names

def head(name, age):
    name = "Person" + name
    def clos():
        print("Name:", name)
        print("Age:", age)

    return clos

f = head("Alice", 30)

# parameter_names_dict = get_parameter_names(f.__closure__[0].cell_contents)
print("parametrs for head function")
parameter_names_dict = get_parameter_names(head)
print(parameter_names_dict)
print("parametrs for closured function")
parameter_names_dict = get_parameter_names(f)
print(parameter_names_dict)

