import ast
import inspect

def loop_analyzer(func):
    tree = ast.parse(inspect.getsource(func))
    for_loops = [node for node in ast.walk(tree) if isinstance(node, ast.For)]

    def wrapper(*args, **kwargs):
        for loop in for_loops:
            iter_count = len(list(loop.iter.elts if isinstance(loop.iter, ast.List) else range(*map(lambda x: x.n, loop.iter.args))))
            print(f"Loop at line {loop.lineno} will iterate {iter_count} times.")
        print(f"Total number of 'for' loops: {len(for_loops)}")
        return func(*args, **kwargs)
    return wrapper

# Usage:
print("usage")
@loop_analyzer
def my_function():
    for i in range(10):
        print(i)
    for j in [1, 2, 3, 4, 5]:
        print(j)


my_function()

print("""
      _____
     |     |
     |     |
     |     |
     |     |
     |     |
     |     |
 ___/       \___
|                 |
 \_______________/
""")

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")


say_hello()