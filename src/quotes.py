from secrets import randbelow

from utils import *
import constant


def quote(update, context):
    if can_play_quote():
        if not is_correct_group(update, context):
            send_text(update, context, '喂，鍵谷以外嘅地方唔準用我')
        else:
            db = get_quote()
            send_text(update, context, '牙空：「' + db[randbelow(len(db))] + '」')


def update_quote(update, context):
    args = context.args

    if is_mukong(update):
        send_text(update, context, '牙空唔好玩自己語錄啦')
    else:
        if len(args) == 0:
            send_text(update, context, '冇寫要加咩新語錄')
        else:
            f = open("data/quotes.txt", 'a')
            new_quote = ''
            for arg in args:
                new_quote = new_quote + arg + '，'
            f.write('\n' + new_quote[:-1])
            f.close()

            send_text(update, context, '語錄已更新')
