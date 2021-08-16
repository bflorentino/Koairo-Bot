import os, cv2
from telegram.ext import ConversationHandler
from telegram import ChatAction

class QrDecoder:

    __QR_IMAGE = 1

    def __init__(self) -> None:
        pass


    def getQRImage(self):

        return self.__QR_IMAGE 


    def qrDecodeCommandHandler(self, update, context):

        update.message.reply_text("Envia una imagen con codigo qr")
        return self.__QR_IMAGE


    def input_img(self, update, context):

        photo = update.message.photo[0].file_id
        obj = context.bot.get_file(photo)
        pr = obj.download("image.jpg")
        text = self.decodeQrImage(pr)
        self.__sendTextFromQr(update.message.chat, text, pr)
        return ConversationHandler.END


    def __sendTextFromQr(self, chat, textS, filename):

        chat.send_action(action = ChatAction.TYPING)
        chat.send_message(text = textS)
        os.unlink(filename)


    def decodeQrImage(self, photo):

        detector = cv2.QRCodeDetector()
        reveal, point, s_qr = detector.detectAndDecode(cv2.imread(photo))
        return reveal