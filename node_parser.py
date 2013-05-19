from lexer import lexer
from yacc import parser, classes, nodes
from flask import Flask, render_template
import json
app = Flask(__name__)

data = '''
node default {}

node base inherits default {
    include ssh
    include ntp
}

node virtual inherits base {
    include vmware
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

# lexer.input(data)

# while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok

def parse_file():
    '''this needs to open file and parse it'''
    parser.parse(data)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/nodes')
def json_nodes():
    return json.dumps(nodes)

# @app.route('/classes')
# def json_classes():
#     return json.dumps(classes)

if __name__ == "__main__":
    parse_file()
    app.run()