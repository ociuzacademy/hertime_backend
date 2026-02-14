from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -----------------------------------------
# Load Environment Variables
# -----------------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")
else:
    print(f"✅ API Key loaded: {api_key[:10]}...")

# -----------------------------------------
# Configure Gemini
# -----------------------------------------
genai.configure(api_key=api_key)

# IMPORTANT: Use unique variable name to avoid
# conflict with ML models like RandomForest
gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------------------
# Keywords
# -----------------------------------------

PERIOD_KEYWORDS = [
    "period", "menstrual", "menstruation", "pms", "cramps",
    "cycle", "bleeding", "ovulation", "menopause", "fertility",
    "flow", "spotting", "pads", "tampons", "menstrual cup",
    "dysmenorrhea", "amenorrhea", "menorrhagia", "endometriosis",
    "fibroids", "ovaries", "uterus", "hormones", "estrogen",
    "progesterone", "follicular phase", "luteal phase",
    "perimenopause", "pcos", "pmdd", "periods",
    "relief", "medication", "pain relief", "cramp relief",
    "medicines", "medicine", "book", "books",
    "suggestions", "suggestion", "skin care",
    "tips", "advice"
]

GREETINGS = [
    "hi", "hello", "hey",
    "good morning", "good evening", "good afternoon"
]


# -----------------------------------------
# Chatbot API View
# -----------------------------------------

