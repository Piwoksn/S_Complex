from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import Subscription, NairaSubscriptionPlan, DollarSubscriptionPlan
# Create your views here.
# subscription


@login_required(login_url='loginform')
def subscription(request):
    if request.user.is_authenticated:
        user = request.user
        nairaGold = NairaSubscriptionPlan.objects.get(plan_type='Gold')
        nairaSilver = NairaSubscriptionPlan.objects.get(plan_type='Silver')
        nairaBronze = NairaSubscriptionPlan.objects.get(plan_type='Bronze')
        nairaPlatinum = NairaSubscriptionPlan.objects.get(plan_type='Platinum')
        nairaBasic = NairaSubscriptionPlan.objects.get(plan_type='Basic')

        foreignnairaGold = NairaSubscriptionPlan.objects.get(
            plan_type='ForeignGold')
        foreignnairaSilver = NairaSubscriptionPlan.objects.get(
            plan_type='ForeignSilver')
        foreignnairaBronze = NairaSubscriptionPlan.objects.get(
            plan_type='ForeignBronze')
        foreignnairaPlatinum = NairaSubscriptionPlan.objects.get(
            plan_type='ForeignPlatinum')
        foreignnairaBasic = NairaSubscriptionPlan.objects.get(
            plan_type='ForeignBasic')

        dollarGold = DollarSubscriptionPlan.objects.get(plan_type='Gold')
        dollarSilver = DollarSubscriptionPlan.objects.get(plan_type='Silver')
        dollarBronze = DollarSubscriptionPlan.objects.get(plan_type='Bronze')
        dollarPlatinum = DollarSubscriptionPlan.objects.get(
            plan_type='Platinum')
        dollarBasic = DollarSubscriptionPlan.objects.get(
            plan_type='Basic')

    context = {'user': user, 'nairaGold': nairaGold, 'nairaSilver': nairaSilver,
               'nairaBronze': nairaBronze, 'nairaPlatinum': nairaPlatinum, 'nairaBasic': nairaBasic, 'dollarGold': dollarGold, 'dollarSilver': dollarSilver, 'dollarBronze': dollarBronze, 'dollarPlatinum': dollarPlatinum, 'dollarBasic': dollarBasic, 'foreignnairaGold': foreignnairaGold, 'foreignnairaSilver': foreignnairaSilver, 'foreignnairaPlatinum': foreignnairaPlatinum, 'foreignnairaBronze': foreignnairaBronze, 'foreignnairaBasic': foreignnairaBasic, }
    return render(request, 'subscription/subscription.html', context)
