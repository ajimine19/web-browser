# sprint-0-part-2-sq2018-ajimine19
sprint-0-part-2-sq2018-ajimine19 created by GitHub Classroom

FOR DR. TRIBELHORN:
  As of Sprint 2, our browser is capable of connecting to real webpages and
  will write the content from that page that is between <p> tags to
  the console. The browser can refresh the current page and show the developer
  source html code. Web page content is stored in the browser's cache. It
  caches up to 3 web pages (3 is a design decision to keep things simple for now).
  "gui.py" is the current main entry point of our browser, so the browser
  should be run using "python gui.py" on the console. We also have back and
  forward navigation buttons on our gui, but we have not implemented their
  functionality yet.

This a read me file

Infrastructure:

Object Oriented design:

Sprint 2:
1) Create helper functions for the html and css parser
   - Classes:
     : Main
     : Parser
       - Token Class:
          - Htmls:
            - start tag
            - end tag
            - comment
            - end-of-file
          - CSS: (Ignore the content of the css Ex. <style> ooki stuff </style>, "ignore ooki stuff" )
            - Style
            - Script
     : Graphic (pyqt)
       - Graphic Class
          - Overall we will take in a token traverse tree
          - List of Strings
3) Error handling create error cases so the program doesnt completely shit itself.
2) Getting real websites and parse it through
3) Implement Pyqt graphics
4) Creating a window and displaying the list of strings
5) Create gui components   
   - back button
   - refresh button
   - url text bar
   - caching

Run WebBrowser.py

Testing:
  - Any file of code or class we will have a unit test that corresponds to the same same file that test the funcitons inside.
  - Ex. The class called make has a corresponding testfile called test_make
      - test_make tests the methods that are inside of class make

    Good Test Websites:
    www.theuserisdrunk.com
    http://www.99lime.com/_bak/topics/you-only-need-10-tags/
    www.trello.com
--------------------------------------------
sprint3)

- Base render class:
  Functionality: Create widget object class and you return widget


- One method getWidget() that is
- optimization problems
<div> will inherit a position,


  ------------------------------------------
sprint 4)

  Quality Attributes

  Top 5
  Simplicity - Fox Browser is simple
  Understadability -  
  Integrity -
  Consistiency -
  Modularity -


  5 To Improve
  Security -
  Timeliness -
  Customizability - Make browser
  Installability - Make it easy to install
  Auditability - Examine code to make improvements

 ------------------------------------------
sprint  5)

Notes:

Add Tabs Button -
  Add new tabs gets the current url and adds it to an array

Array tab (URLs)-   
  Add a tab function in Fox browser Tab that uses the array that stores all the urls
  when it was added the array from tab button. Then return the array.

Array tab (Labels)-  
  Passes the Labels after it was parsed.

Major Refactoring of the code that loaded web-pages.

Bug-Fix: The Browser previously could not decode content from all web-pages.
  We were guessing the original charset used to encode web-pages, so we were
  unable to consistently decode content from all web-pages.
Solution: The Browser now gets the original encoding directly from the request,
  so we no longer have to guess the original encoding. However, if the
  original encoding is not provided in the request, then we resort to guessing.
  Fortunately, it seems rare for a web-page not to include the original encoding
  in the request.

Bug-Fix: Certain web-pages were blocking our browser from requesting their
  content, since the the browser was identifying itself as a script.
Solution: For those web-pages that block requests from non-common web browsers,
  we set our browser to identify itself as Mozilla Firefox in the request.

Bug-Fix: The browser was loading all web-pages twice.
Solution: The loadWebpage() method was being called once in the conditional
  check in an if statement, then was called again in the body. This was changed
  to only call once and make the check using the returned result.

Bug-Fix: The browser was not displaying certain images.
Solution: The previously ignored images were nested within <a> tags, and
  were being ignored during the render step because the code for links
  only looked for text to render. This was changed so that the link elements
  recursively looks for all text and image elements as its children,
  and properly renders those.

Performance Times For Loading Web-Pages: (reported in seconds)
  google.com - 0.2168
  youtube.com - 16.8204
  up.edu - 1.7388
  amazon.com - 38.8032
  en.wikipedia.org/wiki/Main_Page — 3.0628

Bug if the history.csv file is empty the browser will not run


Things being deleted as we clean up:
Date     |   Description    
4/6/2018 - Evan deleted the entire test_htmltokenizer becuase it was an unused test file
4/6/2018 - Devin deleted the original tabs in the gui.py

--------------------------------------
sprint 6)
Features:
1. Load a webpage: type the URL into the URL bar on the top of the browser and press the ENTER key or the "search" button on the right (if  "https://" is not typed in, it will automatically be inserted).
2. Load a previous webpage: press the back arrow button and the browser will load the previous webpage if there is one available (the arrow will unclickable in the case where there is no previous webpage).
3. Go forward to a webpage: press the forward arrow button and the browser will load the webpage that it was on before going backward if there is one available (the arrow will unclickable in the case where there is no previous webpage).
4. Reload a page: press the reload button (the circular arrow) and the current webpage will be reloaded.
5. Add a favorite webpage: Click "Favorite Current Page" button and the current webpage will be added to the list of favorites.
6. Go to a webpage that was favorited: On the favorite list, click on a link to go to the webpage.
7. See list of favorited pages: Click the "Favorites" button and the list will be displayed.
8. See list of pages in history: Click the "History" button and the list will be displayed.
9. Go to a webpage in the browser history: On the history list, click on a link to go to the webpage.
10. Clear browser history: Click "Clear History" button and the history will be cleared except the current webpage and the history list will be displayed.
11: Follow links: Click on a link and the corresponding page will be loaded.
12: Go to the homepage: Press the home button (the house) and the homepage will be loaded.
13: Set a new homepage: Press the "Set home" button and the current webpage will become the new home page.
14: Create a new tab: Click the "New Tab" button and a new tab will be created and load the homepage.
15: Switch between tabs: Click on a tab and it will display the page that the tab was on.
16: Hide/Expand the list of tabs: Click the arrow next to the tab list to hide/show the list.
17: Scroll through the webpage: Scroll through a long webpage with the scrollbar on the side or with an OS gesture (ex. two finger swipe on OSX).

Final Code Coverage: 54%
