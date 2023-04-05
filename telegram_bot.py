# import asyncio
# import telegram
from decouple import config


# async def main():
#     bot = telegram.Bot(config("TELEGRAM_TOKEN"))
#     while True:
#         async with bot:
#             print((await bot.get_updates())[-1]["message"]["text"])


# if __name__ == '__main__':
#     asyncio.run(main())
    
    
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from OpenAIClient import OpenAIClient

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a OpenAI bot, please talk to me!")
    
# async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="You opened new chat window!")
    
# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(update.message.text)
#     print(update.message.from_user.id)
#     # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# if __name__ == '__main__':
#     application = ApplicationBuilder().token(config("TELEGRAM_TOKEN")).build()
    
#     start_handler = CommandHandler('start', start)
#     clear_handler = CommandHandler('clear', clear)
#     echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
#     application.add_handler(start_handler)
#     application.add_handler(clear_handler)
#     application.add_handler(echo_handler)
#     application.run_polling()

class TelegramBot:
    def __init__(self) -> None:
        self.op_ai_cl = OpenAIClient()
        
        application = ApplicationBuilder().token(config("TELEGRAM_TOKEN")).build()
        
        start_handler = CommandHandler('start', self.start)
        clear_handler = CommandHandler('clear', self.clear)
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), self.echo)
        
        application.add_handler(start_handler)
        application.add_handler(clear_handler)
        application.add_handler(echo_handler)
        
        application.run_polling()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a OpenAI bot, please talk to me!")
        
    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You opened new chat window!")
    
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update.message.text)
        print(update.message.from_user.id)
        print(self.op_ai_cl.completion)
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        
if __name__ == '__main__':
    tb = TelegramBot()