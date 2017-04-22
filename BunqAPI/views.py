from django.shortcuts import render
from .forms import GenerateKeyForm

# Create your views here.


def generate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GenerateKeyForm(request.POST)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': form})
