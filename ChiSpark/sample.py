def assign_variable_names(func):
    variable_names = get_variable_names(func)
    closure_variables = func.__closure__ if func.__closure__ else []
    
    variable_assignments = []
    
    for i, name in enumerate(variable_names):
        is_closure = name in [cell.cell_contents for cell in closure_variables]
        assignment = f"var_func_{func.__name__}_{i} = '{name}'"
        if is_closure:
            assignment += "  # Closed variable"
        variable_assignments.append(assignment)

    return variable_assignments

def get_variable_names(func):
    # print(dir(func.__code__))#.co_names)
    for i in dir(func.__code__):
        print(i,':',eval("func.__code__."+i))
    return func.__code__.co_names

def say_name_age(name, age):
    def say_info():
        nested_var = 'some_value_for_nested_var'
        print("nested_var:",nested_var)
        print("Name:", name)
        print("Age:", age)

    return say_info

f = say_name_age("Alice", 30)
variable_names = get_variable_names(f)

"""
# Получаем имена переменных и создаем соответствующие переменные
variable_assignments = assign_variable_names(f)
for assignment in variable_assignments:
    exec(assignment)

# Печатаем созданные переменные
for i, assignment in enumerate(variable_assignments):
    print(f"Variable {i}: {eval(f'var_func_say_info_{i}')}")
"""