from checker.checker import custom_exception, Exceptions

constants = ['string', 'int', 'float']
built_in_types = ['document', 'node', 'attribute']
all_types = ['string', 'int', 'float', 'document', 'node', 'attribute', 'string', 'int[]', 'float[]',
             'document[]', 'node[]', 'attribute[]']
built_in_types_for_params = ['document', 'node', 'attribute']


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
    global_funcs = {
        'print': all_types,
        'del': built_in_types_for_params,
        'save': None,
        'root': None,
        'findNode': ['string'],
        'attributes': None,
        'delete': None,
        'size': None,
        'insert': ['int', 'node'],
        'add': ['node']
    }

    def __init__(self):
        self.line = 0
        self.column = 0
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

    def check_type_cast(self, scope=None):
        if scope is None:
            scope = Node.global_vars
        for i in self.children:
            i.check_type_cast(scope)

    def check_var_init_types(self):
        for i in self.children:
            i.check_var_init_types()

    def check_params_call(self, scope=None):
        if scope is None:
            scope = Node.global_vars
        for i in self.children:
            i.check_params_call(scope)


class VarInit(Node):
    def __init__(self, var_name: str = '', var_type: str = '', new_flag: bool = False, line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.var_type = var_type
        self.new_flag = new_flag
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "VarInit", self.var_type, self.var_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if Node.global_funcs.get(self.var_name) is not None:
            Node.global_funcs.pop(self.var_name)
        scope[self.var_name] = self.var_type
        for i in self.children:
            i.check_vars_scope(scope)

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)

    def check_var_init_types(self):
        if len(self.children) != 0:
            if self.var_type == "node" and self.new_flag:
                type_of_node = self.children[0].check_var_init_types()
                if type_of_node != "'tag'" and type_of_node != "'content'":
                    custom_exception(
                        'Wrong type of node: got ' + type_of_node + ' expected ["tag","content"]',
                        self.line,
                        self.column,
                        Exceptions.TYPE_ERROR
                    )


class Assignment(Node):
    def __init__(self, var_name: str = '', index: int = 0, line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.index = index
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "Assignment", self.var_name, self.index)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        global constants, built_in_types
        for i in self.children:
            i.check_vars_scope(scope)
        expression_type = self.children[0].check_vars_scope(scope)
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                custom_exception(
                    'Isn\'t initialized variable: ' + self.var_name,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
        elif scope[self.var_name] != expression_type:
            if scope[self.var_name] not in built_in_types or expression_type not in constants:
                custom_exception(
                    'Wrong type of expression: got ' + expression_type + ' expected: ' + scope[
                        self.var_name] + ',' + str(constants),
                    self.line,
                    self.column,
                    Exceptions.TYPE_ERROR
                )

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)


class SumAssignment(Node):
    def __init__(self, var_name: str = '', index: int = 0, line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.index = index
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "SumAssignment", self.var_name, self.index)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        global constants
        for i in self.children:
            i.check_vars_scope(scope)
        expression_type = self.children[0].check_vars_scope(scope)
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                custom_exception(
                    'Isn\'t initialized variable: ' + self.var_name,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
        elif scope[self.var_name] != expression_type:
            if scope[self.var_name] != 'node' or (expression_type not in constants and expression_type != 'attribute'):
                custom_exception(
                    'Wrong type of expression: got ' + expression_type + ' expected: ' + scope[
                        self.var_name] + ',' + str(constants),
                    self.line,
                    self.column,
                    Exceptions.TYPE_ERROR
                )

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)


