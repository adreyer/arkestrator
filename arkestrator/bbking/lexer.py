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

t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SLASH = r'/'
t_EQ = r'='
t_SYMBOL = r'[A-Za-z_][A-Za-z0-9_]*'
t_WHITESPACE = r'[ \t\n]+'
t_MISC = r'[^\[\]/=A-Za-z \t\n_]+'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

