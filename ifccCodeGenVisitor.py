from ifccVisitor import ifccVisitor
from ifccParser import ifccParser
from antlr4.tree.Trees import Trees


class ifccCodeGenVisitor(ifccVisitor):
    
    def __init__(self, parser):
        super().__init__()
        self._parser = parser
        self._functions = []
        self._current_function = None


    def visitProg(self, ctx):
        print("I'm seeing a prog\n")
        return self.visitChildren(ctx)

    def visitAxiom(self, ctx):
        print("I'm seeing an axiom\n")
        return self.visitChildren(ctx)