class Get(Node):
    def __init__(self, var_name: str = '', attribute_name: str = '', line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.attribute_name = attribute_name
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "Get", self.var_name, self.attribute_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if self.var_name != '':
            if self.var_name not in scope.keys():
                if self.var_name not in Node.global_vars.keys():
                    custom_exception(
                        'Isn\'t initialized variable: ' + self.var_name,
                        self.line,
                        self.column,
                        Exceptions.NAME_ERROR
                    )

        if self.attribute_name != '':
            if self.attribute_name not in Node.global_vars.keys():
                custom_exception(
                    'Isn\'t initialized attribute: ' + self.attribute_name,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
            else:
                for i in self.children:
                    i.check_vars_scope(scope)
                return Node.global_vars[self.attribute_name]

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)

    def check_params_call(self, scope=None):
        need_params = Node.global_funcs.get(self.attribute_name)
        if len(self.children) != 0:
            get_params = self.children[0].check_params_call(scope)
            if need_params is None:
                custom_exception(
                    "Get invalid params in " + self.attribute_name,
                    self.line,
                    self.column,
                    Exceptions.TYPE_ERROR
                )
            elif len(need_params) != len(get_params):
                custom_exception(
                    "Get " + str(len(get_params)) + " param, expected " + str(len(need_params)),
                    self.line,
                    self.column,
                    Exceptions.TYPE_ERROR
                )
            else:
                index = 0
                for i in get_params:
                    if i != need_params[index]:
                        custom_exception(
                            "Get " + str(len(get_params)) + " param, expected " + str(len(need_params)),
                            self.line,
                            self.column,
                            Exceptions.TYPE_ERROR
                        )
                    index += 1
        elif need_params is not None:
            custom_exception(
                "Get invalid params in " + self.attribute_name,
                self.line,
                self.column,
                Exceptions.TYPE_ERROR
            )
        return Node.global_vars[self.attribute_name]


class GetArrayElement(Node):
    def __init__(self, var_name: str = '', index: int = 0, line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.index = index
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "GetArrayElement", self.var_name, self.index)

    def check_vars_scope(self, scope: dict = None):
        if self.var_name != '':
            if self.var_name not in scope.keys():
                if self.var_name not in Node.global_vars.keys():
                    custom_exception(
                        'Isn\'t initialized variable: ' + self.var_name,
                        self.line,
                        self.column,
                        Exceptions.NAME_ERROR
                    )
                else:
                    return Node.global_vars[self.var_name]
            else:
                return scope[self.var_name]

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)


class FuncCall(Node):
    def __init__(self, func_name: str = '', line: int = 0, column: int = 0):
        super().__init__()
        self.func_name = func_name
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "FuncCall", self.func_name)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope: dict = None):
        if self.func_name != '':
            if self.func_name not in Node.global_vars.keys() and self.func_name not in Node.global_funcs.keys():
                custom_exception(
                    'Isn\'t initialized function: ' + self.func_name,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
            else:
                for i in self.children:
                    i.check_vars_scope(scope)
                return Node.global_vars[self.func_name]

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)

    def check_params_call(self, scope=None):
        need_params = Node.global_funcs.get(self.func_name)
        if need_params is not None and len(self.children[0].children) != 0:
            if self.func_name != 'print' and self.func_name != 'del':
                if len(need_params) != len(self.children[0].children):
                    custom_exception(
                        "Get " + str(len(self.children[0].children)) + " param, expected " + str(len(need_params)),
                        self.line,
                        self.column,
                        Exceptions.TYPE_ERROR
                    )
                else:
                    get_params = self.children[0].check_params_call(scope)
                    for i in range(len(need_params)):
                        if need_params[i] != get_params[i]:
                            custom_exception(
                                "Get " + get_params[i] + " param, expected " + need_params[i],
                                self.line,
                                self.column,
                                Exceptions.TYPE_ERROR
                            )
            else:
                get_params = self.children[0].check_params_call(scope)
                for i in get_params:
                    if i not in need_params:
                        custom_exception(
                            "Get " + i + " param, expected " + str(need_params),
                            self.line,
                            self.column,
                            Exceptions.TYPE_ERROR
                        )
        elif self.func_name in Node.global_funcs.keys():
            custom_exception(
                "Get invalid params in " + self.func_name,
                self.line,
                self.column,
                Exceptions.TYPE_ERROR
            )
        elif self.func_name not in Node.global_funcs.keys():
            custom_exception(
                'Isn\'t initialized function: ' + self.func_name,
                self.line,
                self.column,
                Exceptions.NAME_ERROR
            )


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

    def check_type_cast(self, scope=None):
        if self.if_block is not None:
            self.if_block.check_type_cast(scope)
        if self.elif_block is not None:
            self.elif_block.check_type_cast(scope)
        if self.else_block is not None:
            self.else_block.check_type_cast(scope)

    def check_params_call(self, scope=None):
        if self.if_block is not None:
            self.if_block.check_params_call(scope)
        if self.elif_block is not None:
            self.elif_block.check_params_call(scope)
        if self.else_block is not None:
            self.else_block.check_params_call(scope)


