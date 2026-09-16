import os
from dotenv import load_dotenv
import redis

load_dotenv()
def get_redis_conn():
    password = os.getenv('REDIS_PASSWORD')
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_DB')),
        password=password if password else None,
        protocol=2,
    )

def close_redis_conn(conn):
    conn.close()