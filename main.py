from generated import EasyXMLParser, EasyXMLLexer, EasyXMLListener, EasyXMLVisitor
from antlr4 import *


def main():
    input_stream = InputStream("print(doc.root);")
    lexer = EasyXMLLexer.EasyXMLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = EasyXMLParser.EasyXMLParser(stream)
    tree = parser.xml()
    print(tree.toStringTree(None, parser))
    walker = ParseTreeWalker()
    walker.walk(EasyXMLListener.EasyXMLListener(), tree)
    return None


if __name__ == '__main__':
    main()
