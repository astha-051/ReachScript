from reachscript.lexer import Lexer
from reachscript.parser import Parser
from reachscript.errors import ParserError


source = '''
CAMPAIGN "Tech Outreach"

IF VERIFIED OR RESEARCH_VALID
    PERSONALIZE EMAIL
END
'''


lexer = Lexer(source)

tokens = lexer.tokenize()

parser = Parser(tokens)

try:
    program = parser.parse()

    print("Program parsed successfully!")
    print(program)

except ParserError as error:
    print("\nReachScript Error:")
    print(error)
