import pymysql
import datetime
from pymysql import err
from config import *
errors = {'missing column':1054}
db_name=db_name
def insert_to_files(*,db_name=db_name,**kwargs):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name)
    except:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        query = """INSERT INTO files(user_id,title,loc_long , loc_lat,warehouse,elevator,parking,floor,year,description,area,rooms,price,deposit,property_type,rent,file_type,is_active,created_date)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = (
            kwargs.get('user_id'), kwargs.get('title'), kwargs.get('location_long'),
            kwargs.get('location_lat'),kwargs.get('storage'),kwargs.get('elevator'),kwargs.get('parking'),kwargs.get('floor') ,kwargs.get('year') ,kwargs.get('description'), kwargs.get('area'),
            kwargs.get('rooms'), kwargs.get('price'), kwargs.get('deposit'),
            kwargs.get('property_type'), kwargs.get('rent'), kwargs.get('file_type'),
            kwargs.get('is_active'), datetime.datetime.now().date()
            )
        cur.execute(query,params)
        id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return id
    except Exception as e:
        return f"failed to insert file with error : {e}"


def insert_to_users(*,db_name=db_name,**kwargs):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name)
    except:
        #pass
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        query = """INSERT INTO users (name,national_id,phone,telegram_id,email,registery_date) VALUES(%s,%s,%s,%s,%s,%s)"""
        params = (kwargs.get('name'),kwargs.get('national_id'),kwargs.get('phone'),kwargs.get('telegram_id'),kwargs.get('email'),datetime.datetime.now().date())
        cur.execute(query,params)
        id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        return f"user with id {id} inserted succesfuly."
    except (err.OperationalError , err.IntegrityError) as e:
        return f"failed to insert user with error : {e}"


def insert_to_saves(*,db_name=db_name,**kwargs):
    try:
        conn = pymysql.connect(password=password,host=host,user=user,database=db_name)
    except:
        return(f"failed connecting mysql with error {e}")
    cur = conn.cursor()
    try:
        query = """INSERT INTO saves (user_id,file_id,saved_at) VALUES(%s,%s,%s)"""
        params = (kwargs.get('user_id'),kwargs.get('file_id'),datetime.datetime.now().date())
        cur.execute(query,params)
        conn.commit()
        cur.close()
        conn.close()
        return f"save with id {cur.lastrowid} inserted succesfuly."
    except err.OperationalError as e:
        return f"failed to insert save with error : {e}"


#print(insert_to_files(user_id=3,rooms=2,area=110,price=4000000000,file_type='rent',neighborhood='chitgar',city='tehran',is_active=1,image_1=1,image_2=1,image_3=1))
#print(insert_to_likes(file_id=1,user_id=3))