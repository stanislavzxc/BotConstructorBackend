async def get_current_node(context, default=None):
    nodes = context.bot_data.get('custom_data', {}).get('data', [])
    count = context.user_data.get('count', 0)
    return nodes[count] if count < len(nodes) else default