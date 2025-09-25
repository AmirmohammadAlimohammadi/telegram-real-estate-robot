import telebot
import requests
import math
import os
import jdatetime
from DML import *
from DQL import *
from config import *
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup , InputMediaPhoto
channel_id = -1002832403172
import time
token = token
bot = telebot.TeleBot(token= token)
new_files = dict()
new_accounts = dict()
searchs = dict()
account_searchs = dict()
user_steps = dict()
active_inline_messages = {}
active_inline_messages = {}
def send_final_file(file: dict) -> str:
    file_type = file.get("type") or file.get("file_type")
    prop_type = file.get("property") or file.get("property_type")

    if file_type == "sale":
        price_info = f"💰 *{translate['price']}*: {file.get('price', '-')}"
    else:
        price_info = (
            f"💰 *{translate['deposit']}*: {file.get('deposit', '-')}\n"
            f"💵 *{translate['rent']}*: {file.get('rent', '-')}"
        )

    text = (
        f"🏠 *{translate['file kind']}*: {translate.get(file_type, file_type)}\n"
        f"📌 *{translate['prop kind']}*: {translate.get(prop_type, prop_type)}\n"
        f"🛏 *{translate['rooms']}*: {file.get('rooms', '-')}\n"
        f"📶 *{translate['floor']}*: {file.get('floor', '-')}\n"
        f"🛗 *{translate['elevator']}*: {translate.get(file.get('elevator'), '-')}\n"
        f"🚗 *{translate['parking']}*: {translate.get(file.get('parking'), '-')}\n"
        f"📦 *{translate['storage']}*: {translate.get(file.get('storage'), '-')}\n"
        f"📐 *{translate['area']}*: {file.get('area', '-')}\n"
        f"🏗 *{translate['year']}*: {translate.get(file.get('year'), '-')}\n\n"
        f"📝 *{translate['title']}*: {file.get('title', '-')}\n"
        f"💬 *{translate['explain']}*: {file.get('explain', '-')}\n\n"
        f"{price_info}"
    )
    return text

active_markups = dict()
def register_markups(chat_id , message_id , user_id,markup):
    if active_markups.get(user_id)==None:
        active_markups[user_id] = list()
    message = {'cid':chat_id , 'mid':message_id , 'user_id':user_id , 'markup' :markup}
    active_markups[user_id].append(message)
    return
def deactive_markups(user_id):
    try:
        messages = active_markups[user_id]
    except KeyError as e:
        return
    for message in messages:
        mid = message['mid']
        cid = message['cid']
        try:
            bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=None)
            
        except Exception as e:
            continue
from datetime import datetime

def format_file_result(file: dict) -> str:
    # Translate types
    file_type = file.get("file_type")
    prop_type = file.get("property_type")

    if file_type == "sale":
        price_info = f"💰 *{translate['price']}*: {file.get('price', '-')}"
    else:
        price_info = (
            f"💰 *{translate['deposit']}*: {file.get('deposit', '-')}\n"
            f"💵 *{translate['rent']}*: {file.get('rent', '-')}"
        )

    # Created date formatted nicely
    created = file.get("created_date")
    if isinstance(created, datetime):
        created = created.strftime("%Y-%m-%d")
    else:
        created = str(created or "-")

    # Distance (km, 2 decimals)
    distance = file.get("distance")
    if distance is not None:
        distance = f"{distance:.2f} کیلومتر"
    else:
        distance = "-"

    text = (
        f"📌 *{translate['file kind']}*: {translate.get(file_type, file_type)}\n"
        f"🏠 *{translate['prop kind']}*: {translate.get(prop_type, prop_type)}\n"
        f"🛏 *{translate['rooms']}*: {file.get('rooms', '-')}\n"
        f"📶 *{translate['floor']}*: {file.get('floor', '-')}\n"
        f"🛗 *{translate['elevator']}*: {translate.get(file.get('elevator'), '-')}\n"
        f"🚗 *{translate['parking']}*: {translate.get(file.get('parking'), '-')}\n"
        f"📦 *{translate['storage']}*: {translate.get(file.get('warehouse'), '-')}\n"
        f"📐 *{translate['area']}*: {file.get('area', '-')}\n"
        f"🏗 *{translate['year']}*: {translate.get(file.get('year'), '-')}\n"
        f"🗓 *تاریخ ثبت*: {created}\n"
        f"📝 *{translate['title']}*: {file.get('title', '-')}\n\n"
        f"💬 *{translate['explain']}*: {file.get('description', '-')}\n\n"
        f"{price_info}"
    )

    return text
  
file_keys = ['type' , 'property' , 'floor' , 'rooms' , 'elevator' , 'parking' , 'storage' , 'explain' , 'title']
translate = {'house':'مسکونی','office':'تجاری یا اداری','Yes':'دارد' , 'No':'ندارد' , 'sale': 'فروش' ,'price':'قیمت',
            'rent': 'اجاره' , 'انتخاب':'انتخاب' ,'file kind':'نوع فایل' , 'prop kind':'نوع ملک' ,
            'region':'منطقه' , 'rooms':'تعداد اتاق' , 'floor':'طبقه' , 'elevator':'آسانسور' , 
            'storage':'انباری','parking':'پارکینگ' , 'area': 'متراژ' , 'year':'سال ساخت' , 'title':'عنوان' ,'explain':'توضیحات',
            'north':'شمال تهران' , 'west':'غرب تهران' , 'east':'شرق تهران' , 'north east':'شمال شرق تهران' ,
            'south east':'جنوب شرق تهران' ,'north west':'شمال غرب' , 'south west': 'جنوب غرب تهران' , 'mid_age':'2-10 سال ساخت',
            'new':'نوساز', 'old':'قدیمی' , 'very old':'کلنگی' , 'deposit':'ودیعه'  , 'rent':'اجاره'}

def answer_callback_query(**kwargs):
    try :
       kwargs['bot'].answer_callback_query(callback_query_id=kwargs.get('callback_query_id')  ,text =kwargs.get('text') , show_alert =  kwargs.get('show_alert')  )
    except Exception as e:
        return    
def edit_message_text(**kwargs):
    try:
        kwargs['bot'].edit_message_text(chat_id = kwargs['chat_id'] , message_id = kwargs['message_id'] , text = kwargs['text'] , reply_markup =kwargs.get('reply_markup') )
    except Exception as e:
        return





