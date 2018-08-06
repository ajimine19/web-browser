import datetime
import random

class simpleCache:
        def __init__(self): #constructor
            self.cache = {} #empty dictionary
            self.max_cache_size = 3 #self.getCacheSize() #set the max size of the cache
        def __contains__(self, key):
            return key in self.cache #checks the cache and returns true or false if the key is in the cache
        def sizeOfCache(self):
            return len(self.cache) #return size of cache
        def makeSpace(self):
            oldest = None
            for key in self.cache:
                if oldest is None: #if theres currently nothing set
                    oldest = key #set the oldest entry to the current key
                elif self.cache[key]['date_accessed'] < self.cache[oldest]['date_accessed']: #compare the time stamps
                    oldest = key #reassign the oldest to be the current key
            self.cache.pop(oldest) #pop the oldest entry
            return
        def updateCache(self, key, value):
            if key not in self.cache and len(self.cache) >= self.max_cache_size:
                self.makeSpace()
            self.cache[key] = {'date_accessed': datetime.datetime.now(), 'value' : value} #insert into the dictionary the key with the time and value

        def getElement(self, key):
            return self.cache[key]['value']

        def printCache(self):
            for x in self.cache:
                    print(x + " date:" + str(self.cache[x]['date_accessed']) + " value:" + str(self.cache[x]['value']))
            return

        """
        def setCacheSize(self, size):
            with open("cache.csv", "w") as file:
                file.write(str(size))
            self.max_cache_size = size
            return

        def getCacheSize(self):
            with open("cache.csv") as file:
                size = file.readlines()
            return size
        """


"""
#CODE FOR TESTING FUNCTIONALITY
myCache = simpleCache()
myCache.updateCache("google.com", "HTML FOR GOOGLE")
if myCache.__contains__("google.com") :
    print("key found\n")
else:
    print("not found\n")
myCache.updateCache("amazon.com", "HTML FOR AMAZON")
print(str(myCache.cache)+"\n")
myCache.updateCache("up.com", "HTML FOR UP")
print(str(myCache.cache)+"\n")
myCache.updateCache("apple.com", "HTML FOR APPLE")
print(str(myCache.cache)+"\n")
"""
