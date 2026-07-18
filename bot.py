from telethon import TelegramClient, events, Button
import re

api_id = 32114809
api_hash = '58ae4f5d5c10baad5739ce52cecba0c0'
client = TelegramClient('user_session', api_id, api_hash)

# ID твоего основного чата (получаем из ссылок: 4488149566)
CHAT_ID = -1004488149566 

@client.on(events.NewMessage(chats='tg_gifts_updates'))
async def handler(event):
    text = event.raw_text
    lines = text.split('\n')
    if len(lines) < 3: return

    try:
        # Парсинг данных
        gift_name = lines[0].replace('🎁 ', '').split('#')[0].strip()
        params = lines[2].split(' · ')
        
        # Поиск цены в TON (даже если написано Stars, ты сказал, что лог пишет и в TON)
        ton_match = re.search(r'([\d\.]+) TON', text)
        ton_price = float(ton_match.group(1)) if ton_match else 0.0
        
        # Определяем тему (топик)
        # Если цена >= 15 -> топик 45, иначе -> топик 47
        topic_id = 2 if ton_price >= 15 else 2
        
        # Парсинг параметров
        model_val = params[0] if len(params) > 0 else 'нет'
        fond_val = params[1] if len(params) > 1 else 'нет'
        uzor_val = params[2] if len(params) > 2 else 'нет'
        
        owner_match = re.search(r'👤 (.*?)(?: ·|$)', text)
        owner = owner_match.group(1).strip() if owner_match else 'нет'
        
        nft_link = f"https://t.me/nft/{gift_name}"

        msg = f"🎁 **Лоу-Гифт**\n\n🔗 {nft_link}\n🤖 {model_val}\n✨ {uzor_val}\n🎨 {fond_val}\n💎 Цена: {ton_price} TON\n👤 Владелец: {owner}"
        
        # Отправка в нужную тему (forum_topic_id)
        await client.send_message(
            CHAT_ID, 
            msg, 
            reply_to=topic_id,
            buttons=[[Button.inline("Занять", data=b"claim")]],
            parse_mode='md'
        )
        print(f"Отправлено в тему {topic_id}: {gift_name} ({ton_price} TON)")
        
    except Exception as e:
        print(f"Ошибка: {e}")

print('Юзербот запущен и распределяет по темам...')
client.start()
client.run_until_disconnected()
