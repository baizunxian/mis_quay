from django.shortcuts import render
from information.models import Voyage
from plan.models import Plan_unloading


# Create your views here.


def vessel_job(request):
    voy_list = Voyage.objects.all()
    return render(request, 'job/vessel_job.html', {'voy_list': voy_list})


def unloading_control(request):
    """
    卸船作业控制
    :param request:
    :return:
    """
    plan_un_info = Plan_unloading.objects.all()
    print(plan_un_info)
    data = {
        'plan_un_info': plan_un_info
    }
    return render(request, 'job/unloading_control.html', data)


def unloading_record(request):
    return render(request, 'job/unloading_record.html')


def unloading_job(request):
    return render(request, 'job/unloading_job.html')


def grab_box(request):
    """
    抓箱操作
    :param request:
    :return:
    """
    pass