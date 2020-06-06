from django.shortcuts import render


# Create your views here.
from information.models import *



def vessel_plan(request):
    voy_list = Voyage.objects.all()
    return render(request, "plan/vessel_plan.html", {'voy_list': voy_list})


def vessel_chart(request):
    v_id = request.GET.get('v_id')
    voy = request.GET.get('voy')
    voy_type = request.GET.get('voy')
    print(request.GET)
    return render(request, "plan/vessel_chart.html")


def unloading_plan(request):
    return render(request, "plan/unloading_plan.html")
