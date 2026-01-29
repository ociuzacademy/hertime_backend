# urls.py
from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .import views
from .views import *

from userapp.views import ChatbotAPIView, ProductByCategory, ProductDetailView, login_view,CycleInputViewSet,get_cycle_inputs_by_user,UserViewBook,UserViewProduct,UserViewCategory   

schema_view = get_schema_view(
   openapi.Info(
      title="Hertime App API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Define the router and register the viewset
router = DefaultRouter()
router.register(r'register',tbl_registerViewSet,basename='register')
router.register(r'cycle-inputs', CycleInputViewSet, basename='cycle-input')
router.register(r'hospital_doctors', HospitalDoctorRegisterViewSet,basename='doctor_register')
router.register(r'hospital_doctor_timeslots', HospitalDoctorTimeSlotGroupViewSet, basename='hospital_doctor_timeslot')
hospital_doctor_profile_update = HospitalDoctorProfileViewSet.as_view({
    'patch': 'partial_update'
})



urlpatterns = [
   path('', include(router.urls)),  # Now /api/register/ will work
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path("chatbot/", ChatbotAPIView.as_view(), name="chatbot_api"),
   path("login/", login_view, name="login"),
   path("cycle-inputs/user/<int:user_id>/", get_cycle_inputs_by_user, name="cycle_inputs_by_user"),
   # path('chatbot_view/', chatbot_view, name='chatbot_view'),
   path("user_view_book/", UserViewBook.as_view(), name="user_view_book"),
   path('user_view_category/',UserViewCategory.as_view(),name='user_view_category'),
   path("products/", UserViewProduct.as_view(), name="user_view_product"),
   path("products/category/<int:category_id>/", ProductByCategory.as_view(), name="products_by_category"),
   path("product/<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
   path('product-bookings/', ProductBookingView.as_view(),name='product_booking'),
   path('booking-payment/', BookingPaymentView.as_view(),name='booking_payment'),
   path('cart/<int:product_id>/', CartCreateView.as_view(),name='add_to_cart'),
   path('update-cart-quantity/', UpdateCartQuantity.as_view(), name='update_cart_quantity'),
   path('remove-cart-item/<int:cart_id>/', RemoveCartItem.as_view(), name='remove_cart_item'),

   path('user-cart/<int:user_id>/', ViewCart.as_view(),name='view_cart'),
   path('cart-payments/', CartPaymentView.as_view(),name='cart_payment'),
   path('my-orders/<int:user_id>/', MyOrdersView.as_view(),name='my_orders'),

   path("predict/", PCODPredictionAPI.as_view(), name="pcod_predict"),
   path("user/cancel-booking/<int:booking_id>/<int:user_id>/",UserCancelBookingAPI.as_view(),name="user_cancel_booking"),
   path("doctor/cancel-booking/<int:booking_id>/<int:doctor_id>/",DoctorCancelBookingAPI.as_view(),name="doctor_cancel_booking"),
   path("doctor/complete-booking/<int:booking_id>/<int:doctor_id>/",DoctorCompleteBookingAPI.as_view(),name="doctor_complete_booking"),

    # path("cycle-inputs/user/<int:user_id>/", get_cycle_inputs_by_user, name="cycle_inputs_by_user"),
   path('view_hospital_doctor/<int:doctor_id>/', views.view_hospital_doctor_profile, name='view_hospital_doctor_profile'),
   path('hospital_doctor/update/<int:pk>/', hospital_doctor_profile_update, name='hospital_doctor_profile_update'),
   path('hospital-doctor/<int:doctor_id>/availability/', views.update_hospital_doctor_availability, name='update_hospital_doctor_availability'),
   path('hospital/doctor/<int:doctor_id>/timeslots/', view_hospital_doctor_timeslots, name='view_hospital_doctor_timeslots'),
   path('view_nearby_hospital_doctors/<int:user_id>/', views.view_nearby_hospital_doctors, name='view_nearby_hospital_doctors'),
   path('user-hospital/doctor/feedback/add/', views.add_hospital_doctor_feedback, name='add_hospital_doctor_feedback'),
   path('hospital/doctor/<int:doctor_id>/feedback/', views.view_hospital_doctor_feedback, name='view_hospital_doctor_feedback'),
   path('doctor/<int:doctor_id>/feedback/', GetDoctorFeedbackAPI.as_view(), name='doctor_feedback'),
   path('hospital/doctor/book-slot/', views.book_hospital_doctor_slot, name='book_hospital_doctor_slot'),
   path('user/<int:user_id>/hospital/bookings/', views.user_view_booking_hospital.as_view(), name='user_view_hospital_bookings'),
   path('hospital/doctor/<int:doctor_id>/bookings/', views.doctor_view_booking_hospital.as_view(), name='doctor_view_booking_hospital'),
   path('prediction-results/<int:user_id>/', ViewPredictionResultsByUser.as_view(), name='view_prediction_results_by_user'),
] 


















# http://127.0.0.1:8002/medico/chat_download_pdf/2/1/