from rest_framework import serializers
from adminapp.models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = '__all__'
from rest_framework import serializers
from .models import HospitalDoctorFeedback, HospitalDoctorTimeSlotGroup, tbl_register

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_register
        fields = '__all__'

from rest_framework import serializers
from .models import tbl_register

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


from rest_framework import serializers
from .models import CycleInput

class CycleInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CycleInput
        fields = '__all__' 



from adminapp.models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"


from rest_framework import serializers
from adminapp.models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        # This includes: id, category, name, description, quantity, price, image, created_at, category_name

    def get_image(self, obj):
        # return the media-relative path (e.g. "/media/...")
        if obj.image:
            return obj.image.url  # typically starts with '/media/...'
        return None







#cart and booking serializers
from rest_framework import serializers
from .models import ProductBooking, BookingPayment, Cart, CartPayment

class ProductBookingSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    user_name = serializers.CharField(source='user.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ProductBooking
        fields = [
            'id', 'user_id', 'user_name',
            'product_id', 'product_name', 'category_name',
            'quantity', 'total_price', 'status', 'booking_date'
        ]

class BookingPaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    product_name = serializers.CharField(source='booking.product.name', read_only=True)

    class Meta:
        model = BookingPayment
        fields = [
            'id', 'payment_choice',
            'booking', 'user', 'user_name', 'product_name',
            'payment_type', 'status',
            'card_holder_name', 'card_number', 'expiry_date', 'cvv',
            'total_amount', 'created_at'
        ]


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user_id', 'product_id',
            'product_name', 'product_image', 'category_name',
            'quantity', 'total_price', 'status', 'created_at'
        ]
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        if instance.product.image:
            rep['product_image'] = instance.product.image.url  # returns /media/...
        else:
            rep['product_image'] = None

        return rep


class CartPaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = CartPayment
        fields = [
            'id', 'payment_choice',
            'user', 'user_name', 'cart_ids',
            'payment_type', 'status',
            'card_holder_name', 'card_number', 'expiry_date', 'cvv',
            'total_amount', 'created_at'
        ]




from rest_framework import serializers
from .models import tbl_hospital_doctor_register

class HospitalDoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_hospital_doctor_register
        exclude = ['available']  # 👈 hide from Swagger input

    def create(self, validated_data):
        # 👇 Always mark new hospital doctors as available by default
        validated_data['available'] = True
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        if instance.medical_id:
            rep['medical_id'] = instance.medical_id.url
        rep['available'] = instance.available  # 👈 show in API response
        return rep


from rest_framework import serializers
from .models import TblPredictionResult

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPredictionResult
        fields = "__all__"
        read_only_fields = ("result", "extracted_data", "created_at")


from rest_framework import serializers
from .models import tbl_hospital_doctor_register

class HospitalDoctorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_hospital_doctor_register
        fields = [
            'name', 'email', 'qualification', 'specialization', 'experience',
            'hospital_address', 'hospital_phone', 'latitude', 'longitude', 'age',
            'gender', 'place', 'image', 'medical_id','hospital_name'
        ]
        extra_kwargs = {
            'email': {'required': False},
        }





class HospitalDoctorTimeSlotGroupSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    timeslots = serializers.ListField(
        child=serializers.CharField(), required=False
    )  # ✅ accept list of time strings like ["10:00", "10:30"]

    class Meta:
        model = HospitalDoctorTimeSlotGroup
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time', 'end_time', 'timeslots']




class HospitalDoctorFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = HospitalDoctorFeedback
        fields = ['id', 'user', 'user_name', 'doctor', 'doctor_name', 'rating', 'comments', 'created_at']
        