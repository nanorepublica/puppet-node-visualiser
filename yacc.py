'''yacc file'''
from ply.yacc import yacc
import re
import sys
from collections import defaultdict

from lexer import tokens

t_nodes = defaultdict(list)
nodes = {}
nodes['name'] = 'puppet_nodes'
nodes['children'] = []
nodes['classes'] = []


def traverse_node_tree(tree, name):
    '''Given a tree of nodes and a named node return list of children of the named node'''
    if tree['name'] == name:
        return tree['children']
    else:
        for child in tree['children']:
            return traverse_node_tree(child, name)


def p_start(p):
    '''start : nodes'''
    pass


def p_nodes(p):
    '''nodes : node nodes
             | comment nodes
             | import nodes
             | case_statement nodes
             | if_statement nodes
             | case_content nodes
             | NEWLINE nodes
             | empty'''
    pass

def p_comment(p):
    '''comment : COMMENT'''
    print list(p)

def p_import(p):
    '''import : IMPORT DIR NEWLINE'''
    pass

def p_if_statement(p):
    '''if_statement : IF conditional OCURLY case_content CCURLY
                    | IF conditional OCURLY NEWLINE case_content CCURLY
                    | IF conditional OCURLY NEWLINE case_content CCURLY ELSE OCURLY case_content CCURLY
                    | IF conditional OCURLY case_content CCURLY ELSE OCURLY NEWLINE case_content CCURLY
                    | IF conditional OCURLY NEWLINE case_content CCURLY ELSE OCURLY NEWLINE case_content CCURLY
                    | IF conditional OCURLY NEWLINE case_content CCURLY elsif ELSE OCURLY case_content CCURLY
                    | IF conditional OCURLY NEWLINE case_content CCURLY elsif ELSE OCURLY NEWLINE case_content CCURLY'''
    print 'if statement ', list(p)

def p_elsif(p):
    '''elsif : ELSIF conditional OCURLY case_content CCURLY elsif
             | ELSIF conditional OCURLY NEWLINE case_content CCURLY elsif
             | empty'''
    pass

def p_conditional(p):
    '''conditional : VAR DEQUAL STRCONST
                   | NAME OPAREN STRCONST CPAREN'''
    print 'conditional ', list(p)

def p_case_statement(p):
    '''case_statement : CASE VAR OCURLY switch_content CCURLY
                      | CASE VAR OCURLY NEWLINE switch_content CCURLY'''
    pass

def p_switch_content(p):
    '''switch_content : case_condition COLON OCURLY NEWLINE case_content CCURLY NEWLINE switch_content
                      | case_condition COLON OCURLY case_content CCURLY NEWLINE switch_content
                      | case_condition COLON OCURLY NEWLINE case_content CCURLY NEWLINE
                      | case_condition COLON OCURLY case_content CCURLY NEWLINE''' 
    pass

def p_case_condition(p):
    '''case_condition : STRCONST COMMA case_condition
                      | NAME COMMA case_condition
                      | STRCONST
                      | NAME'''
    pass

def p_case_content(p):
    '''case_content : VAR EQUALS STRCONST NEWLINE case_content
                    | VAR EQUALS STRCONST NEWLINE
                    | VAR EQUALS NAME OPAREN CPAREN NEWLINE case_content
                    | VAR EQUALS NAME OPAREN CPAREN NEWLINE
                    | VAR EQUALS VAR NEWLINE case_content
                    | VAR EQUALS VAR NEWLINE
                    | resource_default NEWLINE case_content
                    | resource_default NEWLINE
                    | resource_default
                    | resource NEWLINE case_content
                    | resource NEWLINE
                    | resource 
                    | statement NEWLINE case_content
                    | statement NEWLINE
                    | statement'''
    print 'case_statement ', list(p)
    if p[1] == 'include':
        p[0] = p[2]

def p_resource_default(p):
    '''resource_default : NAME OCURLY resource_arg CCURLY
                        | NAME OCURLY NEWLINE resource_arg CCURLY'''
    pass

def p_resource_arg(p):
    '''resource_arg : NAME ARROW list resource_delimit resource_arg
                    | NAME ARROW STRCONST resource_delimit resource_arg
                    | NAME ARROW NAME resource_delimit resource_arg
                    | NAME ARROW VAR resource_delimit resource_arg
                    | empty'''
    pass

def p_resource_delimit(p):
    '''resource_delimit : COMMA
                        | COMMA NEWLINE
                        | NEWLINE
                        | empty'''
    pass

def p_resource(p):
    '''resource : NAME OCURLY NAME COLON resource_arg CCURLY'''
    pass


def p_list(p):
    '''list : OSQUARE list_content CSQUARE'''
    pass

def p_list_content(p):
    '''list_content : STRCONST COMMA list_content
                    | STRCONST list_content
                    | NAME list_content
                    | NAME COMMA list_content
                    | VAR list_content
                    | VAR COMMA list_content
                    | empty'''
    pass


def p_node(p):
    '''node : NODE NAME node_inheritance node_content NEWLINE
            | NODE NAME node_inheritance node_content'''
    new = {'name':p[2], 'children':[], 'classes': p[4]}
    if not p[3]:
        nodes['children'].append(new)
        print nodes
    else:
        # new = {'name':p[2], 'children':[], 'classes': p[4]}
        # traverse nodes to find where p[3] == 'name'
        # then add {'name':p[2], 'children':[]
        t_nodes[p[3]].append(new)
        # print t_nodes
        # traverse_node_tree(nodes,p[3]).append(new)



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
    '''statements : statement statements
                  | case_statement NEWLINE statements
                  | if_statement NEWLINE statements
                  | case_content NEWLINE statements
                  | empty'''
#    print list(p)
    if p[1]:
        try:
            if p[3] is None:
                p[0] = [p[1]]
            else:
                p[3].append(p[1])
                p[0] = p[3]
        except IndexError:
            p[0] = [p[1]]


def p_statement(p):
    '''statement : INCLUDE NAME comment
                 | INCLUDE NAME'''
    print 'statement ', list(p)
    if p[1] == 'include':
        p[0] = p[2]


def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input! -> %s" % p
    sys.exit(1)

# Build the parser
parser = yacc()
