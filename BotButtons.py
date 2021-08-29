from telegram.ext import Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BotButtons():

    def __init__(self) -> None:
        pass

    def showButtons(self, update, context):

        update.message.reply_text(
            
            text = '''Presiona el botón de acorde a lo que necesitas
            
            ''',

            reply_markup = InlineKeyboardMarkup([

            [InlineKeyboardButton (text = "Codigo QR", callback_data = "qr")],
            [InlineKeyboardButton(text = "Acortar URL", callback_data="url")],
            [InlineKeyboardButton(text = "Descargar video de youtube en MP3", callback_data="mp3")],
            [InlineKeyboardButton(text = "Conversion de documentos", callback_data = "pdf-docx")]
            ])
        )