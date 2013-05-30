'''This parses the data and serves the webapp'''
from lexer import lexer
from yacc import parser, nodes, t_nodes
from flask import Flask, render_template
import json
APP = Flask(__name__)

DEBUG = 0
LDEBUG = 0 

DATA = '''# site.pp
#
#
    case $hi {
        'a': {
        }
    }

node default {}

node base inherits default {
    include ssh
    include ntp
}

node virtual inherits base {
    include vmware::version6
}

node ithfme01 inherits virtual {
    include app
}'''


# nodes = {
#   'name' : 'default',
#   'children':[
#       {
#           'name': 'base',
#           'children': [
#               {
#                   'name': 'virtual',
#                   'children':[
#                       {
#                           'name': 'ithfme01',
#                           'children': []
#                       }
#                   ]
#               }
#           ]
#       }
#   ]
# }

# classes = {
#   'default':[],
#   'base' : ['ssh'],
#   'virtual': ['vmware'],
#   'ithfme01':['app']
# }


def traverse_node_tree(tree, name):
    '''Given a tree of nodes and a named node return list of children of the named node'''
    if tree['name'] == name:
        return tree['children']
    else:
        for child in tree['children']:
            return traverse_node_tree(child, name)

def parse_file():
    '''this needs to open file and parse it'''
    site = '/etc/puppet/manifests/site.pp'
    with open(site, 'r') as fsite:
        fdata = fsite.read()

    if LDEBUG:
        if DEBUG:
            lexer.input(DATA)
        else:
            lexer.input(fdata)

        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input
            print tok


    if DEBUG:
        parser.parse(DATA)
    else:
        parser.parse(fdata)
    

    print t_nodes['default_base']
    print t_nodes['base']
    print t_nodes['default']
    # for parent, nodes in dict(t_nodes):


@APP.route("/")
def index():
    ''' the index page!'''
    return render_template('index.html')

@APP.route('/nodes')
def json_nodes():
    '''get a JSON of the node data structure'''
    return json.dumps(nodes)

# @app.route('/classes')
# def json_classes():
#     return json.dumps(classes)

if __name__ == "__main__":
    parse_file()
    APP.run(host='0.0.0.0')
