import csv

class SaveFavorites:

    def __init__(self):
        self.favorite = []
        with open("favorite.csv") as file:
            temp = list(csv.reader(file))
            for page in temp:
                self.favorite.append(page)

    def updateFavorites(self):
        with open("favorite.csv") as file:
            temp = csv.reader(file, delimiter = ',')
            for page in temp:
                self.favorite.append(page)

    def addNewFavorite(self, url):
        if url in self.favorite:
            pass
        elif url == "":
            pass
        else:
            self.favorite .append(url)
            favFile = open("favorite.csv",'a')
            writer = csv.writer(favFile, delimiter = ',')
            writer.writerows([url.split(',')])
            favFile.close()
            
    def removeFavorite(self, url):
        if url not in self.favorite:
            pass
        else:
            self.favorite.remove(url)
            with open("favorite.csv", "w") as favFile:
                for webpage in self.favorite:
                    self.addNewFavorite(webpage)

    def printFavorites(self):
        #print("\n-----FAVORITE-----\n")
        tbr = []
        for page in range(len(self.favorite)):
            tbr.append(('<a href="' + "".join(self.favorite[page]) + '">' + "".join(self.favorite[page]) + '<\a>'))
        return tbr

        
