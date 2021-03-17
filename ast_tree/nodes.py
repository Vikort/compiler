constants = ['string', 'int', 'float']
built_in_types = ['document', 'node', 'attribute']


class Node:
    global_vars = {
        'save': '',
        'root': 'node',
        'findNode': 'node[]',
        'attributes': 'attribute[]',
        'insert': '',
        'print': '',
        'del': '',
        'delete': '',
        'size': 'int',
        'add': ''
    }

    def __init__(self):
        self.children = []

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')
        for i in self.children:
            i.print()

    def check_vars_scope(self, scope=None):
        if scope is None:
            scope = Node.global_vars
        for i in self.children:
            i.check_vars_scope(scope)


class VarInit(Node):
    def __init__(self, var_name='', var_type=''):
        super().__init__()
        self.var_name = var_name
        self.var_type = var_type

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("VarInit", self.var_type, self.var_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        scope[self.var_name] = self.var_type
        for i in self.children:
            i.check_vars_scope(scope)


class Assignment(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("Assignment", self.var_name, self.index)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        global constants, built_in_types
        for i in self.children:
            i.check_vars_scope(scope)
        expression_type = self.children[0].check_vars_scope(scope)
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                print(self.var_name, Node.global_vars.keys())
                raise Exception('Isn\'t initialized variable')
        elif scope[self.var_name] != expression_type:
            if scope[self.var_name] not in built_in_types or expression_type not in constants:
                # print(scope[self.var_name], self.var_name, expression_type, self.children[0])
                raise Exception('Invalid type of variable')


class SumAssignment(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("SumAssignment", self.var_name, self.index)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        global constants
        for i in self.children:
            i.check_vars_scope(scope)
        expression_type = self.children[0].check_vars_scope(scope)
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                raise Exception('Isn\'t initialized variable')
        elif scope[self.var_name] != expression_type:
            if scope[self.var_name] != 'node' or (expression_type not in constants and expression_type != 'attribute'):
                raise Exception('Invalid type of variable')


class Get(Node):
    def __init__(self, var_name='', attribute_name=''):
        super().__init__()
        self.var_name = var_name
        self.attribute_name = attribute_name

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("Get", self.var_name, self.attribute_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if self.var_name != '':
            if self.var_name not in scope.keys():
                if self.var_name not in Node.global_vars.keys():
                    raise Exception('Isn\'t initialized variable')

        if self.attribute_name != '':
            if self.attribute_name not in Node.global_vars.keys():
                print(self.attribute_name)
                raise Exception('Isn\'t initialized function')
            else:
                return Node.global_vars[self.attribute_name]
    # TODO check params


class GetArrayElement(Node):
    def __init__(self, var_name='', index=0):
        super().__init__()
        self.var_name = var_name
        self.index = index

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("GetArrayElement", self.var_name, self.index)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if self.var_name != '':
            if self.var_name not in scope.keys():
                if self.var_name not in Node.global_vars.keys():
                    raise Exception('Isn\'t initialized variable')
                else:
                    return Node.global_vars[self.var_name]
            else:
                return scope[self.var_name]


class FuncCall(Node):
    def __init__(self, func_name=''):
        super().__init__()
        self.func_name = func_name

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("FuncCall", self.func_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if self.func_name != '':
            if self.func_name not in Node.global_vars.keys():
                raise Exception('Isn\'t initialized function')
            else:
                return Node.global_vars[self.func_name]
    # TODO check params


class IfStatement(Node):
    def __init__(self, if_block=None, elif_block=None, else_block=None):
        super().__init__()
        self.if_block = if_block
        self.elif_block = elif_block
        self.else_block = else_block

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("IfStatement")
        if self.if_block is not None:
            self.if_block.print(level + 1)
        if self.elif_block is not None:
            self.elif_block.print(level + 1)
        if self.else_block is not None:
            self.else_block.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.if_block is not None:
            self.if_block.check_vars_scope(scope)
        if self.elif_block is not None:
            self.elif_block.check_vars_scope(scope)
        if self.else_block is not None:
            self.else_block.check_vars_scope(scope)


class IfBlock(Node):
    def __init__(self, condition=None):
        super().__init__()
        self.local_vars = {}
        self.condition = condition

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("IfBlock")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)


class ElseIfBlock(Node):
    def __init__(self, condition=None):
        super().__init__()
        self.local_vars = {}
        self.condition = condition

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("ElseIfBlock")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)


class ElseBlock(Node):
    def __init__(self):
        super().__init__()
        self.local_vars = {}

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("ElseBlock")
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        for i in self.children:
            i.check_vars_scope(self.local_vars)


class ForStatement(Node):
    def __init__(self, range_statement=None):
        super().__init__()
        self.local_vars = {}
        self.range_statement = range_statement

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("ForStatement")
        if self.range_statement is not None:
            self.range_statement.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.range_statement is not None:
            self.range_statement.check_vars_scope(self.local_vars)
        for i in self.children:
            i.check_vars_scope(self.local_vars)


class WhileStatement(Node):
    def __init__(self, condition=None):
        super().__init__()
        self.local_vars = {}
        self.condition = condition

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("WhileStatement")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)


class FuncInit(Node):
    def __init__(self, var_type='', var_name='', params=None):
        super().__init__()
        self.local_vars = {}
        self.var_type = var_type
        self.var_name = var_name
        self.params = params
        self.return_statement = None

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("FuncInit")
        self.params.print(level + 1)
        for i in self.children:
            i.print(level + 1)
        print('\treturn ', end='')
        if self.return_statement is not None:
            self.return_statement.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.params is not None:
            self.params.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)
        if self.return_statement is not None:
            self.return_statement.check_vars_scope(self.local_vars)


class TypeCast(Node):
    def __init__(self, var_name='', cast_type=''):
        super().__init__()
        self.var_name = var_name
        self.cast_type = cast_type

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("TypeCast")
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                raise Exception('Isn\'t initialized variable')
        else:
            return self.cast_type


class RangeStatement(Node):
    def __init__(self, var_type='', iterator='', collection=''):
        super().__init__()
        self.var_type = var_type
        self.iterator = iterator
        self.collection = collection

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("RangeStatement", self.var_type, self.iterator, self.collection)

    def check_vars_scope(self, scope=None):
        if self.collection not in scope.keys():
            if self.collection not in Node.global_vars.keys():
                raise Exception('Isn\'t initialized collection')
        scope[self.iterator] = self.var_type


class Condition(Node):
    def __init__(self, is_not=False, and_or=''):
        super().__init__()
        self.is_not = is_not
        self.and_or = and_or

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("Condition", self.is_not, self.and_or)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        for i in self.children:
            i.check_vars_scope(scope)


class Params(Node):
    def __init__(self):
        super().__init__()

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("Params")
        for i in self.children:
            if type(i) == Expression:
                i.print(level + 1)
            elif type(i) == tuple:
                for j in range(level + 1):
                    print('\t', end='')
                print(i[0], i[1])

    def check_vars_scope(self, scope=None):
        for i in self.children:
            if type(i) == Expression:
                i.check_vars_scope(scope)
            elif type(i) == tuple:
                scope[i[1]] = i[0]


class Expression(Node):
    def __init__(self):
        super().__init__()
        self.value = None
        self.left_expression = None
        self.right_expression = None
        self.operator = None

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print("Expression", self.value, self.operator)
        for i in self.children:
            i.print(level + 1)
        if self.right_expression is not None:
            self.right_expression.print(level + 1)
        if self.left_expression is not None:
            self.left_expression.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.value is not None:
            if self.value in scope.keys():
                return scope[self.value]
            elif self.value in Node.global_vars.keys():
                return Node.global_vars[self.value]
            elif '\'' in self.value:
                return 'string'
            elif '.' in self.value:
                return 'float'
            elif self.value[0] in "0123456789":
                return 'int'
            else:
                raise Exception('Isn\'t initialized variable')
        if self.operator is not None:
            left_value = self.left_expression.check_vars_scope(scope)
            right_value = self.right_expression.check_vars_scope(scope)
            if left_value != right_value:
                if (left_value != 'attribute' and left_value != 'node') or right_value not in constants:
                    raise Exception('Invalid type in operation', self.operator, ':', left_value, '!=', right_value)
            else:
                return left_value
        if len(self.children) != 0:
            for i in self.children:
                if type(i) == TypeCast:
                    return i.check_vars_scope(scope)
                elif type(i) == Get:
                    return i.check_vars_scope(scope)
                elif type(i) == FuncCall:
                    return i.check_vars_scope(scope)
                elif type(i) == GetArrayElement:
                    return i.check_vars_scope(scope)
