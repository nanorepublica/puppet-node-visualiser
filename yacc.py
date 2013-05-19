from ply.yacc import yacc
import re

from lexer import tokens

nodes = {}
classes = {}

def traverse_node_tree(tree, name):
    '''Given a tree of nodes and a named node return list of children of the named node'''
    if tree['name'] == name:
        return tree['children']
    else:
        for child in tree['children']:
            return traverse_node_tree(child, name)

def p_start(p):
    '''start : nodes '''
    pass

def p_nodes(p):
    '''nodes : node nodes
             | NEWLINE node nodes
             | empty'''
    pass

def p_node(p):
    '''node : NODE NAME node_inheritance node_content NEWLINE
            | NODE NAME node_inheritance node_content'''
    classes[p[2]] = p[4]
    if not p[3]:
        nodes['name'] = p[2]
        nodes['children'] = []
        nodes['classes'] = p[4]
    else:
        new = {'name':p[2], 'children':[], 'classes': p[4]}
        # traverse nodes to find where p[3] == 'name'
        # then add {'name':p[2], 'children':[]}
        traverse_node_tree(nodes,p[3]).append(new)



def p_node_inheritance(p):
    '''node_inheritance : INHERITS NAME
                        | empty'''
    if p[1]:
        p[0] = p[2]

def p_node_content(p):
    '''node_content : OCURLY statements CCURLY
                    | OCURLY NEWLINE statements CCURLY
                    | OCURLY CCURLY'''
    if p[2] != '}':
        if not re.match('\n+', p[2]):
            p[0] = p[2]
        else:
            p[0] = p[3]
    else:
        p[0] = []

def p_statements(p):
    '''statements : statement NEWLINE statements
                  | empty'''
    if p[1]:
        if p[3] is None:
            p[0] = [p[1]]
        else:
            p[3].append(p[1])
            p[0] = p[3]

def p_statement(p):
    '''statement : INCLUDE NAME'''
    p[0] = p[2]

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input! -> %s" % p

# Build the parser
parser = yacc()
