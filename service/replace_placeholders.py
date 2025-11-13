from telegram.ext import ContextTypes
async def replace_placeholders(next_text: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    number = context.user_data['number']
    email = context.user_data['email']
    first_name = context.user_data['first_name']
    last_name = context.user_data['last_name']
    if '{{ first name }}' in next_text:
        next_text = next_text.replace('{{ first name }}', first_name)

    if '{{ last name }}' in next_text:
        next_text = next_text.replace('{{ last name }}', last_name)

    if '{{ phone }}' in next_text:
        next_text = next_text.replace('{{ phone }}', number or 'nonumber')

    if '{{ email }}' in next_text:
        next_text = next_text.replace('{{ email }}', email or 'noemal')

    return next_text
