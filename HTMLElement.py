"""
    HTMLElement

    This class represents a node in the tree of elements made from
    processing the tokens from parsing the html.
"""

from PyQt5 import QtGui, QtWidgets
import RenderObject
import getHTTPS

class HTMLElement:

    def __init__(self, name = "", value = None):
        self.children = []
        self.name = name
        self.value = value
        self.attributes = None

    def fillRenderObjectList(self, renderObjectList):
        #print("Rendering: " + self.name)
        for child in self.children:
            """
            if (isinstance(child, ImageElement)):
                print("Child is Image")
            elif (isinstance(child, HyperlinkElement)):
                print("Child is Link")
            """
            child.fillRenderObjectList(renderObjectList)

    def getElementRenderObject(self):
        # Elements that are not specifically implemented are ignored.
        return None

    def getElementRepresentationString(self, offset):
        """
            This method is primarily a debugging tool for displaying
            the tree structure.
        """
        # Base Case
        if (len(self.children) == 0):
            return self.name
        returnString = self.name + '\n'
        nextOffset = offset + "|   "
        for child in self.children[:-1]:
            returnString += offset + "|-- " + child.getElementRepresentationString(nextOffset) + '\n'
        nextOffset = offset + "    "
        returnString += offset + "\-- " + self.children[-1].getElementRepresentationString(nextOffset)

        return returnString

        """
        if (isinstance(self, ImageElement)):
            print("From Tree: " + self.imageSourceUrl)
        for child in self.children:
            child.getElementRepresentationString("")
        """

class TextElement(HTMLElement):

    def __init__(self, text = None):
        super().__init__()
        if (text is None):
            self.text = ""
        else:
            self.text = text

    def fillRenderObjectList(self, renderObjectList):
        # Text elements should always be leaves in the tree,
        # so TextElements are a base case element.
        renderObjectList.append(self.getElementRenderObject())

    def getElementRenderObject(self):
        textLabel = QtWidgets.QLabel(self.text)
        textLabel.setWordWrap(True)
        return RenderObject.RenderObject(
            textLabel, RenderObject.ObjectType.Text)

class HyperlinkElement(HTMLElement):

    def __init__(self, hyperlink):
        super().__init__()
        self.href = hyperlink

    def fillRenderObjectList(self, renderObjectList):
        # HyperlinkElements handle their children in
        # their getElementRenderObject() call,
        # so HyperlinkElements are a base case.
        renderObjectList.append(self.getElementRenderObject())

    def getElementRenderObject(self):
        hyperlinkText = ""
        linkHBoxLayout = QtWidgets.QHBoxLayout()
        widgetsList = []
        self.getHyperlinkWidgets(self, widgetsList)
        """
        for child in self.children:
            if (isinstance(child, TextElement)):
                hyperlinkText += child.text
                textWidget = child.getElementRenderObject().widget
                #labelText = '<a href="' + self.href + '">' + hyperlinkText + '</a>'
                labelText = self.getHyperlinkTextForLabel(hyperlinkText)
                textWidget.setText(labelText)
                linkHBoxLayout.addWidget(textWidget)
            elif (isinstance(child, ImageElement)):
                imageWidget = child.getElementRenderObject().widget
                # Images with pixmaps don't work if they also have text set
                #labelText = self.getHyperlinkTextForLabel("")
                #imageWidget.setText(labelText)
                linkHBoxLayout.addWidget(imageWidget)
        """
        """
        hyperlinkLabelText = '<a href="' + self.href + '">' + hyperlinkText + "</a>"
        hyperlinkLabel = QtWidgets.QLabel(hyperlinkLabelText)
        """

        for widget in widgetsList:
            linkHBoxLayout.addWidget(widget)
        hyperlinkWidget = QtWidgets.QWidget()
        hyperlinkWidget.setLayout(linkHBoxLayout)
        return RenderObject.RenderObject(
            hyperlinkWidget, RenderObject.ObjectType.Hyperlink)

    def getHyperlinkWidgets(self, element, widgetsList):
        for child in element.children:
            if (isinstance(child, TextElement)):
                textWidget = child.getElementRenderObject().widget
                #labelText = '<a href="' + self.href + '">' + hyperlinkText + '</a>'
                labelText = self.getHyperlinkTextForLabel(child.text)
                textWidget.setText(labelText)
                widgetsList.append(textWidget)
            elif (isinstance(child, ImageElement)):
                imageWidget = child.getElementRenderObject().widget
                # Images with pixmaps don't work if they also have text set
                #labelText = self.getHyperlinkTextForLabel("")
                #imageWidget.setText(labelText)
                widgetsList.append(imageWidget)
            else:
                self.getHyperlinkWidgets(child, widgetsList)

    def getHyperlinkTextForLabel(self, text):
        return '<a href="' + self.href + '">' + text + "</a>"

class ImageElement(HTMLElement):

    def __init__(self, imageUrl):
        super().__init__()
        self.imageSourceUrl = imageUrl
        self.height = None
        self.width = None

    def fillRenderObjectList(self, renderObjectList):
        # ImageElements are made from a self-closing tag,
        # so they should never have any children and are
        # therefore a base case.
        renderObjectList.append(self.getElementRenderObject())

    def getElementRenderObject(self):
        imageContent = None
        try:
            imageContent = getHTTPS.getUrlContent(self.imageSourceUrl)
            print("Image Successfully Loaded: " + self.imageSourceUrl)
        except:
            print("Image Failed To Load: " + self.imageSourceUrl)
            with open("image_placeholder.gif", 'rb') as imageFile:
                imageContent = imageFile.read()

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imageContent)
        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(pixmap)
        return RenderObject.RenderObject(
            imageLabel, RenderObject.ObjectType.Image)
