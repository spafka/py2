import datetime
import os
import shutil
from contextlib import contextmanager
import time
import psycopg2
from typing import Callable, TypeVar


def get_db_connection():
    from app import db
    return db.session


T = TypeVar('T')
V = TypeVar('V')


def acquire_lock(func, lock_name: str, timeout: int = 10):
    conn = get_db_connection()
    start_time = time.time()
    while True:
        try:
            conn.execute("INSERT INTO distributed_locks (lock_name,cts) VALUES (:lock,:time)",
                         {"lock": lock_name, "time": datetime.datetime.now()})
            conn.commit()
            try:
                print("get lock!!!", "execute func")
                func()
            except Exception as e:
                print(e)
            finally:
                release_lock(lock_name)
            return True
        except Exception as e:  # 锁已被其他会话持有
            conn.rollback()
            if time.time() - start_time > timeout:
                r = conn.execute("SELECT * FROM distributed_locks WHERE lock_name = :lock",
                                 {"lock": lock_name}).fetchall()
                if (len(r) > 0):
                    if time.time()-time.mktime(r[0][1].timetuple()) > timeout:
                        release_lock(lock_name)
                        return
                else:
                    raise TimeoutError(f"Could not acquire lock {lock_name} within {timeout} seconds.")
        time.sleep(1)


def release_lock(lock_name):
    conn = get_db_connection()
    conn.execute("DELETE FROM distributed_locks WHERE lock_name = :lock", {"lock": lock_name})
    conn.commit()