def make_markup_search(search):
    markup = InlineKeyboardMarkup()
    sale = 'فروش'
    rent = 'اجاره'
    if search.get('type')!=None:
        file_type = search.get('type')
        if file_type == 'rent':
            rent = "اجاره✅"
        if file_type == 'sale':
            sale = "فروش✅"
    markup.add(InlineKeyboardButton(text = rent , callback_data='search rent') , InlineKeyboardButton(text = sale , callback_data='search sale'))
    house = 'مسکونی'
    office = 'تجاری یا اداری'
    if search.get('type')!=None:
        prop_type = search.get('property')
        if prop_type == 'house':
            house = "مسکونی✅"
        if prop_type == 'office':
            office = "تجاری یا اداری✅"
    markup.add(InlineKeyboardButton(text = house , callback_data='search house') , InlineKeyboardButton(text = office , callback_data='search office'))
    
    # if search.get('area') !=None:
    #     meter = f" متر {search['area']}"
    # markup.add(InlineKeyboardButton(text = meter  , callback_data="searcharea"))
    markup.add(InlineKeyboardButton(text = "تایید" , callback_data="search confirm"))
    return markup

def create_file_markup(file):
    markup = InlineKeyboardMarkup()
    
    sale = 'فروش'
    rent = 'اجاره'
    if file.get('type')!=None:
        file_type = file.get('type')
        if file_type == 'rent':
            rent = "اجاره✅"
        if file_type == 'sale':
            sale = "فروش✅"
    markup.add(InlineKeyboardButton(text = rent , callback_data='rent') , InlineKeyboardButton(text = sale , callback_data='sale'))
    house = 'مسکونی'
    office = 'تجاری یا اداری'
    if file.get('type')!=None:
        prop_type = file.get('property')
        if prop_type == 'house':
            house = "مسکونی✅"
        if prop_type == 'office':
            office = "تجاری یا اداری✅"
    markup.add(InlineKeyboardButton(text = house , callback_data='house') , InlineKeyboardButton(text = office , callback_data='office'))
    rooms = 'انتخاب'
    if file.get('rooms')!=None:
        rooms = file.get('rooms')
        if rooms == '5':
            rooms = '5 یا بیشتر'
    markup.add(InlineKeyboardButton(text = f"{translate['rooms']} : {rooms}", callback_data='get rooms'))

    floor = 'انتخاب'
    if file.get('floor')!=None:
        floor = file.get('floor')
        if floor == '31':
            floor = '31 یا بیشتر'
    markup.add(InlineKeyboardButton(text = f"{translate['floor']} : {floor}", callback_data='get floor'))

    elevator = 'انتخاب'
    if file.get('elevator')!=None:
        elevator = file.get('elevator')
    markup.add(InlineKeyboardButton(text =  f"{translate['elevator']} : {translate[elevator]}" , callback_data='elevator'))
    parking = 'انتخاب'
    if file.get('parking')!=None:
        parking = file.get('parking')
    markup.add(InlineKeyboardButton(text =  f"{translate['parking']} : {translate[parking]}" , callback_data='parking'))

    storage = 'انتخاب'
    if file.get('storage')!=None:
        storage = file.get('storage')
    markup.add(InlineKeyboardButton(text =  f"{translate['storage']} : {translate[storage]}", callback_data='storage'))
    
    area = 'انتخاب'
    if file.get('area')!=None:
        area = file.get('area')
    markup.add(InlineKeyboardButton(text= f"{translate['area']} : {area}" , callback_data='get area'))
    
    year = 'انتخاب'
    if file.get('year')!=None:
        year = file.get('year')
    markup.add(InlineKeyboardButton(text= f"{translate['year']} : {translate[year]}" , callback_data='get year') )
    
    
    title = 'انتخاب'
    if file.get('title')!=None:
        title = file.get('title')
    markup.add(InlineKeyboardButton(text = f"{translate['title']} : {title}", callback_data='title'))
    markup.add(InlineKeyboardButton(text = 'توضیحات' , callback_data='explain'))
    markup.add(InlineKeyboardButton(text = 'اضافه کردن عکس' , callback_data='add image'))
    markup.add(InlineKeyboardButton(text = 'ویرایش عکس ها عکس' , callback_data='edit image 0'))
    markup.add(InlineKeyboardButton(text = 'مرحله بعد'  , callback_data='next step'))
    return markup
def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance
def find_similar_files(search):
    
    files = get_all_files(search['type'] , search['property'],'Y')
    close_files = []
    
    #print(files)
    for file in files:
        
        distance = haversine(search['long'],search['lat'],file['loc_long'],file['loc_lat'])
        
        if distance < 20 :
            file['distance'] = distance
            close_files.append(file)
    return(sorted(close_files , key= lambda file : (file['distance'])))
   
    
  
       
        
    
@bot.callback_query_handler(func = lambda call : call.data == ' ')
def ignore(call):
    return
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user_steps[user_id] = 'start'
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📃 ایجاد فایل جدید','🔍 جست‌وجوی فایل')
    markup.add('📂 فایل‌های من' , '💾 فایل‌های ذخیره‌شده')
    markup.add('👤 اطلاعات کاربری','📝 ثبت‌نام')
    markup.add('🏠 خانه')

    welcome_text = (
        "👋 **خوش آمدید!**\n\n"
        "این ربات به شما کمک می‌کند تا:\n"
        "📃 فایل‌های ملکی خود را برای *فروش* یا *اجاره* ثبت کنید\n"
        "🔍 فایل‌های موجود را در منطقه‌ی دلخواه جست‌وجو کنید\n"
        "📂 فایل‌های شخصی خود را مدیریت کنید\n"
        "برای شروع، یکی از گزینه‌های منو را انتخاب کنید 👇"
    )

    bot.send_message(
        chat_id=cid,
        text=welcome_text,
        reply_markup=markup,
        parse_mode="Markdown"
    )
@bot.message_handler(func=lambda message: message.text == '💾 فایل‌های ذخیره‌شده')
def send_saved_files(message):
    cid = message.chat.id
    user_id = message.from_user.id
    user = search_user(user_id)
    id = user['user_id']
    saves = search_saves(id)
    try:
        save = saves[0]
    except Exception as e:
        bot.send_message(text = "شما هیچ فایل ذخیره شده ای ندارید" , chat_id=cid)
        user_steps[user_id] = 'home'
    file_id = save['file_id']
    if len(saves)==0:
        bot.send_message(text = "شما هیچ فایل ذخیره شده ای ندارید" , chat_id=cid)
        return
    file = find_file(file_id)
    text = format_file_result(file)
    image_path = os.path.join("images" , f"file {file_id}" , "image 1")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="عکس قبلی" , callback_data=f"save image {file_id} 0"), InlineKeyboardButton(text="عکس بعدی" , callback_data=f"save image {file_id} 2"))
    markup.add(InlineKeyboardButton(text="حذف از فایل های ذخیره شده",callback_data=f"remove save {file_id} {id}"))
    markup.add(InlineKeyboardButton(text = "فایل ذخیره شده قبلی" , callback_data="send save 0"),InlineKeyboardButton(text = "فایل ذخیره شده بعدی" , callback_data="send save 1"))

    if os.path.exists(image_path):
        with open(image_path , 'rb') as f:
            image = f.read()
            
            bot.send_photo(chat_id=cid , photo=image , caption=text , parse_mode='markdown' , reply_markup=markup)
    else:
        
        bot.send_message(chat_id=cid ,text=text , parse_mode='markdown' , reply_markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith("remove save"))
