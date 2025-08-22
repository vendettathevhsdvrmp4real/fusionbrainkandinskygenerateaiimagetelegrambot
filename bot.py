import telebot
from config import API_KEY, SECRET_KEY, API_TOKEN_TELEGRAM
from logic2 import FusionBrainAPI



API_TOKEN = API_TOKEN_TELEGRAM

bot = telebot.TeleBot(API_TOKEN_TELEGRAM)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,'Привет')


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    prompt = message.text

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)
    
    # Сохраняем первое изображение на диск
    api.save_image(files[0], "generated_image.png")


    with open('generated_image.png','rb') as photo:
        bot.send_photo(message.chat.id,photo)



bot.infinity_polling()
