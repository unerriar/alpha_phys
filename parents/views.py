from django.shortcuts import render

def about(request):
    return render(request, 'parents/about.html')

def individual(request):
    return render(request, 'parents/individual.html')

def groups(request):
    return render(request, 'parents/groups.html')

def selfstudy(request):
    return render(request, 'parents/selfstudy.html')
