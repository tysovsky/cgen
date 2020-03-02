from random import randint
from enum import Enum
from randomprob import random_with_prob
from expression import *

class UnaryOperator(Enum):
    MINUS = 0,
    PREFIX_DECREMENT = 1,
    POSTFIX_DECREMENT = 2,
    PREFIX_INCREMENT = 3,
    POSTFIX_INCREMENT = 4,
    NOT = 5,
    ADDRESS_OF = 6,
    BITWISE_NOT = 7,
    SIZE_OF = 8


    @staticmethod
    def random(type = None, exp = None):

        from variable import Variable

        probs = None

        if exp == None:
            probs = ['minus', 10, 'prefix_decrement', 10, 'postfix_decrement', 10, 'prefix_increment', 10, 'postfix_increment', 10,
                     'not', 10, 'bit_not', 10, 'sizeof', 10]

        elif isinstance(exp, Variable):
            if exp.get_return_type().is_float():
                probs = ['minus', 10, 'prefix_decrement', 10, 'postfix_decrement', 10, 'prefix_increment', 10, 'postfix_increment', 10,
                    'not', 10, 'sizeof', 10]
            else:
                probs = ['minus', 10, 'prefix_decrement', 10, 'postfix_decrement', 10, 'prefix_increment', 10, 'postfix_increment', 10,
                    'not', 10, 'bit_not', 10, 'sizeof', 10]
        
        elif exp.get_return_type().is_float():
            probs = ['minus', 10, 'not', 10]
        
        else:
            probs = ['minus', 10, 'not', 10, 'bit_not', 10]

        p = random_with_prob(probs)

        if p == 'minus':
            return UnaryOperator.MINUS
        if p == 'prefix_decrement':
            return UnaryOperator.PREFIX_DECREMENT
        if p == 'postfix_decrement':
            return UnaryOperator.POSTFIX_DECREMENT
        if p == 'prefix_increment':
            return UnaryOperator.PREFIX_INCREMENT
        if p == 'postfix_increment':
            return UnaryOperator.POSTFIX_INCREMENT
        if p == 'not':
            return UnaryOperator.NOT
        if p == 'address_of':
            return UnaryOperator.ADDRESS_OF
        if p == 'bit_not':
            return UnaryOperator.BITWISE_NOT
        if p == 'sizeof':
            return UnaryOperator.SIZE_OF

        return UnaryOperator.MINUS

class BinaryOperators(Enum):
    BITWISE_AND = 0,
    BITWISE_OR = 1,
    BITWISE_XOR = 2,
    LEFT_SHIFT = 3,
    RIGHT_SHIFT = 4,
    ADD = 5,
    SUBTRACT = 6,
    MULTIPLY = 7,
    DIVIDE = 8,
    MODULO = 9,
    LESS_THAN = 10,
    GREATER_THAN = 11,
    EQUAL = 12,
    LOGICAL_AND = 13,
    LOGICAL_OR = 14


    @staticmethod
    def get_random(exp1 = None, exp2 = None, return_type = None):

        probs = None

        if exp1 == None and exp2 == None:
            probs = ['bit_and', 10, 'bit_or', 10, 'bit_xor', 10, 'left_shift', 10, 'right_shift', 10,
                        'add', 10, 'subtract', 10, 'multiply', 10, 'divide', 10, 'modulo', 10,
                        'lt', 10, 'eq', 10, 'gt', 10, 'and', 10, 'or', 10]
        elif exp1.get_return_type().is_int() and exp2.get_return_type().is_int():
            probs = ['bit_and', 10, 'bit_or', 10, 'bit_xor', 10, 'left_shift', 10, 'right_shift', 10,
                        'add', 10, 'subtract', 10, 'multiply', 10, 'divide', 10, 'modulo', 10,
                        'lt', 10, 'eq', 10, 'gt', 10, 'and', 10, 'or', 10]
        else:
            probs = ['add', 10, 'subtract', 10, 'multiply', 10, 'divide', 10,
                        'lt', 10, 'eq', 10, 'gt', 10, 'and', 10, 'or', 10]
        
        d = random_with_prob(probs)

        if d == 'bit_and':
            return BinaryOperators.BITWISE_AND
        if d == 'bit_or':
            return BinaryOperators.BITWISE_OR
        if d == 'bit_xor':
            return BinaryOperators.BITWISE_XOR
        if d == 'left_shift':
            return BinaryOperators.LEFT_SHIFT
        if d == 'right_shift':
            return BinaryOperators.RIGHT_SHIFT
        if d == 'add':
            return BinaryOperators.ADD
        if d == 'subtract':
            return BinaryOperators.SUBTRACT
        if d == 'multiply':
            return BinaryOperators.MULTIPLY
        if d == 'divide':
            return BinaryOperators.DIVIDE
        if d == 'modulo':
            return BinaryOperators.MODULO
        if d == 'lt':
            return BinaryOperators.LESS_THAN
        if d == 'eq':
            return BinaryOperators.EQUAL
        if d == 'gt':
            return BinaryOperators.GREATER_THAN
        if d == 'and':
            return BinaryOperators.LOGICAL_AND
        if d == 'or':
            return BinaryOperators.LOGICAL_OR

        return BinaryOperators.ADD

    @staticmethod
    def get_random_comparison():
        t = random_with_prob('lt', 50, 'eq', 30, 'gt', 20)

        if t == 'lt':
            return BinaryOperators.LESS_THAN
        elif t == 'eq':
            return BinaryOperators.GREATER_THAN
        elif t == 'gt':
            return BinaryOperators.GREATER_THAN

