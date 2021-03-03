from generated import EasyXMLParser, EasyXMLLexer
from listener import MyListener
from antlr4 import *


def main():
    input_stream = FileStream("langExample.el")
    lexer = EasyXMLLexer.EasyXMLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EasyXMLParser.EasyXMLParser(stream)
    tree = parser.xml()
    print(tree.toStringTree(None, parser))
    walker = ParseTreeWalker()
    walker.walk(MyListener.MyListener(), tree)


if __name__ == '__main__':
    main()
