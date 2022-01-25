from __future__ import annotations

from functools import total_ordering
from typing import Any, Optional, Protocol, Type, TypeVar, cast, runtime_checkable

from prop_logic.lexer import Token, TokenType

__all__ = (
    "Connective",
    "UnaryConnective",
    "BinaryConnective",
    "Negation",
    "Conjunction",
    "Disjunction",
    "Implication",
)


@runtime_checkable
class ConnectiveProtocol(Protocol):
    """Specification of the interface all concrete Connectives must implement."""

    type: TokenType
    precedence: int
    lexeme: str


@total_ordering
class Connective(ConnectiveProtocol, type):
    """Base metaclass which represents a logical connective.

    Comparison operators compare the precedences of the operands.
    """

    __type_connectives: dict[TokenType, Connective] = {}

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> Connective:
        """Create a new Connective type and ensure it's uniquely associated with a TokenType."""
        cls = super().__new__(mcls, name, bases, namespace)

        if isinstance(cls, mcls):
            if cls.type in mcls.__type_connectives:
                raise ValueError(f"A {mcls.__name__} with type {cls.type!r} is already defined.")
            else:
                mcls.__type_connectives[cls.type] = cls
        else:
            raise ValueError(f"{cls.__name__} must subtype {ConnectiveProtocol.__name__}.")

        return cls

    def __eq__(cls, other: object) -> bool:
        if isinstance(other, type) and issubclass(other, ConnectiveProtocol):
            return cls.precedence == other.precedence
        else:
            return NotImplemented

    def __lt__(cls, other: object) -> bool:
        if isinstance(other, type) and issubclass(other, ConnectiveProtocol):
            return cls.precedence < other.precedence
        else:
            return NotImplemented

    def __str__(cls) -> str:
        """Return the lexeme which represents the connective."""
        return cls.lexeme

    def __repr__(cls) -> str:
        """Return the connective's name."""
        return cls.__name__

    @classmethod
    def from_token(
        mcls: Type[ConnectiveType], token: Optional[Token]  # noqa: N804
    ) -> Optional[ConnectiveType]:
        """Create a Connective from a `token`. Return None if `token` is invalid."""
        if token is None:
            return None

        try:
            # There doesn't seem to be a good way to annotate the dict value as the subclass's type.
            return cast(ConnectiveType, mcls.__type_connectives[token.type])
        except KeyError:
            return None
            # valid_types = ", ".join(type_.name for type_ in mcls.__type_connectives)
            # raise ValueError(f"Invalid type for {token!r}. Valid types: {valid_types}") from None


ConnectiveType = TypeVar("ConnectiveType", bound=Connective)


class UnaryConnective(Connective):
    """Metaclass for a logical connective with an arity of one."""


class BinaryConnective(Connective):
    """Metaclass for a logical connective with an arity of two."""


class Negation(metaclass=UnaryConnective):
    """Unary connective for logical negation. Commonly known as 'not'."""

    type = TokenType.NOT
    precedence = 5
    lexeme = "¬"


class Conjunction(metaclass=BinaryConnective):
    """Binary connective for a logical conjunction. Commonly known as 'and'."""

    type = TokenType.AND
    precedence = 4
    lexeme = "∧"


class Disjunction(metaclass=BinaryConnective):
    """Binary connective for a logical disjunction. Commonly known as 'or'."""

    type = TokenType.OR
    precedence = 3
    lexeme = "∨"


class Implication(metaclass=BinaryConnective):
    """Binary connective for a material implication. Commonly known as a conditional."""

    type = TokenType.IMPLIES
    precedence = 2
    lexeme = "→"
