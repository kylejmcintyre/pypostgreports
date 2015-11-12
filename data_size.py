#!/usr/bin/env python

import report, sys, psycopg2.extras

import pandas as pd

parser = report.get_parser(sys.argv[0])
parser.add_argument('--title', '-t', required=False, dest='title', default="Database Size Report", help='Report Title')

args = parser.parse_args()
conn = report.get_connection(args)
curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

q = "select pg_size_pretty(pg_database_size('postgres')) as size"

curs.execute(q)
total_size = curs.fetchall()[0]['size']

q = """
select schemaname || '.' || relname as table, n_live_tup as rows
from pg_stat_user_tables 
where schemaname not in ('pg_catalog', 'information_schema')
"""

row_count_table = pd.read_sql(q, conn, index_col="table")

q = """
select nspname || '.' || relname as "table", pg_size_pretty(pg_relation_size(c.oid)) as "table_size"
from pg_class c
left join pg_namespace n on (n.oid = c.relnamespace)
where nspname not in ('pg_catalog', 'information_schema')
"""

table_only_table = pd.read_sql(q, conn, index_col="table")

q = """
select nspname || '.' || relname as "table",
pg_total_relation_size(c.oid) as "raw",
pg_size_pretty(pg_total_relation_size(c.oid)) as "table_plus_indexes_size"
from pg_class c
left join pg_namespace n on (n.oid = c.relnamespace)
where nspname not in ('pg_catalog', 'information_schema')
  and c.relkind <> 'i'
  and nspname !~ '^pg_toast'
  and relname not like('%_id_seq')
"""

rel_size_table = pd.read_sql(q, conn, index_col="table")

rel_size_table = rel_size_table.join(row_count_table).join(table_only_table)
rel_size_table['bytes / row'] = (rel_size_table['raw'] / rel_size_table['rows'])
rel_size_table = rel_size_table.sort(["raw"], ascending=[0])
rel_size_table.drop("raw", 1, inplace=True)

rel_size_table = rel_size_table[['table_size', 'table_plus_indexes_size', 'rows', 'bytes / row']]

q = """
select nspname || '.' || relname as "relation", pg_size_pretty(pg_relation_size(c.oid)) as "size"
from pg_class c
left join pg_namespace n on (n.oid = c.relnamespace)
where nspname not in ('pg_catalog', 'information_schema') and reltype = 0 and nspname not like('%pg_toast%')
order by pg_relation_size(c.oid) desc
"""

index_size_table = pd.read_sql(q, conn)

tmpl_vars = {
   'total_size':       total_size,
   'rel_size_table':   report.fix_html(rel_size_table.to_html(float_format=lambda x: '%10.2f' % x)),
   'index_size_table': report.fix_html(index_size_table.to_html()),
   'title':            args.title
}

report.generate_report(tmpl_vars, args)
