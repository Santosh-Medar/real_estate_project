# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #index page
    path('', views.home, name='home'),

    #Landing pages
    path('landing/seller/', views.seller_landing_page, name='seller_landing_page'),
    path('landing/buyer/', views.buyer_landing_page, name='buyer_landing_page'), 
    path('landing/admin/', views.admin_landing_page, name='admin_landing_page'),

    #Registration
    path('register/buyer/', views.buyer_register, name='buyer_register'),
    path('register/seller/', views.seller_register, name='seller_register'),

    #Login
    path('login/buyer/', views.buyer_login, name='buyer_login'),
    path('login/seller/', views.seller_login, name='seller_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    
    #Logout
    path('logout/', views.logout_view, name='logout'),

    # Placeholders for dashboards (we will create these views next)
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'), 
    # Admin dashboard usually defaults to /admin, but if you want a custom one:
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Property Actions (New)
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/add/', views.add_property, name='add_property'),
    path('property/delete/<int:pk>/', views.delete_property, name='delete_property'),
    path('property/edit/<int:pk>/', views.edit_property, name='edit_property'),
    
    path('property/view/<int:pk>/', views.view_property, name='view_property'),
    path('property/approve/<int:pk>/', views.approve_property, name='approve_property'),
    path('property/reject/<int:pk>/', views.reject_property, name='reject_property'),
    path('api/admin/property/<int:id>/remove/', views.remove_property, name='remove_property'),

    path("api/seller/properties/", views.seller_properties_api, name="seller_properties_api"),
    path("api/properties/delete/<int:id>/", views.delete_property_api, name="delete_property_api"),
    path("api/properties/all/", views.all_properties_api, name="all_properties_api"),
    path("api/admin/properties/approved/", views.all_properties_api, name="approved_properties_api"),
    path("api/admin/properties/pending/", views.pending_properties, name="pending_properties_api"),
# ...
]