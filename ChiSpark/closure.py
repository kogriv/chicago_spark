def say_name(name):
    def say_goodbye():
        print("Don't say me goodbye, " + name + "!")

    return say_goodbye

f = say_name("Ivan")

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