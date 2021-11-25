from utils import *


def mukong_quote(update, context):
	send_quote(update, context, True)


def update_mukong_quote(update, context):
	handle_add_quote(update, context, True)


def grape_quote(update, context):
	send_quote(update, context, False)


def update_grape_quote(update, context):
	handle_add_quote(update, context, False)
