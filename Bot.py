
from BotSongDownloader import BotSongDownloader
from BotButtons import BotButtons
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import QrDecoder, QrCoder
from BotShortener import BotShortener
import os


def start(update, context):

    botButtons.showButtons(update, context)


def qrCallbackHandler(update, context):

    query = update.callback_query
    query.answer()
    query.edit_message_text('Usa /qr para generar un codigo QR o /decode para decodificar una imagen')


def shortenerCallbackHandler(update, context):

    query = update.callback_query
    query.answer()
    query.edit_message_text("Envia la URL que quieres acortar")
    return botShortener.getURL_ShortenerState()


def botSongDownloaderCallbackHandler(update, context):

    query = update.callback_query
    query.answer()
    query.edit_message_text("Envia la URL del video que quieres descargar")
    return botSongDownloader.getYoutubeDownloaderState()


if __name__ == "__main__":

    updater = Updater(token = os.environ["TOKEN"] , use_context=True)    
    dp = updater.dispatcher
    botButtons = BotButtons()
    qrCoder = QrCoder.QrCoder()
    qrDecoder = QrDecoder.QrDecoder()
    botShortener = BotShortener()
    botSongDownloader = BotSongDownloader()

    # Adding handlers 
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(ConversationHandler(
            
            entry_points=[
                            CallbackQueryHandler(pattern = 'qr', callback = qrCallbackHandler),
                            CallbackQueryHandler(pattern = 'url', callback = shortenerCallbackHandler),
                            CallbackQueryHandler(pattern = "mp3", callback = botSongDownloaderCallbackHandler),
                            CommandHandler('qr', qrCoder.qrCommandHandler), 
                            CommandHandler('decode', qrDecoder.qrDecodeCommandHandler)
                            ], 
            states = {
                        qrCoder.getInputQrCodeState(): [MessageHandler(Filters.text, qrCoder.input_text)],
                        qrDecoder.getQRImage():[MessageHandler(Filters.photo, qrDecoder.input_img)],
                        botShortener.getURL_ShortenerState(): [MessageHandler(Filters.text, botShortener.inputUrl)],
                        botSongDownloader.getYoutubeDownloaderState(): [MessageHandler(Filters.text, botSongDownloader.inputURL)]
                        }, 
            fallbacks=[]
            
            ))

    updater.start_polling()
    updater.idle()