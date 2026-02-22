"""
Pyrl Parser Module
Parses tokens into an Abstract Syntax Tree.
"""
from typing import List, Optional, Tuple
from .ast_nodes import *
from .exceptions import ParseError


class Parser:
    """Parser for the Pyrl programming language."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, message: str) -> None:
        token = self.current()
        raise ParseError(message, token.line, token.column)
    
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]
    
    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        return self.current().type in types
    
    def expect(self, token_type: TokenType, message: str = None) -> Token:
        if self.current().type != token_type:
            msg = message or f"Expected {token_type.value}, got {self.current().type.value}"
            self.error(msg)
        return self.advance()
    
    def skip_newlines(self) -> None:
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> ProgramNode:
        """Parse the entire program."""
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return ProgramNode(statements=statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement."""
        self.skip_newlines()
        
        if self.match(TokenType.IF):
            return self.parse_if()
        elif self.match(TokenType.WHILE):
            return self.parse_while()
        elif self.match(TokenType.FOR):
            return self.parse_for()
        elif self.match(TokenType.DEF):
            return self.parse_def()
        elif self.match(TokenType.CLASS):
            return self.parse_class()
        elif self.match(TokenType.RETURN):
            return self.parse_return()
        elif self.match(TokenType.BREAK):
            self.advance()
            return BreakNode()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            return ContinueNode()
        elif self.match(TokenType.PASS):
            self.advance()
            return PassNode()
        elif self.match(TokenType.PRINT):
            return self.parse_print()
        elif self.match(TokenType.IMPORT):
            return self.parse_import()
        elif self.match(TokenType.FROM):
            return self.parse_from_import()
        elif self.match(TokenType.TRY):
            return self.parse_try()
        elif self.match(TokenType.RAISE):
            return self.parse_raise()
        elif self.match(TokenType.WITH):
            return self.parse_with()
        elif self.match(TokenType.GLOBAL):
            return self.parse_global()
        elif self.match(TokenType.NONLOCAL):
            return self.parse_nonlocal()
        else:
            return self.parse_expr_statement()
    
    def parse_expr_statement(self) -> Optional[ASTNode]:
        """Parse an expression statement or assignment."""
        expr = self.parse_expression()
        
        if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
                      TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN):
            op_token = self.advance()
            op = op_token.value or op_token.type.value
            value = self.parse_expression()
            return AssignNode(target=expr, value=value, operator=op)
        
        return expr
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression (handles or)."""
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        """Parse or expression."""
        left = self.parse_and()
        
        while self.match(TokenType.OR):
            self.advance()
            right = self.parse_and()
            left = BinaryOpNode(left=left, operator='or', right=right)
        
        return left
    
    def parse_and(self) -> ASTNode:
        """Parse and expression."""
        left = self.parse_not()
        
        while self.match(TokenType.AND):
            self.advance()
            right = self.parse_not()
            left = BinaryOpNode(left=left, operator='and', right=right)
        
        return left
    
    def parse_not(self) -> ASTNode:
        """Parse not expression."""
        if self.match(TokenType.NOT):
            self.advance()
            operand = self.parse_not()
            return UnaryOpNode(operator='not', operand=operand)
        
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expression."""
        left = self.parse_additive()
        
        while self.match(TokenType.EQ, TokenType.NE, TokenType.LT, 
                         TokenType.LE, TokenType.GT, TokenType.GE):
            op_token = self.advance()
            op_map = {
                TokenType.EQ: '==',
                TokenType.NE: '!=',
                TokenType.LT: '<',
                TokenType.LE: '<=',
                TokenType.GT: '>',
                TokenType.GE: '>=',
            }
            right = self.parse_additive()
            left = BinaryOpNode(left=left, operator=op_map[op_token.type], right=right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expression (+ -)."""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = '+' if op_token.type == TokenType.PLUS else '-'
            right = self.parse_multiplicative()
            left = BinaryOpNode(left=left, operator=op, right=right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expression (* / // %)."""
        left = self.parse_power()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.DOUBLESLASH, TokenType.PERCENT):
            op_token = self.advance()
            op_map = {
                TokenType.STAR: '*',
                TokenType.SLASH: '/',
                TokenType.DOUBLESLASH: '//',
                TokenType.PERCENT: '%',
            }
            right = self.parse_power()
            left = BinaryOpNode(left=left, operator=op_map[op_token.type], right=right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parse power expression (**)."""
        left = self.parse_unary()
        
        if self.match(TokenType.STARSTAR):
            self.advance()
            right = self.parse_power()  # Right associative
            left = BinaryOpNode(left=left, operator='**', right=right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expression (+ -)."""
        if self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = '+' if op_token.type == TokenType.PLUS else '-'
            operand = self.parse_unary()
            return UnaryOpNode(operator=op, operand=operand)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expressions (indexing, calling, attributes)."""
        expr = self.parse_primary()
        
        while True:
            if self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET, "Expected ']'")
                expr = IndexNode(obj=expr, index=index)
            elif self.match(TokenType.LPAREN):
                self.advance()
                args = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN, "Expected ')'")
                expr = CallNode(callee=expr, args=args)
            elif self.match(TokenType.DOT):
                self.advance()
                name = self.expect(TokenType.IDENTIFIER, "Expected attribute name")
                expr = AttributeNode(obj=expr, attr=name.value)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions."""
        if self.match(TokenType.NUMBER):
            token = self.advance()
            return NumberNode(value=token.value)
        
        if self.match(TokenType.STRING):
            token = self.advance()
            return StringNode(value=token.value)
        
        if self.match(TokenType.TRUE):
            self.advance()
            return BooleanNode(value=True)
        
        if self.match(TokenType.FALSE):
            self.advance()
            return BooleanNode(value=False)
        
        if self.match(TokenType.NONE):
            self.advance()
            return NoneNode()
        
        if self.match(TokenType.SCALAR):
            token = self.advance()
            return ScalarNode(name=token.value)
        
        if self.match(TokenType.ARRAY):
            token = self.advance()
            return ArrayNode(name=token.value)
        
        if self.match(TokenType.HASH):
            token = self.advance()
            return HashNode(name=token.value)
        
        if self.match(TokenType.FUNCTION):
            token = self.advance()
            return FunctionRefNode(name=token.value)
        
        if self.match(TokenType.IDENTIFIER):
            token = self.advance()
            return ScalarNode(name=token.value)  # Treat bare identifiers as scalars
        
        if self.match(TokenType.LPAREN):
            return self.parse_paren_expr()
        
        if self.match(TokenType.LBRACKET):
            return self.parse_array_literal()
        
        if self.match(TokenType.LBRACE):
            return self.parse_hash_literal()
        
        if self.match(TokenType.LAMBDA):
            return self.parse_lambda()
        
        self.error(f"Unexpected token: {self.current().type.value}")
    
    def parse_paren_expr(self) -> ASTNode:
        """Parse parenthesized expression or tuple."""
        self.expect(TokenType.LPAREN)
        
        if self.match(TokenType.RPAREN):
            self.advance()
            return ArrayLiteralNode(elements=[])  # Empty tuple
        
        expr = self.parse_expression()
        
        if self.match(TokenType.COMMA):
            elements = [expr]
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RPAREN):
                    break
                elements.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            return ArrayLiteralNode(elements=elements)
        
        self.expect(TokenType.RPAREN)
        return expr
    
    def parse_array_literal(self) -> ArrayLiteralNode:
        """Parse array literal."""
        self.expect(TokenType.LBRACKET)
        
        elements = []
        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACKET):
                    break
                elements.append(self.parse_expression())
        
        self.expect(TokenType.RBRACKET)
        return ArrayLiteralNode(elements=elements)
    
    def parse_hash_literal(self) -> HashLiteralNode:
        """Parse hash/dict literal."""
        self.expect(TokenType.LBRACE)
        
        pairs = {}
        if not self.match(TokenType.RBRACE):
            key_token = self.advance()
            if key_token.type == TokenType.STRING:
                key = key_token.value
            elif key_token.type == TokenType.IDENTIFIER:
                key = key_token.value
            else:
                self.error("Expected string or identifier as hash key")
            
            self.expect(TokenType.COLON, "Expected ':' after key")
            value = self.parse_expression()
            pairs[key] = value
            
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACE):
                    break
                
                key_token = self.advance()
                if key_token.type == TokenType.STRING:
                    key = key_token.value
                elif key_token.type == TokenType.IDENTIFIER:
                    key = key_token.value
                else:
                    self.error("Expected string or identifier as hash key")
                
                self.expect(TokenType.COLON, "Expected ':' after key")
                value = self.parse_expression()
                pairs[key] = value
        
        self.expect(TokenType.RBRACE)
        return HashLiteralNode(pairs=pairs)
    
    def parse_lambda(self) -> LambdaNode:
        """Parse lambda expression."""
        self.expect(TokenType.LAMBDA)
        
        params = []
        if not self.match(TokenType.COLON):
            params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.expect(TokenType.COLON, "Expected ':' in lambda")
        body = self.parse_expression()
        
        return LambdaNode(params=params, body=body)
    
    def parse_block(self) -> List[ASTNode]:
        """Parse a block of statements (indented)."""
        self.expect(TokenType.INDENT, "Expected indented block")
        
        statements = []
        while not self.match(TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_if(self) -> IfNode:
        """Parse if statement."""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        
        self.skip_newlines()
        then_body = self.parse_block()
        
        elif_clauses = []
        else_body = None
        
        self.skip_newlines()
        while self.match(TokenType.ELIF):
            self.advance()
            elif_cond = self.parse_expression()
            self.skip_newlines()
            elif_body = self.parse_block()
            elif_clauses.append((elif_cond, elif_body))
            self.skip_newlines()
        
        if self.match(TokenType.ELSE):
            self.advance()
            self.skip_newlines()
            else_body = self.parse_block()
        
        return IfNode(condition=condition, then_body=then_body, 
                      elif_clauses=elif_clauses, else_body=else_body)
    
    def parse_while(self) -> WhileNode:
        """Parse while statement."""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        
        self.skip_newlines()
        body = self.parse_block()
        
        return WhileNode(condition=condition, body=body)
    
    def parse_for(self) -> ASTNode:
        """Parse for statement."""
        self.expect(TokenType.FOR)
        
        var_token = self.expect(TokenType.IDENTIFIER, "Expected loop variable")
        var = var_token.value
        
        self.expect(TokenType.IN, "Expected 'in' in for loop")
        iterable = self.parse_expression()
        
        self.skip_newlines()
        body = self.parse_block()
        
        return ForNode(var=var, iterable=iterable, body=body)
    
    def parse_def(self) -> DefNode:
        """Parse function definition."""
        self.expect(TokenType.DEF)
        
        name = self.expect(TokenType.IDENTIFIER, "Expected function name").value
        
        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        
        self.skip_newlines()
        body = self.parse_block()
        
        return DefNode(name=name, params=params, body=body)
    
    def parse_class(self) -> ClassNode:
        """Parse class definition."""
        self.expect(TokenType.CLASS)
        
        name = self.expect(TokenType.IDENTIFIER, "Expected class name").value
        
        bases = []
        if self.match(TokenType.LPAREN):
            self.advance()
            if not self.match(TokenType.RPAREN):
                bases.append(self.expect(TokenType.IDENTIFIER, "Expected base class name").value)
                while self.match(TokenType.COMMA):
                    self.advance()
                    bases.append(self.expect(TokenType.IDENTIFIER, "Expected base class name").value)
            self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        body = self.parse_block()
        
        return ClassNode(name=name, bases=bases, body=body)
    
    def parse_return(self) -> ReturnNode:
        """Parse return statement."""
        self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.EOF, TokenType.DEDENT):
            value = self.parse_expression()
        
        return ReturnNode(value=value)
    
    def parse_print(self) -> PrintNode:
        """Parse print statement."""
        self.expect(TokenType.PRINT)
        value = self.parse_expression()
        return PrintNode(value=value)
    
    def parse_import(self) -> ImportNode:
        """Parse import statement."""
        self.expect(TokenType.IMPORT)
        
        module = self.expect(TokenType.IDENTIFIER, "Expected module name").value
        
        # Handle dotted module names
        while self.match(TokenType.DOT):
            self.advance()
            next_part = self.expect(TokenType.IDENTIFIER, "Expected module name part").value
            module += '.' + next_part
        
        alias = None
        if self.match(TokenType.AS):
            self.advance()
            alias = self.expect(TokenType.IDENTIFIER, "Expected alias").value
        
        return ImportNode(module=module, alias=alias)
    
    def parse_from_import(self) -> FromImportNode:
        """Parse from...import statement."""
        self.expect(TokenType.FROM)
        
        module = self.expect(TokenType.IDENTIFIER, "Expected module name").value
        
        # Handle dotted module names
        while self.match(TokenType.DOT):
            self.advance()
            next_part = self.expect(TokenType.IDENTIFIER, "Expected module name part").value
            module += '.' + next_part
        
        self.expect(TokenType.IMPORT, "Expected 'import'")
        
        names = []
        aliases = []
        
        names.append(self.expect(TokenType.IDENTIFIER, "Expected name to import").value)
        
        if self.match(TokenType.AS):
            self.advance()
            aliases.append(self.expect(TokenType.IDENTIFIER, "Expected alias").value)
        else:
            aliases.append(None)
        
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER, "Expected name to import").value)
            
            if self.match(TokenType.AS):
                self.advance()
                aliases.append(self.expect(TokenType.IDENTIFIER, "Expected alias").value)
            else:
                aliases.append(None)
        
        return FromImportNode(module=module, names=names, aliases=aliases)
    
    def parse_try(self) -> TryNode:
        """Parse try statement."""
        self.expect(TokenType.TRY)
        
        self.skip_newlines()
        try_body = self.parse_block()
        
        except_clauses = []
        finally_body = None
        
        self.skip_newlines()
        while self.match(TokenType.EXCEPT):
            self.advance()
            
            exc_type = None
            exc_var = None
            
            if not self.match(TokenType.COLON, TokenType.NEWLINE):
                exc_type = self.expect(TokenType.IDENTIFIER, "Expected exception type").value
                
                if self.match(TokenType.AS):
                    self.advance()
                    exc_var = self.expect(TokenType.IDENTIFIER, "Expected variable name").value
            
            self.skip_newlines()
            exc_body = self.parse_block()
            except_clauses.append((exc_type, exc_var, exc_body))
            self.skip_newlines()
        
        if self.match(TokenType.FINALLY):
            self.advance()
            self.skip_newlines()
            finally_body = self.parse_block()
        
        return TryNode(try_body=try_body, except_clauses=except_clauses, finally_body=finally_body)
    
    def parse_raise(self) -> RaiseNode:
        """Parse raise statement."""
        self.expect(TokenType.RAISE)
        
        exception = self.parse_expression()
        return RaiseNode(exception=exception)
    
    def parse_with(self) -> WithNode:
        """Parse with statement."""
        self.expect(TokenType.WITH)
        
        expr = self.parse_expression()
        
        var = None
        if self.match(TokenType.AS):
            self.advance()
            var = self.expect(TokenType.IDENTIFIER, "Expected variable name").value
        
        self.skip_newlines()
        body = self.parse_block()
        
        return WithNode(expr=expr, var=var, body=body)
    
    def parse_global(self) -> GlobalNode:
        """Parse global statement."""
        self.expect(TokenType.GLOBAL)
        
        names = [self.expect(TokenType.IDENTIFIER, "Expected variable name").value]
        
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER, "Expected variable name").value)
        
        return GlobalNode(names=names)
    
    def parse_nonlocal(self) -> NonlocalNode:
        """Parse nonlocal statement."""
        self.expect(TokenType.NONLOCAL)
        
        names = [self.expect(TokenType.IDENTIFIER, "Expected variable name").value]
        
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER, "Expected variable name").value)
        
        return NonlocalNode(names=names)


def parse(tokens: List[Token]) -> ProgramNode:
    """Convenience function to parse tokens into an AST."""
    parser = Parser(tokens)
    return parser.parse()


def parse_source(source: str) -> ProgramNode:
    """Convenience function to parse source code into an AST."""
    from .lexer import tokenize
    tokens = tokenize(source)
    return parse(tokens)
