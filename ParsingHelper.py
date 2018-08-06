"""
    This module provides helper methods for parsing unicode characters.
"""

def isUppercaseAlphaChar(character):
    return (ord(character) >= ord('A') and ord(character) <= ord('Z'))

def isLowercaseAlphaChar(character):
    return (ord(character) >= ord('a') and ord(character) <= ord('z'))

def isWhiteSpace(character):
    return (
            ord(character) == 9 or  # Unicode value for character tabulation
            ord(character) == 10 or # Unicode value for line feed
            ord(character) == 12 or # Unicode value for form feed
            ord(character) == 32    # Unicode value for space
    )
