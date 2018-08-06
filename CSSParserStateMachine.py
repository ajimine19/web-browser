"""
    CSSParserStateMachine

    This class is responsible for converting CSS text into
    CSSRuleSets.
"""

import enum
from ParsingHelper import *
from CSSRuleSet import *
from CharacterToken import CharacterToken

class CSSParserState(enum.Enum):
    BeforeSelectorNameState = enum.auto()
    SelectorNameState = enum.auto()
    AfterSelectorNameState = enum.auto()
    BeforeDeclarationNameState = enum.auto()
    DeclarationNameState = enum.auto()
    BeforeDeclarationValueState = enum.auto()
    DeclarationValueState = enum.auto()

class CSSParserStateMachine:

    def __init__(self):
        self.currentState = CSSParserState.BeforeSelectorNameState
        self.currentRuleSet = None
        self.allRuleSets = []
        self.ruleSets = {}
        self.stateDictionary = {
            CSSParserState.BeforeSelectorNameState : self.runBeforeSelectorNameState,
            CSSParserState.SelectorNameState : self.runSelectorNameState,
            CSSParserState.AfterSelectorNameState : self.runAfterSelectorNameState,
            CSSParserState.BeforeDeclarationNameState : self.runBeforeDeclarationNameState,
            CSSParserState.DeclarationNameState : self.runDeclarationNameState,
            CSSParserState.BeforeDeclarationValueState : self.runBeforeDeclarationValueState,
            CSSParserState.DeclarationValueState : self.runDeclarationValueState
        }

    def handleCharacter(self, character):
        currentCharacter = ''
        if (isinstance(character, CharacterToken)):
            currentCharacter = character.character
        else:
            currentCharacter = character
        currentStateFunction = self.stateDictionary[self.currentState]
        return currentStateFunction(currentCharacter)

    def runBeforeSelectorNameState(self, character):
        if (isWhiteSpace(character)):
            pass
        elif (character == '{'):
            self.currentState = CSSParserState.BeforeDeclarationNameState
        else:
            self.currentRuleSet = CSSRuleSet()
            self.currentRuleSet.selectors.append(str(character))
            self.currentState = CSSParserState.SelectorNameState
        return 1

    def runSelectorNameState(self, character):
        if (isWhiteSpace(character)):
            self.currentState = CSSParserState.AfterSelectorNameState
        elif (character == ','):
            self.currentState = CSSParserState.BeforeSelectorNameState
        elif (character == '{'):
            self.currentState = CSSParserState.BeforeDeclarationNameState
        else:
            self.currentRuleSet.selectors[-1] += character
        return 1

    def runAfterSelectorNameState(self, character):
        if (isWhiteSpace(character)):
            pass
        elif (character == ','):
            self.currentState = CSSParserState.BeforeSelectorNameState
        elif (character == '{'):
            self.currentState = CSSParserState.BeforeDeclarationNameState
        return 1

    def runBeforeDeclarationNameState(self, character):
        if (isWhiteSpace(character)):
            pass
        elif (character == '}'):
            self.emitRuleSet(self.currentRuleSet)
            self.currentRuleSet = None
            self.currentState = CSSParserState.BeforeSelectorNameState
        else:
            newDeclaration = CSSDeclaration(str(character), "")
            self.currentRuleSet.declarations.append(newDeclaration)
            self.currentState = CSSParserState.DeclarationNameState
        return 1

    def runDeclarationNameState(self, character):
        if (character == ':'):
            self.currentState = CSSParserState.BeforeDeclarationValueState
        else:
            self.currentRuleSet.declarations[-1].dProperty += character
        return 1

    def runBeforeDeclarationValueState(self, character):
        if (isWhiteSpace(character)):
            pass
        else:
            self.currentRuleSet.declarations[-1].dValue = character
            self.currentState = CSSParserState.DeclarationValueState
        return 1

    def runDeclarationValueState(self, character):
        if (character == ';'):
            self.currentState = CSSParserState.BeforeDeclarationNameState
        elif (character == '}'):
            self.emitRuleSet(self.currentRuleSet)
            self.currentRuleSet = None
            self.currentState = CSSParserState.BeforeSelectorNameState
        else:
            self.currentRuleSet.declarations[-1].dValue += character
        return 1

    def emitRuleSet(self, ruleSet):
        # Store selectors in a dictionary so that
        # HTML Elements can search for their style
        # by checking for their name in the dictionary
        for selector in ruleSet.selectors:
            self.ruleSets[selector] = ruleSet.declarations
        self.allRuleSets.append(ruleSet)

    def printAllRuleSets(self):
        for ruleSet in self.allRuleSets:
            selectorString = ""
            declarationString = ""
            for selector in ruleSet.selectors:
                selectorString += selector + ","
            print(selectorString)

            for declaration in ruleSet.declarations:
                print("    " + declaration.dProperty + ":" + declaration.dValue)

if __name__ == "__main__":
    f = open("../file.txt", encoding='utf-8')
    inputText = f.read()
    f.close()

    psm = CSSParserStateMachine()

    i = 0
    while (i < len(inputText)):
        i = i + psm.handleCharacter(inputText[i])
    psm.printAllRuleSets()
