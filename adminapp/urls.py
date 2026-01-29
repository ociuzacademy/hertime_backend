from django.urls import path
from . import views
urlpatterns = [
    path('',views.login,name='admin_login'),
    path('index/',views.index,name='index'),
    path('calendar/',views.calendar,name='calendar'),
    path('categories/', views.category_page, name="category_page"),
    path('category/delete/<int:id>/', views.delete_category, name="delete_category"),
    path("add-product/", views.add_product, name="add_product"),
    path("products/", views.view_products, name="view_products"),
    path("edit-product/<int:pk>/", views.edit_product, name="edit_product"),
    path("delete-product/<int:pk>/", views.delete_product, name="delete_product"),
    path("add-book/", views.add_book, name="add_book"),
    path("books/", views.view_books, name="view_books"),
    path("edit-book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete-book/<int:pk>/", views.delete_book, name="delete_book"),
    path("admin-view-orders/", views.admin_view_orders, name="admin_view_orders"),
    path("admin/users/", views.admin_view_users, name="admin_view_users"),
    path('admin/order-details/<str:order_type>/<int:order_id>/', views.admin_order_details, name='admin_order_details'),
    
    path('view_pending_doctors/', views.view_pending_doctors, name='view_pending_doctors'),
    path('view-all-bookings/', views.admin_view_hospital_bookings, name='view_all_bookings'),
    # Hospital Doctor Actions
    path('approve_hospital_doctor/<int:doctor_id>/', views.approve_hospital_doctor, name='approve_hospital_doctor'),
    path('reject_hospital_doctor/<int:doctor_id>/', views.reject_hospital_doctor, name='reject_hospital_doctor'),

    path('view_approved_doctors/', views.view_approved_doctors, name='view_approved_doctors'),

    path('view_rejected_doctors/', views.view_rejected_doctors, name='view_rejected_doctors'),

]