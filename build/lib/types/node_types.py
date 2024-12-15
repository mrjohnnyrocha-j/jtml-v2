# types.py

class Type:
    def is_compatible_with(self, other):
        return isinstance(other, self.__class__)

class PrimitiveType(Type):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class IntType(PrimitiveType):
    def __init__(self):
        super().__init__('int')

class FloatType(PrimitiveType):
    def __init__(self):
        super().__init__('float')

class StringType(PrimitiveType):
    def __init__(self):
        super().__init__('string')

class BoolType(PrimitiveType):
    def __init__(self):
        super().__init__('bool')

class VoidType(PrimitiveType):
    def __init__(self):
        super().__init__('void')

class FunctionType(Type):
    def __init__(self, param_types, return_type):
        self.param_types = param_types  # List of Type
        self.return_type = return_type  # Type

    def is_compatible_with(self, other):
        if not isinstance(other, FunctionType):
            return False
        if len(self.param_types) != len(other.param_types):
            return False
        for pt1, pt2 in zip(self.param_types, other.param_types):
            if not pt1.is_compatible_with(pt2):
                return False
        return self.return_type.is_compatible_with(other.return_type)

    def __str__(self):
        params = ', '.join([str(pt) for pt in self.param_types])
        return f"({params}) -> {self.return_type}"

class CustomType(Type):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, var_type):
        self.symbols[name] = var_type

    def lookup(self, name):
        var_type = self.symbols.get(name)
        if var_type is not None:
            return var_type
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            return None
class TypeNode:
    def __init__(self, name, generic_arguments=None):
        self.name = name  # Should be a string like 'int'
        self.generic_arguments = generic_arguments

    def __str__(self):
        if self.generic_arguments:
            generics = ', '.join([str(arg) for arg in self.generic_arguments])
            return f"{self.name}<{generics}>"
        return self.name
    
class AnyType(TypeNode):
    def __init__(self):
        super().__init__('any')

    def is_compatible_with(self, other):
        return True  # AnyType is compatible with all types

    def __str__(self):
        return "any"


