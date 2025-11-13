from telegram import Update
from telegram.ext import ContextTypes
from service.nodes.get_current_node import get_current_node
from service.replace_placeholders import replace_placeholders

async def justmessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    node = await get_current_node(context=context)
    text = await replace_placeholders(node['targetNode']['txt'], context=context)
    await update.message.reply_text(text)