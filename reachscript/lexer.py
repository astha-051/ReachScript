from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    KEYWORD = "KEYWORD"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    EQUALS = "EQUALS"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


KEYWORDS = {
    "CAMPAIGN",
    "LOAD",
    "LEADS",
    "FROM",

    "FOR",
    "EACH",

    "VERIFY",
    "COMPANY",
    "RESEARCH",

    "PERSONALIZE",
    "EMAIL",

    "IF",
    "VERIFIED",
    "RESEARCH_VALID",

    "PREVIEW",
    "SEND",

    "TONE",
    "PROFESSIONAL",
    "FRIENDLY",

    "LENGTH",
    "SHORT",
    "MEDIUM",

    "USING",

    "END",

    "SET",
    "TONE",
    "LENGTH",

    "SENDER",

    "SUBJECT",
    "ELSE",
    "NOT",
    "AND",
    "OR"
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []

        while self.position < len(self.source):
            current = self.source[self.position]

            # Ignore spaces and tabs
            if current in " \t\r":
                self.advance()
                continue

            # Comment
            if current == "#":
                while (
                    self.position < len(self.source)
                    and self.source[self.position] != "\n"
                ):
                    self.advance()

                continue

            # New line
            if current == "\n":
                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\\n",
                        self.line,
                        self.column
                    )
                )

                self.advance()
                self.line += 1
                self.column = 1
                continue

            # String
            if current == '"':
                tokens.append(self.read_string())
                continue

            # Number
            if current.isdigit():
                tokens.append(self.read_number())
                continue

            # Identifier / Keyword
            if current.isalpha() or current == "_":
                tokens.append(self.read_identifier())
                continue

            if current == "=":
                tokens.append(
                    Token(
                        TokenType.EQUALS,
                        "=",
                        self.line,
                        self.column
                    )
                )

                self.advance()
                continue
            
            raise SyntaxError(
                f"Unexpected character '{current}' "
                f"at line {self.line}, column {self.column}"
            )

        tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.line,
                self.column
            )
        )

        return tokens

    def read_string(self):
        start_line = self.line
        start_column = self.column

        # Skip opening quote
        self.advance()

        value = ""

        while self.position < len(self.source):
            current = self.source[self.position]

            if current == '"':
                self.advance()

                return Token(
                    TokenType.STRING,
                    value,
                    start_line,
                    start_column
                )

            value += current
            self.advance()

        raise SyntaxError(
            f"Unterminated string at "
            f"line {start_line}, column {start_column}"
        )

    def read_number(self):
        start_line = self.line
        start_column = self.column

        value = ""

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            value += self.source[self.position]
            self.advance()

        return Token(
            TokenType.NUMBER,
            value,
            start_line,
            start_column
        )

    def read_identifier(self):
        start_line = self.line
        start_column = self.column

        value = ""

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):
            value += self.source[self.position]
            self.advance()

        if value.upper() in KEYWORDS:
            token_type = TokenType.KEYWORD
            value = value.upper()
        else:
            token_type = TokenType.IDENTIFIER

        return Token(
            token_type,
            value,
            start_line,
            start_column
        )

    def advance(self):
        self.position += 1
        self.column += 1