
import os
import qrcode
from telegram.ext import ConversationHandler
from telegram import ChatAction

class QrCoder:

    __INPUT_QR_CODE = 0

    def __init__(self) -> None:
        pass

    
    def getInputQrCodeState(self):

        return self.__INPUT_QR_CODE
        

    def qrCommandHandler(self, update, context):

        update.message.reply_text("Envia el texto para generar un codigo QR")
        return self.__INPUT_QR_CODE


    def input_text(self,update, context):

        text = update.message.text
        filename = self.generate_qr(text)
        chat = update.message.chat
        self.send_qr(filename, chat)
        os.unlink(filename)
        return ConversationHandler.END


    def generate_qr(self, text):

        filename = text + ".jpg"
        img = qrcode.make(text)
        img.save(filename)
        return filename


    def send_qr(self, filename, chat):

        chat.send_action(
            action = ChatAction.UPLOAD_PHOTO, timeout = None
        )
        chat.send_photo(
            photo = open(filename, 'rb')
        )