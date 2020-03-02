from enums import *
from scope import *
from randomprob import random_with_prob


def expression_to_string(expr):
    if isinstance(expr, Variable):
        return str(expr)
    else:
        return '({})'.format(expr)


class Statement:
    def __init__(self, scope: Scope, return_type: DataType):
        super().__init__()
        self.return_type = return_type
        self.scope = scope

    def get_return_type(self):
        return self.return_type

    @staticmethod
    def random(scope, return_type: DataType = None, max_depth = 5, current_depth = 0, whitelist = None):

        if whitelist == None:
            statement_type = random_with_prob('binary', 60, 'unary', 40)

            if statement_type == 'binary':
                return BinaryStatement.random(scope, return_type, max_depth = max_depth, current_depth = current_depth)
            elif statement_type == 'unary':
                return UnaryStatement.random(scope, return_type, max_depth = max_depth, current_depth = current_depth)

        else:
            probs = []

            if BinaryStatement in whitelist:
                probs.extend(['binary', 10])
            
            if UnaryStatement in whitelist:
                probs.extend(['unary', 10])

            if AssignmentStatement in whitelist:
                probs.extend(['assignment', 40])

            if ForStatement in whitelist:
                probs.extend(['for', 10])

            if WhileStatement in whitelist:
                probs.extend(['while', 10])

            if IfStatement in whitelist:
                probs.extend(['if', 10])

            p = random_with_prob(probs)

            if p == 'binary':
                return BinaryStatement.random(scope, return_type, max_depth = max_depth, current_depth = current_depth)
            if p == 'unary':
                return UnaryStatement.random(scope, return_type, max_depth = max_depth, current_depth = current_depth)
            
            if p == 'assignment':
                return AssignmentStatement.random(scope)
            
            if p == 'for':
                return ForStatement.random(scope)
            if p == 'while':
                return WhileStatement.random(scope)
            if p == 'if':
                return IfStatement.random(scope)

     
# <operator> <statement>
class UnaryStatement(Statement):

    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __str__(self):
        if self.operator == UnaryOperator.MINUS:
            return '-{}'.format(expression_to_string(self.expression))
        
        elif self.operator == UnaryOperator.PREFIX_DECREMENT:
            return '--{}'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.POSTFIX_DECREMENT:
            return '{}--'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.PREFIX_INCREMENT:
            return '++{}'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.POSTFIX_INCREMENT:
            return '{}++'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.NOT:
            return '!{}'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.ADDRESS_OF:
            return '&{}'.format(expression_to_string(self.expression))
        
        elif self.operator == UnaryOperator.BITWISE_NOT:
            return '~{}'.format(expression_to_string(self.expression))

        elif self.operator == UnaryOperator.ADDRESS_OF:
            return '&{}'.format(expression_to_string(self.expression))
        
        elif self.operator == UnaryOperator.SIZE_OF:
            return 'sizeof({})'.format(expression_to_string(self.expression))

    def get_return_type(self):
        if self.operator == UnaryOperator.SIZE_OF or self.operator == UnaryOperator.ADDRESS_OF:
            return DataType.INT
        else:
            return self.expression.get_return_type()

    @staticmethod
    def random(scope: Scope, return_type, max_depth = 5, current_depth = 0):
        e = None

        if current_depth == max_depth:
            e = Constant.get_random(DataType.get_random_data_type())
        else:
            e = scope.get_random_value(return_type, max_depth = max_depth, current_depth = current_depth + 1)

        return UnaryStatement(UnaryOperator.random(exp = e), e)

# <statement> <operator> <statement>
class BinaryStatement(Statement):
    def __init__(self, exp1, operator, exp2):
        self.exp1 = exp1
        self.operator = operator
        self.exp2 = exp2
    
    def __str__(self):

        exp1 = expression_to_string(self.exp1)
        exp2 = expression_to_string(self.exp2)


        if self.operator == BinaryOperators.BITWISE_AND:
            return '{} & {}'.format(exp1, exp2)
        
        elif self.operator == BinaryOperators.BITWISE_OR:
            return '{} | {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.BITWISE_XOR:
            return '{} ^ {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.LEFT_SHIFT:
            return '{} << {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.RIGHT_SHIFT:
            return '{} >> {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.ADD:
            return '{} + {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.SUBTRACT:
            return '{} - {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.MULTIPLY:
            return '{} * {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.DIVIDE:
            return '{} / {}'.format(exp1, exp2)

        elif self.operator == BinaryOperators.MODULO:
            return '{} % {}'.format(exp1, exp2)
        elif self.operator == BinaryOperators.LESS_THAN:
            return '{} < {}'.format(exp1, exp2)
        elif self.operator == BinaryOperators.GREATER_THAN:
            return '{} > {}'.format(exp1, exp2)
        elif self.operator == BinaryOperators.EQUAL:
            return '{} == {}'.format(exp1, exp2)
        elif self.operator == BinaryOperators.LOGICAL_AND:
            return '{} && {}'.format(exp1, exp2)
        elif self.operator == BinaryOperators.LOGICAL_OR:
            return '{} || {}'.format(exp1, exp2)

    def get_return_type(self):

        if self.operator == BinaryOperators.DIVIDE:
            return DataType.FLOAT

        if self.exp2.get_return_type() == self.exp1.get_return_type():
            return self.exp1.get_return_type()

        if self.exp1.get_return_type().is_float() or self.exp2.get_return_type().is_float():
            return DataType.FLOAT

        if self.exp1.get_return_type().is_int() or self.exp2.get_return_type().is_int():
            return DataType.INT
        
        else:
            return self.exp1.get_return_type()


    @staticmethod
    def random(scope, return_type = None, max_depth = 5, current_depth = 0):

        exp1 = scope.get_random_value(max_depth = max_depth, current_depth = current_depth)
        exp2 = scope.get_random_value(max_depth = max_depth, current_depth = current_depth)

        op = BinaryOperators.get_random(exp1, exp2, return_type)

        return BinaryStatement(exp1, op, exp2)

