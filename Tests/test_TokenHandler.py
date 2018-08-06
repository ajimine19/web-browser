"""
    This file contains the tests for the TokenHandler module.
"""

from TokenHandler import TokenHandler
from StartTagToken import StartTagToken
from EndTagToken import EndTagToken
from CharacterToken import CharacterToken

def test_processTokenHandlesClosingTags():
    testTokens = [
        StartTagToken("p"),
        EndTagToken("p"),
        StartTagToken("a"),
        EndTagToken("a")
        ]

    th = TokenHandler("TestRootUrl/")
    for token in testTokens:
        th.processToken(token)

    assert th.elementTreeRoot.name == "#root#"
    assert len(th.elementTreeRoot.children) == 2
    assert th.elementTreeRoot.children[0].name == "p"
    assert th.elementTreeRoot.children[1].name == "a"

def test_processTokenProcessesIndependentTags():
    testTokens = [
        StartTagToken("br"),
        StartTagToken("img"),
        StartTagToken("html"),
        EndTagToken("html")
        ]
    testTokens[1].isSelfClosing = True

    th = TokenHandler("TestRootUrl/")
    for token in testTokens:
        th.processToken(token)

    assert len(th.elementTreeRoot.children) == 3
    assert th.elementTreeRoot.children[0].name == "br"
    assert th.elementTreeRoot.children[1].name == "img"
    assert th.elementTreeRoot.children[2].name == "html"

def test_processTokenHandlesUnacceptableTags():
    testTokens = [
        StartTagToken("p"),
        StartTagToken("NoHTMLTagShouldEverHaveThisName"),
        StartTagToken("body"),
        StartTagToken("a"),
        EndTagToken("a"),
        EndTagToken("body"),
        EndTagToken("NoHTMLTagShouldEverHaveThisName"),
        EndTagToken("p")
        ]

    th = TokenHandler("TestRootUrl/")
    for token in testTokens:
        th.processToken(token)

    assert len(th.elementTreeRoot.children) == 1
    assert th.elementTreeRoot.children[0].name == "p"

def test_handleStartTagTokenHandlesFirstStartTag():
    testToken = StartTagToken("html")
    th = TokenHandler("TestRootUrl/")
    assert len(th.elementTreeRoot.children) == 0
    th.handleStartTagToken(testToken)
    assert len(th.elementTreeRoot.children) == 1
    assert th.elementTreeRoot.children[0].name == "html"

def test_isRelativeUrl():
    th = TokenHandler("TestRootUrl/")
    testUrls = ["http://google.com", "ARelativeUrl", "/RelativeWithSlash"]
    assert th.isRelativeUrl(testUrls[0]) == False
    assert th.isRelativeUrl(testUrls[1]) == True
    assert th.isRelativeUrl(testUrls[2]) == True

def test_getAbsoluteUrl():
    rootUrl = "TestRootUrl/"
    th = TokenHandler(rootUrl)
    testUrls = ["http://google.com", "https://i.ytimg.com/vi/nrIDL7h9MFQ/hqdefault.jpg?sqp=-oaymwEYCNIBEHZIVfKriqkDCwgBFQAAiEIYAXAB&amp;rs=AOn4CLByrwt1ptJWI5zGkLOZhJpyrFeCSw", "ARelativeUrl", "/RelativeWithSlash"]
    assert th.getAbsoluteUrl(testUrls[0]) == "http://google.com"
    assert th.getAbsoluteUrl(testUrls[1]) == "https://i.ytimg.com/vi/nrIDL7h9MFQ/hqdefault.jpg?sqp=-oaymwEYCNIBEHZIVfKriqkDCwgBFQAAiEIYAXAB&amp;rs=AOn4CLByrwt1ptJWI5zGkLOZhJpyrFeCSw"
    assert th.getAbsoluteUrl(testUrls[2]) == rootUrl + "ARelativeUrl"
    assert th.getAbsoluteUrl(testUrls[3]) == rootUrl + "RelativeWithSlash"
