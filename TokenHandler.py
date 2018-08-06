"""
    TokenHandler

    This class is responsible for processing the tokens emitted by the
    Tokenizer State Machine. The final result is a tree of HTML elements.
"""

import HTMLElement
from StartTagToken import StartTagToken
from EndTagToken import EndTagToken
from CharacterToken import CharacterToken
import getHTTPS
from CSSParserStateMachine import CSSParserStateMachine

class TokenHandler:

    def __init__(self, webpageRootUrl):
        self.rootUrl = webpageRootUrl
        self.__openElementStack = []
        self.__currentTextElement = None
        self.__noWhiteSpace = True
        #self.__currentText = None

        self.elementTreeRoot = HTMLElement.HTMLElement("#root#")
        self.__openElementStack.append(self.elementTreeRoot)

        # This dictionary is used to create specific nodes in the tree
        self.__elementDictionary = {
            "a" : self.createNewHyperlinkElementFromToken,
            "img" : self.createNewImageElementFromToken,
        }

        # normal tags
        self.validTextlessTagNames = {
            "html",
            "div",
            "span",
            "title",
        }

        # tags that shouldn't need to be closed
        self.selfClosingTags = {
            # The root element is not an html tag, it is for
            # initializing the tree structure
            "#root#",

            # Simple Independent HTML Tags:
            "br",
            "hr",
            "img",

            # ALL Independent HTML Tags
            #"area",
            #"base",
            #"br",
            #"col",
            #"command",
            #"embed",
            #"hr",
            #"img",
            #"input",
            #"keygen",
            "link",
            #"menuitem",
            #"meta",
            #"param",
            #"source",
            #"track",
            #"wbr"
        }

        # tags whose inner content can be text
        self.validTextTags = {
            "a",
            "b",
            "body",
            "center",
            "h1","h2","h3","h4","h5","h6",
            "head",
            "i",
            "p",
            "ol",
            "li",
            "ul",
        }

        # acceptedTagNames is the union of the 3 tag-related sets above
        self.acceptedTagNames = self.validTextlessTagNames.union(self.selfClosingTags)
        self.acceptedTagNames = self.acceptedTagNames.union(self.validTextTags)

    def processToken(self, token):

        if (isinstance(token, CharacterToken)):
            self.handleCharacterToken(token)
            return

        # This token isn't a character token, so the end of a
        # sequence of characters was reached if one existed, so
        # the textElement related variables should be reset
        self.__currentTextElement = None
        self.__noWhiteSpace = True

        if (isinstance(token, StartTagToken)):
            if (token.name in self.acceptedTagNames):
                self.handleStartTagToken(token)
            else:
                self.handleUnacceptedStartTag(token)
        elif (isinstance(token, EndTagToken)):
            if (token.name in self.acceptedTagNames):
                self.handleEndTagToken(token)
            else:
                self.handleUnacceptedEndTag(token)

    def handleStartTagToken(self, token):

        """
        If an accepted element is found within an unaccepted element,
        it is treated as if it is a child of the first accepted element
        in the stack. I'm not sure if this should be kept or removed:
        """

        while (not(self.__openElementStack[-1].name in self.acceptedTagNames)):
            self.__openElementStack.pop()

        newElement = self.createElementFromToken(token)

        self.__openElementStack[-1].children.append(newElement)

        # newElement becomes the element at the top of the stack
        if (not(token.isSelfClosing or token.name in self.selfClosingTags)):
            self.__openElementStack.append(newElement)

    def handleUnacceptedStartTag(self, token):
        if (not(token.isSelfClosing)):
            # Unaccepted tag is already the top stack element
            if (not(self.__openElementStack[-1].name in self.acceptedTagNames)):
                self.__openElementStack.pop()
            self.__openElementStack.append(self.createDefaultElement(token))

    def handleEndTagToken(self, token):
        # The first stack element should always be the root node
        if (len(self.__openElementStack) > 1 and
            self.__openElementStack[-1].name == token.name):
            self.__openElementStack.pop()

    def handleUnacceptedEndTag(self, token):
        if (len(self.__openElementStack) > 1 and
            not(self.__openElementStack[-1].name in self.acceptedTagNames)):
            self.__openElementStack.pop()

    def handleCharacterToken(self, token):
        # The first stack element should always be the root node
        if (len(self.__openElementStack) < 2):
            return

        if (self.__openElementStack[-1].name in self.validTextTags):
            nextCharacter = token.character
            if (self.isWhiteSpace(nextCharacter)):
                # Prevent any extra white space past the first one between
                # non-white-space characters
                if (self.__noWhiteSpace):
                    return
                else:
                    # All white space is collapsed to a single space
                    # in valid text elements
                    self.__noWhiteSpace = True
                    nextCharacter = " "
            else:
                self.__noWhiteSpace = False

            if (self.__currentTextElement is None):
                self.__currentTextElement = self.createNewTextElementFromToken(token)
                self.__openElementStack[-1].children.append(self.__currentTextElement)

            self.__currentTextElement.text += nextCharacter

    def handleLinkElement(self, linkElement):
        if (len(self.rootUrl) == 0):
            return
        isCSSLink = False
        CSSUrlSource = ""
        for attribute in linkElement.attributes:
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

    def isWhiteSpace(self, character):
        return (
                ord(character) == 9 or  # Unicode value for character tabulation
                ord(character) == 10 or # Unicode value for line feed
                ord(character) == 12 or # Unicode value for form feed
                ord(character) == 32    # Unicode value for space
        )

    def getTextElements(self, elementNode, totalTextContents):
        if (elementNode.name == "#text"):
            totalTextContents.append(elementNode.value)

        if (len(elementNode.children) == 0):
            return
        else:
            for child in elementNode.children:
                self.getTextElements(child, totalTextContents)

    def getRenderList(self, htmlElement, renderList):
        elementDeclarations = None
        if (htmlElement.name in self.CSSParser.ruleSets):
            elementDeclarations = self.CSSParser.ruleSets[htmlElement.name]

        for element in htmlElement.children:
            if (element.name == "#text"):
                renderList.append(self.getRenderText(element.value, elementDeclarations))
            elif (element.name == "a"):
                urlString = ""
                for attribute in htmlElement.attributes:
                    if (attribute.name == "href"):
                        urlString = attribute.value
                        break
                renderString = '<a href="' + urlString + '">'
                temp = []
                self.getHyperlinkText(temp, htmlElement)
                renderString += "".join(temp)
                renderString += '</a>'
                newRenderElement = RenderText(renderString)
                renderList.append(newRenderElement)
                return
            self.getRenderList(element, renderList)

    def getRenderText(self, text, parentDeclarations):
        newRenderElement = RenderText(text)
        if (parentDeclarations is None):
            return newRenderElement
        for declaration in parentDeclarations:
            if (declaration.dProperty == "font-size"):
                newRenderElement.fontSize = declaration.dValue
                break
        return newRenderElement

    def getHyperlinkText(self, currentString, treeElement):
        if (treeElement.name == "#text"):
            currentString.append(treeElement.value)
        if (len(treeElement.children) == 0):
            return
        else:
            for element in treeElement.children:
                self.getHyperlinkText(currentString, element)

    def createElementFromToken(self, token):
        # __elementDictionary maps token names to specific functions
        # that create the element corresponding to that name
        elementFunction = self.__elementDictionary.get(token.name, self.createDefaultElement)
        element = elementFunction(token)
        element.name = token.name
        return element

    def createNewHyperlinkElementFromToken(self, token):
        href = ""
        for attribute in token.attributesList:
            if (attribute.name == "href"):
                href = attribute.value
                break
        hyperlinkElement = HTMLElement.HyperlinkElement(href)
        if (href == ""):
            # <a> tag did not contain a hyperlink
            return hyperlinkElement
        hyperlinkElement.href = self.getAbsoluteUrl(href)
        return hyperlinkElement

    def createNewImageElementFromToken(self, token):
        imageSourceUrl = ""
        for attribute in token.attributesList:
            if (attribute.name == "src"):
                imageSourceUrl = attribute.value
                break
        imageElement = HTMLElement.ImageElement(imageSourceUrl)
        if (imageSourceUrl == ""):
            # <img> tag did not contain a link to the image
            return imageElement
        imageElement.imageSourceUrl = self.getAbsoluteUrl(imageSourceUrl)
        return imageElement

    def createNewTextElementFromToken(self, token):
        textElement = HTMLElement.TextElement()
        textElement.name = "#text"
        return textElement

    def createDefaultElement(self, token):
        return HTMLElement.HTMLElement()

    def getAbsoluteUrl(self, potentialRelativeUrl):
        absoluteUrl = potentialRelativeUrl
        if (self.isRelativeUrl(potentialRelativeUrl)):
            if (potentialRelativeUrl[0:1] == '//'):
                absoluteUrl = absoluteUrl[2:] # Remove the leading '//'
            elif (potentialRelativeUrl[0] == '/'):
                absoluteUrl = absoluteUrl[1:] # Remove the leading '/'
            absoluteUrl = self.rootUrl + absoluteUrl
        return absoluteUrl

    def isRelativeUrl(self, potentialRelativeUrl):
        if (len(potentialRelativeUrl) < 4):
            return True
        return not(potentialRelativeUrl[0:4] == "http")

if __name__ == "__main__":
    th = TokenHandler()
    token = StartTagToken("a")
    el = th.createNewHTMLElementFromToken(token)
    print(el.href)
