"""
    RenderObject

    This class is responsible for storing the data related to
    webpage contents to be rendered to the browser window.
    This class is used to apply additional settings to certain
    widgets that can only be applied from the main GUI class.
    For example, the loadWebpage method should be connected to
    RenderObjects of type Anchor from the GUI.
"""

import enum

class ObjectType(enum.Enum):
    Image = enum.auto() # i.e. the <img> tag
    Hyperlink = enum.auto() # i.e. the <a> tag
    Text = enum.auto()

class RenderObject:

    def __init__(self, widget, objectType):
        self.widget = widget
        self.objectType = objectType

    def printObjectInfo(self):
        if (self.objectType == ObjectType.Image):
            print("Image")
        else:
            print(self.widget.text())
