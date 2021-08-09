import asyncio
from telethon import TelegramClient  # , sync, events, Button
import logging
import datetime


''' Нижние 7 строчек кода - мощная штука для отлавливания ошибок '''
logger = logging.getLogger("tggt")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("app.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

''' Настраиваем работу клиента '''
api_id = 7617954
api_hash = '27173c0c42d69cab619b96526a821606'
bot_token = '1835914561:AAEgCB5LU6CkFuzK5vquPiDykxY-1_A17fw'
client = TelegramClient('anon', api_id, api_hash)

# client.get_entity('telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg')

''' Различные названия каналов '''
CHAT_GET_NAH = 'Находки AliExpress'  # ('Саня Ладовир', 'Тестинг', 'Безделушки с AliExpress', 'Находки AliExpress')
CHAT_SET_ME = 'me'
CHAT_SET_LAST_MESSAGE_X7 = 1558089642  # 'КостыльX7'
CHAT_SET_ALI_X7 = 1514212507  # 'AliExpress X7'
CHAT_SET_ALI_XER = 'Безделушки с AliExpress'
CHAT_SET_TEST = 'Тестинг'

''' Пауза между сообщениями '''
PAUSE_SUCCESS = 1633
PAUSE_FAILURE = 311

''' Время начала и конца автопостинга. Нужно для ночного поста '''
TIME_START = 7
TIME_END = 0


def change_link(text):
    text_mess = text
    edit_text = text_mess
    # edit_text = ''
    # end = len(text_mess) - text_mess[::-1].find('\n')  # last string with link
    # if end != len(text_mess) + 1:
    #     for t in range(end):
    #         edit_text = edit_text + text_mess[t]
    my_link = '\n\nХочешь ссылку на этот товар за 1 доллар ? 🔥🔥🔥\nПодпишись! Скоро будет 😉 \n'
    # my_link = '\nХочешь ссылку на товар с заманчивой ценой? 🔥🔥🔥\nПодпишись! Скоро будет 😉 \n'

    edit_text = edit_text + my_link
    return edit_text


async def main():
    while True:
        ''' Остановка постинга в ночное время'''
        now = datetime.datetime.now()
        if now.hour < TIME_START:
            break

        """ Получем инфу, какой пост уже был чекнут в группе Находок"""
        temp = await client.get_messages(CHAT_SET_LAST_MESSAGE_X7)
        last_message_id = int(temp[0].message)
        print('Прошлое сообщение: \t\t\t\t\t', last_message_id)

        """ Умменьшаем id последнего поста на 1 и отправляем в КостыльX7 """
        last_message_id = last_message_id - 1
        await client.send_message(CHAT_SET_LAST_MESSAGE_X7, str(last_message_id))

        """ Получаем сообщение из Находок """
        message = await client.get_messages(CHAT_GET_NAH, offset_id=last_message_id)
        print('Сообщение из', str(CHAT_GET_NAH) + ':\t', message)

        """ Редактируем текст сообщения"""
        start_text = 'Вы самые-самые лучшие 👆🔥🔥🔥☝️\n\n'
        end_text = '\n[❤❤❤Мы Вас Любим! ❤❤❤](https://t.me/aliexpressX70)\n\n' \
                   '[🌸Другие полезные каналы🌺](https://t.me/aliexpress_X7)'
        text = message[0].message
        print('Текст Поста:')
        print(text)
        new_text = change_link(text)  # Ищем ссылки и вставляем наши
        final_text = start_text + new_text + end_text

        ''' Отправляем сообщение в чат'''
        try:
            await client.send_file(CHAT_SET_ALI_X7, message, caption=final_text)
            # await client.send_file(CHAT_SET_ALI_XER, message, caption=final_text)
            # мб оттуда будут челы подтягиваться
            await asyncio.sleep(PAUSE_SUCCESS)
        except Exception as e:
            print('Ошибочка', message[0].id)  # message[0].id почему-то на 1 меньше
            await client.send_message(CHAT_SET_LAST_MESSAGE_X7, 'Ошибочка^ ' + str(last_message_id))
            await client.send_message(CHAT_SET_LAST_MESSAGE_X7, str(last_message_id))
            await asyncio.sleep(PAUSE_FAILURE)
            logger.error(e)

    ''' Отправка ночного поста'''
    text_night = 'Дорогие друзья, напоминаем, что это новый канал, так как прошлый забанили 😡 \n\n' \
                 'Благодарим за то, что вы отправляете посты своим друзьям, нам это очень сильно помогает 😌\n\n' \
                 'Скоро, мы начнем проводить Розыгрыши и Дарить подарки нашим подписчикам 😘❤️\n\n' \
                 'Подпишись, чтобы не пропустить 🔥😋'
    await client.send_message(CHAT_SET_ALI_X7, text_night)


with client:
    client.loop.run_until_complete(main())
