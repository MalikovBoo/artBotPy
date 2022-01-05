import art_db
import vk_connect
import phraseDistance

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests


db_name = "art_db.sqlite"
playing_painting = False
playing_artists = False

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=vk_connect.token)
# Подключение для бесед
longpoll = VkBotLongPoll(vk_session, vk_connect.club_id)
session_api = vk_session.get_api()

# Кнопочки
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('1', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('2', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('3', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('4', color=VkKeyboardColor.POSITIVE)
# keyboard.add_line()


def write_game_msg(chat_id, paintings):
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
        key=vk_connect.key,
        server=vk_connect.server,
        ts=vk_connect.ts,
        attachment=d,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )


def write_game_artist_msg(chat_id, paintings):
    a = session_api.photos.getMessagesUploadServer()
    b = requests.post(a['upload_url'], files={'photo': open(paintings['pict'], 'rb')}).json()
    c = session_api.photos.saveMessagesPhoto(photo=b['photo'], server=b['server'], hash=b['hash'])[0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])

    message = 'Кто автор картины: \n'\
              '1. ' + paintings['name1'] + '\n' \
              '2. ' + paintings['name2'] + '\n' \
              '3. ' + paintings['name3'] + '\n' \
              '4. ' + paintings['name4'] + '\n'

    session_api.messages.send(
        keyboard=keyboard.get_keyboard(),
        key=vk_connect.key,
        server=vk_connect.server,
        ts=vk_connect.ts,
        attachment=d,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )


def write_answ_msg(chat_id, paintings, user_answer):
    if int(user_answer) == paintings['corr_answ']:
        message = 'Это верный ответ!'
        session_api.messages.send(
            key=vk_connect.key,
            server=vk_connect.server,
            ts=vk_connect.ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return False
    else:
        message = 'Нет, ещё попытка:'
        session_api.messages.send(
            keyboard=keyboard.get_keyboard(),
            key=vk_connect.key,
            server=vk_connect.server,
            ts=vk_connect.ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return True


def write_answ_artist_msg(chat_id, paintings, user_answer):
    if int(user_answer) == paintings['corr_answ']:
        message = 'Это верный ответ! \nКартина: '+paintings['painting_name']
        session_api.messages.send(
            key=vk_connect.key,
            server=vk_connect.server,
            ts=vk_connect.ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return False
    else:
        message = 'Нет, ещё попытка:'
        session_api.messages.send(
            keyboard=keyboard.get_keyboard(),
            key=vk_connect.key,
            server=vk_connect.server,
            ts=vk_connect.ts,
            random_id=get_random_id(),
            message=message,
            chat_id=chat_id
        )
        return True


def write_stop_msg(chat_id):
    message = 'Останавливаем игру'
    session_api.messages.send(
        key=vk_connect.key,
        server=vk_connect.server,
        ts=vk_connect.ts,
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )
    return False


if __name__ == '__main__':
    connection = art_db.create_connection(db_name)
    # art_db.create_tables(connection)
    # art_db.insert_into_tables(connection)
    artists_dict = art_db.select_artists(connection)
    paintings_dict = art_db.select_paintings(connection)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.from_chat:
                        if (not playing_painting) and (not playing_artists)\
                                and (phraseDistance.ph_distance('Угадай картину', event.object.message['text']) < 4
                                     or phraseDistance.ph_distance('Ещё картину', event.object.message['text']) < 4):
                            playing_painting = True
                            paintings_dict = art_db.select_paintings(connection)
                            write_game_msg(event.chat_id, paintings_dict)
                        elif playing_painting and \
                                ('1' in str(event) or '2' in str(event) or '3' in str(event) or '4' in str(event)):
                            playing_painting = write_answ_msg(event.chat_id, paintings_dict, event.object.message['text'][-1])
                        elif playing_painting and 'Хватит':
                            playing_painting = write_stop_msg(event.chat_id)

                        elif (not playing_painting) and (not playing_artists) \
                                and (phraseDistance.ph_distance('Угадай автора', event.object.message['text']) < 4
                                     or phraseDistance.ph_distance('Ещё автора', event.object.message['text']) < 4):
                            playing_artists = True
                            artists_dict = art_db.select_artists(connection)
                            write_game_artist_msg(event.chat_id, artists_dict)
                        elif playing_artists and \
                                ('1' in str(event) or '2' in str(event) or '3' in str(event) or '4' in str(event)):
                            playing_artists = write_answ_artist_msg(event.chat_id, artists_dict, event.object.message['text'][-1])
                        elif playing_artists and 'Хватит':
                            playing_artists = write_stop_msg(event.chat_id)
        except Exception:
            continue
