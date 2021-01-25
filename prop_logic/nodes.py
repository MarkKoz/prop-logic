from dataclasses import dataclass

from prop_logic.connectives import BinaryConnective, UnaryConnective

__all__ = ("Node", "Formula", "BinaryFormula", "UnaryFormula", "Variable")


class Node:
    """Base class for all nodes of the abstract syntax tree (AST)."""


class Formula(Node):
    """A propositional formula. It is a well-formed formula and has a truth value.

    Also known as a propositional expression, sentence, or sentential formula, it is a formal
    expression which denotes a proposition.
    """


@dataclass
class UnaryFormula(Formula):
    """A propositional formula connected by a unary connective."""

    connective: UnaryConnective
    operand: Formula

    def __str__(self) -> str:
        return f"{self.connective}{self.operand}"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(connective={self.connective!r}, operand={self.operand!r})"


@dataclass
class BinaryFormula(Formula):
    """Two propositional formulas connected by a binary connective."""

    left: Formula
    connective: BinaryConnective
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} {self.connective} {self.right})"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(left={self.left!r}, connective={self.connective!r}, right={self.right!r})"


@dataclass
class Variable(Formula):
    """An atomic propositional formula (atom).

    Also known as a sentential variable or sentential letter, it is the simplest well-formed formula
    in propositional logic; it lacks logical constants and strict subformulas.
    """

    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