def remove_save(call):
    id = int(call.data.split()[-1])
    file_id = int(call.data.split()[-2])
    ans = delete_save(id,file_id)
    print(ans)
    mid = call.message.id
    cid = call.message.chat.id
    
    if ans == 'save removed':
       bot.answer_callback_query(callback_query_id=call.id , text="فایل از فایل های ذخیره شده حذف شد") 
       
    else:
        bot.answer_callback_query(callback_query_id=call.id , text="خطا در حذف فایل ذخیره شده")

@bot.callback_query_handler(func = lambda call : call.data.startswith("send save"))
def send_save(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    user = search_user(user_id)
    mid = call.message.id
    id = user['user_id']
    index = int(call.data.split()[-1])
    saves = search_saves(id)
    if index>= len(saves):
        bot.answer_callback_query(text = "این آخرین فایل ذخیره شده شماست" ,callback_query_id=call.id)
        return
    if index <0:
       bot.answer_callback_query(text = "این اولین فایل ذخیره شده شماست" ,callback_query_id=call.id)
       return 
    bot.delete_message(chat_id=cid , message_id=mid)
    save = saves[index]
    file_id = save['file_id']
    id = save['user_id']
    file = find_file(file_id)
    text = format_file_result(file)
    image_path = os.path.join("images" , f"file {file_id}" , "image 1")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="عکس قبلی" , callback_data=f"save image {file_id} 0"), InlineKeyboardButton(text="عکس بعدی" , callback_data=f"save image {file_id} 2"))
    markup.add(InlineKeyboardButton(text="حذف از فایل های ذخیره شده",callback_data=f"remove save {file_id} {id}"))
    markup.add(InlineKeyboardButton(text = "فایل ذخیره شده قبلی" , callback_data=f"send save {index-1}"),InlineKeyboardButton(text = "فایل ذخیره شده بعدی" , callback_data=f"send save {index+1}"))
    if os.path.exists(image_path):
        with open(image_path , 'rb') as f:
            image = f.read()
            
            bot.send_photo(chat_id=cid , photo=image , caption=text , parse_mode='markdown' , reply_markup=markup)
    else:
        print(image_path)
        bot.send_message(chat_id=cid ,text=text , parse_mode='markdown' , reply_markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('save image'))
def edit_image(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = call.message.id
    image_index = int(call.data.split()[-1])
    file_index = int(call.data.split()[-2])
    file = find_file(file_index)
    image_path = os.path.join("images" , f"file {file_index}" ,f"image {image_index}")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="عکس قبلی" , callback_data=f"save image {file_index} {image_index -1}"), InlineKeyboardButton(text="عکس بعدی" , callback_data=f"save image {file_index} {image_index +1}"))
    markup.add(InlineKeyboardButton(text = "فایل ذخیره شده بعدی" , callback_data=f"send save {file_index}"))
    if os.path.exists(image_path):
        with open(image_path , 'rb') as f:
            image = f.read()
            bot.edit_message_media(media=image , caption = format_file_result(file) , reply_markup=markup)
    elif file_index<=0:
        bot.answer_callback_query(text = "این اولین عکس فایل می باشد" , callback_query_id=call.id)
        return
    else:
        bot.answer_callback_query(text = "این آخرین عکس فایل می باشد" , callback_query_id=call.id)
        return
@bot.message_handler(func=lambda message: message.text == '👤 اطلاعات کاربری')
def show_user_info(message):
    cid = message.chat.id
    user_id = message.from_user.id
    deactive_markups(user_id)
    user = search_user(str(user_id)) 
    if not user:
        bot.send_message(
            chat_id=cid,
            text="⚠️ شما هنوز ثبت‌نام نکرده‌اید.\n\nلطفاً ابتدا از گزینه «ثبت نام» استفاده کنید.",
            parse_mode="Markdown"
        )
        return

   
    jalali_date = "-"
    if user['registery_date']:
        g_date = user['registery_date']
        jalali_date = jdatetime.date.fromgregorian(
            day=g_date.day,
            month=g_date.month,
            year=g_date.year
        ).strftime("%Y/%m/%d")
    text = (
        "👤 *اطلاعات کاربری شما*\n\n"
        f"🆔 *کد کاربر*: `{user['user_id']}`\n"
        f"📱 *آیدی تلگرام*: `{user['telegram_id']}`\n"
        f"🧑‍💼 *نام*: {user['name']}\n"
        f"🪪 *کد ملی*: `{user['national_id']}`\n"
        f"📞 *شماره موبایل*: `{user['phone']}`\n"
        f"📧 *ایمیل*: {user['email'] or '-'}\n"
        f"📅 *تاریخ ثبت‌نام*: {jalali_date}\n\n"
        "✨ از منوی پایین می‌توانید به سایر بخش‌های ربات دسترسی پیدا کنید."
    )

    bot.send_message(chat_id=cid, text=text, parse_mode="Markdown")
@bot.message_handler(func=lambda message: message.text == '🏠 خانه')
def go_home(message):
    cid = message.chat.id
    user_id = message.from_user.id

    user_steps[user_id] = 'home'

    bot.send_message(
        chat_id=cid,
        text=(
            "🏠 شما اکنون در *خانه* هستید.\n\n"
            "از منوی پایین می‌توانید یکی از خدمات ربات را انتخاب کنید ✨"
        ),
        parse_mode="Markdown"
    )
    user_id = message.from_user.id
    deactive_markups(user_id)
@bot.message_handler(func= lambda message : message.text == '📂 فایل‌های من')
def my_files(message):
    cid = message.chat.id
    user_id = message.from_user.id
    id = find_id(user_id)
    deactive_markups(user_id)
    files = find_files(id)
    file = files[0]
    text = send_final_file(file)
    image_path = os.path.join("images", f"file_{file['file_id']}_images", "image_1.jpg")
    markup = InlineKeyboardMarkup()
    active =  " فعال/غیرفعال کردن فایل"
    callback = f"change status {file['file_id']}"
    if file['is_active'] !='Y':
            active =  " فعال/غیرفعال کردن فایل"
            callback = f"change status {file['file_id']}"
    markup.add(InlineKeyboardButton(text = "عکس قبلی" , callback_data=f"open -m image {file['file_id']} 0"),InlineKeyboardButton(text = "عکس بعدی" , callback_data=f"open -m image {file['file_id']} 2"))
    markup.add(InlineKeyboardButton(text =active , callback_data=callback))
    markup.add(InlineKeyboardButton(text="فایل بعدی" , callback_data="my files 1"))
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image = f.read()
            message = bot.send_photo(chat_id=cid , caption =text , photo=(image) , parse_mode='markdown' , reply_markup=markup)
    else:
        message = bot.send_message(chat_id=cid , text =text , parse_mode='markdown' , reply_markup=markup)
    register_markups(message_id=message.id , chat_id=cid , user_id=user_id , markup=markup)
    return
