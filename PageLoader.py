"""
    PageLoader

    This class is responsible for creating the list of widgets to render to
    the browser screen from that page's source html.
"""

import getHTTPS
import RenderObject
from urllib.parse import urlparse
from HTMLTokenizerStateMachine import HTMLTokenizerStateMachine
from CSSParserStateMachine import CSSParserStateMachine
from TokenHandler import TokenHandler
from StartTagToken import StartTagToken
from EndTagToken import EndTagToken
from TagAttribute import TagAttribute
#from NavigationHistory import NavigationHistory

class PageLoader:

    def __init__(self):
        self.mySourceCode = ""

    def loadWebpage(self, url):
        requestResult = getHTTPS.tryGetHTMLSource(url)
        if (requestResult.requestSuccessful == False):
            return None
        self.mySourceCode = requestResult.HTMLSource
        HTMLTokenList = self.convertHTMLSourceToTokenList(requestResult.HTMLSource)
        HTMLElementTreeRoot = self.convertTokenListToHTMLElementTree(url, HTMLTokenList)
        return self.convertElementTreeToRenderObjectList(HTMLElementTreeRoot)

    def convertHTMLSourceToTokenList(self, HTMLSource):
        tsm = HTMLTokenizerStateMachine()
        i = 0
        while (i < len(HTMLSource)):
            i = i + tsm.handleCharacter(HTMLSource[i])
        return tsm.getTokenList()

    def convertTokenListToHTMLElementTree(self, url, tokenList):
        # The root url is needed by the TokenHandler for handling
        # possible relative links
        rootUrl = self.extractRootUrl(url)
        print(rootUrl)
        tokenHandler = TokenHandler(rootUrl)
        for token in tokenList:
            tokenHandler.processToken(token)

        #print(tokenHandler.elementTreeRoot.getElementRepresentationString(""))
        return tokenHandler.elementTreeRoot

    def convertElementTreeToRenderObjectList(self, elementTreeRoot):
        renderObjectList = []
        elementTreeRoot.fillRenderObjectList(renderObjectList)
        return renderObjectList

    def extractRootUrl(self, url):
        parseResult = urlparse(url)
        rootUrl = parseResult.scheme + "://" + parseResult.netloc + parseResult.path + "/"
        return rootUrl

if __name__ == "__main__":
    file = open("sample_html.txt")
    sourceHTML = file.read()
    file.close()

    pl = PageLoader()
    tokens = pl.convertHTMLSourceToTokenList(sourceHTML)
    treeRoot = pl.convertTokenListToHTMLElementTree(tokens)
    print(treeRoot.getElementRepresentationString(""))
