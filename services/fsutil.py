import os

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
                    if time.time() - time.mktime(r[0][1].timetuple()) > timeout:
                        release_lock(lock_name)
                        return
                else:
                    raise TimeoutError(f"Could not acquire lock {lock_name} within {timeout} seconds.")
        time.sleep(1)


def release_lock(lock_name):
    conn = get_db_connection()
    conn.execute("DELETE FROM distributed_locks WHERE lock_name = :lock", {"lock": lock_name})
    conn.commit()


def walk(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f'Found directory: {dirpath}')
        for dirname in dirnames:
            print(f'  Subdirectory: {os.path.join(dirpath, dirname)}')
        for filename in filenames:
            print(f'  File: {os.path.join(dirpath, filename)}')


def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')


def find_files(directory, extension):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))
    return found_files


import os


def remove_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):  # 检查目录是否为空
                os.rmdir(dir_path)
                print(f'Removed empty directory: {dir_path}')


import os


def walk_and_exclude(directory, exclude_dirs):
    for root, dirs, files in os.walk(directory, topdown=True):
        # 修改dirs以排除不需要的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        # 继续处理剩余的目录和文件
        for file in files:
            print(f'File: {os.path.join(root, file)}')


from models import Result

if __name__ == '__main__':
    # walk("./../")
    # print_tree("./../")
    pys = find_files("./../", "services")

    for py in pys:
        print(py)

    list1 = [Result(url="www.baidu.com", id=1, result_all=None, result_no_stop_words=None),
             Result(url="www.google.com", id=2, result_all=None, result_no_stop_words=None),
             Result(url="www.sohu.com", id=3, result_all=None, result_no_stop_words=None)]
    list2 = [Result(url="www.baidu.com", id=2, result_all=None, result_no_stop_words=None),
             Result(url="www.taobao.com", id=1, result_all=None, result_no_stop_words=None),
             Result(url="www.sohu.com", id=4, result_all=None, result_no_stop_words=None)]

    # 使用 & 操作符
    intersection_set = set(list1) & set(list2)
    print("交集:", intersection_set)

    # 或者使用 intersection() 方法
    intersection_set = set(list1).intersection(set(list2))
    print("交集:", intersection_set)

    # 使用 | 操作符
    union_set = set(list1) | set(list2)
    print("并集:", union_set)

    # 或者使用 union() 方法
    union_set = set(list1).union(set(list2))
    print("并集:", union_set)

    # 使用 - 操作符
    difference_set_1 = set(list1) - set(list2)
    print("list1 中存在但 list2 中不存在的元素:", difference_set_1)

    # 或者使用 difference() 方法
    difference_set_1 = set(list1).difference(set(list2))
    print("list1 中存在但 list2 中不存在的元素:", difference_set_1)

    # 使用 - 操作符
    difference_set_2 = set(list2) - set(list1)
    print("list2 中存在但 list1 中不存在的元素:", difference_set_2)

    # 或者使用 difference() 方法
    difference_set_2 = set(list2).difference(set(list1))
    print("list2 中存在但 list1 中不存在的元素:", difference_set_2)
