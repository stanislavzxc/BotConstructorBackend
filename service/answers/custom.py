from telegram import Update
from telegram.ext import ContextTypes
async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    custom_data = context.bot_data.get('custom_data', {})
    nodes = custom_data.get('data', [])
    count = context.user_data.get('count')
    
    if count > len(nodes):
        return

    target = nodes[count]['target']
    target = int(target) - 1
    message_user = update.message.text
    for i in nodes:
        if target == int(i['source']) and i['text'] == message_user:
            await update.message.reply_text(i['targetNode']['txt'])
            count += 1
            context.user_data['count'] += 1

