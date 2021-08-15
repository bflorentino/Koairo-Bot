
from pytube import YouTube
import os
from pytube.__main__ import YouTube
from telegram.ext import ConversationHandler
from telegram import ChatAction

class BotSongDownloader():

    __YOUTUBE_DOWNLOADER_STATE = 3

    def __init__(self) -> None:
        pass

    
    def getYoutubeDownloaderState(self):

        return self.__YOUTUBE_DOWNLOADER_STATE


    def inputURL(self, update, context):

        url = update.message.text

        if "youtube.com" in (url):
            
            yt = YouTube(url)
            video = self.downloadVideo(yt, update)

            if video is not False:
                
                audioMp3 = self.convertVideoToMp3(video, update)

                if audioMp3 is not False:

                    self.sendMP3(update.message.chat, audioMp3)
                    os.unlink(audioMp3)

            return ConversationHandler.END

        else:
            self.somethingBadHappened("No es un link de youtube", update.message.chat)
            return ConversationHandler.END


    def somethingBadHappened(self, errorMessage, chat):

        chat.send_action(
            action = ChatAction.TYPING
        )
        chat.send_message(
            text = errorMessage
        )


    def downloadVideo(self, url, update):

        try:

            stream = url.streams.filter(only_audio = True)
            video = stream.first().download()
            return video
            
        except:

            self.somethingBadHappened("Algo inesperado ocurrio al descargar el video", update.message.chat)
            return False
    

    def convertVideoToMp3(self, video, update):

        try:

            extension = video.split(".")
            extension[1] = ".mp3"
            mp3File = "".join(extension)
            os.rename(video, mp3File)
            return mp3File

        except:

            self.somethingBadHappened("Algo inesperado ocurrio al convertir el video a MP3", update.message.chat)
            return False
        

    def sendMP3(self, chat, mp3File):

        chat.send_action(
            action = ChatAction.TYPING
        )
        chat.send_audio(
            audio =  open(mp3File, "rb")
        )