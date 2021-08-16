
import pyshorteners
from telegram.ext import ConversationHandler
from telegram import ChatAction

class BotShortener():
    
    __URL_SHORTENER = 2

    def __init__(self) -> None:
        pass

    def getURL_ShortenerState(self):

        return self.__URL_SHORTENER


    def inputUrl(self, update, context):

        url = update.message.text
        urlShorter = pyshorteners.Shortener()
        url = urlShorter.chilpit.short(url)
        self.sendURL(url, update.message.chat)
        return ConversationHandler.END


    def sendURL(self, url, chat):

        chat.send_action(
            action = ChatAction.UPLOAD_PHOTO, timeout = None
        )
        chat.send_message(
            text = url
        )
