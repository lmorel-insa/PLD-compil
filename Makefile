OUTPUT=output
GENERATED=./
PACKAGE=ifcc
GRAMMAR=$(PACKAGE).g4

#override with your local installation
ANTLR4=java -jar /home/lmorel/usr/lib/antlr-4.8-complete.jar

CC=clang++
CCARGS=-g -c -I $(ANTLR4_INCDIR) -I $(GENERATED) -std=c++11 -Wno-defaulted-function-deleted -Wno-unknown-warning-option
LDARGS=-g

all: antlr

antlr ifccLexer.py ifccParser.py: $(GRAMMAR)
	$(ANTLR4) $< -Dlanguage=Python3 $(GRAMMAR) -o $(GENERATED) -visitor

clean:
	find . \( -iname "*~" -or -iname ".cache*" -or -iname "*.diff" -or -iname "log*.txt" -or -iname "__pycache__" -or -iname "*.tokens" -or -iname "*.interp" \) -print0 | xargs -0 rm -rf \;
	rm -rf *~ $(PACKAGE)Parser.py $(PACKAGE)Lexer.py $(PACKAGE)Visitor.py $(PACKAGE)Listener.py 