class ChatbotAPIView(APIView):

    def post(self, request):
        user_message = request.data.get("message", "").strip().lower()

        if not user_message:
            return Response(
                {
                    "type": "error",
                    "reply": "Message is empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Greeting check
        if any(greet in user_message for greet in GREETINGS):
            return Response(
                {
                    "type": "greeting",
                    "reply": "Hello! 😊 I'm Her Time, your menstrual health assistant. You can ask me about periods, ovulation, PMS, or cycle tracking."
                }
            )

        # Check topic relevance
        if not any(keyword in user_message for keyword in PERIOD_KEYWORDS):
            return Response(
                {
                    "type": "not_related",
                    "reply": "I can only answer questions related to menstrual health, periods, ovulation, and PMS."
                }
            )

        try:
            # Generate response from Gemini
            response = gemini_model.generate_content(
                f"""
                You are a professional menstrual health assistant.

                Only answer questions related to:
                - Periods
                - Menstrual cycles
                - PMS
                - Ovulation
                - Hormonal health

                Give safe, helpful, and medically responsible advice.

                Question: {user_message}
                """
            )

            return Response(
                {
                    "type": "period_info",
                    "reply": response.text
                }
            )

        except Exception as e:
            return Response(
                {
                    "type": "error",
                    "reply": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





from rest_framework import viewsets

from .models import HospitalDoctorTimeSlotGroup, tbl_register, tbl_hospital_doctor_register
from userapp.serializers import HospitalDoctorRegisterSerializer, HospitalDoctorTimeSlotGroupSerializer, HospitalDoctorProfileUpdateSerializer
#  Hospital Doctor ViewSet
class HospitalDoctorRegisterViewSet(viewsets.ModelViewSet):
    queryset = tbl_hospital_doctor_register.objects.all()
    serializer_class = HospitalDoctorRegisterSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    


from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

# from houseprojectapp.utils.material_budget import get_material_budget

from .models import  tbl_register

from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class tbl_registerViewSet(viewsets.ModelViewSet):
    queryset =tbl_register.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User tbl_registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register
from .serializers import LoginSerializer

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = tbl_register.objects.get(email=email, password=password)
            return Response({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password  # ⚠️ Usually we should NOT send plain password, but you asked for it
            }, status=status.HTTP_200_OK)

        except tbl_register.DoesNotExist:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import viewsets
from .models import CycleInput
from .serializers import CycleInputSerializer

class CycleInputViewSet(viewsets.ModelViewSet):
    queryset = CycleInput.objects.all()
    serializer_class = CycleInputSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CycleInput
from .serializers import CycleInputSerializer,BookSerializer
from adminapp.models import Book

@api_view(["GET"])
def get_cycle_inputs_by_user(request, user_id):
    try:
        inputs = CycleInput.objects.filter(user_id=user_id).order_by("-created_at")
        serializer = CycleInputSerializer(inputs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CycleInput.DoesNotExist:
        return Response({"error": "No cycle inputs found for this user."}, status=status.HTTP_404_NOT_FOUND)



class UserViewBook(APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    
from adminapp.models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewCategory(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class UserViewProduct(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from adminapp.models import Product
from .serializers import ProductSerializer

class ProductByCategory(APIView):
    def get(self, request, category_id, *args, **kwargs):
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import Product
from .serializers import ProductSerializer

class ProductDetailView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)



#product booking and cart purchase
from .serializers import *
class ProductBookingView(APIView):
    def post(self, request):
        serializer = ProductBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        total_price = serializer.validated_data['total_price']

        user = get_object_or_404(tbl_register, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        booking = ProductBooking.objects.create(
            user=user,
            product=product,
            category=product.category,
            quantity=quantity,
            total_price=total_price,
            status='completed'
        )

        return Response({
            "status": "success",
            "booking": ProductBookingSerializer(booking).data
        }, status=201)


class BookingPaymentView(APIView):
    def post(self, request):
        serializer = BookingPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(payment_choice="booking_payment")
        return Response({"status": "success", "payment": serializer.data}, status=201)
    
class CartCreateView(APIView):
    def post(self, request, product_id):
        user_id = request.data.get("user_id")
        quantity = int(request.data.get("quantity", 1))
        total_price = request.data.get("total_price")

        user = get_object_or_404(tbl_register, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        item = Cart.objects.create(
            user=user,
            product=product,
            category=product.category,
            quantity=quantity,
            total_price=total_price,
        )
        return Response({"status": "success", "cart": CartSerializer(item).data}, status=201)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer

class UpdateCartQuantity(APIView):
    def patch(self, request):
        cart_id = request.data.get("cart_id")
        quantity = request.data.get("quantity")
        total_price = request.data.get("total_price")  # Flutter sends this

        if not cart_id or not quantity:
            return Response(
                {"error": "cart_id and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = get_object_or_404(Cart, id=cart_id)

        # Remove item if quantity is 0
        if int(quantity) <= 0:
            cart_item.delete()
            return Response(
                {"message": "Item removed from cart because quantity is 0."},
                status=status.HTTP_200_OK
            )

        cart_item.quantity = int(quantity)

        # Flutter calculates total price, so update only if sent
        if total_price is not None:
            cart_item.total_price = total_price

        cart_item.save()

        return Response({
            "message": "Cart quantity updated successfully.",
            "cart": CartSerializer(cart_item).data
        }, status=status.HTTP_200_OK)
class RemoveCartItem(APIView):
    def delete(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.delete()

        return Response(
            {"status": "success", "message": "Cart item removed"},
            status=200
        )


class ViewCart(APIView):
    def get(self, request, user_id):
        cart = Cart.objects.filter(user_id=user_id, status="pending")
        data = CartSerializer(cart, many=True, context={'request': request}).data
        return Response({"cart": data})
class CartPaymentView(APIView):
    def post(self, request):
        serializer = CartPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pay = serializer.save(payment_choice="cart_payment")

        # ✅ UPDATE CART STATUS AFTER SUCCESSFUL PAYMENT
        cart_ids = pay.cart_ids          # e.g., [1,2,3]
        Cart.objects.filter(id__in=cart_ids).update(status="completed")

        return Response({
            "status": "success",
            "message": "Payment successful and cart status updated",
            "payment": serializer.data
        }, status=201)

# class MyOrdersView(APIView):
#     def get(self, request, user_id):
#         orders = []

#         bookings = ProductBooking.objects.filter(user_id=user_id)
#         for b in bookings:
#             pay = getattr(b, 'payment', None)
#             orders.append({
#                 # "type": "single_product",
#                 "product": b.product.name,
#                 "quantity": b.quantity,
#                 "total_price": b.total_price,
#                 "product_image": product_image_url,
#                 "payment_type": pay.payment_type if pay else None,
#                 "payment_status": pay.status if pay else None,
#             })

#         carts = Cart.objects.filter(user_id=user_id)
#         for c in carts:
#             pay = CartPayment.objects.filter(user_id=user_id, cart_ids__contains=[c.id]).first()
#             orders.append({
#                 # "type": "cart_item",
#                 "product": c.product.name,
#                 "quantity": c.quantity,
#                 "total_price": c.total_price,
#                 "product_image": product_image_url,
#                 "payment_type": pay.payment_type if pay else None,
#                 "payment_status": pay.status if pay else None,
#             })

#         return Response({"orders": orders})

class MyOrdersView(APIView):
    def get(self, request, user_id):
        orders = []

        # ----------- PRODUCT BOOKINGS ----------
        bookings = ProductBooking.objects.filter(user_id=user_id)
        for b in bookings:

            # ✅ Only /media/... 
            product_image_url = b.product.image.url if b.product.image else None

            pay = getattr(b, 'payment', None)

            orders.append({
                "product": b.product.name,
                "quantity": b.quantity,
                "total_price": b.total_price,
                "product_image": product_image_url,
                "payment_type": pay.payment_type if pay else None,
                "payment_status": pay.status if pay else None,
            })

        # ----------- CART PURCHASES ----------
        carts = Cart.objects.filter(user_id=user_id)
        for c in carts:

            # ✅ Only /media/...
            product_image_url = c.product.image.url if c.product.image else None

            pay = CartPayment.objects.filter(
                user_id=user_id,
                cart_ids__contains=[c.id]
            ).first()

            orders.append({
                "product": c.product.name,
                "quantity": c.quantity,
                "total_price": c.total_price,
                "product_image": product_image_url,
                "payment_type": pay.payment_type if pay else None,
                "payment_status": pay.status if pay else None,
            })

        return Response({"orders": orders})







#  Hospital Doctor ViewSet
class HospitalDoctorRegisterViewSet(viewsets.ModelViewSet):
    queryset = tbl_hospital_doctor_register.objects.all()
    serializer_class = HospitalDoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import  TblPredictionResult
from userapp.ml_assets.ml_utils import (
    model, scaler, pcod_label_encoder,
    map_fast_food, encode_blood_group,
    map_cycle, map_severity,
    extract_medical_values, prepare_final_df
)


class PCODPredictionAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            user = tbl_register.objects.get(id=request.data.get("user_id"))

            # -----------------------------
            # BASIC INPUTS
            # -----------------------------
            age = float(request.data.get("age"))
            weight = float(request.data.get("weight"))
            height = float(request.data.get("height"))
            bmi = float(request.data.get("bmi"))

            fast_food = request.data.get("fast_food")
            blood_group = request.data.get("blood_group")
            cycle = request.data.get("cycle")

            hair = request.data.get("hair")
            acne = request.data.get("acne")
            mood = request.data.get("mood_swings")
            skin = request.data.get("skin_darkening")

            # -----------------------------
            # ML INPUT
            # -----------------------------
            user_input = {
                "Age": age,
                "Weight": weight,
                "Height": height,
                "BMI": bmi,
                "Fast_Food_Consumption": map_fast_food(fast_food),
                "Blood_Group": encode_blood_group(blood_group),
                "Cycle_Regularity": map_cycle(cycle),
                "Hair_Growth": map_severity(hair),
                "Acne": map_severity(acne),
                "Mood_Swings": map_severity(mood),
                "Skin_Darkening": map_severity(skin),
            }

            # -----------------------------
            # SAVE INPUT + PDF
            # -----------------------------
            pdf_file = request.FILES["pdf"]

            saved_obj = TblPredictionResult.objects.create(
                user=user,
                age=age,
                weight=weight,
                height=height,
                bmi=bmi,
                fast_food_consumption=fast_food,
                blood_group=blood_group,
                cycle_regularity=cycle,
                hair_growth=hair,
                acne=acne,
                mood_swings=mood,
                skin_darkening=skin,
                pdf_file=pdf_file
            )

            # -----------------------------
            # PDF EXTRACTION
            # -----------------------------
            pdf_values = extract_medical_values(saved_obj.pdf_file.path)

            # -----------------------------
            # PREPARE + SCALE
            # -----------------------------
            df = prepare_final_df(user_input, pdf_values)
            df_scaled = scaler.transform(df)

            # -----------------------------
            # PROBABILITY-BASED PREDICTION
            # -----------------------------
            proba = model.predict_proba(df_scaled)[0]
            classes = pcod_label_encoder.classes_
            prob_map = dict(zip(classes, proba))

            if prob_map.get("High Risk", 0) >= 0.6:
                result_label = "High Risk"
            elif prob_map.get("Likely", 0) >= 0.12:
                result_label = "Likely"
            else:
                result_label = "Unlikely"

            # -----------------------------
            # SAVE RESULT
            # -----------------------------
            saved_obj.result = result_label
            saved_obj.extracted_data = {
                "pdf_values": pdf_values,
                "probabilities": prob_map
            }
            saved_obj.save()

            return Response({
                "status": "success",
                "message": "PCOD prediction generated successfully",
                "user_id": user.id,
                "user_name": user.name,
                "prediction_id": saved_obj.id,
                "result": result_label,
                "probabilities": prob_map,
                "user_inputs": user_input,
                "extracted_pdf_values": pdf_values
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

from adminapp.models import Book
from userapp.serializers import BookSerializer
class UserViewBook(APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalBooking
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalBooking, tbl_register

class UserCancelBookingAPI(APIView):
    def post(self, request, booking_id, user_id):
        try:
            booking = HospitalBooking.objects.get(id=booking_id)
            user = tbl_register.objects.get(id=user_id)

            # 🔒 Ensure booking belongs to this user
            if booking.user != user:
                return Response(
                    {"error": "You are not authorized to cancel this booking"},
                    status=status.HTTP_403_FORBIDDEN
                )

            if booking.status.startswith("cancelled"):
                return Response(
                    {"message": "Booking already cancelled"},
                    status=status.HTTP_200_OK
                )

            booking.status = "cancelled_by_user"
            booking.is_booked = False
            booking.save()

            return Response({
                "status": "success",
                "message": "Booking cancelled by user",
                "booking_id": booking.id,
                "date": booking.date,
                "time": booking.time
            }, status=status.HTTP_200_OK)

        except HospitalBooking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except tbl_register.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )







#Doctor


@api_view(['GET'])
def view_hospital_doctor_profile(request, doctor_id):
    try:
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except tbl_hospital_doctor_register.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = tbl_hospital_doctor_register(doctor)
    return Response(serializer.data, status=status.HTTP_200_OK)




class HospitalDoctorProfileViewSet(viewsets.ViewSet):
    """
    A ViewSet for updating hospital doctor profiles (partial or full updates).
    """

    def partial_update(self, request, pk=None):
        try:
            doctor = tbl_hospital_doctor_register.objects.get(pk=pk)
        except tbl_hospital_doctor_register.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalDoctorProfileUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import viewsets
from .models import HospitalDoctorTimeSlotGroup
from .serializers import HospitalDoctorTimeSlotGroupSerializer

class HospitalDoctorTimeSlotGroupViewSet(viewsets.ModelViewSet):
    queryset = HospitalDoctorTimeSlotGroup.objects.all().order_by('-date')
    serializer_class = HospitalDoctorTimeSlotGroupSerializer







# ✅ View all available hospital doctor time slots
@api_view(['GET'])
def view_hospital_doctor_timeslots(request, doctor_id):
    """
    Get all time slot groups for a hospital doctor with booking info.
    """
    try:
        groups = HospitalDoctorTimeSlotGroup.objects.filter(doctor_id=doctor_id).order_by('date')

        if not groups.exists():
            return Response({"message": "No time slots found for this doctor."}, status=status.HTTP_404_NOT_FOUND)

        result = []
        for group in groups:
            # ✅ Already booked times for that date
            booked_times = list(
                HospitalBooking.objects.filter(
                    doctor_id=doctor_id,
                    date=group.date
                ).values_list('time', flat=True)
            )

            # Normalize booked times (e.g. "10:00:00" → "10:00")
            booked_times = [t[:5] for t in booked_times]

            result.append({
                "id": group.id,
                "doctor": group.doctor.id,
                "doctor_name": group.doctor.name,
                "date": group.date,
                "start_time": group.start_time.strftime("%H:%M:%S"),
                "end_time": group.end_time.strftime("%H:%M:%S"),
                "timeslots": [
                    {"time": t, "is_booked": t in booked_times}
                    for t in group.timeslots
                ],
            })

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['POST'])
def update_hospital_doctor_availability(request, doctor_id):
    try:
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except tbl_hospital_doctor_register.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    available = request.data.get('available')

    if available is None:
        return Response({"error": "Availability value required (true/false)"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert to boolean
    if isinstance(available, str):
        available = available.lower() in ['true', '1', 'yes']

    doctor.available = available
    doctor.save()

    return Response({
        "message": "Availability updated successfully",
        "doctor_id": doctor.id,
        "available": doctor.available
    }, status=status.HTTP_200_OK)




@api_view(['GET'])
def view_nearby_hospital_doctors(request, user_id):
    """
    Get all approved and available hospital doctors 
    who are in the same place as the user.
    """
    try:
        user = tbl_register.objects.get(id=user_id)
    except tbl_register.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not user.place:
        return Response({"error": "User place not available"}, status=400)

    # ✅ Only approved & available doctors in the same place
    doctors = tbl_hospital_doctor_register.objects.filter(
        status='approved', available=True, place__iexact=user.place
    )

    if not doctors.exists():
        return Response({"message": "No nearby hospital doctors found in your area."}, status=200)

    nearby_doctors = []
    for doctor in doctors:
        nearby_doctors.append({
            "id": doctor.id,
            "name": doctor.name,
            "qualification": doctor.qualification,
            "specialization": doctor.specialization,
            "experience": doctor.experience,
            "phone": doctor.hospital_phone,
            "hospital_name": doctor.hospital_name,
            "hospital_address": doctor.hospital_address,
            "place": doctor.place,
            "available": doctor.available,
            "image": doctor.image.url if doctor.image else None,
            "status": doctor.status,
        })

    return Response({"nearby_hospital_doctors": nearby_doctors})




# ✅ Book a hospital doctor time slot (same logic as clinic)
@api_view(['POST'])
def book_hospital_doctor_slot(request):
    """
    Book a specific time slot for a hospital doctor.

    Expected JSON:
    {
        "user": 1,
        "doctor": 3,
        "timeslot_group": 5,
        "date": "2025-11-01",
        "time": "09:30"
    }
    """
    data = request.data

    try:
        user = tbl_register.objects.get(id=data['user'])
        doctor = tbl_hospital_doctor_register.objects.get(id=data['doctor'])
        timeslot_group = HospitalDoctorTimeSlotGroup.objects.get(id=data['timeslot_group'])
    except (tbl_register.DoesNotExist, tbl_hospital_doctor_register.DoesNotExist, HospitalDoctorTimeSlotGroup.DoesNotExist):
        return Response({"error": "Invalid doctor, user, or timeslot group."}, status=404)

    # ✅ Check if time is in available slots
    timeslots = timeslot_group.timeslots
    if data['time'] not in timeslots:
        return Response({"error": "Invalid time slot."}, status=400)

    # ✅ Check if already booked
    if HospitalBooking.objects.filter(
        doctor=doctor,
        date=data['date'],
        time=data['time'],
        is_booked=True
    ).exists():
        return Response({"error": "This time slot is already booked."}, status=400)

    # ✅ Create booking
    booking = HospitalBooking.objects.create(
        user=user,
        doctor=doctor,
        timeslot_group=timeslot_group,
        date=data['date'],
        time=data['time'],
        is_booked=True
    )

    return Response({
        "message": "Slot booked successfully!",
        "booking_id": booking.id,
        "doctor": doctor.name,
        "date": data['date'],
        "time": data['time']
    }, status=201)



# 🧠 User Adds Feedback
@api_view(['POST'])
def add_hospital_doctor_feedback(request):
    user_id = request.data.get('user')
    doctor_id = request.data.get('doctor')
    rating = request.data.get('rating')
    comments = request.data.get('comments', '')

    try:
        user = tbl_register.objects.get(id=user_id)
        doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)
    except (tbl_register.DoesNotExist, tbl_hospital_doctor_register.DoesNotExist):
        return Response({'error': 'Invalid user or doctor ID'}, status=status.HTTP_404_NOT_FOUND)

    feedback = HospitalDoctorFeedback.objects.create(
        user=user, doctor=doctor, rating=rating, comments=comments
    )
    serializer = HospitalDoctorFeedbackSerializer(feedback)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# 🧠 Doctor Views Feedback
@api_view(['GET'])
def view_hospital_doctor_feedback(request, doctor_id):
    feedbacks = HospitalDoctorFeedback.objects.filter(doctor_id=doctor_id).order_by('-created_at')
    serializer = HospitalDoctorFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HospitalDoctorFeedback
from .serializers import HospitalDoctorFeedbackSerializer


class GetDoctorFeedbackAPI(APIView):
    def get(self, request, doctor_id):
        try:
            feedbacks = HospitalDoctorFeedback.objects.filter(doctor_id=doctor_id)

            if not feedbacks.exists():
                return Response({"message": "No feedback found for this doctor."}, status=404)

            serializer = HospitalDoctorFeedbackSerializer(feedbacks, many=True)
            return Response(serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)




from rest_framework import viewsets
from .models import CycleInput
from .serializers import CycleInputSerializer

class CycleInputViewSet(viewsets.ModelViewSet):
    queryset = CycleInput.objects.all()
    serializer_class = CycleInputSerializer



class user_view_booking_hospital(APIView):
    def get(self, request, user_id):
        bookings = HospitalBooking.objects.filter(user_id=user_id)
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "doctor": booking.doctor.id if booking.doctor else None,
                "doctor_name": booking.doctor.name if booking.doctor else "Doctor removed",
                "patient": booking.user.id,
                "patient_name": booking.user.name if booking.user else "User removed",
                "date": booking.date,
                "time": booking.time,
                # "booked_at": getattr(booking, 'created_at', None),
            })
        return Response(data, status=status.HTTP_200_OK)


class doctor_view_booking_hospital(APIView):
    def get(self, request, doctor_id):
        bookings = HospitalBooking.objects.filter(doctor_id=doctor_id)
        data = []
        for booking in bookings:
            data.append({
                "id": booking.id,
                "user": booking.user.id,
                "user_name": booking.user.name,
                "date": booking.date,
                "time": booking.time,
                "status": booking.status,
                # "booked_at": booking.created_at,
            })
        return Response(data, status=status.HTTP_200_OK)
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CycleInput
from .serializers import CycleInputSerializer


class GetCycleInputsByUser(APIView):
    def get(self, request, user_id):
        try:
            cycle_inputs = CycleInput.objects.filter(user_id=user_id).order_by('-created_at')

            if not cycle_inputs.exists():
                return Response(
                    {"message": "No cycle data found for this user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CycleInputSerializer(cycle_inputs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class ViewPredictionResultsByUser(APIView):
    def get(self, request, user_id):
        try:
            results = TblPredictionResult.objects.filter(user_id=user_id).order_by('-created_at')

            if not results.exists():
                return Response(
                    {"message": "No prediction results found for this user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PredictionSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalBooking, tbl_hospital_doctor_register,tbl_register
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalBooking, tbl_hospital_doctor_register,tbl_register


class DoctorCancelBookingAPI(APIView):
    def post(self, request, booking_id, doctor_id):
        try:
            booking = HospitalBooking.objects.get(id=booking_id)
            doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)

            # 🔒 Ensure only assigned doctor can cancel
            if booking.doctor != doctor:
                return Response(
                    {"error": "You are not authorized to cancel this booking"},
                    status=status.HTTP_403_FORBIDDEN
                )

            if booking.status.startswith("cancelled"):
                return Response(
                    {"message": "Booking already cancelled"},
                    status=status.HTTP_200_OK
                )

            booking.status = "cancelled_by_doctor"
            booking.is_booked = False
            booking.save()

            return Response({
                "status": "success",
                "message": "Booking cancelled by doctor",
                "booking_id": booking.id,
                "patient_name": booking.user.name,
                "date": booking.date,
                "time": booking.time
            }, status=status.HTTP_200_OK)

        except HospitalBooking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except tbl_hospital_doctor_register.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import HospitalBooking, tbl_hospital_doctor_register,tbl_register


class DoctorCompleteBookingAPI(APIView):
    def post(self, request, booking_id, doctor_id):
        try:
            booking = HospitalBooking.objects.get(id=booking_id)
            doctor = tbl_hospital_doctor_register.objects.get(id=doctor_id)

            #  Only assigned doctor can complete
            if booking.doctor != doctor:
                return Response(
                    {"error": "You are not authorized to complete this booking"},
                    status=status.HTTP_403_FORBIDDEN
                )

            #  Cannot complete cancelled bookings
            if booking.status.startswith("cancelled"):
                return Response(
                    {"error": "Cancelled booking cannot be completed"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #  Already completed
            if booking.status == "completed":
                return Response(
                    {"message": "Booking already completed"},
                    status=status.HTTP_200_OK
                )

            #  Mark as completed
            booking.status = "completed"
            booking.is_booked = False
            booking.save()

            return Response({
                "status": "success",
                "message": "Booking marked as completed",
                "booking_id": booking.id,
                "patient_name": booking.user.name,
                "date": booking.date,
                "time": booking.time
            }, status=status.HTTP_200_OK)

        except HospitalBooking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except tbl_hospital_doctor_register.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )
