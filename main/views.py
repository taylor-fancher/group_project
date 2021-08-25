from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

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
    errors = User.objects.validator(request.POST) 
    if errors:
        for key, val in errors.items():
            messages.error(request,val)
        return redirect('/register')
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
    return redirect('/register')

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    context = {
        'user': User.objects.get(id=request.session['userid']),
        'trips': Trip.objects.filter(uploaded_by_id=request.session['userid'])
    }
    return render(request, 'home.html', context)

def new_trip(request):
    return render(request, 'new_trip.html')

def create_trip(request):
    errors = Trip.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request,val)
        return redirect('/trip/new')
    else:
        trip1 = Trip.objects.create(
            destination = request.POST['destination'],
            date_from = request.POST['date_from'],
            date_to = request.POST['date_to'],
            description = request.POST['description'],
            spotify = request.POST['spotify'],
            uploaded_by_id = User.objects.get(id=request.session['userid'])
        )
        return redirect(f'/trip/{trip1.id}')

def trip_info(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id)
    }
    return render(request, 'trip.html', context)

def search_trip(request):
    context = {
        'trips': Trip.objects.all(),
        
    }
    return render(request, 'search.html', context)

def search(request):
    query = request.POST['query']
    users = User.objects.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query))
    trips = Trip.objects.filter(Q(destination__icontains = query))
    context =  {
        'users': users,
        'trips': trips,
    }
    return render(request, 'search_results.html', context)

def edit_trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id)
    }
    return render(request, 'edit_trip.html', context)

def add_trip_photo(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
    }
    return render(request, 'trip_upload.html', context)

def trip_upload(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.image.add(request.POST['image'])
    trip.save()
    return redirect(f'/trip/{trip.id}')

def update_trip(request, trip_id):
    errors = Trip.objects.validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request,val)
        return redirect(f'/trip/{trip_id}/edit')
    else:
        trip = Trip.objects.get(id=trip_id)
        trip.destination = request.POST['destination']
        trip.date_from = request.POST['date_from']
        trip.date_to = request.POST['date_to']
        trip.description = request.POST['description']
        trip.spotify = request.POST['spotify']
        trip.save()
        messages.success(request, 'Succesfully updated trip!')
    return redirect(f'/trip/{trip_id}')

def delete_trip(request, trip_id):
    delete_trip = Trip.objects.get(id=trip_id)
    delete_trip.delete()
    return redirect('/trip')

def user_profile(request, user_id):
    context = {
        'this_user': User.objects.get(id=user_id),
        'trips': Trip.objects.filter(uploaded_by_id=request.session['userid'])
    }
    return render(request, 'user_profile.html', context)

def add_profile_photo(request, user_id):
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'profile_upload.html', context)

def profile_upload(request, user_id):
    user = User.objects.get(id=user_id)
    user.profile_pic = request.POST['profile_pic']
    user.save()
    return redirect(f'/user/{user_id}')


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
        return redirect(f'/user/{user_id}/edit')
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
    request.session.clear()
    return redirect('/')