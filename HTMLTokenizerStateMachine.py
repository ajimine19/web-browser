"""
    HTMLTokenizerStateMachine

    This class is responsible for managing the current state and state transitions
    as the machine is used to parse html code.
"""
import enum

from CharacterToken import CharacterToken
from StartTagToken import StartTagToken
from EndTagToken import EndTagToken
from TagAttribute import TagAttribute

# Enum used for representing states
class TokenizerState(enum.Enum):
    DataState = enum.auto()
    TagOpenState = enum.auto()
    TagIgnoreState = enum.auto()
    TagNameState = enum.auto()
    EndTagOpenState = enum.auto()
    BeforeAttributeNameState = enum.auto()
    AttributeNameState = enum.auto()
    AfterAttributeNameState = enum.auto()
    BeforeAttributeValueState = enum.auto()
    AttributeValueDoubleQuotedState = enum.auto()
    AttributeValueSingleQuotedState = enum.auto()
    AttributeValueUnquotedState = enum.auto()
    AfterAttributeValueQuotedState = enum.auto()
    SelfClosingStartTagState = enum.auto()

class HTMLTokenizerStateMachine:

    def __init__(self):
        self.__HTMLTokens = []
        self.currentState = TokenizerState.DataState
        self.stateDictionary = {
            TokenizerState.DataState : self.runDataState,
            TokenizerState.TagOpenState : self.runTagOpenState,
            TokenizerState.TagIgnoreState : self.runTagIgnoreState,
            TokenizerState.TagNameState : self.runTagNameState,
            TokenizerState.EndTagOpenState : self.runEndTagOpenState,
            TokenizerState.BeforeAttributeNameState : self.runBeforeAttributeNameState,
            TokenizerState.AttributeNameState : self.runAttributeNameState,
            TokenizerState.AfterAttributeNameState : self.runAfterAttributeNameState,
            TokenizerState.BeforeAttributeValueState : self.runBeforeAttributeValueState,
            TokenizerState.AttributeValueDoubleQuotedState : self.runAttributeValueDoubleQuotedState,
            TokenizerState.AttributeValueSingleQuotedState : self.runAttributeValueSingleQuotedState,
            TokenizerState.AttributeValueUnquotedState : self.runAttributeValueUnquotedState,
            TokenizerState.AfterAttributeValueQuotedState : self.runAfterAttributeValueQuotedState,
            TokenizerState.SelfClosingStartTagState : self.runSelfClosingStartTagState
        }
        self.tempToken = None
        self.currentEmittedToken = None

    def handleCharacter(self, character):
        # catch ParseErrors here
        # Note that the parser will currently incorrectly parse comments
        # as tags, as of 2/17/18
        currentStateFunction = self.stateDictionary[self.currentState]
        return currentStateFunction(character)

    def runDataState(self, character):
        """
            runDataState should always consume the given character
            (i.e. return 1 for the iterator increment value)
        """
        if (character == '<'): # indicates the start of a tag
            self.currentState = TokenizerState.TagOpenState

        else: # pass off the token for the tree constructor to deal with
            characterToken = CharacterToken(character)
            self.emitToken(characterToken)

        return 1

    def runTagOpenState(self, character):
        """
            runTagOpenState should always consume the given character
            (i.e. return 1 for the iterator increment value),
            unless the previous character was incorrectly judged to be
            the start of a tag (i.e. the else statement in this method is entered),
            in which case the character should not be consumed.

            Transitions available into this state from:
                DataState
            Tranistions available from this state to:
                EndTagOpenState
                TagNameState
                DataState
        """

        if (character == '/'): # indicates that the tag is an end tag
            self.currentState = TokenizerState.EndTagOpenState
        elif (character == '!'): # Ignore comment "tags"
            self.currentState = TokenizerState.TagIgnoreState
        elif (self.isUppercaseAlphaChar(character)):
            # the current character is an uppercase alpha character
            self.tempToken = StartTagToken(character.lower())
            self.currentState = TokenizerState.TagNameState

        elif (self.isLowercaseAlphaChar(character)):
            # the current character is a lowercase alpha character
            self.tempToken = StartTagToken(character)
            self.currentState = TokenizerState.TagNameState

        else:
            # the '<' character was incorrectly processed as the start of a tag;
            # i.e. no tag should be being processed currently.
            # output the '<' as a character token as it should have been
            token = CharacterToken('<')
            self.emitToken(token)
            self.currentState = TokenizerState.DataState
            return 0

        return 1

    def runTagIgnoreState(self, character):
        if (character == '>'):
            self.currentState = TokenizerState.DataState
        return 1

    def runTagNameState(self, character):
        if (self.isWhiteSpace(character)):
            self.currentState = TokenizerState.BeforeAttributeNameState
        elif (character == '/'):
            self.currentState = TokenizerState.SelfClosingStartTagState
        elif (character == '>'):
            # Reached the end of the tag; final tag token can be emitted
            self.emitToken(self.tempToken)
            self.tempToken = None
            self.currentState = TokenizerState.DataState
        elif (self.isUppercaseAlphaChar(character)):
            self.tempToken.name += character.lower()
        else:
            self.tempToken.name += character

        return 1

    def runEndTagOpenState(self, character):
        if (self.isUppercaseAlphaChar(character)):
            self.tempToken = EndTagToken(character.lower())
            self.currentState = TokenizerState.TagNameState
        elif (self.isLowercaseAlphaChar(character)):
            self.tempToken = EndTagToken(character)
            self.currentState = TokenizerState.TagNameState
        else:
            self.currentState = TokenizerState.DataState

        return 1

    def runBeforeAttributeNameState(self, character):
        if (self.isWhiteSpace(character)):
            pass # Ignore white space characters
        elif (character == '/'):
            self.currentState = TokenizerState.SelfClosingStartTagState
        elif (character == '>'):
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None
        elif (self.isUppercaseAlphaChar(character)):
            attribute = TagAttribute(character.lower(), "")
            self.tempToken.attributesList.append(attribute)
            self.currentState = TokenizerState.AttributeNameState
        else:
            attribute = TagAttribute(character, "")
            self.tempToken.attributesList.append(attribute)
            self.currentState = TokenizerState.AttributeNameState

        return 1

    def runAttributeNameState(self, character):
        if (self.isWhiteSpace(character)):
            self.currentState = TokenizerState.AfterAttributeNameState
        elif (character == '/'):
            self.currentState = TokenizerState.SelfClosingStartTagState
        elif (character == '='):
            self.currentState = TokenizerState.BeforeAttributeValueState
        elif (character == '>'):
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None
        elif (self.isUppercaseAlphaChar(character)):
            # The last attribute in the list should be the most recent;
            # i.e. the one we want to modify
            self.tempToken.attributesList[-1].name += character.lower()
        else:
            self.tempToken.attributesList[-1].name += character

        return 1

    def runAfterAttributeNameState(self, character):
        if (self.isWhiteSpace(character)):
            pass # Ignore white space characters
        elif (character == '/'):
            self.currentState = TokenizerState.SelfClosingStartTagState
        elif (character == '='):
            self.currentState = TokenizerState.BeforeAttributeValueState
        elif (character == '>'):
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None
        elif (self.isUppercaseAlphaChar(character)):
            attribute = TagAttribute(character.lower(), "")
            self.tempToken.attributesList.append(attribute)
            self.currentState = TokenizerState.AttributeNameState
        else:
            attribute = TagAttribute(character, "")
            self.tempToken.attributesList.append(attribute)
            self.currentState = TokenizerState.AttributeNameState

        return 1

    def runBeforeAttributeValueState(self, character):
        if (self.isWhiteSpace(character)):
            pass # Ignore white space characters
        elif (character == '\"'):
            self.currentState = TokenizerState.AttributeValueDoubleQuotedState
        elif (character == '\''):
            self.currentState = TokenizerState.AttributeValueSingleQuotedState
        else:
            self.tempToken.attributesList[-1].value += character
            self.currentState = TokenizerState.AttributeValueUnquotedState

        return 1

    def runAttributeValueDoubleQuotedState(self, character):
        if (character == '\"'):
            self.currentState = TokenizerState.AfterAttributeValueQuotedState
        else:
            self.tempToken.attributesList[-1].value += character

        return 1

    def runAttributeValueSingleQuotedState(self, character):
        if (character == '\''):
            self.currentState = TokenizerState.AfterAttributeValueQuotedState
        else:
            self.tempToken.attributesList[-1].value += character

        return 1

    def runAttributeValueUnquotedState(self, character):
        if (self.isWhiteSpace(character)):
            self.currentState = TokenizerState.BeforeAttributeNameState
        elif (character == '>'):
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None
        else:
            self.tempToken.attributesList[-1].value += character
        return 1

    def runAfterAttributeValueQuotedState(self, character):
        if (self.isWhiteSpace(character)):
            self.currentState = TokenizerState.BeforeAttributeNameState
        elif (character == '/'):
            self.currentState = TokenizerState.SelfClosingStartTagState
        elif (character == '>'):
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None

        # The else condition is an error here and should be handled eventually

        return 1

    def runSelfClosingStartTagState(self, character):
        if (character == '>'):
            self.tempToken.isSelfClosing = True
            self.emitToken(self.tempToken)
            self.currentState = TokenizerState.DataState
            self.tempToken = None

        # The else condition is an error here and should be handled eventually
        return 1

    def emitToken(self, token):
        self.__HTMLTokens.append(token)
        self.currentEmittedToken = token

    def getTokenList(self):
        return self.__HTMLTokens

    ### Helper Functions ###

    def isUppercaseAlphaChar(self, character):
        return (ord(character) >= ord('A') and ord(character) <= ord('Z'))

    def isLowercaseAlphaChar(self, character):
        return (ord(character) >= ord('a') and ord(character) <= ord('z'))

    def isWhiteSpace(self, character):
        return (
                ord(character) == 9 or  # Unicode value for character tabulation
                ord(character) == 10 or # Unicode value for line feed
                ord(character) == 12 or # Unicode value for form feed
                ord(character) == 32    # Unicode value for space
        )
