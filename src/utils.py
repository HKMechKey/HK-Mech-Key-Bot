from datetime import datetime, timedelta
from functools import reduce
from secrets import randbelow

from telegram import ForceReply

import constant
from aws import *


def is_mukong(update):
	return update.message.from_user.id == constant.mukong_id


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


def get_quote(filename):
	return download_from_aws(filename)


def get_keycap_gb_list():
	db = open('data/keycap_gb.txt', 'r')
	gb_list = db.read().split('\n')
	gb_dict = {}

	for lines in gb_list:
		line = lines.split(', ')
		gb_dict[line[0]] = line[1:]

	return gb_dict


def get_keyboard_gb_list():
	db = open('data/keyboard_gb.txt', 'r')
	gb_list = db.read().split('\n')
	gb_dict = {}

	for lines in gb_list:
		line = lines.split(', ')
		gb_dict[line[0]] = line[1:]

	return gb_dict


def get_purchase_list():
	return update_header(download_from_aws('purchase.txt'), header='Grapebuy List')


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
		upload_to_aws('purchase.txt', new_list)


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
			new_list = update_header(new_list + reduce(lambda a, b: a + '\n' + b, items), header='Grapebuy List')
			context.bot.sendMessage(chat_id=chat_id, text=new_list)
			upload_to_aws('purchase.txt', new_list)


def send_quote(update, context, isMukong):
	if not is_correct_group(update, context):
		send_text(update, context, '喂，鍵谷以外嘅地方唔準用我')
	else:
		filename = 'quotes.txt' if isMukong else 'grape.txt'
		name = '牙空' if isMukong else '提子'

		db = get_quote(filename).split('\n')
		send_text(update, context, name + '：「' + db[randbelow(len(db))] + '」')


def update_quote(update, context, is_mukong, new_quote):
	filename = 'quotes.txt' if is_mukong else 'grape.txt'
	name = '牙空' if is_mukong else '提子'

	new_quote = get_quote(filename) + '\n' + new_quote

	upload_to_aws(filename, new_quote)
	send_text(update, context, name + '語錄已更新')

	constant.can_update_quote = False


def ask_user_new_quote(update, context):
	update.message.reply_text(
		text='要加乜野quote？',
		reply_markup=ForceReply(selective=True)
	)


def handle_add_quote(update, context, is_mukong):
	constant.can_update_quote = True
	constant.is_add_mukong_quote = is_mukong
	ask_user_new_quote(update, context)


def handle_replied_quote(update, context):
	if constant.can_update_quote:
		update_quote(update, context, constant.is_add_mukong_quote, update.message.text)
