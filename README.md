# pypostreports
A collection of generic "reports" that can be run on a Postgres 
database including a data dictionary generator as well as a 
database size report.

## Dependencies
Tested on Postgres 9.4 and Python 2.7.x and requires the following Python modules:

  * psycopg2
  * jinja2
  * pandas

These are easily available in Anaconda Python.

## Usage

Simply invoke data_dictionary.py or data_size.py. They produce
data_dictionary.html and data_size.html respectively. The HTML
files are meant to piped through a PDF converter like wkhtml2pdf.


