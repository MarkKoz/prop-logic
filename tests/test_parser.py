import pytest

from prop_logic import lexer
from prop_logic.connectives import Conjunction, Implication, Negation
from prop_logic.nodes import BinaryFormula, UnaryFormula, Variable
from prop_logic.parser import Parser

PARAMS_GROUPED = [
    (
        "A & B > C",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "(A & B) > C",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "A & (B > C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "(A & B > C)",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "(A & (B > C))",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "((A & B) > C)",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
]

PARAMS_UNGROUPED_NOT = [
    (
        "~A & B > C",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "A & ~B > C",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "A & B > ~C",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "~A & ~B > C",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "A & ~B > ~C",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    (
        "~A & B > ~C",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "~A & ~B > ~C",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
]

PARAMS_GROUPED_NOT = [
    (
        "(~A & B) > C",
        BinaryFormula(
            BinaryFormula(UnaryFormula(Negation, Variable("A")), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "(A & ~B) > C",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, UnaryFormula(Negation, Variable("B"))),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "(A & B) > ~C",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "(~A & ~B) > C",
        BinaryFormula(
            BinaryFormula(
                UnaryFormula(Negation, Variable("A")),
                Conjunction,
                UnaryFormula(Negation, Variable("B")),
            ),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "(~A & B) > ~C",
        BinaryFormula(
            BinaryFormula(UnaryFormula(Negation, Variable("A")), Conjunction, Variable("B")),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "(A & ~B) > ~C",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, UnaryFormula(Negation, Variable("B"))),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "(~A & ~B) > ~C",
        BinaryFormula(
            BinaryFormula(
                UnaryFormula(Negation, Variable("A")),
                Conjunction,
                UnaryFormula(Negation, Variable("B")),
            ),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    # Next
    (
        "~A & (B > C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "A & (~B > C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "A & (B > ~C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "~A & (~B > C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "~A & (B > ~C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "A & (~B > ~C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    (
        "~A & (~B > ~C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    # Next
    (
        "((~A & B) > C)",
        BinaryFormula(
            BinaryFormula(UnaryFormula(Negation, Variable("A")), Conjunction, Variable("B")),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "((A & ~B) > C)",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, UnaryFormula(Negation, Variable("B"))),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "((A & B) > ~C)",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, Variable("B")),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "((~A & ~B) > C)",
        BinaryFormula(
            BinaryFormula(
                UnaryFormula(Negation, Variable("A")),
                Conjunction,
                UnaryFormula(Negation, Variable("B")),
            ),
            Implication,
            Variable("C"),
        ),
    ),
    (
        "((~A & B) > ~C)",
        BinaryFormula(
            BinaryFormula(UnaryFormula(Negation, Variable("A")), Conjunction, Variable("B")),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "((A & ~B) > ~C)",
        BinaryFormula(
            BinaryFormula(Variable("A"), Conjunction, UnaryFormula(Negation, Variable("B"))),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    (
        "((~A & ~B) > ~C)",
        BinaryFormula(
            BinaryFormula(
                UnaryFormula(Negation, Variable("A")),
                Conjunction,
                UnaryFormula(Negation, Variable("B")),
            ),
            Implication,
            UnaryFormula(Negation, Variable("C")),
        ),
    ),
    # Next
    (
        "(~A & (B > C))",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "(A & (~B > C))",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "(A & (B > ~C))",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "(~A & (~B > C))",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "(~A & (B > ~C))",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "(A & (~B > ~C))",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    (
        "(~A & (~B > ~C))",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    # Next
    (
        "(~A & B > C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, Variable("C")),
        ),
    ),
    (
        "(A & ~B > C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "(A & B > ~C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "(~A & ~B > C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(UnaryFormula(Negation, Variable("B")), Implication, Variable("C")),
        ),
    ),
    (
        "(A & ~B > ~C)",
        BinaryFormula(
            Variable("A"),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
    (
        "(~A & B > ~C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(Variable("B"), Implication, UnaryFormula(Negation, Variable("C"))),
        ),
    ),
    (
        "(~A & ~B > ~C)",
        BinaryFormula(
            UnaryFormula(Negation, Variable("A")),
            Conjunction,
            BinaryFormula(
                UnaryFormula(Negation, Variable("B")),
                Implication,
                UnaryFormula(Negation, Variable("C")),
            ),
        ),
    ),
]


def get_ast(function):
    tokens = lexer.lex(function)
    parser = Parser(tokens)
    return parser.parse()


@pytest.mark.parametrize(["function", "expected"], PARAMS_GROUPED)
def test_parser_grouped(function, expected):
    assert get_ast(function) == expected


@pytest.mark.parametrize(["function", "expected"], PARAMS_UNGROUPED_NOT)
def test_parser_ungrouped_not(function, expected):
    assert get_ast(function) == expected


@pytest.mark.parametrize(["function", "expected"], PARAMS_GROUPED_NOT)
def test_parser_grouped_not(function, expected):
    assert get_ast(function) == expected
