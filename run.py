import sys

from reachscript.lexer import Lexer
from reachscript.parser import Parser
from reachscript.interpreter import Interpreter
from reachscript.errors import RuntimeError


def main():

    if len(sys.argv) != 2:
        print("Usage: python run.py <file.reach>")
        print()
        print("Examples:")
        print("  python run.py examples/basic.reach")
        print("  python run.py examples/conditional.reach")
        print("  python run.py examples/advanced.reach")
        print("  python run.py examples/real_email.reach")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter = Interpreter()
        interpreter.execute(program)

    except FileNotFoundError:
        print(f"\nReachScript Error:")
        print(f"File not found: {filename}")

    except RuntimeError as error:
        print("\nReachScript Error:")
        print(error)

    except Exception as error:
        print("\nUnexpected Error:")
        print(error)


if __name__ == "__main__":
    main()