@bot.callback_query_handler(func = lambda call : call.data.startswith("my files"))
def my_files(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    id = find_id(user_id)
    files = find_files(id)
    index = int(call.data.split()[-1])
    try:
        file = files[index]
    except IndexError as e:
        bot.answer_callback_query(text = "فایل دیگری موجود نیست" ,callback_query_id=call.id )
        return
    text = send_final_file(file)
    image_path = os.path.join("images", f"file_{file['file_id']}_images", "image_1.jpg")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = "عکس قبلی" , callback_data=f"open -m image {file['file_id']} {index}"),InlineKeyboardButton(text = "عکس بعدی" , callback_data=f"open -m image {file['file_id']} {index}"))
    active =  " فعال/غیرفعال کردن فایل"
    callback = f"change status {file['file_id']}"
    if file['is_active'] !='Y':
        active =  " فعال/غیرفعال کردن فایل"
        callback = f"change status {file['file_id']}"
    markup.add(InlineKeyboardButton(text =active , callback_data=callback))
    markup.add(InlineKeyboardButton(text="فایل بعدی" , callback_data=f"my files {index+1}"))
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image = f.read()
            message = bot.send_photo(chat_id=cid , caption =text , photo=(image) , parse_mode='markdown' , reply_markup=markup)
            register_markups(message_id=message.id , chat_id=cid , user_id=user_id , markup=markup)
    else:
        message = bot.send_message(chat_id=cid , text =text , parse_mode='markdown' , reply_markup=markup)
        register_markups(message_id=message.id , chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('open -m image'))
def edit_image(call):
    mid = call.message.id
    cid = call.message.chat.id
    file_id = call.data.split()[-2] 
    index = int(call.data.split()[-1]) 
    file  = find_file(file_id)
    index_file = int(call.data.split()[-2]) 
    if index <=0:
        bot.answer_callback_query(text = "این عکس اولین عکس فایل شماست" , callback_query_id=call.id )
        
        return
    
    markup = InlineKeyboardMarkup()
    active =  " فعال/غیرفعال کردن فایل"
    callback = f"change status {file_id}"
    if file['is_active'] !='Y':
        active =  " فعال/غیرفعال کردن فایل"
        callback = f"change status {file_id}"
    markup.add(InlineKeyboardButton(text = "عکس قبلی" , callback_data=f"open -m image {file_id} {index -1}"),InlineKeyboardButton(text = "عکس بعدی" , callback_data=f"open -m image {file_id} {index+1}"))
    markup.add(InlineKeyboardButton(text =active , callback_data=callback))
    
    markup.add(InlineKeyboardButton(text="فایل بعدی" , callback_data=f"my files {index_file+1}"))
    
    text = send_final_file(file)
    try :
        image_path = os.path.join("images", f"file_{file_id}_images", f"image_{index}.jpg")
        user_id = call.from_user.id
        with open(image_path, "rb") as f:
            image = f.read()
            bot.edit_message_media(message_id=mid , chat_id=cid , media=InputMediaPhoto(image,caption=text , parse_mode='markdown' ), reply_markup=markup)
            
            register_markups(message_id=mid , chat_id=cid , user_id=user_id , markup=markup)
            return 
    except Exception as e:
        bot.answer_callback_query(text = "این آخرین عکس فایل است" , callback_query_id=call.id)
        return   

@bot.callback_query_handler(func = lambda call : call.data.startswith('change status') )
def act(call):
    file_id = int(call.data.split()[-1])
    new_status = 'N'
    file = find_file(file_id)
    if file['is_active'] == 'N':
        new_status = 'Y'
    
    result = change_status(new_status,file_id)
    if result == "status changed successfully":
        text = "غیرفعال"
        if new_status == 'Y':
            text = "فعال"
        bot.answer_callback_query(text = f"فایل {text} شد" , callback_query_id=call.id)
        return
@bot.message_handler(func= lambda message : message.text == '🔍 جست‌وجوی فایل')
def start_search(message):
    cid = message.chat.id
    user_id = message.from_user.id
    deactive_markups(user_id)
    if search_user(f'{user_id}') == None:
        bot.send_message(chat_id=cid , text = "لطفا ابتدا در ربات ثبت نام کنید")
        return
    searchs[user_id] = dict()
    markup = make_markup_search(searchs[user_id])
    message = bot.send_message(chat_id=cid , text='اطلاعات ملک مورد نظر خود را پر کنید' , reply_markup=markup)
    register_markups(message_id=message.id , chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'search rent' or call.data == 'search sale')
def search_type(call):
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    if searchs[user_id].get('type') == call.data.split()[-1]:
        return
    
    searchs[user_id]['type'] = call.data.split()[-1]
    markup = make_markup_search(searchs[user_id])
    bot.edit_message_reply_markup(message_id=mid, chat_id=cid , reply_markup=markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'search office' or call.data == 'search house')
def search_type(call):
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    if searchs[user_id].get('property') == call.data.split()[-1]:
        return
   
    searchs[user_id]['property'] = call.data.split()[-1]
    markup = make_markup_search(searchs[user_id])
    bot.edit_message_reply_markup(message_id=mid, chat_id=cid , reply_markup=markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
# @bot.callback_query_handler(func = lambda call : call.data == 'searcharea')
# def get_search_area(call):
#     user_id = call.from_user.id
#     cid = call.message.chat.id
#     mid = call.message.id
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton(text="زیر 100 متر" , callback_data="search area 0-100") , InlineKeyboardButton(text = "100-200 متر" , callback_data="search area 100-200"))
#     markup.add(InlineKeyboardButton(text="200-300 متر" , callback_data="search area 200-300") , InlineKeyboardButton(text = "300-400 متر" , callback_data="search area 300-400"))
#     markup.add(InlineKeyboardButton(text = "500 متر و بیشتر" , callback_data="search area 500+"))
#     edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('search area'))
def area(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    searchs[user_id]['area'] = call.data.split()[-1]
    markup = make_markup_search(searchs[user_id])
    bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call: call.data == 'search confirm')
