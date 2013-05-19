from ply.lex import lex


reserved = {
      'node':'NODE',
      'inherits':'INHERITS',
      'include':'INCLUDE'
      }

tokens = ['NAME',
          'CCURLY', 'OCURLY', 'NEWLINE'
          ] + list(reserved.values())

t_OCURLY = r'\{'
t_CCURLY = r'\}'

def t_NAME(t):
    r'[A-Za-z0-9_\-\.]+'
    t.type = reserved.get(t.value,'NAME')
    return t

# Ignored Characters
t_ignore = " \t"

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex()

