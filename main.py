from generated import EasyXMLParser, EasyXMLLexer
from visitor.myVisitor import MyVisitor
from antlr4 import *


def main():
    input_stream = FileStream("langExample.el")
    lexer = EasyXMLLexer.EasyXMLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EasyXMLParser.EasyXMLParser(stream)
    tree = parser.xml()
    visitor = MyVisitor()
    visitor.visit(tree)
    print(0)


if __name__ == '__main__':
    main()
