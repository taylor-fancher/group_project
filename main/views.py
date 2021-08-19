from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Trip

# Create your views here.

def login_page(request):
    if 'userid' in request.session:
        return redirect('/trip')
    return render(request, 'login.html')

def login_user(request):
    users = User.objects.filter(email=request.POST['email'])
    if users:
        logged_user = users[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            messages.success(request, 'Successfully logged in!')
            return redirect('/trip')
        else:
            messages.error(request, 'Invalid email or password entered')
    else: 
        messages.error(request, 'Account not found with email')
    return redirect('/')

def register_page(request):
    if 'userid' in request.session:
        return redirect('/trip')
    return render(request, 'registration.html')

def register_user(request):
    errors = User.objects.user_validator(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request,val)
    elif request.method=="POST":
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
        )
        request.session['userid'] = user.id
        messages.success(request, 'Succesfully registered account!')
        return redirect('/trip')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    context = {
        'user': User.objects.get(id=request.session['userid']),
    }
    return render(request, 'home.html', context)

def new_trip(request):
    return render(request, 'new_trip.html')

def create_trip(request):
    errors = Trip.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request,val)
    else:
        Trip.objects.create(
            destination = request.POST['destination'],
            date_from = request.POST['date_from'],
            date_to = request.POST['date_to'],
            description = request.POST['description'],
            uploaded_by_id = User.objects.get(id=request.session['userid'])
        )
    return redirect(f'/trip/{trip_id}')

def trip_info(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id)
    }
    request render(request, 'trip.html', context)

def search_trip(request):
    context = {
        'all_trips': Trip.objects.all(),
        
    }
    return render(request, 'search.html', context)

def edit_trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id)
    }
    return render(request, 'edit_trip.html', context)

def update_trip(request, trip_id):
    errors = Trip.objects.validator(request.POST, trip_id)
    if errors: 
        for val in errors.values():
            messages.error(request,val)
    else:
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination'],
        trip.date_from = request.POST['date_from'],
        trip.date_to = request.POST['date_to'],
        trip.description = request.POST['description'],
        trip.uploaded_by_id = User.objects.get(id=request.session['userid'])
        trip.save()
        messages.success(request, 'Succesfully updated trip!')
    return redirect(f'/trip/{trip_id}')

def delete_trip(request, trip_id):
    delete_trip = Trip.objects.get(id=trip_id)
    delete_trip.delete()
    return redirect('/trip')

def user_profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'user_profile.html', context)

def edit_your_profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'your_profile.html', context)

def update_your_profile(request, user_id):
    errors = User.objects.edit_validator(request.POST, user_id)
    if errors: 
        for val in errors.values():
            messages.error(request,val)
    else:
        user = User.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'Succesfully updated account!')
    return redirect(f'/user/{user_id}/edit')

def delete_your_profile(request, user_id):
    delete_user = User.objects.get(id=user_id)
    delete_user.delete()
    return redirect('/')