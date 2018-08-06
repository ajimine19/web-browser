"""
    HTMLTokenizer

    This class is responsible for converting raw HTML into a sequence of tokens.
"""

#from TokenizerStateMachine import TokenizerStateMachine
from CSSParserStateMachine import CSSParserStateMachine
from StartTagToken import StartTagToken
from EndTagToken import EndTagToken
from CharacterToken import CharacterToken
from TokenHandler import TokenHandler

class HTMLTokenizer:

    """
        All States:
        Data State -> Default state to start in and return to upon completing operations.
        Tag Open State -> State entered upon reading '<'
        End Tag Open State -> State entered when in the Tag Open state and upon reading '/'
        Tag Name State -> State for reading the tag name
        Before Attribute Name State
        Attribute Name State
        After Attribute Name State
        Before Attribute Value State
        Attribute Value (double quoted) State
        Attribute Value (single quoted) State
        Self-Closing Start Tag State

    """

    def __init__(self):
        self.rootUrl = ""
        self.strList = []
        self.tokens = []
        self.renderList = []
        self.renderObjects = []
        self.CSSRuleSetDictionary = None
        self.CSSParser = CSSParserStateMachine()

    def getRenderList(self):
        return self.renderList

    """
        States take in characters and do the following:
        1. Increase the iterator (consume the character)
        2. Output a token or continue operation
    """
    def parseHTML(self, htmlString):
        """
            parseHTML converts the raw htmlString into a list of tokens.
        """
        tsm = TokenizerStateMachine()
        tokenHandler = TokenHandler()
        tokenHandler.rootUrl = self.rootUrl
        i = 0
        while (i < len(htmlString)):
            i = i + tsm.handleCharacter(htmlString[i])
            if (not(tsm.currentEmittedToken == None)):
                if (isinstance(tsm.currentEmittedToken, StartTagToken) and tsm.currentEmittedToken.name == "link"):
                    self.handleLinkToken(tsm.currentEmittedToken)
                else:
                    tokenHandler.processToken(tsm.currentEmittedToken)
                tsm.currentEmittedToken = None

        #self.extractParagraphText(tsm.tokens)
        self.strList.clear()
        self.renderList.clear()
        self.renderObjects.clear()
        #tokenHandler.getRenderList(tokenHandler.elementTreeRoot, self.renderObjects)
        #for r in self.renderObjects:
        #    print(r.text)
        #    if (not(r.fontSize == None)):
        #        print(r.fontSize)
        #print(tokenHandler.elementTreeRoot.getElementRepresentationString(""))
        #tokenHandler.getTextElements(tokenHandler.elementTreeRoot, self.strList)
        self.fillRenderList(tokenHandler.elementTreeRoot, self.renderList)
        for s in self.renderList:
            print(s)

    def handleLinkToken(self, linkToken):
        if (len(self.rootUrl) == 0):
            return
        isCSSLink = False
        CSSUrlSource = ""
        for attribute in linkToken.attributesList:
            if (attribute.name == "rel" and attribute.value == "stylesheet"):
                isCSSLink = True
            elif (isCSSLink and attribute.name == "href"):
                CSSUrlSource = attribute.value
                break

        if (CSSUrlSource == ""):
            return

        if (CSSUrlSource[0] == '/'):
            CSSUrlSource = self.rootUrl + CSSUrlSource
        else:
            CSSUrlSource = self.rootUrl + "/" + CSSUrlSource

        self.parseCSS(CSSUrlSource)

    def parseCSS(self, CSSUrlSource):
        sourceCSS = ""
        try:
            sourceCSS = getHTTPS.getHTML(CSSUrlSource).decode(encoding = 'UTF-8', errors = 'strict')
        except:
            print("Could not get CSS")
            return

        i = 0
        while (i < len(sourceCSS)):
            self.CSSParser.handleCharacter(sourceCSS[i])
            i += 1

    def fillRenderList(self, treeElement, renderList):
        if (treeElement.name == "#text"):
            renderList.append(treeElement.value)
        elif (treeElement.name == "a"):
            urlString = ""
            for attribute in treeElement.attributes:
                if (attribute.name == "href"):
                    urlString = attribute.value
                    break
            renderString = '<a href="' + urlString + '">'
            temp = []
            self.getLinkText(temp, treeElement)
            renderString += "".join(temp)
            renderString += '</a>'
            renderList.append(renderString)
            return

        if (len(treeElement.children) == 0):
            return
        else:
            for element in treeElement.children:
                self.fillRenderList(element, renderList)

    def getLinkText(self, currentString, treeElement):
        if (treeElement.name == "#text"):
            currentString.append(treeElement.value)

        if (len(treeElement.children) == 0):
            return
        else:
            for element in treeElement.children:
                self.getLinkText(currentString, element)

    def extractParagraphText(self, tokenList):
        self.strList.clear()
        tempStr = ""
        getText = False
        for token in tokenList:
            if (getText):
                if (isinstance(token, CharacterToken)):
                    tempStr += token.character
                else:
                    getText = False
                    self.strList.append(tempStr)
                    tempStr = ""
            if (isinstance(token, StartTagToken) and token.name == "p"):
                getText = True
        for s in self.strList:
            print(s)

    def printDebugString(self, tokens):
        s = ""
        for token in tokens:
            if (isinstance(token, StartTagToken) or isinstance(token, EndTagToken)):
                print(token.__repr__())
            else:
                s += token.__repr__()

        print(s)

    def readFile(self):
        filename = "sample_html2.txt"
        f = open(filename, encoding='utf-8')
        inputText = f.read()
        f.close()

        self.parseHTML(inputText)

if __name__ == "__main__":
    filename = "../file.txt"
    f = open(filename, encoding='utf-8')
    inputText = f.read()
    f.close()
    #inputText = "<body><a>1</a>2</body>"
    #inputText = "<html><script><o1><o1></o1></script></o1><p></p></html>"

    t = HTMLTokenizer()
    t.parseHTML(inputText)
    for s in t.renderList:
        print(s)
