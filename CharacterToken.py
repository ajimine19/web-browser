"""
    CharacterToken

    This class stores data related to an individual character that was read
    during the html parsing.
"""

class CharacterToken:

    def __init__(self, character):
        # The given character is the data for the Character token.
        self.character = character

    def __repr__(self):
        return str(self.character)
