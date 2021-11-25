import os

from decouple import config
from telegram.ext import Filters, Updater, CommandHandler, MessageHandler

from gb import *
from media import *
from quotes import *
from text import *
from utils import *


def main():
	TOKEN = config('TOKEN')
	PORT = int(os.environ.get('PORT', 8443))

	updater = Updater(TOKEN, use_context=True)
	dispatcher = updater.dispatcher
	# job_queue = updater.job_queue

	dispatcher.add_handler(CommandHandler('akis', akis))
	dispatcher.add_handler(CommandHandler('frusta', frusta))
	dispatcher.add_handler(CommandHandler('mm', mm))
	dispatcher.add_handler(CommandHandler('harbour', harbour))
	dispatcher.add_handler(CommandHandler('local', local))
	dispatcher.add_handler(CommandHandler('switchtier', switchtier))
	dispatcher.add_handler(CommandHandler('stock', stock))
	dispatcher.add_handler(CommandHandler('profile', profile))
	dispatcher.add_handler(CommandHandler('HJ2QNews', HJ2QInfo))
	dispatcher.add_handler(CommandHandler('bokkey', bokkey))
	dispatcher.add_handler(CommandHandler('scratch', scratch))
	dispatcher.add_handler(CommandHandler('bid', bid))
	dispatcher.add_handler(CommandHandler('dllmch', dllmch))
	dispatcher.add_handler(CommandHandler('askyourmom', askyourmom))
	dispatcher.add_handler(CommandHandler('askyourmum', askyourmom))
	dispatcher.add_handler(CommandHandler('focus', rich))
	dispatcher.add_handler(CommandHandler('studio', studio))
	dispatcher.add_handler(CommandHandler('pricelist', pricelist))
	dispatcher.add_handler(CommandHandler('laugh', laugh))
	dispatcher.add_handler(CommandHandler('gmk', GMK))
	dispatcher.add_handler(CommandHandler('gmmkpro', GMMKPro))
	dispatcher.add_handler(CommandHandler('keychron', Keychron))
	dispatcher.add_handler(CommandHandler('fuyu', fuyu))
	dispatcher.add_handler(CommandHandler('on9son', on9son))
	dispatcher.add_handler(CommandHandler('brush', brush))
	dispatcher.add_handler(CommandHandler('keycapreminder', get_keycap_GB))
	dispatcher.add_handler(CommandHandler('keyboardreminder', get_keyboard_GB))
	dispatcher.add_handler(CommandHandler('holunangry', mad))
	dispatcher.add_handler(CommandHandler('roadmap', roadmap))
	dispatcher.add_handler(CommandHandler('addbuyitem', add_purchase_item))
	dispatcher.add_handler(CommandHandler('grapebuylist', get_current_list))
	dispatcher.add_handler(CommandHandler('delbuyitem', delete_item))
	dispatcher.add_handler(CommandHandler('keebtierlist', HJ2QTierList))
	dispatcher.add_handler(CommandHandler('urgay', gay))
	dispatcher.add_handler(CommandHandler('grapebook', grapebook))
	dispatcher.add_handler(CommandHandler('mukongquote', mukong_quote))
	dispatcher.add_handler(CommandHandler('addmukongquote', update_mukong_quote))
	dispatcher.add_handler(CommandHandler('grapequote', grape_quote))
	dispatcher.add_handler(CommandHandler('addgrapequote', update_grape_quote))
	dispatcher.add_handler(CommandHandler('code', sourcecode))

	dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
	dispatcher.add_handler(MessageHandler(Filters.text, handle_replied_quote))

	# job_queue.run_daily(get_keycap_GB, morning_datetime, context=None)
	# job_queue.run_daily(get_keycap_GB, afternoon_datetime, context=None)
	# job_queue.run_daily(get_keycap_GB, night_datetime, context=None)
	# job_queue.run_daily(get_keyboard_GB, morning_datetime, context=None)
	# job_queue.run_daily(get_keyboard_GB, afternoon_datetime, context=None)
	# job_queue.run_daily(get_keyboard_GB, night_datetime, context=None)

	updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN,
						  webhook_url='https://hkmk-telegram-bot.herokuapp.com/' + TOKEN)

	updater.idle()


if __name__ == '__main__':
	main()
