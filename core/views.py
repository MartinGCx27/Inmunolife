from django.shortcuts import render

# Create your views here.
# Home view
def inmunolife_home(request):
    return render(request, "index.html")