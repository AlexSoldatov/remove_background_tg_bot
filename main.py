# pip install rembg[gpu]
from rembgs import remove_bg
import logging
import config


from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

TOKEN = config.TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# Включаем логирование
logging.basicConfig(level=logging.INFO)

input_imgs = './input_imgs/input.jpg'
output_imgs = './output_imgs/штзге_output.png'


# Обработка команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Приятной работы!")


@dp.message_handler(commands=['help'])
async def helpp(message: types.Message):
    await message.answer(
        text='''
        Это бот был создан для упрощения вырезания фона на фотографии.
        Для начала работы отправьте сообщение /start
        Для получения подсказки отправьте /help 

        Для работы требуется отправить в сообщении фотографию с расширением 
        .jpg результат будет возвращен в обратном сообщении в формате .png.
        Бот не подразумевает пакетной обработки файлов. 
        Обработка происходит сторого последовательно. 
        В случае пакетной загрузки будет обработано последнее фото.
        Размер изображения НЕ должен превышать 20Мб.
        '''
    )





@dp.message_handler(content_types=["photo"])
async def download_photo(message: types.Message):
    # Принимаем месседж с фото и сохраняем в tuday_pictures_path
    await message.photo[-1].download(destination_file=input_imgs)

    # Отправляем подтверждение приема
    await message.reply("Фото загружено!")

    # Удалаяем фон
    remove_bg()

    # Отправляем обработанную картинку
    photo = open(output_imgs, 'rb')
    await bot.send_photo(
        message.chat.id, photo, caption='Сделано!',
        reply_to_message_id=message.message_id)


if __name__ == "__main__":
    executor.start_polling(dp)
