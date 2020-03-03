from function import *
from statements import *
from enums import *
from randomprob import random_with_prob
from variable import Variable

import subprocess


#clean the results folder
process = subprocess.Popen("rm -rf results".split())
process.communicate()
process = subprocess.Popen("mkdir results".split())
process.communicate()
process = subprocess.Popen("mkdir results/c".split())
process.communicate()
process = subprocess.Popen("mkdir results/assembly".split())
process.communicate()

errors = 0
warnings = 0

def setup_funcs():
    scope = Scope()

    scope.add_to_scope(Function('floor', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('round', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('ceil', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('sin', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('cos', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('sin', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('sqrt', DataType.FLOAT, [Variable('x', DataType.FLOAT)], False))
    scope.add_to_scope(Function('pow', DataType.FLOAT, [Variable('x', DataType.FLOAT), Variable('y', DataType.FLOAT)], False))

    scope.get_functions()

    return scope

for i in range(100):
    func = Function.random(scope=setup_funcs())

    imports = "#include <math.h>\n"

    driver = '\nint main(){\n'
    driver += '{}('.format(func.name)
    for p in range(len(func.parameters)):
        driver += str(Constant.get_random(func.parameters[p].get_return_type()))
        if p != len(func.parameters) - 1:
            driver += ', '
    driver += ');\n}'

    filename = "results/c/test{}.c".format(i)

    with open(filename, "w") as test_file:
        test_file.write(imports + str(func) + driver)

    process = subprocess.Popen("gcc -O0 -S -o results/assembly/test{}.asm {}".format(i, filename).split(), stderr=subprocess.PIPE )
    output, error = process.communicate()

    s = str(error)

    if s != "b''":
       
        if 'error:' in s:
            errors += 1
            print('{}: Error'.format(filename))
        elif 'warning:' in s:
            warnings += 1
            print('{}: Warning'.format(filename))
    else:
        print('{}: Done'.format(filename))


print('All programs generated and compiled. Errors: {}. Warnings {}.'.format(errors, warnings))