class DataType(Enum):
    CHAR = 0,
    UNSIGNED_CHAR = 1,
    SIGNED_CHAR = 2,
    INT = 3,
    UNSIGNED_INT = 4,
    SHORT = 5,
    UNSIGNED_SHORT = 6,
    LONG = 7,
    UNSIGNED_LONG = 8,
    FLOAT = 9,
    DOUBLE = 10,
    LONG_DOUBLE = 11,
    VOID = 12,
    STRUCT = 13

    def __str__(self):
        if self == DataType.CHAR:
            return 'char'
        elif self == DataType.UNSIGNED_CHAR:
            return 'unsigned char'
        elif self == DataType.SIGNED_CHAR:
            return 'signed char'
        elif self == DataType.INT:
            return 'int'
        elif self == DataType.UNSIGNED_INT:
            return 'unsigned int'
        elif self == DataType.SHORT:
            return 'short'
        elif self == DataType.UNSIGNED_SHORT:
            return 'unsigned short'
        elif self == DataType.LONG:
            return 'long'
        elif self == DataType.UNSIGNED_LONG:
            return 'unsigned long'
        elif self == DataType.FLOAT:
            return 'float'
        elif self == DataType.DOUBLE:
            return 'double'
        elif self == DataType.LONG_DOUBLE:
            return 'long double'
        else:
            return 'void'

    def is_float(self):
        if self == DataType.FLOAT or self == DataType.DOUBLE or self == DataType.LONG_DOUBLE:
            return True
        return False

    def is_int(self):
        if self == DataType.INT or self == DataType.UNSIGNED_INT or self == DataType.SHORT or self == DataType.UNSIGNED_SHORT  or self == DataType.LONG or self == DataType.UNSIGNED_LONG or self == DataType.CHAR or self == DataType.UNSIGNED_CHAR or self == DataType.SIGNED_CHAR:
            return True
        return False
    
    @staticmethod
    def get_random_data_type():
        n = randint(0, 11)

        if n == 0:
            return DataType.CHAR
        elif n == 1:
            return DataType.UNSIGNED_CHAR
        elif n == 2:
            return DataType.SIGNED_CHAR
        elif n == 3:
            return DataType.INT
        elif n == 4:
            return DataType.UNSIGNED_INT
        elif n == 5:
            return DataType.SHORT
        elif n == 6:
            return DataType.UNSIGNED_SHORT
        elif n == 7:
            return DataType.LONG
        elif n == 8:
            return DataType.UNSIGNED_LONG
        elif n == 9:
            return DataType.FLOAT
        elif n == 10:
            return DataType.DOUBLE
        elif n == 11:
            return DataType.LONG_DOUBLE
        else:
            return DataType.INT
