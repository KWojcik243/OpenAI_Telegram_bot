from decouple import config

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from open_ai_client import OpenAIClient
from db_setup import DbSetup

class TelegramBot:
    def __init__(self) -> None:
        self.op_ai_cl = OpenAIClient()
        self.db_cl = DbSetup()
        self.access = config("ACCESSED_USERS")
        
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
        self.db_cl.delete_mess(user_id = update.message.from_user.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You opened new chat window!")
    
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if str(user_id) in self.access:
            mess = update.message.text
            user_id = update.message.from_user.id
            self.db_cl.insert_mess(role="user", message=mess, user_id=user_id)
            
            records = self.db_cl.get_user_mess(user_id=user_id)
            history_mess = []
            
            for record in records:
                history_mess.append({"role":record[0], "content": record[1]})
                
            bot_message = self.op_ai_cl.completion(messages=history_mess, user_id=user_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_message)
        
if __name__ == '__main__':
    tb = TelegramBot()