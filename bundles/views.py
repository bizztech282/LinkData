from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .payhero_api import PayheroService

def index(request):
    return render(request, 'index.html')

def payment(request):
    return render(request, 'payment.html')

@csrf_exempt
def initiate_stk(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            recipient_phone = data.get('recipient_phone', phone_number) # Fallback to payment phone if not provided
            amount = data.get('amount')
            detail = data.get('detail', "Starlink Bundle")

            if not phone_number or not amount:
                return JsonResponse({"success": False, "message": "Missing details."}, status=400)

            # Initialize Service
            service = PayheroService()
            
            # Generate a unique reference
            reference = f"TXN-{uuid.uuid4().hex[:8].upper()}"
            
            # Call the API
            # We use the recipient phone in the description so you can see it in logs/PayHero
            result = service.initiate_stk_push(
                phone_number=phone_number,
                amount=amount,
                reference=reference,
                description=f"Bundles for {recipient_phone}"
            )
            
            status_code = 200 if result['success'] else 500
            return JsonResponse(result, status=status_code)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
            
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Log the data (in production use a proper logger)
            print("Callback Received:", data)
            
            # TODO: Update your database transaction status based on 'data'
            # Example:
            # external_ref = data.get('ExternalReference')
            # result_code = data.get('ResultCode')
            # if result_code == 0:
            #     # Mark transaction as paid
            #     pass
            
            # Return success to PayHero
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
        except Exception as e:
            print(f"Callback Error: {e}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Failed"}, status=400)
    
    return JsonResponse({"message": "Use POST"}, status=405)
