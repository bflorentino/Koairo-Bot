import os
import pythoncom
from telegram import ChatAction
from telegram.ext import ConversationHandler
from docx2pdf import convert
from pdf2docx import parse
from BotSongDownloader import BotSongDownloader

class BotDocConverter():

    __BOT_DOC_CONVERTER_PDF = 4
    __BOT_DOC_CONVERTER_DOCX = 5


    def __init__(self) -> None:
        pass


    def getBotDocConverterStatePdf(self):

        return self.__BOT_DOC_CONVERTER_PDF


    def getBotDocConverterStateDocx(self):

        return self.__BOT_DOC_CONVERTER_DOCX


    def pdfCommandHandler(self, update, context):

        update.message.reply_text("Envia un documento word (.docx) para convertirlo a pdf")
        return self.__BOT_DOC_CONVERTER_PDF


    def docxCommandHandler(self, update, context):

        update.message.reply_text("Envia un documento pdf (.pdf) para convertirlo a word")
        return self.__BOT_DOC_CONVERTER_DOCX


    def inputDocx(self, update, context):

        document = update.message.document

        try:

            assert(document.file_name.endswith(".docx"))
            obj = context.bot.get_file(document)
            pr = obj.download(document.file_name)
            fileToPdf = self.convertToPdf(pr)
            self.sendDocument(update.message.chat, fileToPdf)

        except AssertionError:

            BotSongDownloader.somethingBadHappened(self, "No es un documento en formato docx", update.message.chat)

        finally:

            return ConversationHandler.END


    def convertToPdf(self, filename):

        file = filename.split(".")
        file[1] = ".pdf"
        pythoncom.CoInitialize()
        convert(filename)
        os.unlink(filename)
        return "".join(file)


    def inputPdf(self, update, context):

        document = update.message.document

        try:
            
            assert(document.file_name.endswith("pdf"))
            obj = context.bot.get_file(document)
            pr = obj.download(document.file_name)
            fileToWord = self.convertToWord(pr)
            self.sendDocument(update.message.chat, fileToWord)

        except AssertionError:

            BotSongDownloader.somethingBadHappened(self, "No es un documento en formato pdf", update.message.chat)

        finally:

            return ConversationHandler.END


    def convertToWord(self, filename):

        file = filename.split(".")
        file[1] = ".docx"
        file = "".join(file)
        parse(filename, file, start = 0, end = None)
        os.unlink(filename)
        return "".join(file)


    def sendDocument(self, chat, filename):

        chat.send_action(ChatAction.TYPING, timeout = None)
        chat.send_document(document = open(filename, "rb"))
        os.unlink(filename)