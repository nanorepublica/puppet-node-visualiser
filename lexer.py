from ply.lex import lex
import sys


reserved = {
      'node':'NODE',
      'inherits':'INHERITS',
      'include':'INCLUDE',
      'if':'IF',
      'elsif':'ELSIF',
      'else':'ELSE',
      'case':'CASE',
      'realize':'REALIZE',
      'notify': 'NOTIFY',
      'import': 'IMPORT',
      }

tokens = ['NAME', 'DIR', 'VAR', 'STRCONST', 'OBJECT',
          'CCURLY', 'OCURLY', 'NEWLINE', 'COMMENT', 'ARROW', 'COMMA', 'NEQUAL',
          'COLON', 'EQUALS', 'DEQUAL', 'OPAREN', 'CPAREN', 'OSQUARE', 'CSQUARE'
          ] + list(reserved.values())

t_OCURLY = r'\{'
t_CCURLY = r'\}'
t_EQUALS = r'='
t_DEQUAL = r'=='
t_NEQUAL = r'!='
t_COLON = r':'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_OSQUARE = r'\['
t_CSQUARE = r'\]'
t_COMMA = r','
t_ARROW = r'\=\>'


def t_COMMENT(t):
    r'\#.*\n'
    pass

def t_STRCONST(t):
    r'(?P<paren>[\'|"]{1})(?![A-Za-z0-9\/:$\.,\{\}@\-\'\|\\\!\_ ]+\.pp)[A-Za-z0-9\/:$\.,\{\}@\-\'\|\\\!\_ ]+(?P=paren)'
    t.type = reserved.get(t.value,'STRCONST')
    return t

def t_DIR(t):
    r'[\'|"]{1}[A-Za-z0-9\/\*\-]+.pp[\'|"]{1}'
    t.type = reserved.get(t.value,'DIR')
    return t

def t_NAME(t):
    r'([a-z0-9_\-\/][A-Za-z0-9_\-\/\$\.\^\\\[\]\+]*)((:{2})?(?=[A-Za-z0-9_\-\/\$\^\\\[\]\+]+)[A-Za-z0-9_\-\/\$\\\^\[\]\+]*)*'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_OBJECT(t):
    r'([A-Z][A-Za-z0-9_\-\/\$]*)((:{2})?(?=[A-Za-z0-9_\-\/\$]+)[A-Za-z0-9_\-\/\$]*)*'
    t.type = reserved.get(t.value,'OBJECT')
    return t

def t_VAR(t):
    r'\$([A-Za-z0-9_\-]*)(:{2})?(?=[A-Za-z0-9_\-]+)[A-Za-z0-9_\-]+'
    t.type = reserved.get(t.value,'VAR')
    return t

# Ignored Characters
t_ignore = " \t><?"

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex()

