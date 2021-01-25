import enum
import re
from typing import Iterator, NamedTuple

__all__ = ("TokenType", "Token", "lex")


class TokenType(enum.Enum):
    """A type of lexical unit."""

    # Unary connectives
    NOT = re.compile(r"[~¬]")

    # Binary connectives
    AND = re.compile(r"[∧&∙]|/\\")
    OR = re.compile(r"[∨|]|\\/")
    IMPLIES = re.compile(r"[>→⇒⊃]")
    # BICONDITIONAL = re.compile(r"[↔≡=]")

    PARENTHESIS_LEFT = re.compile(r"\(")
    PARENTHESIS_RIGHT = re.compile(r"\)")

    VARIABLE = re.compile(r"[a-zA-Z]+")
    WHITESPACE = re.compile(r"\s+")


class Token(NamedTuple):
    """A lexical token; a categorisation of a lexeme as a kind of lexical unit."""

    type: TokenType
    value: str
    pos: int

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(type={self.type.name}, value={self.value!r}, pos={self.pos})"


def lex(formula: str) -> Iterator[Token]:
    """Lex a propositional formula and yield tokens."""
    i = 0
    while i < len(formula):
        for token_type in TokenType:
            match = token_type.value.match(formula, i)
            if match:
                if token_type is not TokenType.WHITESPACE:
                    yield Token(token_type, match[0], i)
                i = match.end(0)
                break
        else:
            raise ValueError(f"Unknown character {formula[i]!r} at position {i}.")
