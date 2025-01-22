# import json
import logging
# from django.http import JsonResponse
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import razorpay
from .models import *
from freelancer.models import *
from django.core.mail import send_mail

# from payment.models import Payment
logger = logging.getLogger(__name__)
# # Create your views here.
# Razorpay Client Setup
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment(request):
    return render(request, 'payment.html')

def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        proposalId = data.get("proposal_id")
        amount = data.get("bid")  # Amount in paise (9900 paise = 99 INR)
        amount = amount * 100
        currency = "INR"
        proposal = FreelancerProposal.objects.get(id = int(proposalId))
        request.session['freelancer_email'] = proposal.freelancer.email
        email = str(request.session.get('email'))  # Get email from session
        if not email:
            logger.error("User email not found in session")
            return JsonResponse({'error': 'User email not found in session'}, status=400)

        try:
            order_info = {
                    "amount": amount,
                    "currency": currency,
                    "payment_capture": 1  # Automatically capture payment
            }
            # Create the Razorpay order
            order = razorpay_client.order.create(order_info)
            order_id = order.get('id')
            if not order_id:
                logger.error(
                    "Failed to retrieve order_id from Razorpay response")
                return JsonResponse({'error': 'Failed to create Razorpay order try again'}, status=500)

            # Save payment details to the database
            payment = Payment.objects.create(
                order_id=order_id, amount=amount / 100, email=email, status='Pending', proposal = proposal
            )

            request.session['proposalId'] = proposalId

            logger.info(f"Payment created successfully: {payment}")

            return JsonResponse({'order_id': order_id, 'amount': amount, 'email': email})
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            return JsonResponse({'error': f'Error creating Razorpay order: {str(e)}'}, status=500)

    logger.error("Invalid request method for create_order")
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def verify_payment(request):
    if request.method == "POST":
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return JsonResponse({'status': 'Failed', 'message': 'Invalid payment data'}, status=400)

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                # Signature verification
                razorpay_client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'status': 'Failed', 'message': 'Payment verification failed. Invalid signature.'}, status=400)

            # Update payment status in the database
            try:
                payment = Payment.objects.get(order_id=razorpay_order_id)
                payment.payment_id = razorpay_payment_id
                payment.signature = razorpay_signature
                payment.status = 'Completed'
                payment.refund_amount = 0
                payment.save()

                proposal = FreelancerProposal.objects.get(id = payment.proposal.id)
                proposal.status = 'Selected'
                proposal.save()
               
                # # Define email parameters
                # subject = 'Payment Confirmation'
                # message = f'Your payment with Razorpay has been successfully completed. Payment ID: {razorpay_payment_id}'
                # from_email = settings.DEFAULT_FROM_EMAIL
                # email = request.session.get('email')
                # recipient_list = [email]  # Add recipient email(s) here

                # # Send the email
                # send_mail(subject, message, from_email, recipient_list)

                # freelancer_email = request.session.get('freelancer_email')

                # subject = 'Your Proposal Has Been Approved!'
                # message = f"""
                # Dear Freelancer,

                # We are pleased to inform you that your proposal for the project '{payment.proposal.title}' has been approved by the client .

                # Here are the details of the project:
                # - **Project Title**: {payment.proposal.title}
               

                # You may now proceed with the next steps as discussed with the client. We wish you all the best in completing the project!

                # If you have any questions, feel free to reach out to us.

                # Best regards,
                # The WorksPhare Team
                # """
                # from_email = settings.DEFAULT_FROM_EMAIL  # Your email address
                # recipient_list = [freelancer_email]  # The freelancer's email address

                # # Send the email
                # send_mail(subject, message, from_email, recipient_list)


            except Payment.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Payment record not found'}, status=404)
            try:
                payment = Payment.objects.get(order_id=razorpay_order_id)

                # Check if the status is 'Completed'
                if payment.status != 'Completed':
                    payment.delete()  # Delete the payment if the status is not 'Completed'

            except:
                # Handle the case where no matching Payment record is found
                print("Payment record not found for the provided order_id.")

            return JsonResponse({'status': 'success', 'message': 'Payment Verified'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'Failed', 'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'status': 'Failed', 'message': 'Invalid request method'}, status=400)