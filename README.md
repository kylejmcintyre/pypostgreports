# pypostgreports
A collection of generic "reports" that can be run on a Postgres 
database including a data dictionary generator as well as a 
database size report.

Note that the data dictionary is intended for Postgres instances
that are thoroughly documented using Postgres comments. 

## Dependencies
Tested on Postgres 9.4 and Python 2.7.x and requires the following Python modules:

  * psycopg2
  * jinja2
  * pandas

These are easily available in Anaconda Python.

## Usage

    usage: ./data_dictionary.py [-h] [--host HOST] [--port PORT] [--user USER]
                                [--pass PASS] [--db DBNAME] [--output OUTPUT]
                                [--title TITLE]
    
    optional arguments:
      -h, --help                 show this help message and exit
      --host HOST                Postgres host
      --port PORT                Postgres port
      --user USER,     -u USER   Postgres user
      --pass PASS,     -p PASS   Postgres password
      --db DBNAME,     -d DBNAME Postgres database
      --output OUTPUT, -o OUTPUT Output file location
      --title  TITLE,  -t TITLE  Title of the report 

Individual reports may have additional arguments beyond these base arguments
shared by all reports. By default, the output file is [name of the report].html
in the current working directory.
    
