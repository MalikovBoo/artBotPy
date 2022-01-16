import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import art_db
import vk_connect
import phraseDistance


# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=vk_connect.token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_connect.club_id)


db_name = "art_db.sqlite"
playing_painting = False
playing_artists = False


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
                            vk_connect.write_game_msg(session_api, event.chat_id, paintings_dict)
                        elif playing_painting and \
                                ('1' in str(event) or '2' in str(event) or '3' in str(event) or '4' in str(event)):
                            playing_painting = vk_connect.write_answ_msg(session_api, event.chat_id, paintings_dict,
                                                                         event.object.message['text'][-1])
                        elif playing_painting and 'хватит':
                            playing_painting = vk_connect.write_stop_msg(session_api, event.chat_id)

                        elif (not playing_painting) and (not playing_artists) \
                                and (phraseDistance.ph_distance('Угадай автора', event.object.message['text']) < 4
                                     or phraseDistance.ph_distance('Ещё автора', event.object.message['text']) < 4):
                            playing_artists = True
                            artists_dict = art_db.select_artists(connection)
                            vk_connect.write_game_artist_msg(session_api, event.chat_id, artists_dict)
                        elif playing_artists and \
                                ('1' in str(event) or '2' in str(event) or '3' in str(event) or '4' in str(event)):
                            playing_artists = vk_connect.write_answ_artist_msg(session_api, event.chat_id, artists_dict,
                                                                               event.object.message['text'][-1])
                        elif playing_artists and 'хватит':
                            playing_artists = vk_connect.write_stop_msg(session_api, event.chat_id)
        except Exception:
            continue
