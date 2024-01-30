def say_name(name):
    def say_goodbye():
        nested_var = 'some_value_for_nested_var'
        print("Don't say me goodbye, " + name + "!")

    return say_goodbye

f = say_name("Ivan")

def get_variable_names(func):
    return func.__code__.co_varnames

def assign_variable_names(func):
    variable_names = get_variable_names(func)
    # print("Variable names for function",repr(func),': ',variable_names)
    variable_assignments = [f"var_func_{func.__name__}_{i} = '{name}'" for i, name in enumerate(variable_names)]
    return variable_assignments

print("Global scope dict:", globals())
print('------------------------------------------')
print("Local scope dict:", locals())
print('------------------------------------------')
print("Local scope list:", dir())
print('------------------------------------------')
print("Scope list of variable 'f':", dir(f))
print('------------------------------------------')

print("Closure f.__closure__:", f.__closure__)
print('------------------------------------------')
print("Local variables f.__code__.co_varnames:", f.__code__.co_varnames)
print('------------------------------------------')
print("Globals f.__globals__:", f.__globals__)
print('------------------------------------------')

# Извлекаем значение переменной name из замыкания
closure_value = f.__closure__[0].cell_contents
print("Value of closed variable 'name':", closure_value)
print('------------------------------------------')

print("Variable assignments for nested [f=say_name(..)]:")
# Получаем имена переменных и создаем соответствующие переменные
variable_assignments = assign_variable_names(f)
for assignment in variable_assignments:
    exec(assignment)
# Печатаем созданные переменные
for i in range(len(variable_assignments)):
    print(f"Variable {i}: {eval(f'var_func_say_goodbye_{i}')}")
print('------------------------------------------')

print("Variable assignments for outer [say_name]:")
# Получаем имена переменных и создаем соответствующие переменные
variable_assignments = assign_variable_names(say_name)
for assignment in variable_assignments:
    exec(assignment)
# Печатаем созданные переменные
for i in range(len(variable_assignments)):
    print(f"Variable {i}: {eval(f'var_func_say_name_{i}')}")
print('------------------------------------------')