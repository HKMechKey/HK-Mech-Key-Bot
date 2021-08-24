from datetime import datetime, timedelta
from functools import reduce

from decouple import config

import constant


def is_mukong(update):
    return update.message.from_user.id == constant.mukong_id


def can_play_quote():
    return constant.status


def is_correct_group(update, context):
    chat_id = update.message.chat_id
    return chat_id == constant.group_chat_id or chat_id == constant.test_chat_id


def can_use_command():
    now = datetime.now()

    if constant.current_time is None:
        constant.current_time = now
        return True
    else:
        tdelta = now - constant.current_time
        if tdelta.total_seconds() > constant.CD:
            constant.current_time = now
            return True
        else:
            return False

    return False


def send_text(update, context, input_text):
    if can_use_command():
        context.bot.sendMessage(chat_id=update.message.chat_id, text=input_text)


def send_image(update, context, link):
    if can_use_command():
        context.bot.sendPhoto(chat_id=update.message.chat_id, photo=link)


def send_voice(update, context, file_dir):
    if can_use_command():
        context.bot.sendVoice(chat_id=update.message.chat_id, voice=open(file_dir, 'rb'))


def send_animation(update, context, file_dir):
    if can_use_command():
        context.bot.sendAnimation(chat_id=update.message.chat_id, animation=open(file_dir, 'rb'))


def update_header(CV, header):
    new_header = header + ' (' + get_time() + ' ver.)\n'
    index = CV.find('ver.)')
    return new_header + CV[index + 6:]


def get_quote():
    db = open('data/quotes.txt', 'r')
    return db.read().split('\n')


def get_gb():
    db = open('data/gb.txt', 'r')
    gb_list = db.read().split('\n')
    gb_dict = {}
    
    for lines in gb_list:
        line = lines.split(', ')
        gb_dict[line[0]] = line[1:]

    return gb_dict


def get_purchase_list():
    f = open("data/purchase.txt", "r")
    purchase_list = update_header(f.read(), header='Grapebuy List')
    return purchase_list


def get_time(month=False, value=7):
    now = datetime.now()

    if not month:
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S")
        return date_time
    else:
        arr = []
        for i in range(value):
            res = now + timedelta(days=i)
            arr.append(res.strftime("%m-%d"))
        return arr

    return None


def get_current_list(update, context):
    send_text(update, context, get_purchase_list())


def add_purchase_item(update, context):
    chat_id = update.message.chat_id
    args = context.args

    if len(args) == 0:
        context.bot.sendMessage(chat_id=chat_id, text='冇寫要加咩新item')
    else:
        new_title = ''
        for arg in args:
            new_title = new_title + arg + ' '
        new_title = new_title[:-1]
        purchase_list = get_purchase_list()
        items = purchase_list.split('\n')
        new_num = int(items[-1][:items[-1].find('.')]) + 1
        new_list = update_header(purchase_list + '\n' + str(new_num) + '. ' + new_title, header='Grapebuy List')
        context.bot.sendMessage(chat_id=chat_id, text=new_list)
        f = open("data/purchase.txt", 'w')
        f.write(new_list)
        f.close()


def delete_item(update, context):
    chat_id = update.message.chat_id
    args = context.args

    if len(args) != 1:
        context.bot.sendMessage(chat_id=chat_id, text='Format Error')
    else:
        del_index = int(args[0])
        purchase_list = get_purchase_list()
        items = purchase_list.split('\n')
        if del_index > len(items) - 1:
            context.bot.sendMessage(chat_id=chat_id, text='Format Error')
        else:
            for i in range(del_index + 2, len(items)):
                items[i] = str(int(items[i][:items[i].find('.')]) - 1) + items[i][items[i].find('.'):]
            items.pop(del_index + 1)
            new_list = items[0] + '\n'
            items.pop(0)
            new_list = update_header(new_list + reduce(lambda a,b: a + '\n' + b, items), header='Grapebuy List')
            context.bot.sendMessage(chat_id=chat_id, text=new_list)
            f = open("data/purchase.txt", 'w')
            f.write(new_list)
            f.close()