class IfBlock(Node):
    def __init__(self, condition=None, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.condition = condition
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "IfBlock")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        if self.condition is not None:
            self.condition.check_type_cast(self.local_vars)
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        if self.condition is not None:
            self.condition.check_params_call(self.local_vars)
        for i in self.children:
            i.check_params_call(self.local_vars)


class ElseIfBlock(Node):
    def __init__(self, condition=None, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.condition = condition
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "ElseIfBlock")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        if self.condition is not None:
            self.condition.check_type_cast(self.local_vars)
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        if self.condition is not None:
            self.condition.check_params_call(self.local_vars)
        for i in self.children:
            i.check_params_call(self.local_vars)


class ElseBlock(Node):
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "ElseBlock")
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        for i in self.children:
            i.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        for i in self.children:
            i.check_params_call(self.local_vars)


class ForStatement(Node):
    def __init__(self, range_statement=None, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.range_statement = range_statement
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "ForStatement")
        if self.range_statement is not None:
            self.range_statement.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.range_statement is not None:
            self.range_statement.check_vars_scope(self.local_vars)
        for i in self.children:
            i.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        for i in self.children:
            i.check_params_call(self.local_vars)


class WhileStatement(Node):
    def __init__(self, condition=None, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.condition = condition
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "WhileStatement")
        if self.condition is not None:
            self.condition.print(level + 1)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.condition is not None:
            self.condition.check_vars_scope(scope)
        for i in self.children:
            i.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        if self.condition is not None:
            self.condition.check_type_cast(self.local_vars)
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        if self.condition is not None:
            self.condition.check_params_call(self.local_vars)
        for i in self.children:
            i.check_params_call(self.local_vars)


class FuncInit(Node):
    def __init__(self, var_type='', var_name='', params=None, line: int = 0, column: int = 0):
        super().__init__()
        self.local_vars = {}
        self.var_type = var_type
        self.var_name = var_name
        self.params = params
        self.return_statement = None
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "FuncInit")
        self.params.print(level + 1)
        for i in self.children:
            i.print(level + 1)
        print('\treturn ', end='')
        if self.return_statement is not None:
            self.return_statement.print(level + 1)

    def check_vars_scope(self, scope=None):
        scope[self.var_name] = self.var_type
        if self.params is not None:
            Node.global_funcs[self.var_name] = self.params.check_params_call(scope)
            self.params.check_vars_scope(scope)
        else:
            Node.global_funcs[self.var_name] = None
        for i in self.children:
            i.check_vars_scope(self.local_vars)
        if self.return_statement is not None:
            self.return_statement.check_vars_scope(self.local_vars)

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(self.local_vars)

    def check_params_call(self, scope=None):
        for i in self.children:
            i.check_params_call(self.local_vars)


