from service.nodes.justmessage import justmessage 
from service.nodes.chain import chain 
from telegram.ext import ContextTypes
from service.nodes.get_current_node import get_current_node
from telegram import  Update

async def manager(name: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
    print('manager', name)
    match name:
        case 'JustMessage':
            await justmessage(update, context) 
        case 'TheChain':
            await chain(update, context) 
    