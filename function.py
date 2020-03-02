from random import randint
from scope import *
from statements import *
from variable import Variable

class Function:
    def __init__(self, name: str, return_type: DataType, parameters, new = True, scope = Scope()):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

        self.scope = scope
        self.statements = []

        self.new = new

        for parameter in self.parameters:
            self.scope.add_to_scope(parameter)

    def add_random_statement(self):
        s = randint(0, 4)

    def add_statement(self, statement):
        self.statements.append(statement)

    def __str__(self):

        if self.new:
            s = "{} {} (".format(self.return_type, self.name)

            for parameter in self.parameters:
                s += '{}, '.format(parameter)
            if len(self.parameters) > 0:
                s = s[:-2]
            s+='){\n'

            for statement in self.statements:
                s+= str(statement)

                if not isinstance(statement, (IfStatement, ForStatement, WhileStatement)):
                    s+= ';'

                s += '\n'

            s+='}'

            return s
        else:
            s = '{}('.format(self.name)
            for i in range(self.parameters):
                s += self.parameters[i].value
                if i != len(self.parameters)-1:
                    s += ', '
            s += ');'
            return s

    @staticmethod
    def random(scope: Scope = None, min_num_statements = 5, max_num_statements = 15):
        if scope == None:
            scope = Scope()
        num_params = random_with_prob(0, 10, 1, 20, 2, 40, 3, 20, 4, 10)

        params = []

        for _ in range(num_params):
            v = Variable.random(scope)
            scope.add_to_scope(v)
            params.append(v)

        func =  Function('func'+str(scope.get_num_functions()), DataType.get_random_data_type(), params, scope=scope)

        num_statements = randint(min_num_statements, max_num_statements)
        last_statement = None
        for i in range(num_statements):
            

            if isinstance(last_statement, AssignmentStatement) or last_statement == None:
                statement = Statement.random(func.scope, whitelist=[AssignmentStatement, IfStatement, WhileStatement, ForStatement])
                func.add_statement(statement)
                last_statement = statement
            else:
                probs = ['new_scope', 40, 'old_scope', 10]

                p = random_with_prob(probs)

                if p == 'new_scope':
                    statement = Statement.random(last_statement.scope, whitelist=[AssignmentStatement, IfStatement, WhileStatement, ForStatement])
                    last_statement.add_statement(statement)
                elif p == 'old_scope':
                    statement = Statement.random(func.scope, whitelist=[AssignmentStatement, IfStatement, WhileStatement, ForStatement])
                    func.add_statement(statement)
                    last_statement = statement


        
        return func



