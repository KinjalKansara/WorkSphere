import logging
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import razorpay
from notification.models import Notification
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
        # project = ClientPostProject.objects.get(id = proposal.project.id)
        # project.status = 'closed'
        # project.save()
        
        # delete_proposals = FreelancerProposal.objects.filter(project=proposal.project).exclude(id = proposalId)
        # delete_proposals.delete()
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

                # Update proposal status to 'Selected'
                proposal = FreelancerProposal.objects.get(id=payment.proposal.id)
                proposal.status = 'Selected'
                proposal.save()

                # Update project status to 'closed'
                project = ClientPostProject.objects.get(id=proposal.project.id)
                project.status = 'Closed'
                project.save()

                # Delete other proposals for the same project
                delete_proposals = FreelancerProposal.objects.filter(project=proposal.project).exclude(id=payment.proposal.id)
                delete_proposals.delete()

                # Send email notification to the client
                client = proposal.client
                subject = f"Proposal Selected for '{proposal.project.title}'"
                message = f"Hello {client.first_name},\n\nYour project '{proposal.project.title}' has successfully selected a freelancer: {proposal.freelancer.first_name} {proposal.freelancer.last_name}. Payment for the proposal has been successfully completed.\n\nYou can now contact the freelancer directly for further details:\n\nFreelancer's Email: {proposal.freelancer.email}\nFreelancer's Phone: {proposal.freelancer.phone_number}\n\nBest regards,\nWorkSphere Team"
                from_email = 'worksphere05@gmail.com'
                recipient_list = [client.email]
                send_mail(subject, message, from_email, recipient_list)

                # Send email notification to the freelancer
                freelancer = proposal.freelancer
                subject_for_freelancer = f"Congratulations! Proposal for '{proposal.project.title}' Selected"
                message_for_freelancer = f"Hello {freelancer.first_name},\n\nCongratulations! Your proposal for the project '{proposal.project.title}' has been selected by the {proposal.client.first_name} {proposal.client.last_name}, and the payment has been successfully completed.\n\nBest regards,\nWorkSphere Team"
                send_mail(subject_for_freelancer, message_for_freelancer, from_email, [freelancer.email])

                # Send notification to the freelancer
                Notification.objects.create(
                    title="Proposal Selected",
                    message=f"Your proposal for the project '{proposal.project.title}' has been selected, and payment has been completed.",
                    notification_type='freelancer',
                    username=freelancer.username,
                    is_read=False
                )

                # Send notification to the client
                Notification.objects.create(
                    title="Proposal Selected",
                    message=f"Your project '{proposal.project.title}' has successfully selected a freelancer.",
                    notification_type='client',
                    username=client.username,
                    is_read=False
                )

                # Send notification to the admin
                Notification.objects.create(
                    title="Proposal Selected",
                    message=f"Freelancer {freelancer.first_name} {freelancer.last_name} has been selected for the project '{proposal.project.title}' posted by {client.first_name} {client.last_name}. Payment has been successfully completed.",
                    notification_type='admin',
                    username='ADMIN',
                    is_read=False
                )

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
