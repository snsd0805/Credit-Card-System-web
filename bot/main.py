from urllib import response
from cairo import Filter
from telegram import Update
import torch
from telegram.ext import Application, MessageHandler, CallbackContext, CommandHandler, filters

TOKEN = ""

class BankBot():
    def __init__(self):
        self.application = Application.builder().token(TOKEN).build()
        self.application.add_handler(MessageHandler(filters.ALL, self.response))
        self.application.add_handler(CommandHandler('shop', self.addShop))

    def start_polling(self):
        print("start...")
        self.application.run_polling()
        
    async def response(self, update, context):
        q = update.message.text
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=q
        )

    async def addShop(self, update, context):
        args = context.args
        if len(args) != 1:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="usage: /shop [YOUR_ADDRESS]"    
            )
        else:
            address = args[0]
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=address    
            )

if __name__ == '__main__':

    bot = BankBot()
    bot.start_polling()