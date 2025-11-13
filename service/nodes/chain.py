from telegram import Update
from telegram.ext import ContextTypes
from service.nodes.get_current_node import get_current_node
from service.replace_placeholders import replace_placeholders
import io
import filetype

async def chain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    node = await get_current_node(context=context)
    start_text = await replace_placeholders(node['targetNode']['txt'], context=context)
    await update.message.reply_text(start_text)
    for i in node['targetNode']['chain']:
        if isinstance(i, str) and i.isprintable():  
            text = await replace_placeholders(i, context=context)
            await update.message.reply_text(text)
        else:
           if isinstance(i, str):  
               i_bytes = i.encode('latin-1')
           else:
               i_bytes = i 
           
           bio = io.BytesIO()
           bio.write(i_bytes)
           bio.seek(0)
           file_type = filetype.guess(bio)
           if file_type.mime.startswith('image/'):
               await update.message.reply_photo(bio) 
           elif file_type.mime.startswith('video/'):
               await update.message.reply_video(bio) 
           elif file_type.mime.startswith('audio/'):
               await update.message.reply_audio(bio) 
           else:
               text = await replace_placeholders(i, context=context)
               await update.message.reply_text(text)
               