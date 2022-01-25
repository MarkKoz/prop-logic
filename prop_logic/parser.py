from typing import Iterator, Optional

from prop_logic import nodes
from prop_logic.connectives import BinaryConnective, UnaryConnective
from prop_logic.lexer import Token, TokenType


class Parser:
    """Parser of propositional formulas in propositional logic."""

    def __init__(self, tokens: Iterator[Token]):
        self.tokens = tokens
        self.token = self.next()

    def next(self) -> Optional[Token]:
        """Save and return the next token."""
        self.token = next(self.tokens, None)
        return self.token

    def accept(self, type_: TokenType) -> bool:
        """Return True if the current token matches `type_` and advance to the next token."""
        if self.token and self.token.type is type_:
            self.next()
            return True
        else:
            return False

    def expect(self, type_: TokenType) -> bool:
        """Same as `accept`, but raise ValueError for `type_` mismatches."""
        if self.accept(type_):
            return True
        else:
            found_type = self.token.type if self.token else "EOF"
            raise ValueError(f"Unexpected token: expected {type_} but found {found_type}")

    def parse(self) -> nodes.Formula:
        """Parse tokens into an abstract syntax tree representing a propositional formula.

        This is a recursive descent parser combined with an operator-precedence parser for
        binary formulas.
        """
        node = self.parse_formula()
        if self.token is not None:
            raise ValueError(f"Syntax error: unexpected token {self.token.value!r}")
        else:
            return node

    def parse_term(self) -> nodes.Formula:
        """Parse tokens into a variable, a grouped formula, or a unary formula."""
        token = self.token
        if self.accept(TokenType.VARIABLE):
            return nodes.Variable(token.value)
        elif self.accept(TokenType.PARENTHESIS_LEFT):
            return self.parse_group()
        elif connective := UnaryConnective.from_token(token):
            return self.parse_unary(connective)
        else:
            raise ValueError(f"Unexpected token {token}")

    def parse_group(self) -> nodes.Formula:
        """Parse tokens as an formula surrounded by parenthesis."""
        node = self.parse_formula()
        self.expect(TokenType.PARENTHESIS_RIGHT)
        return node

    def parse_unary(self, connective: UnaryConnective) -> nodes.UnaryFormula:
        """Parse tokens as a unary formula."""
        self.next()  # Consume unary connective token.
        operand = self.parse_term()

        return nodes.UnaryFormula(connective, operand)

    def parse_formula(self) -> nodes.Formula:
        """Parse tokens as a term and maybe a binary formula."""
        left = self.parse_term()
        return self.parse_binary(left)

    def parse_binary(self, left: nodes.Formula, min_precedence: int = 0) -> nodes.Formula:
        """Maybe parse tokens as a binary formula.

        If the current token is not a binary connective with a higher precedence than
        `min_precedence`, then return the node `left` as-is.

        This is an operator-precedence parser based on http://lisperator.net/pltut/parser/the-parser
        """
        token = self.token
        if connective := BinaryConnective.from_token(token):
            if connective.precedence > min_precedence:
                self.next()  # Consume binary connective token.
                right = self.parse_binary(self.parse_term(), connective.precedence)
                left = nodes.BinaryFormula(left, connective, right)

                # Another binary formula with a higher precedence may follow.
                return self.parse_binary(left, min_precedence)

        # Return the left if the token is not a binary connective or its precedence is lower.
        return left

    def parse_binary_old(self, left: nodes.Formula, min_precedence: int = 0) -> nodes.Formula:
        """Operator-precedence parser based on pseudocode from Wikipedia."""
        token = self.token
        while (
            connective := BinaryConnective.from_token(token)
        ) and connective.precedence >= min_precedence:
            self.next()  # Consume binary connective token.
            right = self.parse_term()
            token = self.token
            while (
                next_connective := BinaryConnective.from_token(token)
            ) and next_connective.precedence > connective.precedence:
                self.next()  # Consume binary connective token.
                right = self.parse_binary(right, next_connective.precedence)
                token = self.token

            left = nodes.BinaryFormula(left, connective, right)

        return left


if __name__ == "__main__":
    from prop_logic.lexer import lex

    tokens_ = lex("A & B > C")
    parser = Parser(tokens_)
    result = parser.parse()
    print(result, repr(result))
