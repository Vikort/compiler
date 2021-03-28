from generated import EasyXMLParser, EasyXMLLexer
from visitor.myVisitor import MyVisitor
from checker.checker import Checker
from antlr4 import *


def main():
    input_stream = FileStream("langExample.el")
    lexer = EasyXMLLexer.EasyXMLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EasyXMLParser.EasyXMLParser(stream)
    tree = parser.xml()
    if parser.getNumberOfSyntaxErrors():
        exit(1)
    visitor = MyVisitor()
    visitor.visit(tree)
    # visitor.root.print()
    checker = Checker(visitor.root)
    checker.check()


if __name__ == '__main__':
    main()
