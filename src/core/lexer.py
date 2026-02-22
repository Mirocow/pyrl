"""
Pyrl Lexer Module
Tokenizes Pyrl source code into tokens.
"""
from typing import List, Optional, Generator, Any
from .ast_nodes import Token, TokenType
from .exceptions import LexerError


KEYWORDS = {
    'if': TokenType.IF,
    'elif': TokenType.ELIF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'def': TokenType.DEF,
    'return': TokenType.RETURN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'print': TokenType.PRINT,
    'True': TokenType.TRUE,
    'False': TokenType.FALSE,
    'None': TokenType.NONE,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'import': TokenType.IMPORT,
    'from': TokenType.FROM,
    'as': TokenType.AS,
    'class': TokenType.CLASS,
    'try': TokenType.TRY,
    'except': TokenType.EXCEPT,
    'finally': TokenType.FINALLY,
    'raise': TokenType.RAISE,
    'with': TokenType.WITH,
    'lambda': TokenType.LAMBDA,
    'yield': TokenType.YIELD,
    'global': TokenType.GLOBAL,
    'nonlocal': TokenType.NONLOCAL,
    'pass': TokenType.PASS,
}


class Lexer:
    """Lexer for the Pyrl programming language."""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.tokens: List[Token] = []
        self.at_line_start = True
    
    def error(self, message: str) -> None:
        raise LexerError(message, self.line, self.column)
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.source):
            char = self.source[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self) -> None:
        """Skip spaces and tabs (not newlines)."""
        while self.peek() in (' ', '\t'):
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip a comment until end of line."""
        while self.peek() is not None and self.peek() != '\n':
            self.advance()
    
    def read_string(self, quote: str) -> str:
        """Read a string literal."""
        result = []
        while self.peek() is not None and self.peek() != quote:
            char = self.advance()
            if char == '\\':
                next_char = self.advance()
                if next_char == 'n':
                    result.append('\n')
                elif next_char == 't':
                    result.append('\t')
                elif next_char == 'r':
                    result.append('\r')
                elif next_char == '\\':
                    result.append('\\')
                elif next_char == quote:
                    result.append(quote)
                else:
                    result.append('\\')
                    result.append(next_char)
            else:
                result.append(char)
        
        if self.peek() is None:
            self.error("Unterminated string")
        
        self.advance()  # Closing quote
        return ''.join(result)
    
    def read_number(self) -> float:
        """Read a number literal."""
        result = []
        has_dot = False
        
        while self.peek() is not None:
            char = self.peek()
            if char.isdigit():
                result.append(self.advance())
            elif char == '.' and not has_dot:
                has_dot = True
                result.append(self.advance())
            else:
                break
        
        return float(''.join(result))
    
    def read_identifier(self) -> str:
        """Read an identifier."""
        result = []
        while self.peek() is not None:
            char = self.peek()
            if char.isalnum() or char == '_':
                result.append(self.advance())
            else:
                break
        return ''.join(result)
    
    def get_indent(self) -> int:
        """Calculate current indentation level."""
        indent = 0
        while self.peek() in (' ', '\t'):
            if self.peek() == ' ':
                indent += 1
            else:  # tab
                indent += 4  # Treat tab as 4 spaces
            self.advance()
        return indent
    
    def make_token(self, token_type: TokenType, value: Any = None) -> Token:
        return Token(token_type, value, self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            # Handle line start (indentation)
            if self.at_line_start:
                self.at_line_start = False
                indent = self.get_indent()
                
                # Skip empty lines and comment-only lines
                if self.peek() is None or self.peek() == '\n':
                    if self.peek() == '\n':
                        self.advance()
                        self.at_line_start = True
                    continue
                
                if self.peek() == '#':
                    self.skip_comment()
                    continue
                
                # Handle indent/dedent
                current_indent = self.indent_stack[-1]
                if indent > current_indent:
                    self.indent_stack.append(indent)
                    self.tokens.append(self.make_token(TokenType.INDENT))
                elif indent < current_indent:
                    while self.indent_stack and self.indent_stack[-1] > indent:
                        self.indent_stack.pop()
                        self.tokens.append(self.make_token(TokenType.DEDENT))
            
            char = self.peek()
            
            # Skip whitespace (not at line start)
            if char in (' ', '\t'):
                self.skip_whitespace()
                continue
            
            # Newline
            if char == '\n':
                self.tokens.append(self.make_token(TokenType.NEWLINE))
                self.advance()
                self.at_line_start = True
                continue
            
            # Comment
            if char == '#':
                self.skip_comment()
                continue
            
            # String literals
            if char in ('"', "'"):
                quote = self.advance()
                value = self.read_string(quote)
                self.tokens.append(self.make_token(TokenType.STRING, value))
                continue
            
            # Numbers
            if char.isdigit():
                value = self.read_number()
                self.tokens.append(self.make_token(TokenType.NUMBER, value))
                continue
            
            # Sigil variables and identifiers
            if char == '$':
                self.advance()
                name = self.read_identifier()
                if not name:
                    self.error("Expected identifier after $")
                self.tokens.append(self.make_token(TokenType.SCALAR, name))
                continue
            
            if char == '@':
                self.advance()
                name = self.read_identifier()
                if not name:
                    self.error("Expected identifier after @")
                self.tokens.append(self.make_token(TokenType.ARRAY, name))
                continue
            
            if char == '%':
                self.advance()
                name = self.read_identifier()
                if not name:
                    self.error("Expected identifier after %")
                self.tokens.append(self.make_token(TokenType.HASH, name))
                continue
            
            if char == '&':
                self.advance()
                name = self.read_identifier()
                if not name:
                    self.error("Expected identifier after &")
                self.tokens.append(self.make_token(TokenType.FUNCTION, name))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char == '_':
                name = self.read_identifier()
                token_type = KEYWORDS.get(name, TokenType.IDENTIFIER)
                self.tokens.append(self.make_token(token_type, name))
                continue
            
            # Multi-character operators
            two_char = self.source[self.pos:self.pos + 2] if self.pos + 1 < len(self.source) else ''
            three_char = self.source[self.pos:self.pos + 3] if self.pos + 2 < len(self.source) else ''
            
            if three_char == '...':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.IDENTIFIER, '...'))
                continue
            
            if two_char == '**':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.STARSTAR))
                continue
            
            if two_char == '//':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.DOUBLESLASH))
                continue
            
            if two_char == '==':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.EQ))
                continue
            
            if two_char == '!=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.NE))
                continue
            
            if two_char == '<=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.LE))
                continue
            
            if two_char == '>=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.GE))
                continue
            
            if two_char == '->':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.ARROW))
                continue
            
            if two_char == '+=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.PLUS_ASSIGN))
                continue
            
            if two_char == '-=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.MINUS_ASSIGN))
                continue
            
            if two_char == '*=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.STAR_ASSIGN))
                continue
            
            if two_char == '/=':
                self.advance()
                self.advance()
                self.tokens.append(self.make_token(TokenType.SLASH_ASSIGN))
                continue
            
            # Single character operators
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '%': TokenType.PERCENT,
                '=': TokenType.ASSIGN,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }
            
            if char in single_char_tokens:
                self.advance()
                self.tokens.append(self.make_token(single_char_tokens[char]))
                continue
            
            self.error(f"Unexpected character: {char}")
        
        # Emit remaining dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(self.make_token(TokenType.DEDENT))
        
        self.tokens.append(self.make_token(TokenType.EOF))
        return self.tokens


def tokenize(source: str) -> List[Token]:
    """Convenience function to tokenize source code."""
    lexer = Lexer(source)
    return lexer.tokenize()
