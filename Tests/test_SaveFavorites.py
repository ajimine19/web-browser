import csv
from SaveFavorites import SaveFavorites

def test_addNewFavorite():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    functionCall = myFav.addNewFavorite("webpage4")
    assert (len(myFav.favorite) == 4)

def test_addEmpty():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    functionCall = myFav.addNewFavorite("")
    assert (len(myFav.favorite) == 3)

def test_addNull():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    try:
        functionCall = myFav.addNewFavorite()
    except Exception as e: 
        assert (type(e) == TypeError)

def test_addExistingFavorite():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    functionCall = myFav.addNewFavorite("webpage3")
    assert (len(myFav.favorite) == 3)
    
def test_removeFavorite():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    functionCall = myFav.removeFavorite("webpage1")
    assert (len(myFav.favorite) == 2)

def test_removeNonexistent():
    myFav = SaveFavorites()
    myFav.favorite = ["webpage1","webpage2","webpage3"]
    functionCall = myFav.removeFavorite("webpage4")
    assert (len(myFav.favorite) == 3)
