from django.shortcuts import render

# Create your views here.
def vessel_plan(request):

    return render(request, "plan/vessel_plan.html")


def vessel_chart(request):

    return render(request, "plan/vessel_chart.html")


def unloading_plan(request):

    return render(request, "plan/../templates/job/unloading_plan.html")