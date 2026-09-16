import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv
load_dotenv()

def get_mysql_conn():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER'),
        passwd=os.getenv('MYSQL_PASSWORD'),
        charset=os.getenv('MYSQL_CHARSET'),
        database=os.getenv('MYSQL_DATABASE'),
        cursorclass=pymysql.cursors.DictCursor,
    )
