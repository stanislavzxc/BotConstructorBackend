from telegram.ext import ContextTypes
from telegram import  Update
from service.nodes.manager import manager
from service.answers.any import any_answer
from service.answers.custom import custom
from service.answers.skip import skip
from service.answers.manager import answermanager
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['count'] = 0
    custom_data = context.bot_data.get('custom_data', {})
    nodes = custom_data.get('data', [])
    start = nodes[0]['targetNode']['name'] 
    answer = nodes[1]['text'] 
    if 'number' not in context.user_data:
        context.user_data['number'] = ''
    if 'email' not in context.user_data:
        context.user_data['email'] = update.message.from_user.username or 'noemail'
    if 'button_text' not in context.user_data:
        context.user_data['button_text'] = ''
    if 'first_name' not in context.user_data:
        context.user_data['first_name'] = update.message.from_user.first_name or 'noname' 
    if 'last_name' not in context.user_data:
        context.user_data['last_name'] = update.message.from_user.last_name or 'nolastname'
    await manager(start, update, context)
    context.user_data['count'] += 1
    await answermanager(answer,update,context)