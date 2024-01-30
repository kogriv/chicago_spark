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