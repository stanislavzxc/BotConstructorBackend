from telegram import Update
from telegram.ext import ContextTypes
from service.answers.any import any_answer
from service.answers.skip import skip
from service.answers.custom import custom 
async def answermanager(answer:str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if answer == 'skip':
        await skip(update, context)
    elif answer == 'any':
        await any_answer(update, context)
    else:
        await custom(update, context)