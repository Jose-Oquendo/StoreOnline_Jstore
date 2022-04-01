from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required(login_url='login')
def create(request):
    return render(request, 'billing_profiles/create.html', {

    })
