from telegram.ext import Filters, Updater, CommandHandler, MessageHandler
from decouple import config

from utils import *
from media import *
from text import *
from quotes import *
from gb import *


def main():
    updater = Updater(config('TOKEN'))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('akis', akis))
    dp.add_handler(CommandHandler('frusta', frusta))
    dp.add_handler(CommandHandler('mm', mm))
    dp.add_handler(CommandHandler('harbour', harbour))
    dp.add_handler(CommandHandler('local', local))
    dp.add_handler(CommandHandler('switchtier', switchtier))
    dp.add_handler(CommandHandler('stock', stock))
    dp.add_handler(CommandHandler('profile', profile))
    dp.add_handler(CommandHandler('HJ2QNews', HJ2QInfo))
    dp.add_handler(CommandHandler('scratch', scratch))
    dp.add_handler(CommandHandler('bid', bid))
    dp.add_handler(CommandHandler('dllmch', dllmch))
    dp.add_handler(CommandHandler('askyourmom', askyourmom))
    dp.add_handler(CommandHandler('askyourmum', askyourmom))
    dp.add_handler(CommandHandler('focus', rich))
    dp.add_handler(CommandHandler('studio', studio))
    dp.add_handler(CommandHandler('pricelist', pricelist))
    dp.add_handler(CommandHandler('laugh', laugh))
    dp.add_handler(CommandHandler('gmk', GMK))
    dp.add_handler(CommandHandler('gmmkpro', GMMKPro))
    dp.add_handler(CommandHandler('keychron', Keychron))
    dp.add_handler(CommandHandler('fuyu', fuyu))
    dp.add_handler(CommandHandler('on9son', on9son))
    dp.add_handler(CommandHandler('brush', brush))
    dp.add_handler(CommandHandler('gbreminder', get_keycap_GB))
    dp.add_handler(CommandHandler('holunangry', mad))
    dp.add_handler(CommandHandler('roadmap', roadmap))
    dp.add_handler(CommandHandler('addbuyitem', add_purchase_item))
    dp.add_handler(CommandHandler('grapebuylist', get_current_list))
    dp.add_handler(CommandHandler('delbuyitem', delete_item))
    dp.add_handler(CommandHandler('keebtierlist', HJ2QTierList))
    dp.add_handler(CommandHandler('urgay', gay))
    dp.add_handler(CommandHandler('grapebook', grapebook))
    dp.add_handler(CommandHandler('quote', quote))
    dp.add_handler(CommandHandler('addquote', update_quote))
    dp.add_handler(CommandHandler('code', sourcecode))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
