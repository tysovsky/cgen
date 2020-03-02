from random import randint
from enums import *
from expression import *


class Constant(Expression):
    def __init__(self, value, datatype):
        self.value = value
        self.datatype = datatype

    def __str__(self):

        if self.datatype == DataType.CHAR or self.datatype == DataType.UNSIGNED_CHAR or self.datatype == DataType.SIGNED_CHAR:
            return "'{}'".format(self.value)

        return str(self.value)

    def get_return_type(self):
        return self.datatype

    @staticmethod
    def get_random(of_type: DataType):

        if of_type == None:
            of_type = random_with_prob(DataType.CHAR, 10, DataType.UNSIGNED_CHAR, 10, DataType.SIGNED_CHAR, 10, DataType.INT, 10, DataType.UNSIGNED_INT, 10, DataType.SHORT, 10, DataType.UNSIGNED_SHORT, 10, DataType.LONG, 10, DataType.UNSIGNED_LONG, 10, DataType.FLOAT, 10, DataType.DOUBLE, 10, DataType.LONG_DOUBLE, 10)

        if of_type == DataType.CHAR or of_type == DataType.UNSIGNED_CHAR or of_type == DataType.SIGNED_CHAR:
            return Constant(chr(randint(65, 89)), of_type)
                

        elif of_type == DataType.INT or of_type == DataType.SHORT or of_type == DataType.LONG:
            return Constant(randint(0, 65534) - 32768, of_type)

        elif of_type == DataType.UNSIGNED_INT or of_type == DataType.UNSIGNED_SHORT or of_type == DataType.UNSIGNED_LONG:
            return Constant(randint(0, 65534), of_type)

        elif of_type == DataType.FLOAT or of_type == DataType.DOUBLE or of_type == DataType.LONG_DOUBLE:
            return Constant(randint(0, 200000)/200000, of_type)

        return Constant(DataType.INT,0)

class Variable(Expression):
    def __init__(self, name: str, datatype: DataType, value = None):
        self.name = name
        self.datatype = datatype
        self.declared = True
        self.value = value

    def __str__(self):
        if self.declared:
            self.declared = False
            return "{} {}".format(self.datatype, self.name)
        else:
            return self.name

    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name
    
    def get_return_type(self):
        return self.datatype
    
    def type_and_name(self):
        return "{} {}".format(self.datatype, self.name)

    @staticmethod
    def random(scope):
        return Variable('var'+str(scope.get_num_variables()), DataType.get_random_data_type())