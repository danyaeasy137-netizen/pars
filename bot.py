from telethon import TelegramClient, events, Button
import re

api_id = 32114809
api_hash = '58ae4f5d5c10baad5739ce52cecba0c0'
client = TelegramClient('user_session', api_id, api_hash)

CHAT_ID = -1004488149566 

@client.on(events.NewMessage(chats='tg_gifts_updates'))
async def handler(event):
    text = event.raw_text
    lines = text.split('\n')
    if len(lines) < 3: return

    try:
        # Парсинг названия (убираем номер после тире)
        raw_name = lines[0].replace('🎁 ', '').split('#')[0].strip()
        gift_model = raw_name.split('-')[0]
        
        # Поиск цены в GRAM (ищет число перед словом GRAM)
        gram_match = re.search(r'([\d\.]+)\s?GRAM', text)
        gram_price = float(gram_match.group(1)) if gram_match else 0.0
        
        # Определяем тему (топик): 2 для >15, 3 для <15
        topic_id = 2 if gram_price >= 15 else 3
        category = "Больше 15" if gram_price >= 15 else "Меньше 15"
        
        # Парсинг параметров
        params = lines[2].split(' · ')
        model_val = params[0] if len(params) > 0 else 'нет'
        uzor_val = params[1] if len(params) > 1 else 'нет'
        fond_val = params[2] if len(params) > 2 else 'нет'
        
        owner_match = re.search(r'👤 (@\w+)', text)
        owner = owner_match.group(1) if owner_match else 'нет'
        
        nft_link = f"https://t.me/nft/{raw_name}"

        # Формируем сообщение по шаблону
        msg = (
            "Лоу-Гифт\n\n"
            f"Ссылка: {nft_link}\n"
            f"Модель: {model_val}\n"
            f"Узор : {uzor_val}\n"
            f"Фон: {fond_val}\n"
            f"Цена: {gram_price} GRAM\n"
            f"Владелец: {owner}\n\n"
            f"Категория: {category}"
        )
        
        await client.send_message(
            CHAT_ID, 
            msg, 
            reply_to=topic_id,
            buttons=[[Button.inline("Занять", data=b"claim")]]
        )
        print(f"Отправлено в тему {topic_id}: {raw_name} ({gram_price} GRAM)")
        
    except Exception as e:
        print(f"Ошибка: {e}")

print('Юзербот запущен...')
client.start()
client.run_until_disconnected()
