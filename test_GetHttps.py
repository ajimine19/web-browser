import getHTTPS
import urllib

def test_testActualWebsiteFirst100():
    website = "https://www.tanoshiijapanese.com/home/"
    functionCall = getHTTPS.getHTML(website)
    assert len(functionCall) > 0

def test_testEmptyString():
    website = ""
    try:
        getHTTPS.getHTML(website)
    except Exception as e:
        assert (type(e) == ValueError)

def test_testNothing():
    try:
        getHTTPS.getHTML()
    except Exception as e:
        assert(type(e) == TypeError)

def test_testFourOhFour():
    try:
        getHTTPS.getHTML("https://www.cnn.con")
    except Exception as e:
        assert(type(e) == urllib.error.URLError)