class TypeCast(Node):
    def __init__(self, var_name: str = '', cast_type: str = '', line: int = 0, column: int = 0):
        super().__init__()
        self.var_name = var_name
        self.cast_type = cast_type
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "TypeCast", self.var_name, self.cast_type)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        if self.var_name not in scope.keys():
            if self.var_name not in Node.global_vars.keys():
                custom_exception(
                    'Isn\'t initialized variable: ' + self.var_name,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
        else:
            return self.cast_type

    def check_type_cast(self, scope: dict = None):
        primordial_type = scope.get(self.var_name)
        if primordial_type is None:
            primordial_type = Node.global_vars.get(self.var_name)
        if primordial_type == "node":
            if self.cast_type != "document":
                custom_exception(
                    "Can\'t reduce node to" + self.cast_type,
                    self.line,
                    self.column,
                    Exceptions.VALUE_ERROR
                )
        elif primordial_type == "document":
            if self.cast_type != "node":
                custom_exception(
                    "Can\'t reduce document to" + self.cast_type,
                    self.line,
                    self.column,
                    Exceptions.VALUE_ERROR
                )
        elif primordial_type == "string":
            if self.cast_type != "int" and self.cast_type != "float":
                custom_exception(
                    "Can\'t reduce string to" + self.cast_type,
                    self.line,
                    self.column,
                    Exceptions.VALUE_ERROR
                )
        elif primordial_type == "int":
            if self.cast_type != "string" and self.cast_type != "float":
                custom_exception(
                    "Can\'t reduce int to" + self.cast_type,
                    self.line,
                    self.column,
                    Exceptions.VALUE_ERROR
                )
        elif primordial_type == "float":
            if self.cast_type != "string" and self.cast_type != "int":
                custom_exception(
                    "Can\'t reduce float to" + self.cast_type,
                    self.line,
                    self.column,
                    Exceptions.VALUE_ERROR
                )
        else:
            custom_exception(
                'Irreducible type' + primordial_type,
                self.line,
                self.column,
                Exceptions.VALUE_ERROR
            )


class RangeStatement(Node):
    def __init__(self, var_type: str = '', iterator: str = '', collection: str = '', line: int = 0, column: int = 0):
        super().__init__()
        self.var_type = var_type
        self.iterator = iterator
        self.collection = collection
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "RangeStatement", self.var_type, self.iterator, self.collection)

    def check_vars_scope(self, scope=None):
        if self.collection not in scope.keys():
            if self.collection not in Node.global_vars.keys():
                custom_exception(
                    'Isn\'t initialized collection: ' + self.collection,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
        scope[self.iterator] = self.var_type


class Condition(Node):
    def __init__(self, is_not: bool = False, and_or: bool = False, line: int = 0, column: int = 0):
        super().__init__()
        self.is_not = is_not
        self.and_or = and_or
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "Condition", self.is_not, self.and_or)
        for i in self.children:
            i.print(level + 1)

    def check_vars_scope(self, scope=None):
        for i in self.children:
            i.check_vars_scope(scope)

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)


class Params(Node):
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__()
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "Params")
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

    def check_type_cast(self, scope=None):
        for i in self.children:
            if type(i) == Expression:
                i.check_type_cast(scope)

    def check_params_call(self, scope=None):
        types_of_params = []
        for i in self.children:
            if type(i) == Expression:
                types_of_params.append(i.check_params_call(scope))
            elif type(i) == tuple:
                types_of_params.append(i[0])
        return types_of_params


class Expression(Node):
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__()
        self.value = None
        self.left_expression = None
        self.right_expression = None
        self.operator = None
        self.line = line
        self.column = column

    def print(self, level=0):
        for i in range(level):
            print('\t', end='')

        print(self.line, self.column, "Expression", self.value, self.operator)
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
                custom_exception(
                    'Isn\'t initialized variable: ' + self.value,
                    self.line,
                    self.column,
                    Exceptions.NAME_ERROR
                )
        if self.operator is not None:
            left_value = self.left_expression.check_vars_scope(scope)
            right_value = self.right_expression.check_vars_scope(scope)
            if left_value != right_value:
                if (left_value != 'attribute' and left_value != 'node') or right_value not in constants:
                    custom_exception(
                        'Invalid type in operation' + self.operator + ':' + left_value + '!=' + right_value,
                        self.line,
                        self.column,
                        Exceptions.TYPE_ERROR
                    )
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

    def check_type_cast(self, scope=None):
        for i in self.children:
            i.check_type_cast(scope)
        if self.right_expression is not None:
            self.right_expression.check_type_cast(scope)
        if self.left_expression is not None:
            self.left_expression.check_type_cast(scope)

    def check_var_init_types(self):
        if self.value is not None:
            return self.value
        else:
            if self.left_expression is not None:
                return self.left_expression.check_var_init_types()
            elif self.right_expression is not None:
                return self.right_expression.check_var_init_types()
            elif len(self.children) != 0:
                return self.children[0].check_var_init_types()

    def check_params_call(self, scope=None):
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
            if self.left_expression is not None:
                return self.left_expression.check_params_call(scope)
            elif self.right_expression is not None:
                return self.right_expression.check_params_call(scope)
            elif len(self.children) != 0:
                return self.children[0].check_params_call(scope)
