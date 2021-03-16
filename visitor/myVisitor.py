from generated.EasyXMLVisitor import EasyXMLVisitor
from generated.EasyXMLParser import EasyXMLParser
from ast_tree.nodes import *


class MyVisitor(EasyXMLVisitor):
    def __init__(self):
        super(MyVisitor, self).__init__()
        self.root = Node()

    # Visit a parse tree produced by EasyXMLParser#var_init.
    def visitVar_init(self, ctx: EasyXMLParser.Var_initContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        if ctx.TYPE() is not None and len(ctx.TYPE()) == 2:
            if ctx.TYPE()[0].getText() != ctx.TYPE()[1].getText():
                raise Exception(ctx.TYPE()[0].getText(), '!=', ctx.TYPE()[1].getText())
            else:
                var_type = ctx.TYPE()[0].getText()
        else:
            if ctx.TYPE() is not None and type(ctx.TYPE()) != list:
                var_type = ctx.TYPE().getText()
            elif type(ctx.TYPE()) == list and len(ctx.TYPE()) != 0:
                var_type = ctx.TYPE()[0].getText()
            elif ctx.ARRAY_TYPE() is not None and type(ctx.ARRAY_TYPE()) != list:
                var_type = ctx.ARRAY_TYPE().getText()
            else:
                var_type = ctx.ARRAY_TYPE()[0].getText()
        if ctx.expression() is None:
            expression = Expression()
        else:
            expression = self.visitExpression(ctx.expression())
        if ctx.assignment() is not None:
            assignment = self.visitAssignment(ctx.assignment(), parent_node='var_init')
            var_name = assignment.var_name
            expression = assignment.children[0]
        else:
            var_name = ctx.VARNAME().getText()
        var_init_node = VarInit(
            var_name,
            var_type
        )
        var_init_node.children.append(expression)
        parent_node.children.append(var_init_node)
        return var_init_node

    # Visit a parse tree produced by EasyXMLParser#assignment.
    def visitAssignment(self, ctx: EasyXMLParser.AssignmentContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        var_name = ctx.VARNAME().getText()
        expression = self.visitExpression(ctx.expression())
        index = ctx.NUMBER_LITERAL().getText() if ctx.NUMBER_LITERAL() is not None else 0
        assignment_node = Assignment(
            var_name,
            index
        )
        assignment_node.children.append(expression)
        if parent_node != 'var_init':
            parent_node.children.append(assignment_node)
        return assignment_node

    # Visit a parse tree produced by EasyXMLParser#sum_assignment.
    def visitSum_assignment(self, ctx: EasyXMLParser.Sum_assignmentContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        var_name = ctx.VARNAME().getText()
        expression = self.visitExpression(ctx.expression())
        index = ctx.NUMBER_LITERAL().getText() if ctx.NUMBER_LITERAL() is not None else 0
        sum_assignment_node = SumAssignment(
            var_name,
            index
        )
        sum_assignment_node.children.append(expression)
        parent_node.children.append(sum_assignment_node)
        return sum_assignment_node

    # Visit a parse tree produced by EasyXMLParser#get.
    def visitGet(self, ctx: EasyXMLParser.GetContext, parent_node=None, level=0):
        if parent_node is None:
            parent_node = self.root
        get_node = Get()
        if ctx.get() is not None:
            get_node = self.visitGet(ctx.get(), parent_node, level + 1)
            if ctx.params() is not None:
                params = self.visitParams(ctx.params())
                get_node.children.append(params)
        else:
            get_node.var_name = ctx.VARNAME()[0].getText()
            get_node.attribute_name = ctx.VARNAME()[1].getText()
        if level == 0:
            parent_node.children.append(get_node)
        return get_node

    # Visit a parse tree produced by EasyXMLParser#get_array_element.
    def visitGet_array_element(self, ctx: EasyXMLParser.Get_array_elementContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        get_array_element_node = GetArrayElement(
            ctx.VARNAME().getText(),
            ctx.NUMBER_LITERAL().getText()
        )
        parent_node.children.append(get_array_element_node)
        return get_array_element_node

    # Visit a parse tree produced by EasyXMLParser#func_call.
    def visitFunc_call(self, ctx: EasyXMLParser.Func_callContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        params = Params()
        if ctx.params() is not None:
            params = self.visitParams(ctx.params())
        func_call_node = FuncCall(
            ctx.VARNAME().getText()
        )
        func_call_node.children.append(params)
        parent_node.children.append(func_call_node)
        return func_call_node

    # Visit a parse tree produced by EasyXMLParser#if_statement.
    def visitIf_statement(self, ctx: EasyXMLParser.If_statementContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root

        if_state = IfStatement(
            self.visitIf_block(ctx.if_block()),
            self.visitElse_if_block(ctx.else_if_block()) if len(ctx.else_if_block()) != 0 else None,
            self.visitElse_block(ctx.else_block()) if ctx.else_block() is not None else None
        )
        parent_node.children.append(if_state)
        return if_state

    # Visit a parse tree produced by EasyXMLParser#if_block.
    def visitIf_block(self, ctx: EasyXMLParser.If_blockContext):
        if_block = IfBlock(
            self.visitCondition(ctx.condition())
        )
        operations = ctx.operation()
        for i in operations:
            if_block.children.append(self.visitOperation(i))
        return if_block

    # Visit a parse tree produced by EasyXMLParser#else_if_block.
    def visitElse_if_block(self, ctx: EasyXMLParser.Else_if_blockContext):
        else_if_block = ElseIfBlock(
            self.visitCondition(ctx.condition())
        )
        operations = ctx.operation()
        for i in operations:
            else_if_block.children.append(self.visitOperation(i))
        return else_if_block

    # Visit a parse tree produced by EasyXMLParser#else_block.
    def visitElse_block(self, ctx: EasyXMLParser.Else_blockContext):
        else_block = ElseBlock()
        operations = ctx.operation()
        for i in operations:
            else_block.children.append(self.visitOperation(i))
        return else_block

    # Visit a parse tree produced by EasyXMLParser#for_statement.
    def visitFor_statement(self, ctx: EasyXMLParser.For_statementContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        for_state = ForStatement(
            self.visitRange_statement(ctx.range_statement())
        )
        operations = ctx.operation()
        for i in operations:
            for_state.children.append(self.visitOperation(i))
        parent_node.children.append(for_state)
        return for_state

    # Visit a parse tree produced by EasyXMLParser#while_statement.
    def visitWhile_statement(self, ctx: EasyXMLParser.While_statementContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        while_state = WhileStatement(
            self.visitCondition(ctx.condition())
        )
        operations = ctx.operation()
        for i in operations:
            while_state.children.append(self.visitOperation(i))
        parent_node.children.append(while_state)
        return while_state

    # Visit a parse tree produced by EasyXMLParser#func_init.
    def visitFunc_init(self, ctx: EasyXMLParser.Func_initContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        if ctx.RETURN() is None:
            raise Exception('return not found')
        func_init = FuncInit(
            ctx.TYPE().getText() if ctx.TYPE() is not None else ctx.ARRAY_TYPE().getText(),
            ctx.VARNAME().getText(),
            self.visitParams(ctx.params()) if ctx.params() is not None else None
        )
        operations = ctx.operation()
        for i in operations:
            func_init.children.append(self.visitOperation(i))

        func_init.return_statement.append(self.visitExpression(ctx.expression()))
        parent_node.children.append(func_init)
        return func_init

    # Visit a parse tree produced by EasyXMLParser#type_cast.
    def visitType_cast(self, ctx: EasyXMLParser.Type_castContext, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        type_cast_node = TypeCast(
            ctx.VARNAME().getText(),
            ctx.TYPE().getText()
        )
        parent_node.children.append(type_cast_node)
        return type_cast_node

    # Visit a parse tree produced by EasyXMLParser#range_statement.
    def visitRange_statement(self, ctx: EasyXMLParser.Range_statementContext):
        range_node = RangeStatement(
            ctx.TYPE().getText() if ctx.TYPE() is not None else ctx.ARRAY_TYPE().getText(),
            ctx.VARNAME()[0].getText(),
            ctx.VARNAME()[1].getText()
        )
        return range_node

    # Visit a parse tree produced by EasyXMLParser#condition.
    def visitCondition(self, ctx: EasyXMLParser.ConditionContext):
        if ctx.NOT() is not None and type(ctx.NOT()) != list:
            is_not = bool(ctx.NOT().getText())
        else:
            is_not = bool(ctx.NOT()[0].getText()) if len(ctx.NOT()) == 1 else False
        if ctx.ANDOR() is not None and type(ctx.ANDOR()) != list:
            and_or = bool(ctx.ANDOR().getText())
        else:
            and_or = bool(ctx.ANDOR()[0].getText()) if len(ctx.ANDOR()) == 1 else False
        condition = Condition(
            is_not,
            and_or
        )
        condition.children.append(self.visitExpression(ctx.expression()))
        for i in ctx.condition():
            condition.children.append(self.visitCondition(i))
        return condition

    # Visit a parse tree produced by EasyXMLParser#params.
    def visitParams(self, ctx: EasyXMLParser.ParamsContext):
        # TODO add visit func_init params
        expressions = ctx.expression()
        params = Params()
        if len(expressions) != 0:
            for i in expressions:
                params.children.append(self.visitExpression(i))
        return params

    # Visit a parse tree produced by EasyXMLParser#expression.
    def visitExpression(self, ctx: EasyXMLParser.ExpressionContext):
        expression = Expression()
        if ctx.ACTION_OPERATOR() is not None:
            expression.operator = ctx.ACTION_OPERATOR().getText()
        elif ctx.BOOL_OPERATOR() is not None:
            expression.operator = ctx.BOOL_OPERATOR().getText()
        if expression.operator is not None:
            expression.left_expression = self.visitExpression(ctx.expression()[0])
            expression.right_expression = self.visitExpression(ctx.expression()[1])
            return expression

        if ctx.NUMBER_LITERAL() is not None:
            expression.value = ctx.NUMBER_LITERAL().getText()
        elif ctx.STRING_LITERAL() is not None:
            expression.value = ctx.STRING_LITERAL().getText().replace('\'', '')
        elif ctx.VARNAME() is not None:
            expression.value = ctx.VARNAME().getText()
        if expression.value is not None:
            return expression

        if ctx.get_operation() is not None:
            expression.children.append(self.visitGet_operation(ctx.get_operation()))
        elif ctx.type_cast() is not None:
            expression.children.append(self.visitType_cast(ctx.type_cast()))
        if len(expression.children) != 0:
            return expression

        if ctx.expression() is not None:
            expression = self.visitExpression(ctx.expression())
        return expression

    # Visit a parse tree produced by EasyXMLParser#get_operation.
    def visitGet_operation(self, ctx: EasyXMLParser.Get_operationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EasyXMLParser#operation.
    def visitOperation(self, ctx: EasyXMLParser.OperationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EasyXMLParser#xml.
    def visitXml(self, ctx: EasyXMLParser.XmlContext):
        return self.visitChildren(ctx)
