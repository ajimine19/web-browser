"""
    test_HTMLTokenizerStateMachine

    This class is responsible for testing the functionality of the
    TokenizerStateMachine class
"""
from HTMLTokenizerStateMachine import *

def test_isUppercaseAlphaCharDetectsUppercase():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['a', 'A', 'j', 'D', 'z', 'Z', '0', '$']
    assert tsm.isUppercaseAlphaChar(testCharacters[0]) == False
    assert tsm.isUppercaseAlphaChar(testCharacters[1]) == True
    assert tsm.isUppercaseAlphaChar(testCharacters[2]) == False
    assert tsm.isUppercaseAlphaChar(testCharacters[3]) == True
    assert tsm.isUppercaseAlphaChar(testCharacters[4]) == False
    assert tsm.isUppercaseAlphaChar(testCharacters[5]) == True
    assert tsm.isUppercaseAlphaChar(testCharacters[6]) == False
    assert tsm.isUppercaseAlphaChar(testCharacters[7]) == False

def test_isLowercaseAlphaCharDetectsLowercase():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['a', 'A', 'j', 'D', 'z', 'Z', '0', '$']
    assert tsm.isLowercaseAlphaChar(testCharacters[0]) == True
    assert tsm.isLowercaseAlphaChar(testCharacters[1]) == False
    assert tsm.isLowercaseAlphaChar(testCharacters[2]) == True
    assert tsm.isLowercaseAlphaChar(testCharacters[3]) == False
    assert tsm.isLowercaseAlphaChar(testCharacters[4]) == True
    assert tsm.isLowercaseAlphaChar(testCharacters[5]) == False
    assert tsm.isLowercaseAlphaChar(testCharacters[6]) == False
    assert tsm.isLowercaseAlphaChar(testCharacters[7]) == False

def test_isWhiteSpaceDetectsWhitespace():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', '\n', '\f', ' ', 'a', '%']
    assert tsm.isWhiteSpace(testCharacters[0]) == True
    assert tsm.isWhiteSpace(testCharacters[1]) == True
    assert tsm.isWhiteSpace(testCharacters[2]) == True
    assert tsm.isWhiteSpace(testCharacters[3]) == True
    assert tsm.isWhiteSpace(testCharacters[4]) == False
    assert tsm.isWhiteSpace(testCharacters[5]) == False

def test_runDataState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['%', 'a', '>', '<']
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runDataState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runDataState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runDataState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runDataState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagOpenState

def test_runTagOpenState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['/', 'A', 'z', '%']

    result = tsm.runTagOpenState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.EndTagOpenState

    result = tsm.runTagOpenState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == "a"

    result = tsm.runTagOpenState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == "z"

    result = tsm.runTagOpenState(testCharacters[3])
    assert result == 0
    assert tsm.currentState == TokenizerState.DataState

def test_runTagNameState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', '\n', ' ', '/', '>', 'A', 'z', '3']
    tsm.tempToken = StartTagToken("")

    result = tsm.runTagNameState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runTagNameState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runTagNameState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runTagNameState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.SelfClosingStartTagState

    result = tsm.runTagNameState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

    tsm.tempToken = StartTagToken("")
    tsm.currentState = TokenizerState.TagNameState
    result = tsm.runTagNameState(testCharacters[5])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert tsm.tempToken.name == "a"

    tsm.tempToken = StartTagToken("")
    result = tsm.runTagNameState(testCharacters[6])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert tsm.tempToken.name == "z"

    tsm.tempToken = StartTagToken("")
    result = tsm.runTagNameState(testCharacters[7])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert tsm.tempToken.name == "3"

def test_runEndTagOpenState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['A', 'z', '$', ' ', '9']

    assert tsm.tempToken is None
    result = tsm.runEndTagOpenState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert isinstance(tsm.tempToken, EndTagToken)
    assert tsm.tempToken.name == "a"

    tsm.tempToken = None
    result = tsm.runEndTagOpenState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.TagNameState
    assert isinstance(tsm.tempToken, EndTagToken)
    assert tsm.tempToken.name == "z"

    result = tsm.runEndTagOpenState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runEndTagOpenState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

    result = tsm.runEndTagOpenState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState

def test_runBeforeAttributeNameState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['/', '>', 'A', 'z']

    result = tsm.runBeforeAttributeNameState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.SelfClosingStartTagState

    tsm.tempToken = StartTagToken("")
    result = tsm.runBeforeAttributeNameState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

    tsm.tempToken = StartTagToken("")
    result = tsm.runBeforeAttributeNameState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "a"
    assert tsm.tempToken.attributesList[0].value == ""

    tsm.tempToken = StartTagToken("")
    result = tsm.runBeforeAttributeNameState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "z"
    assert tsm.tempToken.attributesList[0].value == ""

def test_runAttributeNameState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', '\n', '/', '=', '>', 'A', 'z', '9']

    result = tsm.runAttributeNameState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeNameState

    result = tsm.runAttributeNameState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeNameState

    result = tsm.runAttributeNameState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.SelfClosingStartTagState

    result = tsm.runAttributeNameState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeValueState

    result = tsm.runAttributeNameState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

    tsm.currentState = TokenizerState.AttributeNameState
    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("name", ""))
    result = tsm.runAttributeNameState(testCharacters[5])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "namea"
    assert tsm.tempToken.attributesList[0].value == ""

    tsm.currentState = TokenizerState.AttributeNameState
    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("name", ""))
    result = tsm.runAttributeNameState(testCharacters[6])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "namez"
    assert tsm.tempToken.attributesList[0].value == ""

    tsm.currentState = TokenizerState.AttributeNameState
    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("name", ""))
    result = tsm.runAttributeNameState(testCharacters[7])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "name9"
    assert tsm.tempToken.attributesList[0].value == ""