def search_confirm(call):
    
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    keys = ['type','property']
    for key in keys:
        if searchs[user_id].get(key) == None:
            bot.answer_callback_query(callback_query_id=call.id , text="لطفا تمام اطلاعات را تکمیل کنید" , show_alert=True)
            
            return
    bot.edit_message_text(chat_id=cid , message_id=mid , text="لطفا لوکیشن حدودی منطقه مورد نظر خود را ارسال کنید" , reply_markup=None)
    user_steps[user_id] = 'search location'
@bot.message_handler(content_types=['location'] , func = lambda message: user_steps.get(message.from_user.id) == 'search location')
def search_location(message):
    
    user_id = message.from_user.id
    cid = message.chat.id
    bot.send_message(chat_id=cid , text="⌛در حال جست و جوی فایل های مد نظر شما")
    time.sleep(3)
    long = message.location.longitude
    lat = message.location.latitude
    searchs[user_id]['long'] = long
    searchs[user_id]['lat'] = lat
    files = find_similar_files(searchs.get(user_id))
    if len(files) == 0:
        bot.send_message(text = "متاسفانه فایلی مشابه درخواست شما در محدوده تعیین شده یافت نشد" , chat_id=cid)
        return
    for file in files:
        text = format_file_result(file)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = "ذخیره این فایل" , callback_data=f"save file {file['file_id']}") )
        markup.add(InlineKeyboardButton(text = "عکس قبلی" , callback_data=f"open image {file['file_id']} 0"),InlineKeyboardButton(text = "عکس بعدی" , callback_data=f"open image {file['file_id']} 2"))
        image_path = os.path.join("images", f"file_{file['file_id']}_images", "image_1.jpg")
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                image = f.read()
                message = bot.send_photo(caption=text  , reply_markup=markup , photo=image , chat_id=cid , parse_mode='markdown')
                register_markups(message_id=message.id, chat_id=cid , user_id=user_id , markup=markup)
        else:
            message = bot.send_message(text=text  , reply_markup=markup , chat_id=cid , parse_mode='markdown')
            register_markups(message_id=message.id, chat_id=cid , user_id=user_id , markup=markup)   
        bot.send_location(chat_id=cid ,longitude=file['loc_long'] , latitude=file['loc_lat'])
@bot.callback_query_handler(func = lambda call : call.data.startswith('save file'))
def add_to_saves(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    file_id = call.data.split()[-1]
    id = find_id(user_id)
    if not find_save(id , file_id):
       bot.answer_callback_query(text = "فایل قبلا ذخیره شده" , callback_query_id=call.id) 
       return
    
    ans = insert_to_saves(file_id = file_id , user_id = id)

    if ans.startswith('save with id'):
        bot.answer_callback_query(text = "فایل ذخیره شد" , callback_query_id=call.id)

@bot.callback_query_handler(func = lambda call : call.data.startswith('open image'))
def edit_image(call):
    mid = call.message.id
    cid = call.message.chat.id
    file_id = call.data.split()[-2] 
    index = int(call.data.split()[-1]) 
    if index <=0:
        bot.answer_callback_query(text = "این عکس اولین عکس فایل است" , callback_query_id=call.id )
        
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = "ذخیره این فایل" , callback_data=f"save file {file_id}") )
    markup.add(InlineKeyboardButton(text = "عکس قبلی" , callback_data=f"open image {file_id} {index -1}"),InlineKeyboardButton(text = "عکس بعدی" , callback_data=f"open image {file_id} {index+1}"))
    file  = find_file(file_id)
    text = format_file_result(file)
    try :
        image_path = os.path.join("images", f"file_{file_id}_images", f"image_{index}.jpg")
        with open(image_path, "rb") as f:
            image = f.read()
            bot.edit_message_media(message_id=mid , chat_id=cid , media=InputMediaPhoto(image,caption=text , parse_mode='markdown' ), reply_markup=markup)
            user_id = call.from_user.id
            register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
            return
    except Exception as e:
        
        bot.answer_callback_query(text = "این آخرین عکس فایل است" , callback_query_id=call.id)
        return
@bot.message_handler(func=lambda message: message.text == '📝 ثبت‌نام')
def register(message):
    cid = message.chat.id
    user_id = message.from_user.id
    deactive_markups(user_id)
    if search_user(f'{user_id}') != None:
        bot.send_message(chat_id=cid , text = "شما قبلا در ربات ثبت نام کرده اید لطفا خدمات مورد نظر خود را انتخاب کنید")
        return
    bot.send_message(chat_id=cid,text = " لطفا نام و نام خانوادگی ارسال کنید")
    user_steps[user_id] = 'getting name'
    new_accounts[user_id] = dict()
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting name')
def get_name(message):
    cid = message.chat.id
    user_id = message.from_user.id
    new_accounts[user_id]['name'] = message.text
    user_steps[user_id] = 'getting phone'
    bot.send_message(chat_id=cid,text = " لطفا شماره تلفن ارسال کنید")
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting phone')
def get_name(message):
    cid = message.chat.id
    user_id = message.from_user.id
    new_accounts[user_id]['phone'] = message.text
    user_steps[user_id] = 'getting national id'
    bot.send_message(chat_id=cid,text = " لطفا کد ملی خود را ارسال کنید")
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting national id')
def get_name(message):
    cid = message.chat.id
    user_id = message.from_user.id
    new_accounts[user_id]['national id'] = message.text
    user_steps[user_id] = 'getting email'  
    bot.send_message(chat_id=cid,text = " لطفا ایمیل  خود را ارسال کنید")   

@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting email')
def get_name(message):
    cid = message.chat.id
    user_id = message.from_user.id
    new_accounts[user_id]['email'] = message.text
    
    try:

        print(insert_to_users(name = new_accounts[user_id]['name']  ,national_id = new_accounts[user_id]['national id'],phone = new_accounts[user_id]['phone'], email = new_accounts[user_id]['email'] , telegram_id = f"{user_id}" ))
        bot.send_message(chat_id=cid,text = 'ثبت نام شما تکمیل شد')
    except Exception as e:
        print(e)
    user_steps[user_id] = 'Home'
@bot.message_handler(func=lambda message: message.text == '📃 ایجاد فایل جدید')
def create_file(message):
    
    cid = message.chat.id
    user_id = message.from_user.id
    deactive_markups(user_id)
    if search_user(f'{user_id}') == None:
        bot.send_message(chat_id=cid , text = "لطفا ابتدا در ربات ثبت نام کنید")
        return
    new_files[user_id] = dict()
    user_steps[user_id] = 'create first page'
    new_files[user_id]['images'] = []
    markup = create_file_markup(new_files[user_id])
    message_sent = bot.send_message(
        chat_id=cid , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup=markup)
    register_markups(message_id=message_sent.id, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'file type')
