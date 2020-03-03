from variable import *
from randomprob import random_with_prob

class Scope:
    def __init__(self, parent = None):
        super().__init__()
        self.in_scope = []
        self.parent = parent

    def add_to_scope(self, thing):
        self.in_scope.append(thing)

    def get_variables(self, of_type = None, blacklist = []):

        vars = []
        if self.parent:
            vars.extend(self.parent.get_variables())

        if of_type == None:
            vars.extend([x for x in self.in_scope if isinstance(x, Variable) and x not in blacklist])
        else:
            vars.extend([x for x in self.in_scope if isinstance(x, Variable) and x.datatype == of_type and x not in blacklist])
        return vars

    def get_functions(self, return_type = None, blacklist = []):
        from function import Function
        funcs = []

        if self.parent:
            funcs.extend(self.parent.get_functions(return_type=return_type, blacklist=blacklist))

        if return_type == None:
            funcs.extend([x.copy() for x in self.in_scope if isinstance(x, Function) and x not in blacklist])
        else:
            funcs.extend([x.copy() for x in self.in_scope if isinstance(x, Function) and x.return_type == return_type and x not in blacklist])
        return funcs

    def get_random_variable(self, of_type = None, blacklist = []):
        vars = self.get_variables(of_type, blacklist=blacklist)
        if not vars:
            return None
        
        return vars[randint(0, len(vars) - 1)]

    def get_random_function(self, return_type = None, blacklist = []):
        funcs = self.get_functions(return_type, blacklist=blacklist)
        if not funcs:
            return None
        return funcs[randint(0, len(funcs) - 1)]
    
    #either statement, function of variable or constant
    def get_random_value(self, of_type = None, blacklist = [], max_depth = 5, current_depth = 0, no_consts = False):
        from statements import Statement
        
        if no_consts:
            value_type = random_with_prob('variable', 35, 'statement', 30, 'function', 40)
        else:
            value_type = random_with_prob('constant', 35, 'variable', 35, 'statement', 30, 'function', 40)
        
        if value_type == 'constant':
            return Constant.get_random(of_type)
        
        elif value_type == 'variable':
            val = self.get_random_variable(of_type, blacklist=blacklist)
            if val == None:
                p = ['statement', 50]

                if not no_consts:
                    p.extend(['constant', 50])

                value_type = random_with_prob(p)
                if value_type == 'constant':
                    return Constant.get_random(of_type)
                elif value_type == 'statement':
                    val = Statement.random(self, of_type, max_depth=max_depth, current_depth = current_depth + 1)
                    if val == None:
                        return Constant.get_random(of_type)
            return val
        
        elif value_type == 'statement':
            val = Statement.random(self, of_type, max_depth=max_depth, current_depth = current_depth + 1)

            if val == None:
                p = ['variable', 50]

                if not no_consts:
                    p.extend(['constant', 50])
                value_type = random_with_prob(p)
                if value_type == 'constant':
                    return Constant.get_random(of_type)
                elif value_type == 'variable':
                    val = self.get_random_variable(of_type)
                    if val == None:
                        return Constant.get_random(of_type)
            
            return val

        elif value_type == 'function':
            val = self.get_random_function(of_type)

            if val == None:
                p = ['variable', 50]

                if not no_consts:
                    p.extend(['constant', 50])
                value_type = random_with_prob(p)
                if value_type == 'constant':
                    return Constant.get_random(of_type)
                elif value_type == 'variable':
                    val = self.get_random_variable(of_type)
                    if val == None:
                        return Constant.get_random(of_type)
            else:
                for parameter in val.parameters:
                    parameter.value = self.get_random_value(parameter.datatype, max_depth=max_depth, current_depth=current_depth+1, blacklist=[val])
            
            return val

    def get_num_variables(self):
        return len(self.get_variables())

    def get_num_functions(self):
        return len(self.get_functions())
