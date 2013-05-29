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
             | import nodes
             | statements nodes
             | empty'''
    pass

# nodes
def p_node(p):
    '''node : NODE NAME node_inheritance node_content opt_line_end'''
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
    '''node_content : OCURLY opt_line_end statements CCURLY
                    | OCURLY CCURLY'''
    if p[2] != '}':
        if not re.match('\n+', p[2]):
            p[0] = p[2]
        else:
            p[0] = p[3]
    else:
        p[0] = []


def p_import(p):
    '''import : IMPORT DIR line_end'''
    pass

def p_statements(p):
    '''statements : assignment statements
                  | resource statements
                  | include statements
                  | case_statement statements
                  | if_statement statements
                  | line_end statements
                  | line_end'''
    print 'statements ', list(p)
    # if p[1] == 'include':
    #     p[0] = p[2]

#    print list(p)
    # if p[1]:
    #     try:
    #         if p[3] is None:
    #             p[0] = [p[1]]
    #         else:
    #             p[3].append(p[1])
    #             p[0] = p[3]
    #     except IndexError:
    #         p[0] = [p[1]]

def p_assignment(p):
    '''assignment : VAR EQUALS STRCONST opt_line_end
                  | VAR EQUALS VAR opt_line_end
                  | VAR EQUALS NAME OPAREN CPAREN opt_line_end'''
    pass

# resources
def p_resource(p):
    '''resource : NAME OCURLY resource_default opt_line_end resource_arg CCURLY opt_line_end'''
    pass

def p_resource_default(p):
    '''resource_default : NAME COLON
                        | empty'''
    pass

def p_resource_arg(p):
    '''resource_arg : NAME ARROW list resource_delimit resource_arg
                    | NAME ARROW STRCONST resource_delimit resource_arg
                    | NAME ARROW NAME resource_delimit resource_arg
                    | NAME ARROW VAR resource_delimit resource_arg
                    | empty'''
    print 'resource_arg ', list(p)

def p_resource_delimit(p):
    '''resource_delimit : COMMA opt_line_end
                        | opt_line_end'''
    pass

# if & case
def p_if_statement(p):
    '''if_statement : IF conditional OCURLY opt_line_end statements CCURLY
                    | IF conditional OCURLY opt_line_end statements CCURLY ELSE OCURLY opt_line_end statements CCURLY
                    | IF conditional OCURLY opt_line_end statements CCURLY elsif ELSE OCURLY opt_line_end statements CCURLY'''
    print 'if statement ', list(p)

def p_elsif(p):
    '''elsif : ELSIF conditional OCURLY opt_line_end statements CCURLY elsif
             | empty'''
    pass

def p_conditional(p):
    '''conditional : VAR DEQUAL STRCONST
                   | NAME OPAREN STRCONST CPAREN'''
    print 'conditional ', list(p)

def p_case_statement(p):
    '''case_statement : CASE VAR OCURLY opt_line_end switch_content CCURLY'''
    pass

def p_switch_content(p):
    '''switch_content : case_condition COLON OCURLY opt_line_end statements CCURLY opt_line_end switch_content
                      | case_condition COLON OCURLY opt_line_end statements CCURLY opt_line_end''' 
    pass

def p_case_condition(p):
    '''case_condition : STRCONST COMMA case_condition
                      | NAME COMMA case_condition
                      | STRCONST
                      | NAME'''
    pass

# include modules = important one!
def p_include(p):
    '''include : INCLUDE NAME line_end'''
    print 'include ', list(p)
    if p[1] == 'include':
        p[0] = p[2]

#line endings
def p_line_end(p):
    '''line_end : COMMENT
                | NEWLINE'''
    print 'line_end ', list(p)

def p_opt_line_end(p):
    '''opt_line_end : line_end
                    | empty'''
    pass

# lists
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

def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input! -> %s" % p
    sys.exit(1)

# Build the parser
parser = yacc()
