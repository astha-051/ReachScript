from reachscript.lexer import Lexer
from reachscript.parser import Parser
from reachscript.interpreter import Interpreter
from reachscript.errors import RuntimeError


with open("examples/basic.reach", "r") as file:
    source = file.read()


lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse()

interpreter = Interpreter()
interpreter.verified = False
interpreter.research_valid = False

try:
    interpreter.execute(program)

except RuntimeError as error:
    print("\nReachScript Error:")
    print(error)