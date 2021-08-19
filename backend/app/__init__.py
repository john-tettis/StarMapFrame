import os
from flask import Blueprint
import sqlite3
from sqlite3.dbapi2 import Error


blueprint = Blueprint('respina', __name__)

HOST = "https://sky.respina.store/api"
FRONTEND = "https://sky.respina.store"
PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(PATH, 'db.sqlite3')


ORDERS_TBL = """CREATE TABLE IF NOT EXISTS orders (
id integer PRIMARY KEY,
name text NOT NULL,
mobile text NOT NULL,
address text NOT NULL,
province text NOT NULL,
city text NOT NULL,
post text NOT NULL,
is_paid integer NOT NULL,
is_deliverd integer NOT NULL,
is_printed integer NOT NULL,
product text NOT NULL,
amount text NOT NULL,
tracking text NOT NULL UNIQUE,
timestamp text NOT NULL
);
"""

USERS_TBL = """CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY,
name text NOT NULL,
username text NOT NULL UNIQUE,
password text NOT NULL
);
"""

TOKEN_TBL = """
CREATE TABLE IF NOT EXISTS tokens (
    id integer PRIMARY KEY,
    userID integer NOT NULL,
    token text NOT NULL
)
"""

DISCOUNT_TBL ="""
CREATE TABLE IF NOT EXISTS discounts (
    id integer PRIMARY KEY,
    code text NOT NULL,
    amount integer NOT NULL
)
"""


def get_db():
    db = getattr(blueprint, '_database', None)
    if db is None:
        db = blueprint._database = sqlite3.connect(DATABASE)
        try:
            c = db.cursor()
            c.execute(ORDERS_TBL)
            c.execute(USERS_TBL)
            c.execute(TOKEN_TBL)
            c.execute(DISCOUNT_TBL)
        except Error as e:
            print(e)
    return db

def to_json(rows: list, fields: list)-> list:
    column_list = []
    for i in fields:
        column_list.append(i[0])
    jsonData_list = []
    for row in rows:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        jsonData_list.append(data_dict)

    return jsonData_list


from . import orders
from . import starmap
from . import auth
from . import assets
from . import discount
from . import redirects