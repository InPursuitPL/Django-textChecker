from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import StringTextForm, UploadFileForm, RegistrationForm, AddDeleteForm
from .textChecker import CheckedText, gives_file_text, creates_words_list
from .models import PersonalData


def choice(request):
    """
    Displays main page with choices of login/registration and choices
    how to provide data to the program.
    """
    return render(request, 'textChecker/index.html')


def file_input(request):
    """Displays page with form to upload a file in txt/docx/pdf format."""
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
            if not request.user.is_anonymous():
                user_wrong_words = request.user.personaldata.wrong_words
                finalResult = CheckedText(result, user_wrong_words)
            else:
                finalResult = CheckedText(result)
            return render(request, 'textChecker/text_output.html',
                          {'result': finalResult})

    form = UploadFileForm()
    return render(request, 'textChecker/input.html', {'form': form})


def text_input(request):
    """Displays page with form to upload a text."""
    if request.method == "POST":
        form = StringTextForm(request.POST)
        if form.is_valid():
            stringText = request.POST['text']
            if not request.user.is_anonymous():
                user_wrong_words = request.user.personaldata.wrong_words
                result = CheckedText(stringText, user_wrong_words)
            else:
                result = CheckedText(stringText)
            return render(request, 'textChecker/text_output.html',
                          {'result': result})

    form = StringTextForm()
    return render(request, 'textChecker/input.html', {'form': form})


@login_required
def wrong_words(request):
    """
        Displays incorrect elements to search and enables user to
        add or remove elements from his own personal list.
    """
    if request.method == "POST":
        form = AddDeleteForm(request.POST)
        if form.is_valid():
            choice = request.POST['select']
            word = request.POST['word']
            obj = PersonalData.objects.get(user=request.user)
            if choice == 'Add':
                obj.wrong_words += '\n' + word.strip()
            elif choice == 'Delete':
                if word in obj.wrong_words:
                    obj.wrong_words = obj.wrong_words.replace('\n' + word, '')
            obj.save()
            result = request.user.personaldata.wrong_words
            return render(request, 'textChecker/wrong_words_changed.html',
                          {'result': result})

    user_wrong_words = request.user.personaldata.wrong_words
    # Using external function from textChecker module.
    wrongWordsList = creates_words_list('incorrectWords.txt')
    form = AddDeleteForm()
    return render(request, 'textChecker/wrong_words.html',
                  {'user_wrong_words': user_wrong_words,
                   'wrong_words': wrongWordsList,
                   'form': form})


def register_page(request):
    """Page for new user registration."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
            return render(request, 'registration/register_success.html',
                          {'user': form.cleaned_data['username']})
        else:
            return render(request, 'registration/register.html', {'form': form})

    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

