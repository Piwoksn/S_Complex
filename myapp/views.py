from django.shortcuts import render, redirect
import json
from django.utils import timezone
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Count  # Import Count from django.db.models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserForm
from django.contrib.auth import update_session_auth_hash
from .forms import ChangePasswordForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from shopapp.models import Product, CartItem
from shopapp.utils import calculate_cart_total
from django.utils.text import slugify
from datetime import datetime
from django.db.models import Q
from subscription.models import Subscription, NairaSubscriptionPlan, DollarSubscriptionPlan
from django.utils import timezone
import requests
from django.contrib.auth import logout


# paystack function
from django.views.decorators.csrf import csrf_exempt
# Paypal
from django.views.decorators.http import require_POST
from django.db.models.functions import Concat
from django.db.models import Value
#
# Coin daily
# from django_background_tasks.models import Task
from datetime import timedelta
#
# Rest_FrameWork imports
from rest_framework import generics, status
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from chats.models import SentChats
import time
from django.utils import timezone


# Keep record in txt format
def record(businessname, moredesc, firstname, lastname, email, gender, phone, country, state, address, meansofid, idnumber, whatsapp, facebook, instagram):
    t = time.ctime()
    file = open('records/'+f'{email}_record'+'.txt', 'a+')

    file.write(f"\n\n\nDate: {t}\nBusiness Name: {businessname}\nDesc: {moredesc}\nfirstname: {firstname}\nLastname: {lastname}\nEmail: {email}\nGender: {gender}\nPhone: {phone}\nCountry: {country}\nState: {state}\nAddress: {address}\nMeans of Id: {meansofid}\nId Number: {idnumber}\nWhatsapp: {whatsapp}\nFacebook: {facebook}\nInstagram: {instagram}")

    file.close()



# Add Coin DAily Task
def add_coins_daily(request, user):
    # Check if the user has logged in within the last 3 minutes (for testing)
    last_login = user.last_login.date()
    current_time = timezone.now().date()
    if last_login != current_time:
        print(current_time)
        print(last_login)
        # User logged in every new day, add 50 coins (for testing)
        user.coins += 50
        user.last_login = timezone.now()
        user.save()
        messages.success(request, "You Received 50 coins Daily Bonus.")
        # Update the last_login and daily_bonus_received attributes
    
        




def aboutus(request):
    return render(request, 'myapp/aboutus.html')


def terms_of_service(request):
    return render(request, 'myapp/terms_of_service.html')


def privacy_policy(request):
    return render(request, 'myapp/privacy_policy.html')


