from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login_user', views.login_user),
    path('register', views.register_page),
    path('register_user', views.register_user),
    path('logout', views.logout),
    path('trip', views.home),
    path('/trip/new', views.new_trip),
    path('/trip/create', views.create_trip),
    path('/trip/search', views.search_trip),
    path('/trip/<int:trip_id>', views.trip_info),
    path('/trip/<int:trip_id>/edit', views.edit_trip),
    path('/trip/<int:trip_id>/delete', views.delete_trip),
    path('/trip/<int:user_id>', views.user_profile),
    path('/user/<int:user_id>/edit', views.edit_your_profile),
    path('/user/<int:user_id>/update', views.update_your_profile),
    path('/user/<int:user_id>/delete', views.delete_your_profile),

]
