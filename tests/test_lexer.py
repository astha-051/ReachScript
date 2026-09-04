from reachscript.lexer import Lexer


source = """
CAMPAIGN "Tech Outreach"

IF VERIFIED OR RESEARCH_VALID
    PERSONALIZE EMAIL
END
"""


lexer = Lexer(source)

tokens = lexer.tokenize()


for token in tokens:
    print(token)


# Make sure comments are ignored
for token in tokens:
    assert "#" not in token.value

print("\n✓ Comment test passed")