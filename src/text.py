from telegram.ext import Filters, Updater, CommandHandler, MessageHandler, InlineQueryHandler
from telegram import ParseMode
import requests
import re

from utils import *
import constant


def harbour(update, context):
    send_text(update, context, 'Harbour資訊Group：\n\nhttps://t.me/kibouhaba')


def mm(update, context):
    send_text(
        update,
        context,
        '想買二手機械鍵盤可以留意以下地方：\n\n1. Discord：https://discord.gg/kk77tnJJ5z\n' +
        '2. Reddit：https://www.reddit.com/r/mechmarket/\n3. 閒魚（支那手機App）'
    )


def bokkey(update, context):
    send_text(update, context, 'Bokkey幫到你 @Hinsonli')


def frusta(update, context):
    send_text(update, context, 'Frusta資訊台：\n\nhttps://t.me/joinchat/RzLPs5N8GaEQ_uN2')


def fuyu(update, context):
    send_text(update, context, 'Fuyu資訊台：\n\nhttps://t.me/joinchat/3mFIsiq1pCk0ZDI9')


def new_member(update, context):
    for member in update.message.new_chat_members:
        update.message.reply_text('歡迎加入香港機械鍵盤TG Group！有咩疑難雜症歡迎喺度隨便問，無論你玩廠board定自組，新手定大佬，呢度好多人都樂意幫你。\n\n'
                                  + '另外鍵谷有個bot，新人可以用下啲Commands，入面有各種有用資料。新人想嘅，可以自貼自己嘅鍵盤交流下 :)')


def akis(update, context):
    send_text(update, context, 'AKI-S資訊台：\n\nhttps://t.me/hj2qnews')


def local(update, context):
    send_text(
        update,
        context,
        '香港近年盛產客製化鍵盤作者，本谷有幸收納當中四位。玩家可以於以下連結留意作者最新消息：\n\n' +
        '1. Jeff（Thic Thock）\n- AKI-S | 65% | Top Mount\n- 資訊發佈：https://t.me/hj2qnews\n' +
        '- Typing Demo：https://youtu.be/NZ82MLR4Gok\n\n' +
        '2. 目空（Picolab）\n- Frusta Fundemental | 65% | Multi Mount\n- 資訊發佈：https://t.me/joinchat/RzLPs5N8GaEQ_uN2\n' +
        '- Typing Demo：https://youtu.be/BLGTq045X0g\n\n' +
        '3. 牙仲（kibou）\n- Harbour | 65% | Gasket Mount\n- 資訊發佈：https://t.me/kibouhaba\n\n' +
        '4. 腐乳\n- Fuyu | 75% | Gasket Mount\n- Lamy | TKL | Top Mount\n- 資訊發佈：https://t.me/joinchat/3mFIsiq1pCk0ZDI9'
    )


def pricelist(update, context):
    send_text(
        update,
        context,
        'HJ2Q Studio (Thic Thock X Bokkey) 物價表：\n\n' +
        'https://docs.google.com/spreadsheets/d/1KCaWmZHqTRJyimor_btQFTgPgwdpYezSP7dzVfR9ZaM/edit#gid=0\n'
    )


def studio(update, context):
    send_text(
        update,
        context,
        'HJ2Q Studio (Thic Thock X Bokkey) 現已開放！\n\n' +
        '地址：新界火炭華樂工業中心E座12樓4室\n' +
        '開放日子：14/8, 20/8, 21/8, 27/8, 28/8\n' +
        '開放時間：13:00 - 19:00\n\n' +
        '交流會：28/8\n' +
        '展示鍵盤：\n' + '- Geonworks Frog TKL\n' + '- GOK 7V\n' + '- AKI-S\n\n' +
        #'潤滑工作坊：10/7(SAT) | 14:00 - 17:00 | HKD400\n\n' +
        '詳情請留意 https://t.me/hj2qnews'
    )


def HJ2QInfo(update, context):
    send_text(update, context, 'HJ2Q Studio資訊台：\n\nhttps://t.me/hj2qnews')


def HJ2QTierList(update, context):
    send_text(update, context, 'HJ2Q Studio 鍵盤排行榜: ' + 'https://bit.ly/3cM0ruc')


def GMMKPro(update, context):
    send_text(update, context, 'GMMK Pro Review（By Bokkey）：\n\nhttps://www.bokkey.me/post/gmmkpro')


def Keychron(update, context):
    send_text(update, context, 'Keychron K6 Review（By Bokkey）：\n\nhttps://www.bokkey.me/keychron-k6-review')


def brush(update, context):
    send_text(update, context, 'Bokkey潤滑專用筆の推薦與講解：\n\nhttps://www.bokkey.me/post/brush')


def grapebook(update, context):
    send_text(update, context, '提子天書，aka 香港鍵谷寶典：\n' + 'https://drive.google.com/drive/folders/1nNmqXb_wfQDiqq6TlErVkXMkp8oUnD8K')

def sourcecode(update, context):
    send_text(update, context, '我啲Code喺曬度：\nhttps://github.com/toothskyfansclub/HK-Mech-Key-Bot.git')
