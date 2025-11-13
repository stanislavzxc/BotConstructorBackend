import logging
import io
import filetype

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
async def handle_blockname(update, context, chain: list, next_blockname: str, condition: str, channels: list, next_text: str, gmail_head: str, gmail_name: str, contact: str) -> None:
    global button_text
    if next_blockname == 'TheChain':
        print('chain!')
        for i in chain:
            if isinstance(i, str) and i.isprintable():  # Check if i is a string and contains only printable characters
                print(i)
                if button_text == '':
                    await update.message.reply_text(i)  # Send as a text message
                else:
                    await update.reply_text(i)  # Send as a text message
            else:
                if isinstance(i, str):  # If i is a string but contains non-printable characters, encode it as bytes
                    i_bytes = i.encode('latin-1')
                else:
                    i_bytes = i  # If i is already bytes, use it as is
                
                bio = io.BytesIO()
                bio.write(i_bytes)
                bio.seek(0)
                
                # Determine file type using filetype
                file_type = filetype.guess(bio)
                logger.info(f"File type: {file_type.mime}")
                # Check file type
                if file_type.mime.startswith('image/'):
                    if button_text == '':
                        await update.message.reply_photo(bio)  # Send as a text message
                    else:
                        await update.reply_photo(bio)
                    
                elif file_type.mime.startswith('video/'):
                    if button_text == '':
                        await update.message.reply_video(bio)  # Send as a text message
                    else:
                        await update.reply_video(bio)
                elif file_type.mime.startswith('audio/'):
                    if button_text == '':
                        await update.message.reply_audio(bio)  # Send as a text message
                    else:
                        await update.reply_audio(bio)
                else:
                    if button_text == '':
                        await update.message.reply_document(bio)  # Send as a text message
                    else:
                        await update.reply_document(bio)  # Send as a text message
    elif next_blockname == "TheCondition":
        # Move the condition handling logic here
        if condition == 'Контакт подписан на Телеграм канал/группу':
            chat_id = update.effective_chat.id
            for channel in channels:
                try:
                    member = context.bot.get_chat_member(channel, chat_id)
                    if member.status != 'left':
                        # User is subscribed to the channel
                        pass
                    else:
                        # User is not subscribed to the channel
                        await update.message.reply_text(f"Вы не подписаны на канал {channel}")
                        count -= 1
                        break
                except Exception as e:
                    logger.error(f"Error checking subscription: {e}")
            else:
                # User is subscribed to all channels
                await update.message.reply_text(next_text)
    elif next_blockname == "TheEmailSend":
        print(gmail_head, gmail_name, next_text)
    elif next_blockname == "TheNot":
        await context.bot.send_message(chat_id=contact, text=next_text)
        count+=1
        # await context.bot.send_message(chat_id=chat.id, text=next_text)
    else:
        # Handle other block types or default behavior
        pass
