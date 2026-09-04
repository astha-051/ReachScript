class ReachScriptError(Exception):
    """Base error for ReachScript."""

    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

        if line is not None:
            location = f"Line {line}"
            if column is not None:
                location += f", Column {column}"

            message = f"{location}: {message}"

        super().__init__(message)


class LexerError(ReachScriptError):
    pass


class ParserError(ReachScriptError):
    pass


class RuntimeError(ReachScriptError):
    pass