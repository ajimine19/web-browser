import urllib.request
import ssl
import collections

def getHTML(url):
    # Renamed for clarity
    return getUrlContent(url)

def tryGetHTMLSource(url):
    htmlSource = ""
    requestSuccessful = True
    try:
        responseInfo = getUrlContentAndCharset(url)
        charset = responseInfo.Charset
        if (charset is None):
            # We should probably try a variety of
            # fallback encodings no encoding is provided.
            # Just one is used for now
            charset = 'windows-1252'
        htmlSource = responseInfo.UrlContent.decode(encoding = charset)
        print("Decode successful")
    except:
        htmlSource = None
        requestSuccessful = False
        print("Decode failed")

    ReturnValue = collections.namedtuple('ReturnValue', ['requestSuccessful', 'HTMLSource'])
    return ReturnValue(requestSuccessful, htmlSource)

def getUrlContent(url):
    c = ssl._create_unverified_context()
    urlContent = None
    with urllib.request.urlopen(url, context=c) as response:
        urlContent = response.read()
    return urlContent

def getUrlContentAndCharset(url):
    c = ssl._create_unverified_context()
    urlContent = None
    charset = None
    urlRequest = urllib.request.Request(url)
    # This header change causes our browser to identify itself as Firefox, instead of as a script.
    # This is done because certain web-pages will deny requests unless the User Agent is a
    # well-known browser, e.g. Firefox.
    # We don't want to do this for every site, however, because other sites don't display
    # properly if they think our browser is Firefox.
    if (("amazon" in url) or ("reddit" in url)):
        urlRequest.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/59.0")
    with urllib.request.urlopen(urlRequest, context=c) as response:
        charset = response.info().get_content_charset()
        urlContent = response.read()

    HTTPResponseInfo = collections.namedtuple('HTTPResponseInfo', ['UrlContent', 'Charset'])
    return HTTPResponseInfo(urlContent, charset)

if __name__ == "__main__":
    tryGetHTMLSource("http://faculty.up.edu/oster")
    #tryGetHTMLSource("http://www.google.com")
