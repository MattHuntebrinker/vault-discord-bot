

class bot():
    def __init__(self):
        self.videoList = []

    def addVideo(self, url):
        #add valid url check
        self.videoList.append(url)
        print(self.videoList)