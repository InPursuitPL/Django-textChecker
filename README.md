# textChecker
This is my textChecker app, created to learn Django framework in practice.
App works with Polish interface, as it works on polish texts. You can paste text
that you want to check (eg. essay) directly on a page or you can upload txt/docx/pdf 
file. App checks mistakes in text, such as:
<br>-small letters after the dot
-repeated words
-multiple spaces
-erroneous words and phrases
-words with missing comma.
You can also register user and then you are able to create your own, additional
list of erroneous words/phrases to include in text checking (eg. erroneous words that are not
present in the basic list but you are aware that you use a lot).

Installation:
Program uses external modules - docx and PyPDF2 - to open files with such extentions.

