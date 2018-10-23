from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
import random
import bcrypt
from .models import *
from ..usersLogin.models import *

def showUser(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
        'logged': User.objects.get(email_hash=request.session['email_checker']),
        'quotes': Quote.objects.filter(user = User.objects.get(id=user_id))
    }
    return render(request, 'quotes/showUser.html', context)

def editUser(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(email_hash=request.session['email_checker'])
    }
    return render(request, 'quotes/userEdit.html', context)
def editorUser(request):
    if request.method == "POST":
        if 'email_checker' not in request.session:
            return redirect('/')
        errors = User.objects.editUser(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes/editUser')
        else:
            b = User.objects.get(email_hash=request.session['email_checker'])
            all_emails = User.objects.exclude(email = request.POST['user_email'])
            print(all_emails)
            try: 
                User.objects.get(email=request.POST['email']) in all_emails
                messages.error(request, "Email already in use")
                return redirect('/quotes/editUser')
            except:
                pass
            
            b.first_name = request.POST['first_name']
            b.last_name = request.POST['last_name']
            b.email = request.POST['email']
            b.save()
            return redirect('/quotes')
def editUserPass(request):
    if request.method == "POST":
        errors = User.objects.editPassword(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/quotes/editUser')
        else:
            b = User.objects.get(email_hash=request.session['email_checker'])
            hash1 = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt())
            b.password = hash1
            b.save()
            return redirect('/quotes')

def quotes(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(email_hash=request.session['email_checker']),
        'quotes': Quote.objects.all()
    }
    return render(request, 'quotes/wall.html', context)

def create_message(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    errors = Quote.objects.mes_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        Quote.objects.insertMessage(request.POST)
    return redirect('/quotes')

def delete_message(request, mes_id):
    if 'email_checker' not in request.session:
        return redirect('/')
    user = User.objects.get(email_hash = request.session['email_checker'])
    b = Quote.objects.get(id=mes_id)
    if user.id == b.user.id:
        b.delete()
    return redirect('/quotes')


def like_message(request, mes_id):
    if 'email_checker' not in request.session:
        return redirect('/')
    x = User.objects.get(email_hash = request.session['email_checker'])
    results = Quote.objects.get(id=mes_id)
    results.likes.add(x)
    results.save()
    return redirect('/quotes')



def logout(request):
    request.session.clear()
    return redirect('/')