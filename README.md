## HOW TO RUN LOCALLY

1. Create `.env`
2. Add `TOKEN=<<YOUR_BOT_TOKEN>>` to `.env`
3.  `python3 src/main.py`

## HEROKU

1. Bot is now deployed in Heroku App: `hkmk-telegram-bot`
2. Instead of polling, webhook is used in the deployed version:
```
TOKEN = config('TOKEN')
PORT = int(os.environ.get('PORT', 5000))

updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
updater.bot.setWebhook('https://hkmk-telegram-bot.herokuapp.com/' + TOKEN)

updater.idle()
```
