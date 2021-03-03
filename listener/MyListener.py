from antlr4 import *
from generated.EasyXMLParser import EasyXMLParser
from generated.EasyXMLListener import EasyXMLListener


class MyListener(EasyXMLListener):
    # Enter a parse tree produced by EasyXMLParser#var_init.
    def enterVar_init(self, ctx: EasyXMLParser.Var_initContext):
        print(
            ctx.TYPE()[0].getText(),
            ctx.VARNAME().getText(),
            ctx.TYPE()[1].getText(),
            ctx.expression().getText()
        )

    # Exit a parse tree produced by EasyXMLParser#var_init.
    def exitVar_init(self, ctx: EasyXMLParser.Var_initContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#assignment.
    def enterAssignment(self, ctx: EasyXMLParser.AssignmentContext):

        print(
            ctx.VARNAME().getText(),
            ctx.expression().getText()
        )

    # Exit a parse tree produced by EasyXMLParser#assignment.
    def exitAssignment(self, ctx: EasyXMLParser.AssignmentContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#sum_assignment.
    def enterSum_assignment(self, ctx: EasyXMLParser.Sum_assignmentContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#sum_assignment.
    def exitSum_assignment(self, ctx: EasyXMLParser.Sum_assignmentContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#get.
    def enterGet(self, ctx: EasyXMLParser.GetContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#get.
    def exitGet(self, ctx: EasyXMLParser.GetContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#get_array_element.
    def enterGet_array_element(self, ctx: EasyXMLParser.Get_array_elementContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#get_array_element.
    def exitGet_array_element(self, ctx: EasyXMLParser.Get_array_elementContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#func_call.
    def enterFunc_call(self, ctx: EasyXMLParser.Func_callContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#func_call.
    def exitFunc_call(self, ctx: EasyXMLParser.Func_callContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#if_statement.
    def enterIf_statement(self, ctx: EasyXMLParser.If_statementContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#if_statement.
    def exitIf_statement(self, ctx: EasyXMLParser.If_statementContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#if_block.
    def enterIf_block(self, ctx: EasyXMLParser.If_blockContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#if_block.
    def exitIf_block(self, ctx: EasyXMLParser.If_blockContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#else_if_block.
    def enterElse_if_block(self, ctx: EasyXMLParser.Else_if_blockContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#else_if_block.
    def exitElse_if_block(self, ctx: EasyXMLParser.Else_if_blockContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#else_block.
    def enterElse_block(self, ctx: EasyXMLParser.Else_blockContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#else_block.
    def exitElse_block(self, ctx: EasyXMLParser.Else_blockContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#for_statement.
    def enterFor_statement(self, ctx: EasyXMLParser.For_statementContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#for_statement.
    def exitFor_statement(self, ctx: EasyXMLParser.For_statementContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#while_statement.
    def enterWhile_statement(self, ctx: EasyXMLParser.While_statementContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#while_statement.
    def exitWhile_statement(self, ctx: EasyXMLParser.While_statementContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#func_init.
    def enterFunc_init(self, ctx: EasyXMLParser.Func_initContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#func_init.
    def exitFunc_init(self, ctx: EasyXMLParser.Func_initContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#type_cast.
    def enterType_cast(self, ctx: EasyXMLParser.Type_castContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#type_cast.
    def exitType_cast(self, ctx: EasyXMLParser.Type_castContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#range_statement.
    def enterRange_statement(self, ctx: EasyXMLParser.Range_statementContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#range_statement.
    def exitRange_statement(self, ctx: EasyXMLParser.Range_statementContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#condition.
    def enterCondition(self, ctx: EasyXMLParser.ConditionContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#condition.
    def exitCondition(self, ctx: EasyXMLParser.ConditionContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#params.
    def enterParams(self, ctx: EasyXMLParser.ParamsContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#params.
    def exitParams(self, ctx: EasyXMLParser.ParamsContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#expression.
    def enterExpression(self, ctx: EasyXMLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#expression.
    def exitExpression(self, ctx: EasyXMLParser.ExpressionContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#get_operation.
    def enterGet_operation(self, ctx: EasyXMLParser.Get_operationContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#get_operation.
    def exitGet_operation(self, ctx: EasyXMLParser.Get_operationContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#operation.
    def enterOperation(self, ctx: EasyXMLParser.OperationContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#operation.
    def exitOperation(self, ctx: EasyXMLParser.OperationContext):
        pass

    # Enter a parse tree produced by EasyXMLParser#xml.
    def enterXml(self, ctx: EasyXMLParser.XmlContext):
        pass

    # Exit a parse tree produced by EasyXMLParser#xml.
    def exitXml(self, ctx: EasyXMLParser.XmlContext):
        pass
