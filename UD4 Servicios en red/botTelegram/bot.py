import logging
import sys
from asyncore import dispatcher

from telegram import Update, Animation
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
token = os.environ['BOT_TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def calculadoraEsPrimo(numero):
    if numero < 2:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='# Bienvenido al Bot de Ivan\n'
                                                                          '# Comandos:\n'
                                                                          '/saludar\n'
                                                                          '/help\n'
                                                                          '/roll\n'
                                                                          '/reverse\n'
                                                                          '/esPrimo\n'
                                                                          '/significado\n'
                                                                          '# Mensajes:\n'
                                                                          'Hola\n'
                                                                          'Fiesta')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='# Bienvenido al Bot de Ivan\n'
                                                                          '# Comandos:\n'
                                                                          '/start\n'
                                                                          '/saludar\n'
                                                                          '/help\n'
                                                                          '/roll <xdy> (x - Numero de tiradas | y - Numero de caras)\n'
                                                                          '/reverse <Palabra> (Revertir palabra)\n'
                                                                          '/esPrimo <Numero> (Saber si numero es primo)\n'
                                                                          '/significado <Palabra> (Buscar el significado de una palabra)'
                                                                          '# Mensajes:\n'
                                                                          'Hola\n'
                                                                          'Fiesta')
    
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) != 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Debes escribir un agumento - /roll <xdy> (x - Numero de tiradas | y - Numero de caras)')
    else:
        if args[0][1] != "d":
            await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Argumento incorrecto xdy (x - Numero de tiradas | y - Numero de caras)')
        else:
            tiradas = args[0].split("d")[0]
            caras = args[0].split("d")[1]

            try:
                for i in range(1, int(tiradas)+1):
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='Ronda: ' + str(i) + " - Resultado: " + str(random.randint(1, int(caras))))
                    print('Ronda: ' + str(i) + " - Resultado: " + str(random.randint(1, int(caras))))
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Argumento incorrecto xdy (x - Numero de tiradas | y - Numero de caras)')


async def reverse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Debes de escribir una palabra para revertir - /reverse <Palabra>')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=args[0][::-1])

async def esPrimo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Debes de escribir un numero como parametro para decir si es primo - /esPrimo <Numero>')
    else:
        try:
            if(calculadoraEsPrimo(int(args[0]))):
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Es primo')
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='No es primo')
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='ERROR - Debes de escribir un numero como parametro para decir si es primo - /esPrimo <Numero>')

async def saludar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user

    mensaje = (
        f"Hola {user.first_name}! 👋\n"
        f"¡Gracias por usarme! Soy onlyBot de Telegram.\n"
        f"Tu ID de usuario es: {user.id}"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)


async def obtener_significado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    palabra = ' '.join(context.args)

    if not palabra:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona una palabra para obtener su significado.")
        return

    url = f'https://www.wordreference.com/definicion/{palabra}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        significado_element = soup.find('div', {'id': 'article'})

        if significado_element:
            significado = significado_element.get_text().strip()

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Significado de '{palabra}':\n{significado}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"No se encontró significado para la palabra: {palabra}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error al obtener el significado. Por favor, inténtalo de nuevo más tarde.")

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensaje_recibido = update.message.text

    if mensaje_recibido.lower() == "hola":
        mensaje_respuesta = "¡Hola! ¿Cómo estás?"

        await context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje_respuesta)
    elif mensaje_recibido.lower() == "fiesta":
        gif_path = "fiesta.gif"

        await context.bot.send_animation(chat_id=update.effective_chat.id, animation=gif_path)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    # Registrar el comando start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Registrar el comando help
    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    # Registrar el comando roll
    roll_handler = CommandHandler('roll', roll)
    application.add_handler(roll_handler)

    # Registrar el comando reverse
    reverse_handler = CommandHandler('reverse', reverse)
    application.add_handler(reverse_handler)

    # Registrar el comando esPrimo
    esPrimo_handler = CommandHandler('esPrimo', esPrimo)
    application.add_handler(esPrimo_handler)

    # Registrar el comando saludar
    saludar_handler = CommandHandler('saludar', saludar)
    application.add_handler(saludar_handler)

    # Registrar comando significado
    significado_handler = CommandHandler('significado', obtener_significado)
    application.add_handler(significado_handler)

    # Responser a mensaje hola
    hola_handler = MessageHandler(filters.ALL, manejar_mensajes)
    application.add_handler(hola_handler)

    application.run_polling()