from telegram import Update
from telegram.ext import ContextTypes
from service.nodes.get_current_node import get_current_node
from service.nodes.manager import manager

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    custom_data = context.bot_data.get('custom_data', {})
    nodes = custom_data.get('data', [])
    count = context.user_data.get('count', 0) 
    node = None

    while count < len(nodes) and nodes[count]['text'] == 'skip':
        node = await get_current_node(context)
        await manager(node['targetNode']['name'], update, context)
        context.user_data['count'] += 1
        count = context.user_data['count']
