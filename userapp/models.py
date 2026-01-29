from django.db import models

# Create your models here.


class tbl_register(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.IntegerField(default=1)
    user_type = models.CharField(default='user', max_length=50)


    def __str__(self):
        return self.name



from django.db import models
from userapp.models import tbl_register   # import your user table

class CycleInput(models.Model):

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name="cycle_inputs")
    last_day_of_period = models.DateField()
    duration = models.IntegerField(help_text="Duration of period in days")
    flow_intensity = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True, help_text="List symptoms like cramps, headache, etc.")
    description = models.TextField(blank=True, null=True)
    average_cycle_length = models.IntegerField(help_text="Average cycle length in days", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cycle input for {self.user.name} on {self.last_day_of_period}"






#Product purchase and cart purhase
from django.db import models
from adminapp.models import Category, Product
from userapp.models import tbl_register

class ProductBooking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()   # Flutter sends this
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.name}"


class BookingPayment(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash on Delivery'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    payment_choice = models.CharField(max_length=20, default='booking_payment')

    booking = models.OneToOneField(ProductBooking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')

    # Card only
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)  # last 4 digits only
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)

    total_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Cart(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()  # Flutter sends
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.name}"


class CartPayment(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash on Delivery'),
    ]

    payment_choice = models.CharField(max_length=20, default='cart_payment')

    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    cart_ids = models.JSONField(default=list)   # [1,2,3]

    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, default='completed')

    # Card only
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)

    total_amount = models.FloatField(default=0)   # Flutter sends
    created_at = models.DateTimeField(auto_now_add=True)





# ✅ Hospital Doctor Model
class tbl_hospital_doctor_register(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    hospital_address = models.TextField(null=True, blank=True)
    hospital_phone = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    role = models.CharField(max_length=30, default='hospital_doctor')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='hospital_doctor_images/', null=True, blank=True)
    medical_id = models.ImageField(upload_to='hospital_medical_ids/', null=True, blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return self.name






#pcod prediction model
from django.db import models
from .models import tbl_register   # your user model


class TblPredictionResult(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    bmi = models.FloatField(default=0)

    fast_food_consumption = models.CharField(max_length=50, default="0")
    blood_group = models.CharField(max_length=10, default="Unknown")
    cycle_regularity = models.CharField(max_length=50, default="0")

    hair_growth = models.CharField(max_length=50, default="0")
    acne = models.CharField(max_length=50, default="0")
    mood_swings = models.CharField(max_length=50, default="0")
    skin_darkening = models.CharField(max_length=50, default="0")

    pdf_file = models.FileField(upload_to="medical_reports/")
    result = models.CharField(max_length=50, default="Pending")
    extracted_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} → {self.result}"




class HospitalDoctorTimeSlotGroup(models.Model):
    doctor = models.ForeignKey('tbl_hospital_doctor_register', on_delete=models.CASCADE, related_name='slot_groups')
    date = models.DateField()
    start_time = models.TimeField()   # doctor’s working start time
    end_time = models.TimeField()     # doctor’s working end time
    timeslots = models.JSONField(default=list, blank=True)  # ✅ store list of selected times

    def __str__(self):
        return f"{self.doctor.name} - {self.date} ({self.start_time} to {self.end_time})"





class HospitalBooking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    doctor = models.ForeignKey(tbl_hospital_doctor_register, on_delete=models.SET_NULL, null=True, blank=True)
    timeslot_group = models.ForeignKey(HospitalDoctorTimeSlotGroup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='booked')
    is_booked = models.BooleanField(default=True)

    def __str__(self):
        if self.doctor:
            return f"{self.user.name} booked {self.doctor.name} at {self.time} on {self.date}"
        return f"{self.user.name} booked (Doctor deleted) at {self.time} on {self.date}"






class HospitalDoctorFeedback(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE, related_name='hospital_feedbacks')
    doctor = models.ForeignKey('tbl_hospital_doctor_register', on_delete=models.CASCADE, related_name='hospital_feedbacks')
    rating = models.IntegerField()  # e.g., 1–5 stars
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.doctor.name}"

