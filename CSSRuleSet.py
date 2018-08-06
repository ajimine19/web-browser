"""
    CSSRuleSet

    This class is responsible for storing data related to
    CSS rule-sets.
"""

class CSSRuleSet:

    def __init__(self):
        self.selectors = []
        self.declarations = []

"""
    CSSDeclaration

    This class stores the data for a CSS Declaration.
"""
class CSSDeclaration:

    def __init__(self, CSSproperty, value):
        self.dProperty = CSSproperty
        self.dValue = value
