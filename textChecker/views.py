from django.shortcuts import render
from .forms import StringTextForm, UploadFileForm
from .textChecker import CheckedText, gives_file_text
from django.http import HttpResponseRedirect, HttpResponse

def choice(request):
    return render(request, 'textChecker/choice.html')

def file_input(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            result = gives_file_text(request.FILES['file'])
            if result == 'Wrong file format!':
                form = UploadFileForm()
                return render(request,
                              'textChecker/input.html',
                              {'form': form,
                               'error': 'Zły format pliku, spróbuj ponownie'})
            finalResult = CheckedText(result)
            return render(request, 'textChecker/text_output.html',{'result': finalResult})

    form = UploadFileForm()
    return render(request, 'textChecker/input.html', {'form': form})



def text_input(request):
    if request.method == "POST":
        form = StringTextForm(request.POST)
        if form.is_valid():
            stringText = form.save(commit=False)
            stringText.save()
            result = CheckedText(stringText.text)

            return render(request, 'textChecker/text_output.html', {'result': result})
        
    form = StringTextForm()
    return render(request, 'textChecker/input.html', {'form': form})

def add_wrong_words(request):
    user_bad_words = request.user.personaldata.bad_words
    wordsFile = open('incorrectWords.txt')
    wordsList = wordsFile.readlines()
    wrongWordsList = []
    for word in wordsList:
        if word.endswith('\n'):
            word = word[:-1]
        wrongWordsList.append(word)
    return render (request, 'textChecker/add_wrong_words.html',
                   {'user_bad_words': user_bad_words, 'bad_words': wrongWordsList})