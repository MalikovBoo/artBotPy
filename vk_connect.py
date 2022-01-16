import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests


# Данные для авторизации
token = "cc6ae870b49ac9dc6baaeef148e81b3c74cfaf1bb5d3ff05ddad066ebf97032d88ed752092e173146639f"
key = '9a95b34aa82de205be2ef30f902c67d5a4b89f97'
server = 'https://lp.vk.com/wh209916870'
ts = '18'
club_id = 209916870


# Кнопочки
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('1', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('2', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('3', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('4', color=VkKeyboardColor.POSITIVE)
# keyboard.add_line()


def write_game_msg(session_api, chat_id, paintings):
    a = session_api.photos.getMessagesUploadServer()
    b = requests.post(a['upload_url'], files={'photo': open(paintings['pict'], 'rb')}).json()
    c = session_api.photos.saveMessagesPhoto(photo=b['photo'], server=b['server'], hash=b['hash'])[0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])

    message = 'Что за картину вы видите: \n'\
              '1. ' + paintings['name1'] + '\n' \
              '2. ' + paintings['name2'] + '\n' \
              '3. ' + paintings['name3'] + '\n' \
              '4. ' + paintings['name4'] + '\n'

    session_api.messages.send(
        keyboard=keyboard.get_keyboard(),
        key=key,
        server=server,
        ts=ts,
        attachment=d,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )


def write_game_artist_msg(session_api, chat_id, paintings):

    a = session_api.photos.getMessagesUploadServer()
    b = requests.post(a['upload_url'], files={'photo': open(paintings['pict'], 'rb')}).json()
    c = session_api.photos.saveMessagesPhoto(photo=b['photo'], server=b['server'], hash=b['hash'])[0]
    attachment = "photo{}_{}".format(c["owner_id"], c["id"])

    message = 'Кто автор картины: \n'\
              '1. ' + paintings['name1'] + '\n' \
              '2. ' + paintings['name2'] + '\n' \
              '3. ' + paintings['name3'] + '\n' \
              '4. ' + paintings['name4'] + '\n'

    session_api.messages.send(
        keyboard=keyboard.get_keyboard(),
        key=key,
        server=server,
        ts=ts,
        attachment=attachment,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )


def write_answ_msg(session_api, chat_id, paintings, user_answer):
    if int(user_answer) == paintings['corr_answ']:
        message = 'Это верный ответ!'
        session_api.messages.send(
            key=key,
            server=server,
            ts=ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return False
    else:
        message = 'Нет, ещё попытка:'
        session_api.messages.send(
            keyboard=keyboard.get_keyboard(),
            key=key,
            server=server,
            ts=ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return True


def write_answ_artist_msg(session_api, chat_id, paintings, user_answer):
    if int(user_answer) == paintings['corr_answ']:
        message = 'Это верный ответ! \nКартина: '+paintings['painting_name'] + \
                  '\nНаписана в '+paintings['pict_date'] + \
                  '\nСтрана художника: '+paintings['county'] + \
                  '\nСтиль художника: '+paintings['style']
        session_api.messages.send(
            key=key,
            server=server,
            ts=ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return False
    else:
        message = 'Нет, ещё попытка:'
        session_api.messages.send(
            keyboard=keyboard.get_keyboard(),
            key=key,
            server=server,
            ts=ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return True


def write_stop_msg(session_api, chat_id):
    message = 'Останавливаем игру'
    session_api.messages.send(
        key=key,
        server=server,
        ts=ts,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )
    return False
