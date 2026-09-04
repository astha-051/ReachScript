from .lexer import TokenType
from .ast import (
    ProgramNode,
    CampaignNode,
    LoadLeadsNode,
    VerifyCompanyNode,
    ResearchCompanyNode,
    PersonalizeEmailNode,
    PreviewEmailNode,
    SendEmailNode,
    ForEachNode,
    IfNode,
    SetNode,
)
from .errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()

        if self.position < len(self.tokens) - 1:
            self.position += 1

        return token

    def skip_newlines(self):
        while self.current().type == TokenType.NEWLINE:
            self.advance()

    def expect_keyword(self, keyword):
        token = self.current()

        if (
            token.type != TokenType.KEYWORD
            or token.value != keyword
        ):
            raise ParserError(
                f"Expected '{keyword}'",
                token.line,
                token.column
            )

        self.advance()

    def check(self, token_type):
        return self.current().type == token_type

    
    def check_keyword(self, keyword):
        token = self.current()

        return (
            token.type == TokenType.KEYWORD
            and token.value == keyword
        )

    def expect_string(self):
        token = self.current()

        if token.type != TokenType.STRING:
            raise ParserError(
                "Expected string",
                token.line,
                token.column
            )

        self.advance()
        return token.value

    def expect_identifier(self):
        token = self.current()

        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected identifier at "
                f"line {token.line}, column {token.column}"
            )

        self.advance()
        return token.value

    def parse(self):
        statements = []

        self.skip_newlines()

        while self.current().type != TokenType.EOF:
            statement = self.parse_statement()

            if statement:
                statements.append(statement)

            self.skip_newlines()

        return ProgramNode(statements)

    def parse_statement(self):
        token = self.current()

        if token.type != TokenType.KEYWORD:
            raise SyntaxError(
                f"Unexpected token '{token.value}' at "
                f"line {token.line}, column {token.column}"
            )

        if token.value == "CAMPAIGN":
            return self.parse_campaign()

        if token.value == "LOAD":
            return self.parse_load_leads()

        if token.value == "VERIFY":
            return self.parse_verify()

        if token.value == "RESEARCH":
            return self.parse_research()

        if token.value == "PERSONALIZE":
            return self.parse_personalize()

        if token.value == "PREVIEW":
            return self.parse_preview()

        if token.value == "SEND":
            return self.parse_send()

        if token.value == "FOR":
            return self.parse_for_each()

        if token.value == "IF":
            return self.parse_if()

        if token.value == "SET":
            return self.parse_set()

        raise SyntaxError(
            f"Unknown statement '{token.value}' "
            f"at line {token.line}"
        )

    def parse_set(self):

        self.expect_keyword("SET")

        variable = self.current().value
        self.advance()

        token = self.current()

        if token.type != TokenType.EQUALS:
            raise ParserError(
                "Expected '=' after variable",
                token.line,
                token.column
            )

        self.advance()

        token = self.current()

        if token.type == TokenType.STRING:
            value = self.expect_string()
        else:
            value = token.value
            self.advance()

        return SetNode(
            variable=variable,
            value=value
        )

    def parse_campaign(self):
        self.expect_keyword("CAMPAIGN")

        name = self.expect_string()

        return CampaignNode(name)

    def parse_load_leads(self):
        self.expect_keyword("LOAD")
        self.expect_keyword("LEADS")
        self.expect_keyword("FROM")

        filename = self.expect_string()

        return LoadLeadsNode(filename)

    def parse_verify(self):
        self.expect_keyword("VERIFY")
        self.expect_keyword("COMPANY")

        return VerifyCompanyNode()

    def parse_research(self):
        self.expect_keyword("RESEARCH")
        self.expect_keyword("COMPANY")

        return ResearchCompanyNode()

    def parse_personalize(self):
        self.expect_keyword("PERSONALIZE")
        self.expect_keyword("EMAIL")

        tone = "PROFESSIONAL"
        length = "SHORT"
        use_verified_research = False

        while self.current().type == TokenType.KEYWORD:

            if self.current().value == "USING":
                self.advance()

                self.expect_keyword("VERIFIED")
                self.expect_keyword("RESEARCH")

                use_verified_research = True

            elif self.current().value == "TONE":
                self.advance()

                tone_token = self.current()

                if tone_token.value not in {
                    "PROFESSIONAL",
                    "FRIENDLY",
                }:
                    raise SyntaxError(
                        f"Invalid tone '{tone_token.value}' "
                        f"at line {tone_token.line}"
                    )

                tone = tone_token.value
                self.advance()

            elif self.current().value == "LENGTH":
                self.advance()

                length_token = self.current()

                if length_token.value not in {
                    "SHORT",
                    "MEDIUM",
                }:
                    raise SyntaxError(
                        f"Invalid length '{length_token.value}' "
                        f"at line {length_token.line}"
                    )

                length = length_token.value
                self.advance()

            else:
                break

        return PersonalizeEmailNode(
            tone=tone,
            length=length,
            use_verified_research=use_verified_research
        )

    def parse_preview(self):
        self.expect_keyword("PREVIEW")
        self.expect_keyword("EMAIL")

        return PreviewEmailNode()

    def parse_send(self):
        self.expect_keyword("SEND")
        self.expect_keyword("EMAIL")

        return SendEmailNode()

    def parse_for_each(self):
        self.expect_keyword("FOR")
        self.expect_keyword("EACH")

        variable = self.expect_identifier()

        self.skip_newlines()

        body = []

        while not self.is_end_keyword("END"):
            body.append(self.parse_statement())
            self.skip_newlines()

        self.expect_keyword("END")

        return ForEachNode(
            variable=variable,
            body=body
        )

    def parse_if(self):

        self.expect_keyword("IF")

        # First condition
        is_not = False

        if self.check_keyword("NOT"):
            self.advance()
            is_not = True

        condition = self.current().value
        self.advance()

        if is_not:
            condition = "NOT_" + condition

        # AND / OR
        if self.check_keyword("AND") or self.check_keyword("OR"):

            operator = self.current().value
            self.advance()

            is_not_second = False

            if self.check_keyword("NOT"):
                self.advance()
                is_not_second = True

            second_condition = self.current().value
            self.advance()

            if is_not_second:
                second_condition = "NOT_" + second_condition

            condition = (
                condition,
                operator,
                second_condition
            )

        self.skip_newlines()

        # IF body
        body = []

        while (
            not self.check_keyword("ELSE")
            and not self.check_keyword("END")
            and not self.check(TokenType.EOF)
        ):
            body.append(self.parse_statement())
            self.skip_newlines()

        else_if = []
        else_body = []

        # ELSE / ELSE IF
        while self.check_keyword("ELSE"):

            self.advance()
            self.skip_newlines()

            if self.check_keyword("IF"):

                self.advance()

                is_not = False

                if self.check_keyword("NOT"):
                    self.advance()
                    is_not = True

                else_if_condition = self.current().value
                self.advance()

                if is_not:
                    else_if_condition = "NOT_" + else_if_condition

                # Support AND / OR in ELSE IF
                if (
                    self.check_keyword("AND")
                    or self.check_keyword("OR")
                ):

                    operator = self.current().value
                    self.advance()

                    is_not_second = False

                    if self.check_keyword("NOT"):
                        self.advance()
                        is_not_second = True

                    second_condition = self.current().value
                    self.advance()

                    if is_not_second:
                        second_condition = "NOT_" + second_condition

                    else_if_condition = (
                        else_if_condition,
                        operator,
                        second_condition
                    )

                self.skip_newlines()

                else_if_body = []

                while (
                    not self.check_keyword("ELSE")
                    and not self.check_keyword("END")
                    and not self.check(TokenType.EOF)
                ):
                    else_if_body.append(
                        self.parse_statement()
                    )
                    self.skip_newlines()

                else_if.append(
                    (
                        else_if_condition,
                        else_if_body
                    )
                )

            else:

                while (
                    not self.check_keyword("END")
                    and not self.check(TokenType.EOF)
                ):
                    else_body.append(
                        self.parse_statement()
                    )
                    self.skip_newlines()

                break

        self.expect_keyword("END")

        return IfNode(
            condition=condition,
            body=body,
            else_if=else_if,
            else_body=else_body
        )

    def is_end_keyword(self, keyword):
        token = self.current()

        return (
            token.type == TokenType.KEYWORD
            and token.value == keyword
        )