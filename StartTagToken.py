"""
    StartTagToken

    This class is responsible for storing data related to an HTML start tag.
"""

class StartTagToken:

    def __init__(self, tagName = None, tagSelfClosing = None, tagAttributes = None):
        if (tagName is None):
            self.name = ""
        else:
            self.name = tagName

        if (tagSelfClosing is None):
            self.isSelfClosing = False
        else:
            self.isSelfClosing = tagSelfClosing

        if (tagAttributes is None):
            self.attributesList = []
        else:
            self.attributesList = tagAttributes

    def __repr__(self):
        infoString = "StartTagToken | Name: " + self.name
        infoString += " Attributes: "
        for a in self.attributesList:
            infoString += a.name + ", " + a.value + " "
        return infoString
