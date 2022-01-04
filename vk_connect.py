import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests
# from vk_api.longpoll import VkLongPoll, VkEventType


# Данные для авторизации
token = "cc6ae870b49ac9dc6baaeef148e81b3c74cfaf1bb5d3ff05ddad066ebf97032d88ed752092e173146639f"
key = '9a95b34aa82de205be2ef30f902c67d5a4b89f97'
server = 'https://lp.vk.com/wh209916870'
ts = '18'
club_id = 209916870
# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

# Для бесед
longpoll = VkBotLongPoll(vk_session, club_id)
session_api = vk_session.get_api()

""" Для ЛС
Ls_longpoll = VkLongPoll(vk_session)
Ls_session_api = vk_session.get_api()
"""

# Кнопочки
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()


def write_msg_user(user_id, random_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        "random_id": random_id, 'message': message})


def write_msg_chat(chat_id, message):
    session_api.messages.send(
        # keyboard=keyboard.get_keyboard(),
        key=key,
        server=server,
        ts=ts,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )


def vkbot_start(message: dict):
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if 'Ку' in str(event):
                        if event.from_chat:
                            write_msg_chat(event.chat_id, message)
        except requests.exceptions.ReadTimeout as timeout:
            continue