def test_runAfterAttributeNameState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', '\n', '/', '=', '>', 'A', 'z', '9']

    # white space is not supposed to change state
    tsm.currentState = TokenizerState.AfterAttributeNameState
    result = tsm.runAfterAttributeNameState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeNameState

    tsm.currentState = TokenizerState.AfterAttributeNameState
    result = tsm.runAfterAttributeNameState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeNameState

    result = tsm.runAfterAttributeNameState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.SelfClosingStartTagState

    result = tsm.runAfterAttributeNameState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeValueState

    result = tsm.runAfterAttributeNameState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

    tsm.currentState = TokenizerState.AfterAttributeNameState
    tsm.tempToken = StartTagToken("")
    result = tsm.runAfterAttributeNameState(testCharacters[5])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "a"
    assert tsm.tempToken.attributesList[0].value == ""

    tsm.currentState = TokenizerState.AfterAttributeNameState
    tsm.tempToken = StartTagToken("")
    result = tsm.runAfterAttributeNameState(testCharacters[6])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "z"
    assert tsm.tempToken.attributesList[0].value == ""

    tsm.currentState = TokenizerState.AfterAttributeNameState
    tsm.tempToken = StartTagToken("")
    result = tsm.runAfterAttributeNameState(testCharacters[7])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeNameState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == "9"
    assert tsm.tempToken.attributesList[0].value == ""

def test_runBeforeAttributeValueState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', '\n', '\"', '\'', 'A', 'z', '9']

    # white space is not supposed to change state
    tsm.currentState = TokenizerState.BeforeAttributeValueState
    result = tsm.runBeforeAttributeValueState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeValueState

    tsm.currentState = TokenizerState.BeforeAttributeValueState
    result = tsm.runBeforeAttributeValueState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeValueState

    result = tsm.runBeforeAttributeValueState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueDoubleQuotedState

    result = tsm.runBeforeAttributeValueState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueSingleQuotedState

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    result = tsm.runBeforeAttributeValueState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "A"

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    result = tsm.runBeforeAttributeValueState(testCharacters[5])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "z"

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    result = tsm.runBeforeAttributeValueState(testCharacters[6])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "9"

def test_runAttributeValueDoubleQuotedState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\"', 'A', 'z', '9', '#']

    result = tsm.runAttributeValueDoubleQuotedState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeValueQuotedState

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    tsm.currentState = TokenizerState.AttributeValueDoubleQuotedState
    result = tsm.runAttributeValueDoubleQuotedState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueDoubleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "A"

    result = tsm.runAttributeValueDoubleQuotedState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueDoubleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az"

    result = tsm.runAttributeValueDoubleQuotedState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueDoubleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9"

    result = tsm.runAttributeValueDoubleQuotedState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueDoubleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9#"

def test_runAttributeValueSingleQuotedState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\'', 'A', 'z', '9', '#']

    result = tsm.runAttributeValueSingleQuotedState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.AfterAttributeValueQuotedState

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    tsm.currentState = TokenizerState.AttributeValueSingleQuotedState
    result = tsm.runAttributeValueSingleQuotedState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueSingleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "A"

    result = tsm.runAttributeValueSingleQuotedState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueSingleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az"

    result = tsm.runAttributeValueSingleQuotedState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueSingleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9"

    result = tsm.runAttributeValueSingleQuotedState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueSingleQuotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9#"

def test_runAttributeValueUnquotedState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['\t', ' ', '>', 'A', 'z', '9', '#']

    result = tsm.runAttributeValueUnquotedState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runAttributeValueUnquotedState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runAttributeValueUnquotedState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

    tsm.tempToken = StartTagToken("")
    tsm.tempToken.attributesList.append(TagAttribute("", ""))
    tsm.currentState = TokenizerState.AttributeValueUnquotedState
    result = tsm.runAttributeValueUnquotedState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "A"

    result = tsm.runAttributeValueUnquotedState(testCharacters[4])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az"

    result = tsm.runAttributeValueUnquotedState(testCharacters[5])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9"

    result = tsm.runAttributeValueUnquotedState(testCharacters[6])
    assert result == 1
    assert tsm.currentState == TokenizerState.AttributeValueUnquotedState
    assert isinstance(tsm.tempToken, StartTagToken)
    assert tsm.tempToken.name == ""
    assert len(tsm.tempToken.attributesList) == 1
    assert tsm.tempToken.attributesList[0].name == ""
    assert tsm.tempToken.attributesList[0].value == "Az9#"

def test_runAfterAttributeValueQuotedState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = [' ', '\n', '/', '>']

    result = tsm.runAfterAttributeValueQuotedState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runAfterAttributeValueQuotedState(testCharacters[1])
    assert result == 1
    assert tsm.currentState == TokenizerState.BeforeAttributeNameState

    result = tsm.runAfterAttributeValueQuotedState(testCharacters[2])
    assert result == 1
    assert tsm.currentState == TokenizerState.SelfClosingStartTagState

    result = tsm.runAfterAttributeValueQuotedState(testCharacters[3])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None

def test_runSelfClosingStartTagState():
    tsm = HTMLTokenizerStateMachine()
    testCharacters = ['>']

    tsm.tempToken = StartTagToken("")
    result = tsm.runSelfClosingStartTagState(testCharacters[0])
    assert result == 1
    assert tsm.currentState == TokenizerState.DataState
    assert tsm.tempToken is None
