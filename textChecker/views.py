from django.shortcuts import render
from .forms import StringTextForm, UploadFileForm
from .textChecker import CheckedText, gives_file_text
from django.http import HttpResponseRedirect

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
            #return HttpResponseRedirect('text_output/', finalResult)

    form = UploadFileForm()
    return render(request, 'textChecker/input.html', {'form': form})

# def text_output(request, result):
#     if request.method == 'GET':
#         return render(request, 'textChecker/text_output.html', {'result': result})

def text_input(request):
    if request.method == "POST":
        #Not quite sure about this line.
        form = StringTextForm(request.POST)
        if form.is_valid():
            stringText = form.save(commit=False)
            #Lower line saves object to database.
            #stringText.save()
            result = CheckedText(stringText.text)

            return render(request, 'textChecker/text_output.html', {'result': result})
        
    form = StringTextForm()
    return render(request, 'textChecker/input.html', {'form': form})

