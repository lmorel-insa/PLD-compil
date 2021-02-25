from ifccLexer import ifccLexer
from ifccParser import ifccParser
from ifccCodeGenVisitor import ifccCodeGenVisitor

import argparse

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

import os
import sys
import traceback

class CountErrorListener(ErrorListener):
    """Count number of errors.

    Parser provides getNumberOfSyntaxErrors(), but the Lexer
    apparently doesn't provide an easy way to know if an error occurred
    after the fact. Do the counting ourserves with a listener.
    """

    def __init__(self):
        super(CountErrorListener, self).__init__()
        self.count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.count += 1



def main(inputname, 
         stdout=False, output_name=None):
    (basename, rest) = os.path.splitext(inputname)
    if stdout:
        output_name = None
        print("Code will be generated on standard output")
    elif output_name is None:
        output_name = basename + ".s"
        print("Code will be generated in file " + output_name)

    input_s = FileStream(inputname, encoding='utf-8')
    lexer = ifccLexer(input_s)
    counter = CountErrorListener()
    lexer._listeners.append(counter)
    stream = CommonTokenStream(lexer)
    parser = ifccParser(stream)
    parser._listeners.append(counter)
    tree = parser.prog()
    if counter.count > 0:
        exit(3)  # Syntax or lexicography errors occurred, don't try to go further.

    visitor3 = ifccCodeGenVisitor(parser)
    # dump generated code on stdout or file.
    with open(output_name, 'w') if output_name else sys.stdout as output:
        visitor3.visit(tree)


# command line management
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate code for .c file')

    parser.add_argument('filename', type=str,
                        help='Source file.')
    parser.add_argument('--stdout', action='store_true',
                        help='Generate code to stdout')
    parser.add_argument('--output', type=str,
                        help='Generate code to outfile')

    args = parser.parse_args()

    try:
        main(args.filename, args.stdout, args.output)
    except Exception:
        traceback.print_exc() 
        print("Exception raised\n")
        exit(4)
