import argparse, psycopg2

import pandas as pd
import jinja2, os, sys

pd.set_option("display.precision", 2)

def fix_html(html):
    return html.replace('border="1"', 'border="0"')

def get_parser(app):
    parser = argparse.ArgumentParser(prog=app)
    parser.add_argument('--host', dest='host', default='localhost', help='Postgres host')
    parser.add_argument('--port', dest='port', default='5432',      help='Postgres port')
    parser.add_argument('--user', dest='user', default='postgres',  help='Postgres user')
    parser.add_argument('--pass', dest='pass', default='',          help='Postgres password')

    return parser

def get_connection(args):
    return psycopg2.connect("dbname='postgres' user='{args.user}' host='{args.host}' port='{args.port}' password='{args.pass}'".format(**vars()))

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

def generate_report(tmpl_vars):
    name = os.path.splitext(sys.argv[0])[0]
    tmpl = env.get_template(name + '.tmpl')

    html_out = tmpl.render(tmpl_vars)

    with open(name + '.html', 'w') as f:
        f.write(html_out.encode('utf8'))
