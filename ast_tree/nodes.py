class Node:
    def __init__(self):
        self.children = []


class VarInit(Node):
    def __init__(self, var_name='', var_type=''):
        super().__init__()
        self.var_name = var_name
        self.var_type = var_type


class Assignment(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index


class SumAssignment(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index


class Get(Node):
    def __init__(self, var_name='', attribute_name=''):
        super().__init__()
        self.var_name = var_name
        self.attribute_name = attribute_name


class GetArrayElement(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index


class FuncCall(Node):
    def __init__(self, func_name=''):
        super().__init__()
        self.func_name = func_name


class IfStatement(Node):
    def __init__(self, if_block=None, elif_block=None, else_block=None):
        super().__init__()
        self.if_block = if_block
        self.elif_block = elif_block
        self.else_block = else_block


class IfBlock(Node):
    def __init__(self, condition=None, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.condition = condition
        self.code_block = code_block


class ElseIfBlock(Node):
    def __init__(self, condition=None, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.condition = condition
        self.code_block = code_block


class ElseBlock(Node):
    def __init__(self, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.code_block = code_block


class ForStatement(Node):
    def __init__(self, range_statement=None, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.range_condition = range_statement,
        self.code_block = code_block


class WhileStatement(Node):
    def __init__(self, condition=None, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.condition = condition
        self.code_block = code_block


class FuncInit(Node):
    def __init__(self, var_type='', var_name='', params=None, code_block=None):
        super().__init__()
        if code_block is None:
            code_block = []
        self.var_type = var_type
        self.var_name = var_name
        self.params = params
        self.code_block = code_block
        self.return_statement = []


class TypeCast(Node):
    def __init__(self, var_name='', cast_type=''):
        super().__init__()
        self.var_name = var_name
        self.cast_type = cast_type


class RangeStatement(Node):
    def __init__(self, var_type='', iterator='', collection=''):
        super().__init__()
        self.var_type = var_type
        self.iterator = iterator
        self.collection = collection


class Condition(Node):
    def __init__(self, is_not=False, and_or=''):
        super().__init__()
        self.is_not = is_not
        self.and_or = and_or


class Params(Node):
    def __init__(self):
        super().__init__()


class Expression(Node):
    def __init__(self):
        super().__init__()
        self.value = None
        self.left_expression = None
        self.right_expression = None
        self.operator = None