def get_file_type(call):
    mid = call.message.id
    cid = call.message.chat.id
    
    markup = InlineKeyboardMarkup()
    
    markup.add(
        InlineKeyboardButton(text='فروش' , callback_data='sale'),
        InlineKeyboardButton(text='اجاره', callback_data='rent')
    )
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    
    bot.edit_message_text( chat_id=cid , message_id=mid , text='نوع فایل خود را انتخاب کنید' , reply_markup=markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'prop type')
def get_file_type(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='مسکونی' , callback_data='house'),
        InlineKeyboardButton(text='تجاری یا اداری', callback_data='office')
    )
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text(chat_id=cid , message_id=mid , text='نوع ملک خود را انتخاب کنید' , reply_markup=markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)


@bot.callback_query_handler(func = lambda call: call.data == 'get area')
def area(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get area'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = " 0-50 متر" ,callback_data='area 0-50'),InlineKeyboardButton(text = " 50-100 متر" ,callback_data='area 50-100'))
    markup.add(InlineKeyboardButton(text = "100-150 متر  " ,callback_data='area 100-150'),InlineKeyboardButton(text = " 150-200 متر" ,callback_data='area 150-200'))
    markup.add(InlineKeyboardButton(text = "200-250 متر  " ,callback_data='area 200-250'),InlineKeyboardButton(text = " 250-300 متر" ,callback_data='area 250-300'))
    markup.add(InlineKeyboardButton(text = "بالای 300 متر" , callback_data="area 300+"))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'متراژ ملک خود را ارسال کنید' , reply_markup = markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get year')
def get_year(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = "نوساز(0-2 سال ساخت)" , callback_data=f'choose year new'))
    markup.add(InlineKeyboardButton(text = "سن متوسط(2-10 سال ساخت)" , callback_data=f'choose year mid_age'))
    markup.add(InlineKeyboardButton(text = "قدیمی (10-30 سال ساخت)" , callback_data=f'choose year old'))
    markup.add(InlineKeyboardButton(text = "کلنگی (بیش از 30 سال ساخت)" , callback_data=f'choose year very old'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'سال ساخت ملک خود را انتخاب کنید' , reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get rooms')
def get_rooms(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(0,5):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose rooms {i}'))
    markup.add(InlineKeyboardButton(text='5 یا بیشتر '  , callback_data='choose rooms 5'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    user_id = call.from_user.id
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'تعداد اتاق های ملک خود را انتخاب کنید' , reply_markup = markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call: call.data == 'get floor')
def get_rooms(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    for i in range(0,5,2):
        markup.add(InlineKeyboardButton(text=f'{i}' , callback_data=f'choose floor {i}'),InlineKeyboardButton(text=f'{i+1}' , callback_data=f'choose floor {i+1}'))
    markup.add(InlineKeyboardButton(text='5 یا بیشتر '  , callback_data='choose floor 5'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    user_id = call.from_user.id
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'طبقه ملک خود را انتخاب کنید' , reply_markup = markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
    
@bot.callback_query_handler(func= lambda call : call.data == 'elevator')
def get_elevator(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes elevator') , InlineKeyboardButton(text='خیر' , callback_data='No elevator'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'آیا ملک شما آسانسور دارد' , reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
#@bot.message_handler(func = lambda message: user_steps.get(message.from_user.id) == 'create first page')
#def bot.delete_messages(message):
    #cid= message.chat.id
    #mid = message.id
    #delete_message(bot = bot , chat_id=cid , message_id=mid)
@bot.callback_query_handler(func= lambda call : call.data == 'parking')
def get_parking(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes parking') , InlineKeyboardButton(text='خیر' , callback_data='No parking'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'آیا ملک شما پارکینگ دارد' , reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func= lambda call : call.data == 'storage')
def get_storage(call):
    mid = call.message.id
    cid = call.message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'بله' , callback_data='Yes storage') , InlineKeyboardButton(text='خیر' , callback_data='No storage'))
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'آیا ملک شما انباری دارد' , reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'first page')
def first_page(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'rent' or call.data == 'sale')
def file_type(call):
    user_id = call.from_user.id
    if new_files[user_id].get('type') == call.data:
        return
    new_files[user_id]['type'] = call.data
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'house' or call.data == 'office')
def file_type(call):
    user_id = call.from_user.id
    if new_files[user_id].get('property') == call.data:
        return
    new_files[user_id]['property'] = call.data
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('choose'))
def get_num(call):
    user_id = call.from_user.id
    key , value = call.data.split()[-2],call.data.split()[-1]
    new_files[user_id][key] = value
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data.startswith('Yes') or call.data.startswith('No'))
def get_num(call):
    user_id = call.from_user.id
    key , value = call.data.split()[1],call.data.split()[0]
    new_files[user_id][key] = value
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call: call.data.startswith('area'))

def get_area(call):
    user_id = call.from_user.id
    value = call.data.split()[1]
    new_files[user_id]['area'] = value
    cid = call.message.chat.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    user_steps[user_id] = 'create first page'
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'اطلاعات زیر را تکمیل کنید', reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.callback_query_handler(func = lambda call : call.data == 'add image')
def get_image(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    
    user_steps[user_id] = f'get image {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text( chat_id = cid , message_id = mid , text = 'عکس ملک خود را ارسال کنید' , reply_markup = markup)
    user_id = call.from_user.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)

@bot.message_handler(content_types=['photo'] ,func = lambda message: user_steps.get(message.from_user.id).startswith('get image') )
def get_image(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    image_id = message.photo[-1].file_id
    image_info = bot.get_file(image_id)
    image_path = image_info.file_path
    image_url = f"https://api.telegram.org/file/bot{bot.token}/{image_path}"
    image = requests.get(image_url).content
    new_files[user_id]['images'].append(image)
    
    markup = create_file_markup(new_files[user_id])
    bot.delete_message(chat_id=cid , message_id=mid)
    bot.edit_message_text(chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    user_id = message.from_user.id
    mid = int(user_steps[user_id].split()[-1])
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
    user_steps[user_id] = 'create first page'
   
@bot.callback_query_handler(func = lambda call : call.data == 'title')
def title(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get title {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text(chat_id = cid , message_id = mid , text = ' بین 3 تا 7 کلمه)عنوان ملک خود را ارسال کنید)' , reply_markup = markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.message_handler(func = lambda message:  user_steps.get(message.from_user.id)!= None and user_steps.get(message.from_user.id).startswith('get title'))
def get_title(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['title'] = message.text
    
    bot.delete_message(chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    bot.edit_message_text( chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    mid = int(user_steps[user_id].split()[-1])
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
    user_steps[user_id] = 'create first page'

@bot.callback_query_handler(func = lambda call : call.data == 'explain')
def explain(call):
    mid = call.message.id
    cid = call.message.chat.id
    user_id = call.from_user.id
    user_steps[user_id] = f'get explain {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data='first page'))
    bot.edit_message_text(chat_id = cid , message_id = mid , text = 'توضیحات ملک خود را ارسال کنید' , reply_markup = markup)
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
@bot.message_handler(func = lambda message:  user_steps.get(message.from_user.id)!= None and user_steps.get(message.from_user.id).startswith('get explain'))
def get_explain(message):
    
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['explain'] = message.text
    
    bot.delete_message( chat_id=cid , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    
    bot.edit_message_text(chat_id = cid , message_id = int(user_steps[user_id].split()[-1]) , text = 'اطلاعات زیر را تکمیل کنید' , reply_markup = markup)
    mid = int(user_steps[user_id].split()[-1])
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
    user_steps[user_id] = 'create first page'
@bot.callback_query_handler(func = lambda call : call.data.startswith('edit image') or call.data.startswith('edit_image'))
def edit_image(call):
    
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    if len (new_files[user_id].get('images')) == 0  or new_files[user_id].get('images') == None:
        answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="فایل شما هیچ عکسی ندارد",
            show_alert=True
        )
        return
    index = int(call.data.split()[-1])
    
    if index <0 or index>=len(new_files[user_id]['images']):
        
        return
    
    bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=None)
    user_steps[user_id] = f'edit image {mid}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='قبلی' , callback_data=f"edit_image {index - 1}") , InlineKeyboardButton(text = "بعدی" , callback_data=f"edit_image {index + 1}"))
    markup.add(InlineKeyboardButton(text = "صفحه تکمیل اطلاعات"  , callback_data= f'back to first page'))
    if call.data.startswith('edit_image'):
        bot.edit_message_media(chat_id=cid , message_id=mid , media=InputMediaPhoto(new_files[user_id]['images'][index],caption = send_final_file(new_files[user_id]),parse_mode='markdown' ), reply_markup=markup)
        return
    message = bot.send_photo( chat_id=cid,photo = new_files[user_id]['images'][index] ,caption=send_final_file(new_files[user_id]), reply_markup=markup , parse_mode='markdown')

    mid = message.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
    return
@bot.callback_query_handler(func = lambda call : call.data.startswith('delete image'))
def delete_image(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = user_steps[user_id].split()[-1]
    index =  int(call.data.split()[-1])
    if len(new_files[user_id]['images']==1):
        with open('noimage.png' , 'rb') as f:
            photo = f.read()
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text = 'بازگشت به صفحه قبل' , callback_data=f'back to first page'))
            bot.edit_message_media( chat_id=cid , message_id=mid,media= InputMediaPhoto(photo,caption="فاقد عکس دیگر") ,reply_markup= markup)
            register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup)
            return
    markup = InlineKeyboardMarkup()
    if index >0:
        markup.add(InlineKeyboardButton(text = 'قبلی' , callback_data=f"edit image b {index - 1}"),InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
        bot.edit_message_media(chat_id=cid, message_id=mid)
    if index== 0 and index < len(new_files[user_id]['images']) -1:
        markup.add(InlineKeyboardButton(text = 'بعدی' , callback_data=f"edit image {index + 1}"))
    markup.add(InlineKeyboardButton(text = 'صفحه قبل' , callback_data=f'back to first page'))
    del new_files[user_id]['images'][index]
    if index > 0:
        bot.edit_message_media(chat_id=cid , message_id=call.message.id,media=InputMediaPhoto(new_files[user_id]['images'][index ]) , reply_markup=markup) 
        register_markups(message_id=call.message.id, chat_id=cid , user_id=user_id , markup=markup)     
        return
    bot.edit_message_media(chat_id=cid , message_id=call.message.id,media=InputMediaPhoto(new_files[user_id]['images'][index]) , reply_markup=markup) 
    register_markups(message_id=call.message.id, chat_id=cid , user_id=user_id , markup=markup) 
@bot.callback_query_handler(func = lambda call : call.data.startswith('back to first page'))
def back(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = call.message.id
    markup = create_file_markup(new_files[user_id])
    bot.delete_message(chat_id=cid , message_id=mid)
    
    message = bot.send_message(chat_id=cid,text = "اطلاعات زیر را تکمیل کنید", reply_markup=markup)
    mid = call.message.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 
    return
@bot.callback_query_handler(func = lambda call : call.data == 'next step')
def get_price(call):
    cid = call.message.chat.id
    mid = call.message.id
    user_id = call.from_user.id
    
    for feature in file_keys:
        if new_files[user_id].get(feature) == None:
            answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="لطفا همه اطلاعات را تکمیل کنید",
            show_alert=True
            )
            return
        if len (new_files[user_id].get('images')) == 0 :
            answer_callback_query(
            bot = bot,
            callback_query_id=call.id,
            text="ارسال حداقل یک عکس الزامی است",
            show_alert=True
            )
            return
    bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=None)
  
    if new_files[user_id]['type'] == 'sale':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data= 'first page'))
        message = bot.send_message(chat_id=cid , text = 'قیمت مد نظر برای ملک خود را ارسال کنید' , reply_markup=markup)
        mid = message.id
        register_markups(message_id=call.message.id, chat_id=cid , user_id=user_id , markup=markup) 
        user_steps[user_id] = 'getting sell price'
        return
    if new_files[user_id]['type'] == 'rent':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'مرحله قبل' , callback_data= 'first page'))
        message =bot.send_message(chat_id=cid , text = 'ودیعه مد نظر برای ملک خود را ارسال کنید' , reply_markup=markup)
        mid = message.id
        register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 
        user_steps[user_id] = 'getting deposit'
        return
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting deposit')
def get_depos(message):
    
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['deposit'] = message.text
    user_steps[user_id] = 'getting rent'
    
    bot.send_message(chat_id=cid , text = 'اجاره مد نظر خود را برای ملک خود ارسال کنید')
    
    return
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting rent')
def get_rent(message):
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['rent'] = message.text
    text = send_final_file(new_files[user_id])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='تایید و ایجاد فایل' , callback_data='confirm'))
    markup.add(InlineKeyboardButton(text='ویرایش' , callback_data='back to first page'))
    markup.add(InlineKeyboardButton(text = 'عکس بعدی', callback_data='next image 0'),InlineKeyboardButton(text = 'عکس قبلی', callback_data='pre image 0'))
    message = bot.send_photo(chat_id = cid,caption=text , photo=new_files[user_id]['images'][0],reply_markup=markup , parse_mode="Markdown")
    mid = message.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 
    
    
    user_steps[user_id] = 'review file'
    return
@bot.callback_query_handler(func = lambda call : call.data == 'back')
def back(call):
    cid = call.message.chat.id
    user_id  = call.from_user.id
    mid = call.message.id
    bot.delete_message(chat_id=cid  , message_id=mid)
    markup = create_file_markup(new_files[user_id])
    message = bot.send_message(chat_id=cid , text="اطلاعات زیر را تکمیل کنید" , reply_markup=markup)
    mid = message.id
    register_markups(message_id=call.message.id, chat_id=cid , user_id=user_id , markup=markup) 
@bot.message_handler(func = lambda message : user_steps.get(message.from_user.id) == 'getting sell price')
def get_price(message):
    user_id = message.from_user.id
    cid = message.chat.id
    new_files[user_id]['price'] = message.text
    text = send_final_file(new_files[user_id])
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'ویرایش' , callback_data='back to first page'))
    markup.add(InlineKeyboardButton(text = "تایید" , callback_data= 'confirm'))
    markup.add(InlineKeyboardButton(text = 'عکس بعدی', callback_data='next image 0'),InlineKeyboardButton(text = 'عکس قبلی', callback_data='pre image 0'))
    message = bot.send_photo(chat_id = cid,caption=text , photo=new_files[user_id]['images'][0],reply_markup=markup , parse_mode="Markdown")
    mid = message.id
    register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 
    user_steps[user_id] = 'review file'
    user_steps[user_id] = 'review file'
