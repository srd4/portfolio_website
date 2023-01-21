from django.shortcuts import render

# Create your views here.

def sanke(request):
    return render(request, "sanke/sanke.html")
