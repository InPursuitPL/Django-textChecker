from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import StringTextForm, UploadFileForm, AddWrongWordForm
from .textChecker import CheckedText, gives_file_text, creates_wrong_words_list
from .models import PersonalData


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
            return render(request, 'textChecker/text_output.html',
                          {'result': finalResult})
    form = UploadFileForm()
    return render(request, 'textChecker/input.html', {'form': form})

def text_input(request):
    if request.method == "POST":
        form = StringTextForm(request.POST)
        if form.is_valid():
            stringText = form.save(commit=False)
            stringText.save()
            if not request.user.is_anonymous():
                user_wrong_words = request.user.personaldata.wrong_words
                result = CheckedText(stringText.text, user_wrong_words)
            else:
                result = CheckedText(stringText.text)
            return render(request, 'textChecker/text_output.html',
                          {'result': result})
    form = StringTextForm()
    return render(request, 'textChecker/input.html', {'form': form})

@login_required
def add_wrong_words(request):
    if request.method == "POST":
        form = AddWrongWordForm(request.POST)
        if form.is_valid():
            wordToAdd = request.POST['word']
            obj = PersonalData.objects.get(user=request.user)
            obj.wrong_words += '\n' + wordToAdd.strip()
            obj.save()
            result = request.user.personaldata.wrong_words
            return render(request, 'textChecker/wrong_words_added.html',
                          {'result': result})
    user_wrong_words = request.user.personaldata.wrong_words
    # Using external function from textChecker module.
    wrongWordsList = creates_wrong_words_list('incorrectWords.txt')
    form = AddWrongWordForm()
    return render(request, 'textChecker/add_wrong_words.html',
                   {'user_wrong_words': user_wrong_words,
                    'wrong_words': wrongWordsList,
                    'form': form})