@bot.callback_query_handler(func = lambda call : call.data.startswith('next image'))
def nex_image(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    index = int(call.data.split()[-1])
    if index == len(new_files[user_id]['images'])-1:
        bot.answer_callback_query(callback_query_id=call.id , text = 'این عکس آخرین عکس فایل شماست',show_alert=True)
    else:
        bot.edit_message_media(chat_id=cid , message_id=mid,media=InputMediaPhoto( new_files[user_id]['images'][index+1] , caption = send_final_file(new_files[user_id]),parse_mode='markdown') )
        markup = InlineKeyboardMarkup()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'ویرایش' , callback_data='back to first page'))
        markup.add(InlineKeyboardButton(text = "تایید" , callback_data= 'confirm'))
        markup.add(InlineKeyboardButton(text = 'عکس بعدی', callback_data=f"next image {index+1}"),InlineKeyboardButton(text = 'عکس قبلی', callback_data=f"pre image {index+1}"))
        bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=markup)
        register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 

@bot.callback_query_handler(func = lambda call : call.data.startswith('pre image'))
def pre_image(call):
    user_id = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.id
    index = int(call.data.split()[-1])
    if index == 0:
        bot.answer_callback_query(callback_query_id=call.id , text = 'این عکس اولین عکس فایل شماست',show_alert=True)
    else:
        bot.edit_message_media(chat_id=cid , message_id=mid,media=InputMediaPhoto(new_files[user_id]['images'][index-1] , caption=send_final_file(new_files[user_id]),parse_mode='markdown') )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text = 'ویرایش' , callback_data='back to first page'))
        markup.add(InlineKeyboardButton(text = "تایید" , callback_data= 'confirm'))
        markup.add(InlineKeyboardButton(text = 'عکس بعدی', callback_data=f"next image {index-1}"),InlineKeyboardButton(text = 'عکس قبلی', callback_data=f"pre image {index-1}"))
        bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=markup)
        register_markups(message_id=mid, chat_id=cid , user_id=user_id , markup=markup) 
