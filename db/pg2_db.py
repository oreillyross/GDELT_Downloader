import os

import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])