# <variable> = <statement>
class AssignmentStatement(Statement):
    def __init__(self, variable, value, op = ''):
        self.variable = variable
        self.value = value
        self.op = op

    def __str__(self):
        return "{} {}= {}".format(self.variable, self.op, self.value)

    @staticmethod
    def random(scope: Scope):
        v: Variable = None
        
        var_type = random_with_prob('new',  60, 'existing', 40)

        if var_type == 'new':
            v = Variable("var" + str(scope.get_num_variables()), DataType.get_random_data_type())
            scope.add_to_scope(v)
        else:
            v = scope.get_random_variable()

            if v == None:
                v = Variable("var" + str(scope.get_num_variables()), DataType.get_random_data_type())
                scope.add_to_scope(v)


        right = scope.get_random_value(v.datatype, blacklist = [v])


        return AssignmentStatement(v, right)

#return <statement>
class ReturnStatement(Statement):
    def __init__(self, return_value):
        self.return_value = return_value

    def __str__(self):
        return 'return {}'.format(self.return_value)

    @staticmethod
    def random(scope: Scope, of_type: DataType):
        return ReturnStatement(scope.get_random_value(of_type))
   

#if (<statement>; <statement>; <statement>)
class IfStatement(Statement):
    def __init__(self, scope, condition):
        self.scope = Scope(scope)
        self.else_scope = Scope(scope)
        self.condition = condition
        self.statements = []
        self.else_statements = []

    def add_statement(self, statement: Statement):
        self.statements.append(statement)

    def add_else_statement(self, statement: Statement):
        self.else_statements.append(statement)

    def add_random_statement(self):
        self.add_statement(Statement.random(self.scope))

    def __str__(self):
        s = 'if({})'.format(self.condition)

        s += '{\n'

        for statement in self.statements:
            s += str(statement) + ';\n'

        s+= '}'

        if len(self.else_statements) > 0:
            s += '\nelse{\n'
            for statement in self.else_statements:
                s += str(statement) + ';\n'
            s += '}'

        return s

    @staticmethod
    def random(scope: Scope):

        s = Scope(scope)

        var = s.get_random_value()

        cond = None

        d = random_with_prob('var', 10, 'unary', 2, 'binary', 20)

        if d == 'var':
            cond = var
        elif d == 'unary':
            cond = UnaryStatement(UnaryOperator.random(exp=var), var)
        elif d == 'binary':
            cond = BinaryStatement(var, BinaryOperators.get_random_comparison(), s.get_random_value(var.get_return_type()))

        return IfStatement(s, cond)

class ForStatement(Statement):
    def __init__(self, scope, pre, check, post):
        self.scope = Scope(scope)
        self.pre = pre
        self.check = check
        self.post = post
        self.statements = []

    def __str__(self):
        s = 'for({}; {}; {})'.format(self.pre, self.check, self.post)

        s += '{\n'

        for statement in self.statements:
            s += '{};\n'.format(statement)

        s += '}'

        return s

    def add_statement(self, statement):
        self.statements.append(statement)

    @staticmethod
    def random(scope: Scope):

        s = Scope(scope)

        pre = AssignmentStatement.random(s)
        check = BinaryStatement(pre.variable, BinaryOperators.get_random_comparison(), s.get_random_value(pre.variable.datatype, blacklist = [pre.variable]))
        post = None

        post_type = random_with_prob('unary', 50, 'binary', 50)

        if post_type == 'unary':
            post = UnaryStatement(UnaryOperator.random(exp = pre.variable), pre.variable)
        elif post_type == 'binary':

            op = random_with_prob('+', 10, '-', 10, '*', 5, '', 2)

            post = AssignmentStatement(pre.variable, s.get_random_value(pre.variable.datatype, blacklist = [pre.variable]), op = op)


        return ForStatement(s, pre, check, post)

class WhileStatement(Statement):
    def __init__(self, scope, cond):
        self.cond = cond
        self.statements = []
        self.scope = Scope(scope)

    def __str__(self):
        s = 'while ({})'.format(self.cond)

        s += '{\n'

        for statement in self.statements:
            s += '{};\n'.format(statement)

        s += '}'

        return s

    def add_statement(self, statement):
        self.statements.append(statement)

    @staticmethod
    def random(scope: Scope):
        return WhileStatement(scope, scope.get_random_value())

class SwitchStatement(Statement):
    def __init__(self):
        super().__init__()

class CaseStatement(Statement):
    def __init__(self):
        super().__init__()