@bot.callback_query_handler(func = lambda call : call.data == 'confirm')
def get_location(call):
    cid = call.message.chat.id
    user_id = call.from_user.id
    mid = call.message.id
    bot.edit_message_reply_markup(chat_id=cid , message_id=mid , reply_markup=None)
    bot.send_message(chat_id=cid , text = "در آخر لطفا لوکیشن ملک خود را ارسال کنید")
    user_steps[user_id] = 'getting location'

@bot.message_handler(content_types=['location'] , func = lambda message: user_steps[message.from_user.id] == 'getting location' )
def add_file(message):
    cid = message.chat.id
    user_id = message.from_user.id
    mid = message.id
    new_files[user_id]['location_long'] = message.location.longitude
    new_files[user_id]['location_lat'] = message.location.latitude
    file = new_files[user_id]
    user = search_user(f'{user_id}')
    
    
    try:
        answer = insert_to_files(user_id = user['user_id'] , title = file['title'], storage = file['storage'],description = file['explain'] ,year = file['year'],parking = file['parking'],elevator = file['elevator'] , floor = file['floor'] ,area = file['area'], rooms = file['rooms'] , price = file.get('price') , rent =  file.get('rent')  , deposit = file.get('deposit') , file_type = file['type'] , property_type = file['property'], is_active = 'Y' , location_long = file['location_long'],location_lat = file['location_lat'])
        base_path = "images"
        file_dir = os.path.join("images", f"file_{answer}_images")
        os.makedirs(file_dir, exist_ok=True)
        images = file['images']
        i=1
        for image in images:
            image_path = os.path.join(file_dir, f"image_{i}.jpg")
            with open(image_path, "wb") as f:
                f.write(image)
                i+=1
        if isinstance(answer,int):
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text = "قرار دادن روی کانال", callback_data=f"put on channel {answer}" ))
            bot.send_message(chat_id=cid , text = "فایل شما با موفقیت ایجاد شد" , reply_markup=markup)
            print(f"inserted images for file {answer} successfuly")
    except Exception as e:
        print(f'failed to insert file with error : {e}')
@bot.callback_query_handler(func = lambda call : call.data.startswith("put on channel"))
def send_file_to_channel(call):
    cid = call.message.chat.id
    file_id = int(call.data.split()[-1])
    image_path = os.path.join("images", f"file {file_id} images\image 1")
    file = find_file(file_id)
    text = format_file_result(file)
    image_path = os.path.join("images", f"file_{file_id}_images", "image_1.jpg")
    with open(image_path, "rb") as f:
        image = f.read()
        markup = InlineKeyboardMarkup()
        url = rf"https://t.me/{bot_username}?start=file_{file_id}"
        markup.add(InlineKeyboardButton(text = "مشاهده فایل و شماره تماس صاحب ملک" , url=url))
        bot.send_photo(chat_id=channel_user ,photo=image , caption=text , parse_mode='markdown' , reply_markup=markup )
        bot.answer_callback_query(text = "فایل شما روی کانال قرار گرفت" , callback_query_id=call.id)
        return

bot.infinity_polling()
