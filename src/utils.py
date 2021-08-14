from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, InlineQueryHandler
from datetime import datetime, timedelta
import requests
import re
import pickle
from functools import reduce

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


def check_status(update, context):
    res = constant.awake or update.message.from_user.username == 'mekakibodo'

    if not res:
        send_text(update, context, '未係weekend，冇得玩quote呀')

    return res


def update_header(CV, header):
    new_header = header + ' (' + get_time() + ' ver.)\n'
    index = CV.find('ver.)')
    return new_header + CV[index + 6:]


def get_quote():
    db = open('data/quotes.txt', 'r')
    return db.read().split('\n')


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


def get_today_GB(update, context):
    args =context.args
    val = 7 if len(args) == 0 else int(args[0])

    date_list = get_time(month=True, value=val)

    M = pickle.load(open("data/GBmap.p", "rb"))

    res = '由今天計起，未來' + str(val) + '日內終結的鍵帽團購有：\n'    

    for date in date_list:
        if date in M:
            res += ('\n' + date + '\n')
            for GB in M[date]:
                res += ('- ' + GB + '\n')

    send_text(update, context, res + '\n完\n\n*基於資訊網可信性成疑，以及時區問題，Bot不確保100%準確，玩家請自行Double Check')


def GB_reminder(update, context):
    get_today_GB(update, context)


def add_GB_map(update, context):
    if update.message.from_user.username == 'mekakibodo':
        args =context.args

        if len(args) < 3:
            context.bot.sendMessage(
                chat_id=update.message.chat_id,
                text='[ERR] args error'
            )
        else:
            chat_id = update.message.chat_id
            mode = args[0]
            date = args[1]
            name = ' '.join(args[2:])

            res = pickle.load(open("data/GBmap.p", "rb"))

            if mode == 'list':
                context.bot.sendMessage(
                    chat_id=chat_id,
                    text='[ERR] Non existing entry' if date not in res else '\n'.join(res[date])
                )
            else:
                if date not in res and mode == 'add':
                    res[date] = [name]
                elif name not in res[date] and mode == 'add':
                    res[date].append(name)
                elif date in res and name in res[date] and mode == 'del':
                    res[date].remove(name)
                    if len(res[date]) == 0:
                        res.pop(date, None)
                else:
                    context.bot.sendMessage(
                        chat_id=chat_id,
                        text='[ERR] add map error'
                    )

                print(res)

                pickle.dump(res, open("data/GBmap.p", "wb"))

                context.bot.sendMessage(
                    chat_id=chat_id,
                    text='DONE'
                )


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