@csrf_exempt
def coins(request):
    user = request.user
    context = {'user': user, }
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Retrieve the data from the JSON object
            coins = data.get('coins')

            main_coin = int(coins)

            # Save the data to your database or perform any other necessary actions
            user = request.user

            total_coin = user.coins + main_coin

            user.coins = total_coin  # Fix the attribute name

            user.save()  # Call the save method

            response_data = {
                'coins': coins,
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    return render(request, 'myapp/coins.html', context)


@login_required(login_url='loginform')
def submethod(request):
    return render(request, 'myapp/submethod.html')


@login_required(login_url='loginform')
def coinsub(request):
    return render(request, 'myapp/coinsub.html')


@login_required(login_url='loginform')
def coinsub(request):
    if request.user.is_authenticated:
        user = request.user
        nairaGold = NairaSubscriptionPlan.objects.get(plan_type='Gold')
        nairaSilver = NairaSubscriptionPlan.objects.get(plan_type='Silver')
        nairaBronze = NairaSubscriptionPlan.objects.get(plan_type='Bronze')
        nairaPlatinum = NairaSubscriptionPlan.objects.get(plan_type='Platinum')
        nairaBasic = NairaSubscriptionPlan.objects.get(plan_type='Basic')
        # foreignnairaGold = NairaSubscriptionPlan.objects.get(plan_type='ForeignGold')
        # foreignnairaSilver = NairaSubscriptionPlan.objects.get(plan_type='ForeignSilver')
        # foreignnairaBronze = NairaSubscriptionPlan.objects.get(plan_type='ForeignBronze')
        # foreignnairaPlatinum = NairaSubscriptionPlan.objects.get(plan_type='ForeignPlatinum')
        # foreignnairaBasic = NairaSubscriptionPlan.objects.get(plan_type='ForeignBasic')
        # dollarGold = DollarSubscriptionPlan.objects.get(plan_type='Gold')
        # dollarSilver = DollarSubscriptionPlan.objects.get(plan_type='Silver')
        # dollarBronze = DollarSubscriptionPlan.objects.get(plan_type='Bronze')
        # dollarPlatinum = DollarSubscriptionPlan.objects.get(plan_type='Platinum')
        # dollarBasic = DollarSubscriptionPlan.objects.get(plan_type='Basic')
    context = {'user': user, 'nairaGold': nairaGold, 'nairaSilver': nairaSilver, 'nairaBronze': nairaBronze, 'nairaPlatinum': nairaPlatinum, 'nairaBasic': nairaBasic,
               # 'dollarGold': dollarGold, 'dollarSilver': dollarSilver, 'dollarBronze': dollarBronze, 'dollarPlatinum': dollarPlatinum, 'dollarBasic': dollarBasic, 'foreignnairaGold': foreignnairaGold, 'foreignnairaSilver': foreignnairaSilver, 'foreignnairaPlatinum': foreignnairaPlatinum, 'foreignnairaBronze': foreignnairaBronze, 'foreignnairaBasic': foreignnairaBasic,

               }
    return render(request, 'myapp/coinsub.html', context)


# @csrf_exempt
# def coincallback(request):
#     #
#     if request.user.is_authenticated:
#         user = request.user
#         if Subscription.objects.filter(user=user).exists():
#             sub = Subscription.objects.get(user=user)
#             if user.coins >= sub.naira_plan.price:
#                 # paid = user.coins - sub.naira_plan.price
#                 # user.coins = paid
#                 user.coins -= sub.naira_plan.price
#                 user.save()
#                 sub.ref_no = 'coin_sub'
#                 sub.save()
#                 return redirect('portal')
#             else:
#                 messages.warning(request, 'Insufficient Coin')
#                 return redirect('submethod')
#         else:
#             pass
#     else:
#         pass

#     #

#     if request.method == 'POST':
#         try:
#             # Parse JSON data from the request body
#             data = json.loads(request.body.decode('utf-8'))

#             # Retrieve the data from the JSON object
#             confirmation_id = request.GET.get('reference')
#             email = data.get('email')
#             datetime = data.get('datetime')
#             due_date = data.get('due_date')
#             subscription_type = data.get('subscription_type')

#             # Save the data to your database or perform any other necessary actions
#             sub = Subscription()
#             user = request.user

#             sub.naira_plan = NairaSubscriptionPlan.objects.get(
#                 plan_type=subscription_type)
#             sub.user = user
#             sub.email = email

#             sub.paystack_sub_date = datetime
#             sub.paystack_due_date = due_date

#             # You should be able to use NairaSubscriptionPlan here
#             # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

#             sub.save()

#             # Check and update the user's subscription status based on subscription_type
#             user.subscribed = True
#             user.slug = slugify(user.businessname)
#             user.save()
#             print(subscription_type, sub.naira_plan.price)
#             response_data = {
#                 'confirmation_id': confirmation_id,
#                 'email': email,
#                 'datetime': datetime,
#                 'due_date': due_date,
#                 'subscription_type': subscription_type,
#             }
#             return JsonResponse(response_data)
#         except json.JSONDecodeError:
#             return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

#     # Handle GET requests or invalid requests here
#     return redirect('portal')


# Latest Below
# @csrf_exempt
# def coincallback(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data from the request body
#             data = json.loads(request.body.decode('utf-8'))

#             # Retrieve the data from the JSON object
#             confirmation_id = data.get('reference')
#             email = data.get('email')
#             datetime = data.get('datetime')
#             due_date = data.get('due_date')
#             subscription_type = data.get('subscription_type')

#             # Save the data to your database or perform any other necessary actions
#             sub = Subscription()
#             user = request.user

#             sub.naira_plan = NairaSubscriptionPlan.objects.get(
#                 plan_type=subscription_type)
#             sub.user = user
#             sub.email = email

#             sub.paystack_sub_date = datetime
#             sub.paystack_due_date = due_date

#             # You should be able to use NairaSubscriptionPlan here
#             # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

#             sub.save()

#             # Check if the user has sufficient coins
#             if user.coins >= sub.naira_plan.price:
#                 # Deduct coins from user's balance
#                 user.coins -= sub.naira_plan.price
#                 user.save()

#                 # Update user's subscription status
#                 user.subscribed = True
#                 user.save()

#                 # Update reference number and save subscription
#                 sub.ref_no = 'coin_sub'
#                 sub.save()

#                 response_data = {
#                     'confirmation_id': confirmation_id,
#                     'email': email,
#                     'datetime': datetime,
#                     'due_date': due_date,
#                     'subscription_type': subscription_type,
#                 }
#                 return JsonResponse(response_data)
#             else:
#                 # User doesn't have sufficient coins
#                 messages.warning(request, 'Insufficient Coins')
#                 return JsonResponse({'message': 'Insufficient Coins'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

#     # Handle GET requests or invalid requests here
#     return redirect('portal')


@csrf_exempt
def coincallback(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Retrieve the data from the JSON object
            confirmation_id = data.get('reference')
            email = data.get('email')
            datetime = data.get('datetime')
            due_date = data.get('due_date')
            subscription_type = data.get('subscription_type')

            # Check if the user is already subscribed
            user = request.user
            if user.subscribed:
                return JsonResponse({'message': 'User is already subscribed'}, status=400)

            # Save the data to your database or perform any other necessary actions
            sub = Subscription()

            sub.naira_plan = NairaSubscriptionPlan.objects.get(
                plan_type=subscription_type)
            sub.user = user
            sub.email = email

            sub.paystack_sub_date = datetime
            sub.paystack_due_date = due_date

            # You should be able to use NairaSubscriptionPlan here
            # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

            sub.save()

            # Check if the user has sufficient coins
            if user.coins >= sub.naira_plan.price:
                # Deduct coins from user's balance
                user.coins -= sub.naira_plan.price
                user.save()

                # Update user's subscription status
                user.subscribed = True
                user.save()

                # Update reference number and save subscription
                sub.ref_no = 'coin_sub'
                sub.save()

                response_data = {
                    'confirmation_id': confirmation_id,
                    'email': email,
                    'datetime': datetime,
                    'due_date': due_date,
                    'subscription_type': subscription_type,
                }
                return JsonResponse(response_data)
            else:
                # User doesn't have sufficient coins
                messages.warning(request, 'Insufficient Coins')
                return JsonResponse({'message': 'Insufficient Coins'}, status=400)
                # return redirect('submethod')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    # Handle GET requests or invalid requests here
    return redirect('portal')


# PayPal------------------------------------------


@csrf_exempt
@require_POST
def paypal_callback(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))

        # Retrieve the data from the JSON object
        subscription_id = data.get('reference')
        payment_reference = request.GET.get('reference')

        print(payment_reference)

        #
        email = data.get('payer').get('email_address')
        datetime = data.get('create_time')
        # Calculate due date based on your business logic
        # PayPal provides 'billing_cycle' information; you may need to parse it accordingly
        # due_date = "Your Logic Here"
        due_date = data.get('due_time')

        # Map PayPal plan_id to your subscription type
        plan_id = data.get('plan_id')
        subscription_type = get_subscription_type_from_plan_id(plan_id)

        # Save the data to your database or perform any other necessary actions
        # For example, create a Subscription object and save it to your database
        sub = Subscription()
        user = request.user

        sub.user = user
        # sub.email = email
        sub.ref_no = payment_reference
        sub.paypal_sub_date = datetime
        sub.paypal_due_date = due_date

        print(subscription_id, email, datetime, due_date, subscription_type)
        # You should be able to use NairaSubscriptionPlan here
        # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

        sub.dollar_plan = DollarSubscriptionPlan.objects.get(
            plan_type=subscription_type)
        sub.save()

        # Check and update the user's subscription status based on subscription_type
        user.subscribed = True
        user.slug = slugify(user.businessname)
        user.save()

        response_data = {
            'subscription_id': subscription_id,
            'email': email,
            'datetime': datetime,
            'due_date': due_date,
            'subscription_type': subscription_type,
        }
        # return JsonResponse(response_data)

        messages.success(request, 'Subscription Successful')
        return redirect('portal')
        # ---------------
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    # Handle invalid requests here
    return JsonResponse({'message': 'Invalid request.'})


def get_subscription_type_from_plan_id(plan_id):
    # Implement your logic to map PayPal plan_id to your subscription type here
    # You may want to query your database or use a predefined mapping
    # For example:
    if plan_id == 'P-5FU22958U7878843NMU7PULQ':
        return 'Basic'
    elif plan_id == 'P-3AB54408H3241991XMU7OXEY':
        return 'Platinum'
    elif plan_id == 'P-01K04061PD845750YMUZJRCY':
        return 'Bronze'
    elif plan_id == 'P-2AN79546XT068413DMUZJT7Q':
        return 'Silver'
    elif plan_id == 'P-1KK7174087845174BMUZJLBY':
        return 'Gold'
    else:
        messages.warning(request, 'Plan not recognized')
        return redirect('portal')
    # Add more plan_id to subscription type mappings as needed
    return 'Unknown'  # Return a default value or handle unknown cases

# ---------------------------------------------------
#
#
#
#
#
#
#
#
#
#
#
#
# More Info


@login_required(login_url='loginform')
def info(request):
    user = request.user
    nairaGold = NairaSubscriptionPlan.objects.get(plan_type='Gold')
    nairaSilver = NairaSubscriptionPlan.objects.get(plan_type='Silver')
    nairaBronze = NairaSubscriptionPlan.objects.get(plan_type='Bronze')
    nairaPlatinum = NairaSubscriptionPlan.objects.get(plan_type='Platinum')
    # Foreign
    # foreignnairaGold = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignGold')
    # foreignnairaSilver = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignSilver')
    # foreignnairaBronze = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignBronze')
    # foreignnairaPlatinum = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignPlatinum')
    # foreignnairaBasic = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignBasic')

    dollarGold = DollarSubscriptionPlan.objects.get(plan_type='Gold')
    dollarSilver = DollarSubscriptionPlan.objects.get(plan_type='Silver')
    dollarBronze = DollarSubscriptionPlan.objects.get(plan_type='Bronze')
    dollarPlatinum = DollarSubscriptionPlan.objects.get(
        plan_type='Platinum')

    if request.method == 'POST':
        accept = request.POST.get('accept')
        if accept:
            return redirect('portal')
        else:
            pass

    context = {'user': user, 'nairaGold': int(nairaGold.price), 'nairaSilver': int(nairaSilver.price),
               'nairaBronze': int(nairaBronze.price), 'nairaPlatinum': int(nairaPlatinum.price), 'dollarGold': int(dollarGold.price), 'dollarSilver': int(dollarSilver.price), 'dollarBronze': int(dollarBronze.price), 'dollarPlatinum': int(dollarPlatinum.price),
               # 'foreignnairaGold': int(foreignnairaGold.price), 'foreignnairaSilver': int(foreignnairaSilver.price), 'foreignnairaPlatinum': int(foreignnairaPlatinum.price), 'foreignnairaBronze': int(foreignnairaBronze.price), 'foreignnairaBasic': int(foreignnairaBasic.price),

               }
    return render(request, "myapp/info.html", context)


# Cancel Sub-----------------------------------------------


def cancelsub(request, user):
    sub = Subscription.objects.get(user=user)
    if sub.end_date <= timezone.now():
        sub.delete()


# Check expifre
def check_expired(request, user):
    if Subscription.objects.filter(user=user).exists():
        cancelsub(request, user)
        if Subscription.objects.filter(user=user).exists():
            user.subscribed = True
            user.slug = slugify(user.businessname)
        else:
            user.slug = None
            user.subscribed = False
        user.save()
    else:
        user.slug = None
        user.subscribed = False

    user.save()


# PAYSTACK

@csrf_exempt
def paystack_callback(request):
    if request.user.is_authenticated:
        user = request.user
        confirmation_id = request.GET.get('reference')
        if confirmation_id:
            if Subscription.objects.filter(user=user).exists():
                sub = Subscription.objects.get(user=user)
                sub.ref_no = confirmation_id
                sub.save()
                return redirect('portal')

                # print(f"from portal ref_id = {sub} {confirmation_id}")
            else:
                pass
        else:
            pass
    else:
        pass
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Retrieve the data from the JSON object
            confirmation_id = request.GET.get('reference')
            email = data.get('email')
            datetime = data.get('datetime')
            due_date = data.get('due_date')
            subscription_type = data.get('subscription_type')

            # Save the data to your database or perform any other necessary actions
            if Subscription.objects.filter(user=request.user).exists():
                pass
            else:
                sub = Subscription()
                user = request.user

                sub.user = user
                sub.email = email
                sub.ref_no = confirmation_id
                sub.paystack_sub_date = datetime
                sub.paystack_due_date = due_date

                # You should be able to use NairaSubscriptionPlan here
                # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

                sub.naira_plan = NairaSubscriptionPlan.objects.get(
                    plan_type=subscription_type)
                sub.save()

                # Check and update the user's subscription status based on subscription_type
                user.subscribed = True
                user.slug = slugify(user.businessname)
                user.save()

            response_data = {
                'confirmation_id': confirmation_id,
                'email': email,
                'datetime': datetime,
                'due_date': due_date,
                'subscription_type': subscription_type,
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    # Handle GET requests or invalid requests here
    return JsonResponse({'message': 'Invalid request.'})


@csrf_exempt
def flutterwave_callback(request):
    if request.user.is_authenticated:
        user = request.user
        confirmation_id = request.GET.get('tx_ref')
        if confirmation_id:
            if Subscription.objects.filter(user=user).exists():
                sub = Subscription.objects.get(user=user)
                sub.ref_no = confirmation_id
                sub.save()
                return redirect('portal')

                # print(f"from portal ref_id = {sub} {confirmation_id}")
            else:
                pass
        else:
            pass
    else:
        pass
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Retrieve the data from the JSON object
            confirmation_id = request.GET.get('tx_ref')
            email = data.get('email')
            datetime = data.get('datetime')
            due_date = data.get('due_date')
            subscription_type = data.get('subscription_type')

            # Save the data to your database or perform any other necessary actions
            if Subscription.objects.filter(user=request.user).exists():
                pass
            else:
                sub = Subscription()
                user = request.user

                sub.user = user
                sub.email = email
                sub.ref_no = confirmation_id
                sub.paystack_sub_date = datetime
                sub.paystack_due_date = due_date

                # You should be able to use NairaSubscriptionPlan here
                # Example: NairaSubscriptionPlan.objects.get(plan_type=subscription_type)

                sub.naira_plan = NairaSubscriptionPlan.objects.get(
                    plan_type=subscription_type)
                sub.save()

                # Check and update the user's subscription status based on subscription_type
                user.subscribed = True
                user.slug = slugify(user.businessname)
                user.save()

            response_data = {
                'confirmation_id': confirmation_id,
                'email': email,
                'datetime': datetime,
                'due_date': due_date,
                'subscription_type': subscription_type,
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    # Handle GET requests or invalid requests here
    return JsonResponse({'message': 'Invalid request.'})


# ____________Admin_______________________________


# Retun to this
def superadminlogin(request):
    if request.method == 'POST':
        try:
            emails = request.POST.get('superemail')
            password = request.POST.get('superpassword')

            email = str(emails)
            if email == 'admin@admin.com':
                user = auth.authenticate(email=email, password=password)

                if user is not None:
                    auth.login(request, user)
                    return redirect('superadmin')
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('superadminlogin')
            else:
                messages.warning(request, 'are you lost?')
                return redirect('loginform')
        except:
            return redirect('home')
    return render(request, 'myapp/superadminlogin.html')


@login_required(login_url='superadminlogin')
def superadminlogout(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            auth.logout(request)
        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')
    return render(request, 'myapp/superadminlogin.html')


@login_required(login_url='superadminlogin')
def superadmindelete(request, pk):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            person = User.objects.get(id=pk)
            users = User.objects.all()

        # Counter
            number = users.count() - 1  # Total number of users

            # -------------------------

            if request.method == "POST":
                person.delete()

                messages.success(request, "user deleted")
                return redirect('superadminsearch')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            context = {'user': person, 'number': number, }
        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')
    return render(request, 'myapp/superadmindelete.html', context)


@login_required(login_url='superadminlogin')
def superadminsearch(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            # Counter
            users = User.objects.all()

        # Counter
            number = users.count() - 1  # Total number of users
            # --------------

            q = request.GET.get('q') if request.GET.get('q') != None else ''

            people = User.objects.filter(Q(first_name__icontains=q) |
                                         Q(last_name__icontains=q) |
                                         Q(businessname__icontains=q) |
                                         Q(slug__icontains=q) |
                                         Q(country__icontains=q) |
                                         Q(phone__icontains=q) |
                                         Q(email__icontains=q)

                                         )

            # Fetch subscription information for each user
            user_subscriptions = {}
            for user in people:
                try:
                    subscription = Subscription.objects.get(user=user)
                    user_subscriptions[user] = subscription
                except Subscription.DoesNotExist:
                    user_subscriptions[user] = None

            context = {'people': people, 'number': number,
                       'user_subscriptions': user_subscriptions}

        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')
    return render(request, 'myapp/superadminsearch.html', context)


@login_required(login_url='superadminlogin')
def superadminsubscription(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            # Counter
            users = User.objects.all()
            number = users.count() - 1  # Total number of users

            if request.method == 'POST':
                user_email = request.POST.get('user')
                ref = request.POST.get('ref')
                naira_plan = request.POST.get('naira_plan')
                dollar_plan = request.POST.get('dollar_plan')

                user = get_object_or_404(User, email=user_email)
                subscription, created = Subscription.objects.get_or_create(
                    user=user, ref_no=ref)

                if naira_plan:
                    subscription.naira_plan = NairaSubscriptionPlan.objects.get(
                        plan_type=naira_plan)

                elif dollar_plan:
                    subscription.dollar_plan = DollarSubscriptionPlan.objects.get(
                        plan_type=dollar_plan)
                else:
                    pass

                start_date = datetime.now()

                if naira_plan is None:
                    subscription.end_date = start_date + \
                        timezone.timedelta(days=30)  # Default end_date
                else:
                    if naira_plan == 'Platinum':
                        end_date = start_date + timezone.timedelta(days=30)
                    elif naira_plan == 'Basic':
                        end_date = start_date + timezone.timedelta(days=1)
                    elif naira_plan == 'Bronze':
                        end_date = start_date + timezone.timedelta(days=90)
                    elif naira_plan == 'Silver':
                        end_date = start_date + timezone.timedelta(days=180)
                    elif naira_plan == 'Gold':
                        end_date = start_date + timezone.timedelta(days=365)
                    else:
                        return HttpResponseBadRequest("Invalid naira_plan")

                if subscription.end_date is None:
                    subscription.end_date = end_date

                subscription.save()
                messages.success(
                    request, f'Successfully Subscribed {user_email}')
                return redirect('superadminsubscription')

            context = {'number': number}
        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')

    return render(request, 'myapp/superadminsubscription.html', context)


@login_required(login_url='superadminlogin')
def superadmincancelsub(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            if request.method == 'POST':
                user_email = request.POST.get('user')

                user = get_object_or_404(User, email=user_email)
                subscription, created = Subscription.objects.get_or_create(
                    user=user)
                subscription.delete()
                messages.success(
                    request, f'{user_email} Subscription Cancelled')
                return redirect('superadminsubscription')
        else:
            return redirect('superadminlogin')


# @login_required(login_url='superadminlogin')
# def superadmincoin(request):
#     if request.user.is_authenticated:
#         if request.user.email == 'admin@admin.com':
#             if request.method == 'POST':
#                 user_email = request.POST.get('user')
#                 user_coin = int(request.POST.get('amount'))

#                 user = User.objects.get(email=user_email)

#                 user.coins = user.coins + user_coin

#                 user.save()

#                 messages.success(
#                     request, f'{user_email} received {user_coin} coins')
#                 return redirect('superadminsubscription')
#         else:
#             return redirect('superadminlogin')

@login_required(login_url='superadminlogin')
def superadmincoin(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            if request.method == 'POST':
                user_email = request.POST.get('user')
                user_coin = int(request.POST.get('amount'))
                # ------
                people = user_email.split()
                for i in people:
                    person = User.objects.get(email=i)
                    person.coins = person.coins + user_coin
                    person.save()
                # ---------

                messages.success(
                    request, f'{user_email} received {user_coin} coins')
                return redirect('superadminsubscription')
        else:
            return redirect('superadminlogin')


@login_required(login_url='superadminlogin')
def superadmin(request):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            users = User.objects.all()

            # Counter
            number = users.count() - 1  # Total number of users

            # Initialize counts
            other_country = 0
            nigeria = 0

            # Distinct countries
            usercountry = User.objects.values('country').annotate(
                count=Count('country')).order_by('country')

            # Update counts for Nigeria and other countries
            for country_data in usercountry:
                country = country_data['country']
                count = country_data['count']

                if country is not None:
                    if country.lower() == 'nigeria':
                        nigeria += count
                    else:
                        other_country += count

            # ---------------SUb Plans-------------------
            nairaGold = NairaSubscriptionPlan.objects.get(plan_type='Gold')
            nairaSilver = NairaSubscriptionPlan.objects.get(plan_type='Silver')
            nairaBronze = NairaSubscriptionPlan.objects.get(plan_type='Bronze')
            nairaPlatinum = NairaSubscriptionPlan.objects.get(
                plan_type='Platinum')
            nairaBasic = NairaSubscriptionPlan.objects.get(plan_type='Basic')

            dollarGold = DollarSubscriptionPlan.objects.get(plan_type='Gold')
            dollarSilver = DollarSubscriptionPlan.objects.get(
                plan_type='Silver')
            dollarBronze = DollarSubscriptionPlan.objects.get(
                plan_type='Bronze')
            dollarPlatinum = DollarSubscriptionPlan.objects.get(
                plan_type='Platinum')
            dollarBasic = DollarSubscriptionPlan.objects.get(
                plan_type='Basic')

            context = {
                'users': users,
                'number': number,
                'nigeria': nigeria,
                'usercountry': usercountry,  # Updated usercountry list with counts
                'othercountry': other_country,
                'nairaGold': nairaGold,
                'nairaSilver': nairaSilver,
                'nairaBronze': nairaBronze,
                'nairaPlatinum': nairaPlatinum,
                'nairaBasic': nairaBasic,
                'dollarGold': dollarGold,
                'dollarSilver': dollarSilver,
                'dollarBronze': dollarBronze,
                'dollarPlatinum': dollarPlatinum,
                'dollarBasic': dollarBasic,
            }

            if request.method == 'POST':
                if 'nairabutton' in request.POST:
                    basicprice = request.POST.get('basicprice')
                    platinumprice = request.POST.get('platinumprice')
                    bronzeprice = request.POST.get('bronzeprice')
                    silverprice = request.POST.get('silverprice')
                    goldprice = request.POST.get('goldprice')

                    basic = NairaSubscriptionPlan.objects.get(
                        plan_type='Basic')
                    basic.price = basicprice
                    basic.save()

                    platinum = NairaSubscriptionPlan.objects.get(
                        plan_type='Platinum')
                    platinum.price = platinumprice
                    platinum.save()

                    bronze = NairaSubscriptionPlan.objects.get(
                        plan_type='Bronze')
                    bronze.price = bronzeprice
                    bronze.save()

                    silver = NairaSubscriptionPlan.objects.get(
                        plan_type='Silver')
                    silver.price = silverprice
                    silver.save()

                    gold = NairaSubscriptionPlan.objects.get(
                        plan_type='Gold')
                    gold.price = goldprice
                    gold.save()

                    messages.success(request, 'NairaPlan Updated Successfully')
                    return redirect('superadmin')

                elif 'dollarbutton' in request.POST:
                    basicprice = request.POST.get('basicprice')
                    platinumprice = request.POST.get('platinumprice')
                    bronzeprice = request.POST.get('bronzeprice')
                    silverprice = request.POST.get('silverprice')
                    goldprice = request.POST.get('goldprice')

                    basic = DollarSubscriptionPlan.objects.get(
                        plan_type='Basic')
                    basic.price = basicprice
                    basic.save()

                    platinum = DollarSubscriptionPlan.objects.get(
                        plan_type='Platinum')
                    platinum.price = platinumprice
                    platinum.save()

                    bronze = DollarSubscriptionPlan.objects.get(
                        plan_type='Bronze')
                    bronze.price = bronzeprice
                    bronze.save()

                    silver = DollarSubscriptionPlan.objects.get(
                        plan_type='Silver')
                    silver.price = silverprice
                    silver.save()

                    gold = DollarSubscriptionPlan.objects.get(
                        plan_type='Gold')
                    gold.price = goldprice
                    gold.save()

                    messages.success(
                        request, 'DollarPlan Updated Successfully')
                    return redirect('superadmin')

                else:
                    pass
        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')

    return render(request, 'myapp/superadmin.html', context)


@login_required(login_url='superadminlogin')
def superadminedit(request, pk):
    if request.user.is_authenticated:
        if request.user.email == 'admin@admin.com':
            person = User.objects.get(id=pk)
            users = User.objects.all()

        # Counter
            number = users.count() - 1  # Total number of users

            # -------------------------

            if request.method == "POST":
                phone = request.POST.get("phone")
                coin = request.POST.get("coin")
                whatsapp = request.POST.get("whatsapp")
                facebook = request.POST.get("facebook")
                instagram = request.POST.get("instagram")
                address = request.POST.get("address")
                state = request.POST.get("state")
                country = request.POST.get("country")
                securityquestion = request.POST.get("securityquestion")
                securityanswer = request.POST.get("securityanswer")

                person.phone = phone
                person.coins = coin
                person.whatsapp = whatsapp
                person.facebook = facebook
                person.instagram = instagram
                person.address = address
                person.state = state
                person.country = country
                person.securityquestion = securityquestion
                person.securityanswer = securityanswer

                person.save()

                messages.success(request, "Saved Successfully")
                return redirect('superadminsearch')
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            context = {'user': person, 'number': number, }
        else:
            return redirect('superadminlogin')
    else:
        return redirect('superadminlogin')
    return render(request, 'myapp/superadminedit.html', context)


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        user = request.user
                
        if not user.businessname:
            messages.success(
                request, f"Welcome back {user.first_name} {user.last_name}, please complete your registration process")
            return redirect('more_info')
        else:
            add_coins_daily(request, user)
            return redirect('portal')
        add_coins_daily(request, user)
        return redirect('portal')
    return render(request, 'myapp/index.html')


def registerform(request):
    return render(request, 'myapp/register.html')

# Password Reset--------------------------------


def fgt_pwd(request):
    page = 'forgetpassword'
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            if User.objects.filter(email=email).exists():
                return redirect('securityquestion', pk=email)

            else:
                messages.warning(request, 'email does not exist')
        except Exception as e:
            messages.warning(request, 'scurity bridged, can not proceed')
    context = {'page': page}
    return render(request, 'myapp/fgt_pwd.html', context)


def securityquestion(request, pk):
    # Define context as an empty dictionary
    try:
        page = 'securityquestion'
        user = User.objects.get(email=pk)
        question = user.securityquestion
        passwordresetcode = user.passwordresetcode
        if request.method == 'POST':
            answer = request.POST.get('securityanswer')
            business = request.POST.get('businessname')
            businessname = slugify(business)
            correctanswer = f"{answer}{businessname}"
            if passwordresetcode == correctanswer:
                return redirect('confirmnumber', pk=passwordresetcode)
            else:
                messages.warning(request, 'Incorrect answer')
        context = {'page': page, 'question': question}
    except Exception as e:
        messages.warning(request, 'Security breached, cannot proceed')
    return render(request, 'myapp/fgt_pwd.html', context)


def confirmnumber(request, pk):
    try:
        page = 'confirmnumber'
        user = User.objects.get(passwordresetcode=pk)
        completephone = user.passwordresetphone
        firstpart = user.phone[:5]
        lastpart = user.phone[-2:]
        if request.method == 'POST':

            phonee = request.POST.get('phone')
            business = request.POST.get('businessname')
            businessname = slugify(business)
            phone = f"{phonee}{businessname}"
            if completephone == phone:
                auth.login(request, user)
                # messages.success(
                #     request, f'Welcome back {user.first_name}, Quickly goto your profile to change password by clicking "Continue to Portal"')
                # return HttpResponseRedirect(request.path_info)
                return redirect('changepassword', pk=phone)
            else:
                messages.warning(request, 'Incorrect answer')

        context = {'page': page, 'firstpart': firstpart, 'lastpart': lastpart}
    except Exception as e:
        messages.warning(request, 'scurity bridged, can not proceed')
    return render(request, 'myapp/fgt_pwd.html', context)


# Original

def changepassword(request, pk):
    try:

        page = 'changepassword'

        user = User.objects.get(passwordresetphone=pk)
        if request.user.is_authenticated:
            if page == 'changepassword':
                if request.method == 'POST':

                    firstpassword = request.POST.get('firstpassword')
                    secondpassword = request.POST.get('secondpassword')

                    if firstpassword == secondpassword:
                        request.user.set_password(firstpassword)
                        request.user.save()

                        messages.success(
                            request, 'password changed successfully')
                        return redirect('loginform')
                    else:
                        messages.warning(request, 'passwords does not match')
                        return HttpResponseRedirect(request.path_info)

                else:
                    context = {'page': page}

            else:
                auth.logout(request)
                messages.warning(
                    request, 'scurity bridged, password change not successful')
                return redirect('loginform')

    except Exception as e:
        auth.logout(request)
        messages.warning(request, 'scurity bridged, can not proceed try again')
        return redirect('loginform')
    return render(request, 'myapp/fgt_pwd.html', context)


# ----------------------------------------


# def loginform(request):

#     if request.user.is_authenticated:
#         return redirect('portal')

#     if request.method == 'POST':
#         try:
#             email = request.POST['email']
#             password = request.POST['password']

#             user = auth.authenticate(email=email, password=password)
#             if user is not None:
#                 if not user.businessname:
#                     auth.login(request, user)
#                     messages.success(
#                         request, f"Welcome back {user.first_name} {user.last_name}, please complete your registration process")
#                     return redirect('more_info')
#                 else:
#                     auth.login(request, user)
#                     return redirect('portal')

#             else:
#                 messages.warning(request, 'Invalid Credentials')
#                 # Redirects to current activity
#                 return HttpResponseRedirect(request.path_info)
#         except:
#             messages.warning(request, 'An error occured. Please try again')
#             return redirect('loginform')
#     else:
#         return render(request, 'myapp/login.html')

# Modify the loginform view function to call add_coins_daily and reset daily_bonus_received
def loginform(request):
    if request.user.is_authenticated:
        return redirect('portal')

    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                if not user.businessname:
                    auth.login(request, user)
                    messages.success(
                        request, f"Welcome back {user.first_name} {user.last_name}, please complete your registration process")
                    return redirect('more_info')
                else:
                    # Call add_coins_daily function after successful login
                    add_coins_daily(request, user)
                    # ----End of coin
                    auth.login(request, user)

                    return redirect('portal')
            else:
                messages.warning(request, 'Invalid Credentials')
                # Redirects to current activity
                return HttpResponseRedirect(request.path_info)
        except:
            messages.warning(request, 'An error occured. Please try again')
            return redirect('loginform')
    else:
        return render(request, 'myapp/login.html')

@login_required(login_url='loginform')
def more_info(request):
    if request.user.is_authenticated:

        if request.method == "POST":

            # Extract user input from the request
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            # gender = request.POST['gender']
            # dob = request.POST['dob']
            # status = request.POST['status']
            country = request.POST['country']
            # state = request.POST['state']
            # address = request.POST['address']

            # More Info
            securityquestion = request.POST['securityquestion']
            securityanswer = request.POST['securityanswer']
            phone1 = request.POST['phone']
            phone = ''.join(phone1.split())
            meansofid = request.POST['identification']
            idnumber = request.POST['cardnumber']
            idpic = request.FILES.get('uploadedFile')
            profilepic = request.FILES.get('profilepic')
            businessname = request.POST['businessname']
            logo = request.FILES.get('logo')
            # businesstype = request.POST['businesstype']
            currency = request.POST['currency']
            shopcategory = request.POST['shopcategory']
            moredesc = request.POST['moredesc']
            # whatsap1 = request.POST['whatsapp']
            # whatsap = ''.join(whatsap1.split())

            whatsapp = f"https://wa.me/{whatsap}"
            # facebookk = request.POST['facebook']
            # facebook = f"https://www.facebook.com/{facebookk}"
            # instagramm = request.POST['instagram']
            # instagram = f"https://www.instagram.com/{instagramm}"
            # ---------End of More_info-----------

            # Check if business name is already taken
            if User.objects.filter(businessname=businessname).exists():
                messages.warning(request, 'Business Name is already taken')
                return redirect('more_info')

            else:
                # user = User.objects.latest('id')
                user = User.objects.get(id=request.user.id)
                # Update user profile
                user.securityquestion = securityquestion
                user.securityanswer = securityanswer
                user.phone = phone
                user.profilepic = profilepic
                user.businessname = businessname
                user.logo = logo
                user.businesstype = businesstype
                user.currency = currency
                user.shopcategory = shopcategory
                user.moredesc = moredesc
                user.whatsapp = whatsapp
                user.facebook = facebook
                user.instagram = instagram

                user.save()

                # Call the function to set trial dates
                set_trial_dates(user)

                # Password Recovery------------------
                passwordreset = f"{user.securityanswer}{user.slug}"
                passwordresetphone = f"{user.phone}{user.slug}"
                user.passwordresetcode = passwordreset
                user.passwordresetphone = passwordresetphone
                # ------------------------------------------
                user.save()

                return redirect('info')

                # return HttpResponseRedirect(request.path_info)
        else:
            return render(request, 'myapp/more_info.html')
    else:
        return redirect('loginform')


@login_required(login_url='loginform')
def contact(request):
    user = request.user

    facebookk = user.facebook
    facebook = facebookk[25:]

    whatsap = user.whatsapp
    whatsapp = whatsap[14:]

    instagramm = user.instagram
    instagram = instagramm[26:]
    # Check the subscription status (and set user.slug)
    check_expired(request, user)

    product = Product.objects.filter(owner=request.user)
    categories = product.values('itemcategory').distinct()

    # For Order Notification ---------------------------------------
    cart = CartItem.objects.filter(slug=request.user.slug)
    carts = cart.values('phone').distinct()

    # -----------------------------------------------------------------

    context = {}
    if request.user.is_authenticated:
        contact_form = UserForm(request.POST, instance=request.user)

        if request.method == 'POST':
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Updated Successfully')
            else:
                messages.warning(request, 'Not Updated')
        context = {'facebook': facebook, 'whatsapp': whatsapp, 'instagram': instagram,
                   'contact_form': contact_form, 'carts': carts, }

    return render(request, 'myapp/contact.html', context)


@login_required(login_url='loginform')
def portal(request):
    if request.user.is_authenticated:
        # Get the user
        user = request.user

        # -------------------------------------------
        if Subscription.objects.filter(user=user).exists():
            sub = Subscription.objects.get(user=user)
            if sub.ref_no:
                pass
            else:
                sub.delete()
        else:
            pass

        # ----------------------------------
        # Daily Coin 50coins
        add_coins_daily(request, user)

        # ----------------------------------
        # ----------------------------------

        if not user.businessname:
            messages.success(
                request, f"Welcome back {user.first_name} {user.last_name}, please complete your registration process")
            return redirect('more_info')
        else:
            pass

        # Check the subscription status (and set user.slug)
        check_expired(request, user)

        # Get the current time
        current_time = timezone.now()

        if Subscription.objects.filter(user=user).exists():
            subscription = Subscription.objects.get(user=user)
            subenddate = subscription.end_date
            subplannaira = subscription.naira_plan
            subplandollar = subscription.dollar_plan

        # Check if the user is within their trial period (2 weeks)
        trial_end = user.trial_end
        if current_time < trial_end:
            # User is still in the trial period

            notify = f"2 weeks Free-Trial"
            due = f"Ends: {trial_end.strftime('%b. %d, %Y')} at {trial_end.strftime('%I:%M%p')} (GMT +00:00)"
        elif user.slug:
            if user.country == 'Nigeria' or user.country == 'nigeria':
                notify = f"{subplannaira}"
                due = f"Due on: {subenddate.strftime('%b. %d, %Y')} at {subenddate.strftime('%I:%M%p')} (GMT +00:00)"
            else:
                # notify = f"{subplandollar}, valid till: {subenddate.strftime('%b. %d, %Y')}"
                notify = f"{subplannaira}"
                due = f"Due on: {subenddate.strftime('%b. %d, %Y')} at {subenddate.strftime('%I:%M%p')} (GMT +00:00)"
        else:
            notify = "Please subscribe to activate"
            due = ""

        # Save the user to update the slug status
        user.save()

        # Rest of your view logic
        product = Product.objects.filter(owner=user)
        categories = product.values('itemcategory').distinct()

        # For Order Notification ---------------------------------------
        cart = CartItem.objects.filter(slug=user.slug)
        carts = cart.values('phone').distinct()

        # Chat
        chats = SentChats.objects.filter(receiver=request.user)
        chat = chats.values('user').distinct()
        # End Chat

        context = {
            'user': user,
            'chats': chat,
            'date': datetime.now(),
            'due': due,
            'notify': notify,
            'product': product,
            'categories': categories,
            'carts': carts,
            'item': item
        }
        return render(request, 'myapp/portal.html', context)

    # Handle the case when the user is not authenticated
    return redirect('loginform')


@login_required(login_url='loginform')
def profile(request):
    context = {}
    if request.user.is_authenticated:
        # user_form = UserForm(instance=request.user)
        password_form = ChangePasswordForm()  # Create ChangePasswordForm instance
        user = request.user
        # Check the subscription status (and set user.slug)
        check_expired(request, user)
        if request.method == 'POST':
            try:
                if 'update_pic' in request.POST:
                    profilepic = request.FILES.get('profilepic')

                    user.profilepic = profilepic
                    user.save()

                    messages.success(request, 'Photo updated successfully')
                    return redirect('profile')
                elif 'update_logo' in request.POST:
                    logo = request.FILES.get('logo')

                    user.logo = logo
                    user.save()
                    messages.success(request, 'Logo updated successfully')
                    return redirect('profile')
                elif 'update_profile' in request.POST:
                    firstname = request.POST.get('first_name')
                    lastname = request.POST.get('last_name')
                    moredesc = request.POST.get('moredesc')
                    businessname = request.POST.get('businessname')
                    businesstype = request.POST.get('businesstype')
                    country = request.POST.get('country')
                    currency = request.POST.get('currency')
                    address = request.POST.get('address')
                    phone1 = request.POST.get('phone')
                    phone = ''.join(phone1.split())

                    email = request.POST.get('email')
                    # facebook = request.POST.get('facebook')
                    # whatsapp = request.POST.get('whatsapp')
                    # instagram = request.POST.get('instagram')

                    whatsap1 = request.POST['whatsapp']
                    whatsap = ''.join(whatsap1.split())
                    whatsapp = f"https://wa.me/{whatsap}"
                    facebookk = request.POST['facebook']
                    facebook = f"https://www.facebook.com/{facebookk}"
                    instagramm = request.POST['instagram']
                    instagram = f"https://www.instagram.com/{instagramm}"

                    # Record on txt
                    record(businessname, moredesc, firstname, lastname, user.email, user.gender, phone, country, user.state, address, user.meansofid, user.idnumber, whatsapp, facebook, instagram)
                    
                    user.first_name = firstname
                    user.last_name = lastname
                    user.moredesc = moredesc
                    user.businessname = businessname
                    user.businesstype = businesstype
                    user.country = country
                    user.currency = currency
                    user.address = address
                    user.phone = phone
                    user.email = email
                    user.facebook = facebook
                    user.whatsapp = whatsapp
                    user.instagram = instagram
                    user.record = str(f'{user}_record')+'.txt'

                    
                    
                    user.save()
                    messages.success(
                        request, 'Your profile was successfully updated!')
                    return redirect('profile')

                elif 'change_password' in request.POST:
                    password_form = ChangePasswordForm(request.POST)
                    if password_form.is_valid():
                        user = request.user
                        old_password = password_form.cleaned_data['old_password']
                        new_password = password_form.cleaned_data['new_password1']
                        new_passwordd = password_form.cleaned_data['new_password2']

                        # Check if the old password is correct
                        if user.check_password(old_password):
                            if new_password == new_passwordd:
                                user.set_password(new_password)
                                user.save()
                                update_session_auth_hash(request, user)
                                messages.success(
                                    request, 'Your password was successfully updated!')
                                return redirect('profile')
                            else:
                                messages.warning(
                                    request, 'Your new passwords does not match!')
                                return redirect('profile')
                        else:
                            messages.warning(
                                request, 'Incorrect old password. Please try again.')
            except:
                messages.warning(request, 'An error occured. Please try again')
                return redirect('profile')

        # For Order Notification ---------------------------------------
        cart = CartItem.objects.filter(slug=request.user.slug)
        carts = cart.values('phone').distinct()

        # -----------------------------------------------------------------
        facebookk = user.facebook
        facebook = facebookk[25:]

        whatsap = user.whatsapp
        whatsapp = whatsap[14:]

        instagramm = user.instagram
        instagram = instagramm[26:]

        context = {'facebook': facebook, 'whatsapp': whatsapp,
                   'instagram': instagram, 'password_form': password_form, 'carts': carts}
    return render(request, 'myapp/profile.html', context)


# Functions

# FREE TRIAL
# @receiver(post_save, sender=User)
# def set_trial_dates(sender, instance, created, **kwargs):
#     if created:
#         # instance.trial_start = datetime.now()
#         instance.trial_start = user.date_joined
#         instance.trial_end = instance.trial_start + \
#             timedelta(days=2)  # 2 days trial
#         instance.save()

def set_trial_dates(user):
    # Set the trial start date to the current date
    user.trial_start = user.date_joined
    # Adjust the trial period as needed
    user.trial_end = user.trial_start + timedelta(days=14)


def process_data(request):
    if request.method == 'POST':

        # Extract user input from the request
        # firstname = request.POST['firstname']
        # lastname = request.POST['lastname']
        username = request.POST.get("username")
        email = request.POST['email']
        # gender = request.POST['gender']
        # dob = request.POST['dob']
        # status = request.POST['status']
        # country = request.POST['country']
        # state = request.POST['state']
        # address = request.POST['address']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        # More Info
        # Extract additional user input
        # securityquestion = request.POST['securityquestion']
        # securityanswer = request.POST['securityanswer']
        # phone1 = request.POST['phone']
        # phone = ''.join(phone1.split())
        # meansofid = request.POST['identification']
        # idnumber = request.POST['cardnumber']
        # idpic = request.FILES.get('uploadedFile')
        # profilepic = request.FILES.get('profilepic')
        # businessname = request.POST['businessname']
        # logo = request.FILES.get('logo')
        # businesstype = request.POST['businesstype']
        # currency = request.POST['currency']
        # shopcategory = request.POST['shopcategory']
        # moredesc = request.POST['moredesc']
        # whatsap1 = request.POST['whatsapp']
        # whatsap = ''.join(whatsap1.split())

        # whatsapp = f"https://wa.me/{whatsap}"
        # facebookk = request.POST['facebook']
        # facebook = f"https://www.facebook.com/{facebookk}"
        # instagramm = request.POST['instagram']
        # instagram = f"https://www.instagram.com/{instagramm}"
        # ---------End of More_info-----------

        # Check if passwords match
        if password == confirmpassword:
            # Check if email and username are already in use
            if User.objects.filter(email=email).exists():
                user = auth.authenticate(
                    email=email, password=password)
                if user is not None:
                    auth.login(request, user)
                    # return redirect('more_info')
                    return redirect('portal')
                else:
                    messages.warning(
                        request, 'Email is already used')
                    return HttpResponseRedirect(request.path_info)

                # New line for More Info-------------------------------------
            # elif User.objects.filter(businessname=businessname).exists():
            #     messages.warning(request, 'Business Name already taken')
            #     return HttpResponseRedirect(request.path_info)
                # return redirect(request.META.get('HTTP_REFERER', 'registerform'))
                # return redirect('registerform')
            else:
                # Create the user
                # record(businessname, moredesc, firstname, lastname, email, gender, phone, country, state, address, meansofid, idnumber, whatsapp, facebook, instagram)
                user = User.objects.create_user(
                    first_name=None,
                    username=username, last_name=None, email=email,
                    gender=None, country=None, state=None, address=None, password=password,
                    # Added More Info
                    securityquestion=None,
                    securityanswer=None,
                    phone=None,
                    meansofid=None,
                    idnumber=None,
                    idpic=None,
                    profilepic=None,
                    businessname=None,
                    logo=None,
                    # businesstype=businesstype,
                    currency=None,
                    # shopcategory=shopcategory,
                    moredesc=None,
                    whatsapp=None,
                    facebook=None,
                    instagram=None,
                    # dob=dob, status=status,
                    record = f'{email}_record'+'.txt'
                )

                # Call the function to set trial dates
                set_trial_dates(user)
                # ----------------------------------

                user = auth.authenticate(
                    email=email, password=password)
                auth.login(request, user)

                # Password Recovery------------------
                # passwordreset = f"{user.securityanswer}{user.slug}"
                # passwordresetphone = f"{user.phone}{user.slug}"
                # user.passwordresetcode = passwordreset
                # user.passwordresetphone = passwordresetphone
                # ------------------------------------------
                user.save()

                return redirect('more_info')
                # return redirect('info')

        else:
            messages.warning(request, 'Password does not match')
            return redirect(request.META.get('HTTP_REFERER', 'registerform'))

    else:
        return render(request, 'myapp/register.html')


@login_required(login_url='loginform')
def logoutbutton(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='loginform')
def category(request):

    if request.user.is_authenticated:
        user = request.user
        # Check the subscription status (and set user.slug)
        check_expired(request, user)

        product = Product.objects.filter(owner=request.user)

        categories = product.values('itemcategory').distinct()

        # For Order Notification ---------------------------------------
        cart = CartItem.objects.filter(slug=request.user.slug)
        carts = cart.values('phone').distinct()

        # -----------------------------------------------------------------

        context = {'categories': categories,
                   'product': product, 'carts': carts}
    return render(request, 'myapp/category.html', context)


@login_required(login_url='loginform')
def item(request, selected_category):
    if request.user.is_authenticated:
        shop = Product.objects.filter(
            owner=request.user, itemcategory=selected_category)
        categories = Product.objects.filter(
            owner=request.user).values('itemcategory').distinct()

        # For Order Notification ---------------------------------------
        cart = CartItem.objects.filter(slug=request.user.slug)
        carts = cart.values('phone').distinct()

        # -----------------------------------------------------------------

        context = {'categories': categories, 'shop': shop, 'carts': carts}

    return render(request, 'myapp/category.html', context)


@login_required(login_url='loginform')
def editproduct(request, pk):
    shop = Product.objects.get(id=pk)
    user = shop.owner

    # Check the subscription status (and set user.slug)
    check_expired(request, user)

    product = Product.objects.filter(owner=user)

    categories = product.values('itemcategory').distinct()

    # For Order Notification ---------------------------------------
    cart = CartItem.objects.filter(slug=request.user.slug)
    carts = cart.values('phone').distinct()

    # -----------------------------------------------------------------

    context = {'shop': shop,
               'user': user, 'categories': categories, 'carts': carts}

    if request.method == 'POST':
        try:
            if 'update_pic' in request.POST:
                itemimage = request.FILES.get('itemimage')

                shop.itemimage = itemimage
                shop.save()
                messages.success(request, 'Product photo updated successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif 'update_pic2' in request.POST:
                itemimage2 = request.FILES.get('itemimage2')

                shop.itemimage2 = itemimage2
                shop.save()

                messages.success(request, 'Product photo updated successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif 'update_pic3' in request.POST:

                itemimage3 = request.FILES.get('itemimage3')

                shop.itemimage3 = itemimage3
                shop.save()
                messages.success(request, 'Product photo updated successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif 'update_vid' in request.POST:

                itemvideo = request.FILES.get('itemvideo4')

                shop.itemvideo = itemvideo
                shop.save()

                messages.success(request, 'Product Video updated successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif 'update_product' in request.POST:
                itemname = request.POST.get('itemname')
                itemcategory = request.POST.get('category')
                itemprice = request.POST.get('itemprice')
                itemdiscount = request.POST.get('itemdiscount')
                itemcolour = request.POST.get('itemcolour')
                itemsize = request.POST.get('itemsize')
                itemdescription = request.POST.get('itemdescription')

                if itemdiscount != 0:
                    amount = float(itemprice)-float(itemdiscount)

                else:
                    amount = itemprice

                shop.itemname = itemname
                shop.itemcategory = itemcategory
                shop.itemprice = itemprice
                shop.itemamount = amount
                shop.itemdiscount = itemdiscount
                shop.itemcolors = itemcolour
                shop.itemsize = itemsize
                shop.itemdescription = itemdescription

                shop.save()

                messages.success(request, 'Product updated successfully')
                return redirect('category')
            else:
                messages.warning(request, 'Not Successful')
                return redirect('category')
        except:
            messages.warning(
                request, 'An unexpected error occured. Please fill in the fields correctly')
            return redirect('category')

    return render(request, 'myapp/editproduct.html', context)


@login_required(login_url='loginform')
def delete(request, pk):
    product = Product.objects.get(id=pk)

    # For Order Notification ---------------------------------------
    cart = CartItem.objects.filter(slug=request.user.slug)
    carts = cart.values('phone').distinct()

    # -----------------------------------------------------------------

    if request.method == "POST":
        product.delete()

        messages.success(request, "Item deleted")
        return redirect('category')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'product': product, 'carts': carts}

    return render(request, 'myapp/deleteproduct.html', context)


@login_required(login_url='loginform')
def order(request, pk):
    context = {}
    if request.user.is_authenticated:
        person = CartItem.objects.filter(phone=pk)

        # person = person.values('purchaser').distinct()
        persons = person.values('phone').distinct()

        # print(person)

        # For Order Notification ---------------------------------------
        cart = CartItem.objects.filter(slug=request.user.slug)
        carts = cart.values('phone').distinct()
        cartname = carts.values('purchaser').distinct()

    # -----------------------------------------------------------------

        # Cart Function--------------------------------------
        user = request.user

        cart_items = []

        for cart_item in CartItem.objects.filter(slug=user.slug):
            if cart_item.phone == pk:
                cart_items.append({
                    'product_it': cart_item.product,
                    'name': cart_item.name,
                    'price': cart_item.price,
                    'quantity': cart_item.quantity,
                    'size': cart_item.size,
                    'color': cart_item.color,
                    'image_url': cart_item.image_url,
                    'cart_image': cart_item.cart_image,
                    'purchaser': cart_item.purchaser,
                    'phone': cart_item.phone,
                })

    for person in person:
        if person.slug == request.user.slug:

            cart_total = calculate_cart_total(cart_items)
            context = {'person': person,
                       'carts': carts, 'cartname': cartname, 'user': user, 'cart_items': cart_items, 'cart_item': cart_item, 'cart_total': cart_total, 'persons': persons}
    return render(request, 'myapp/order.html', context)


@login_required(login_url='loginform')
def clear(request, pk):
    user = request.user.slug
    product = CartItem.objects.filter(phone=pk)

    if request.method == 'POST':
        for product in product:
            if product.slug == user:
                product.delete()

        return redirect('portal')
    else:
        return render(request, 'myapp/portal.html')


def purchaser(request, pk, pk2):
    context = {}
    # if request.user.is_authenticated:
    # person = CartItem.objects.filter(phone=pk)
    person = CartItem.objects.filter(phone=pk)
    person2 = person.filter(slug=pk2)
    user = User.objects.get(slug=pk2)

    # person = person.values('purchaser').distinct()
    persons = person.values('phone').distinct()

    # print(person)

    # For Order Notification ---------------------------------------
    # cart = CartItem.objects.filter(slug=request.user.slug)
    # carts = cart.values('phone').distinct()
    # cartname = carts.values('purchaser').distinct()

    # -----------------------------------------------------------------

    # Cart Function--------------------------------------
    # user = request.user

    cart_items = []

    for cart_item in CartItem.objects.filter(slug=pk2):
        if cart_item.phone == pk:
            cart_items.append({
                'product_it': cart_item.product,
                'name': cart_item.name,
                'price': cart_item.price,
                'quantity': cart_item.quantity,
                'size': cart_item.size,
                'color': cart_item.color,
                'image_url': cart_item.image_url,
                'cart_image': cart_item.cart_image,
                'purchaser': cart_item.purchaser,
                'phone': cart_item.phone,
            })

    for person in person:
        if person.slug == pk2:

            cart_total = calculate_cart_total(cart_items)
            context = {'person': person,
                       #    'carts': carts, 'cartname': cartname,
                       'user': user,
                       'cart_items': cart_items, 'cart_item': cart_item, 'cart_total': cart_total, 'persons': persons}
    return render(request, 'myapp/purchaser.html', context)


# def search(request, pk):
#     user = get_object_or_404(User, slug=pk)
#     shop = Product.objects.filter(owner=user)

#     q = request.GET.get('q', '')

#     # Filter for exact name match
#     exact_name_match = shop.filter(itemname__iexact=q)

#     # Filter for items containing the name
#     contains_name = shop.annotate(full_name=Concat(
#         'itemname', Value(' '))).filter(full_name__icontains=q)

#     # Filter numeric fields with exact match, and other fields with case-insensitive exact match
#     product = exact_name_match | contains_name

#     # Filter itemamount with exact match only if it's numeric
#     if q.isdigit():
#         product = product.filter(itemamount=q)

#     categories = product.values('itemcategory').distinct()

#     context = {'categories': categories, 'shop': product, 'user': user}

#     return render(request, 'myapp/cat_search.html', context)

def cat_search(request, pk):
    user = request.user

    shop = Product.objects.filter(owner=request.user)

    q = request.GET.get('q', '')

    # Filter for exact name match
    exact_name_match = shop.filter(itemname__iexact=q)

    # Filter for items containing the name
    contains_name = shop.annotate(full_name=Concat(
        'itemname', Value(' '))).filter(full_name__icontains=q)

    # Filter numeric fields with exact match, and other fields with case-insensitive exact match
    product = exact_name_match | contains_name

    # Filter itemamount with exact match only if it's numeric
    if q.isdigit():
        product = product.filter(itemamount=q)

    categories = product.values('itemcategory').distinct()

    # For Order Notification ---------------------------------------
    cart = CartItem.objects.filter(slug=request.user.slug)
    carts = cart.values('phone').distinct()

    #

    context = {'categories': categories,
               'product': product, 'user': user, 'carts': carts}

    return render(request, 'myapp/cat_search.html', context)


# ----------Django Rest Framework------------------
class UserPostListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def delete(self, request, *args, **kwargs):
    #     User.objects.all().delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"


def refund_policy(request):
    nairaGold = NairaSubscriptionPlan.objects.get(plan_type='Gold')
    nairaSilver = NairaSubscriptionPlan.objects.get(plan_type='Silver')
    nairaBronze = NairaSubscriptionPlan.objects.get(plan_type='Bronze')
    nairaPlatinum = NairaSubscriptionPlan.objects.get(plan_type='Platinum')
    # Foreign
    # foreignnairaGold = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignGold')
    # foreignnairaSilver = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignSilver')
    # foreignnairaBronze = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignBronze')
    # foreignnairaPlatinum = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignPlatinum')
    # foreignnairaBasic = NairaSubscriptionPlan.objects.get(
    #     plan_type='ForeignBasic')

    dollarGold = DollarSubscriptionPlan.objects.get(plan_type='Gold')
    dollarSilver = DollarSubscriptionPlan.objects.get(plan_type='Silver')
    dollarBronze = DollarSubscriptionPlan.objects.get(plan_type='Bronze')
    dollarPlatinum = DollarSubscriptionPlan.objects.get(
        plan_type='Platinum')

    context = {'nairaGold': int(nairaGold.price), 'nairaSilver': int(nairaSilver.price),
               'nairaBronze': int(nairaBronze.price), 'nairaPlatinum': int(nairaPlatinum.price), 'dollarGold': int(dollarGold.price), 'dollarSilver': int(dollarSilver.price), 'dollarBronze': int(dollarBronze.price), 'dollarPlatinum': int(dollarPlatinum.price),
               # 'foreignnairaGold': int(foreignnairaGold.price), 'foreignnairaSilver': int(foreignnairaSilver.price), 'foreignnairaPlatinum': int(foreignnairaPlatinum.price), 'foreignnairaBronze': int(foreignnairaBronze.price), 'foreignnairaBasic': int(foreignnairaBasic.price),

               }
    return render(request, "myapp/refund_policy.html", context)
