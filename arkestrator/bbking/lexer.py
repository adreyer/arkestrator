import ply.lex as lex

tokens = (
    'LBRACKET',
    'RBRACKET',
    'SLASH',
    'EQ',
    'SYMBOL',
    'WHITESPACE',
    'MISC',
)

t_LBRACKET = '\['
t_RBRACKET = '\]'
t_SLASH = '/'
t_EQ = '='
t_SYMBOL = '[A-Za-z_][A-Za-z0-9_]*'
t_WHITESPACE = '[ \t\n]+'
t_MISC = '[^\[\]/=A-Za-z \t\n_]+'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

