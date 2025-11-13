from telegram import Update
from telegram.ext import ContextTypes
from service.nodes.get_current_node import get_current_node
from service.answers.manager import answermanager
async def OnMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # logger = 'zxc'
    count = context.user_data['count']
    # number = context.user_data['number']
    # email = context.user_data['email']
    count += 1 
    node = await get_current_node(context)
    answer = node['text']
    await answermanager(answer, update, context)