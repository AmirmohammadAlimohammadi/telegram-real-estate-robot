import pymysql
from pymysql.cursors import DictCursor
from config import *


def search_saves(user_id):
    try:
        conn = pymysql.connect(password=password,host=host,user='root',database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM saves WHERE user_id=%s", (user_id))
        saves = cur.fetchall()
        cur.close()
        conn.close()
        return saves
    except Exception as e:
        cur.close()
        conn.close()
        return(f"failed to find save with error {e}")
def search_user(telegram_id):
    try:
        conn = pymysql.connect(password=password,host=host,user='root',database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        cur.close()
        conn.close()
        return(f"failed to find user with error {e}")
def get_all_files(file_type,property,active,db_name = db_name):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM files WHERE file_type=%s AND property_type=%s AND is_active=%s",(file_type,property,active))
        files = cur.fetchall()
        cur.close()
        conn.close()
        return files
    except Exception as e:
        cur.close()
        conn.close()
        return(f"failed to find user with error {e}") 
def find_id(id,db_name = db_name):
    try:
        conn = pymysql.connect(password=password,host=host,user='root',database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id=%s",(id))
    user = cur.fetchone()
    return user['user_id']
def find_save(id, file_id):
    try:
        conn = pymysql.connect(password=password,host=host,user='root',database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    cur.execute("SELECT * FROM saves WHERE user_id=%s AND file_id=%s",(id,file_id))
    saves = cur.fetchall()
    return len(saves)==0
def find_files(user_id):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE user_id=%s",(user_id))
    files = cur.fetchall()
    return files
def find_file(file_id):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE file_id=%s",(file_id))
    file = cur.fetchone()
    return file
def change_status(status , file_id):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        cur.execute("UPDATE files SET is_active=%s WHERE file_id=%s", (status, file_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return "status changed successfully"
    except Exception as e:
        return f"failed to change file status with error : {e}"
def delete_save(user_id , file_id):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name ,cursorclass=DictCursor)
    except Exception as e:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM saves WHERE user_id=%s AND file_id=%s", (user_id, file_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return "save removed"
    except Exception as e:
        return f"failed to remove save with error : {e}"
