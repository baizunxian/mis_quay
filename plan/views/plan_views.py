from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
from equipment.models import Quay_crane
from information.models import *
from django.db.models import Q
from plan.models import Plan_unloading

from utils.common import Handling_check


def vessel_plan(request):
    voy_list = Voyage.objects.all()
    return render(request, "plan/vessel_plan.html", {'voy_list': voy_list})


# def vessel_chart(request):
#     v_id = request.GET.get('v_id')
#     voy = request.GET.get('voy')
#     voy_type = request.GET.get('voy')
#     print(request.GET)
#     return render(request, "plan/vessel_chart.html")


# def unloading_plan(request):
#     return render(request, "plan/../../templates/job/unloading_plan.html")


def unloading_plan_manage(request):
    sql = 'select * from plan_plan_unloading p , info_container i where p.plan_id = i.plan_id'
    plan_un_info = Plan_unloading.objects.raw(sql)
    data = {
        'plan_un_info': plan_un_info
    }
    return render(request, 'unloading_plan_manage.html', data)


def unloading_planning_page(request):
    """
    卸船计划页面
    :param request:
    :return:
    """
    qc_id = request.GET.get('qc')
    voy_id = request.GET.get('voy_id')
    voyage_info = Voyage.objects.get(id=voy_id)
    if qc_id:
        container_list = Container.objects.filter(~Q(qc_id=None), type=0, qc_id=qc_id).order_by('bay_id')
        qc_list = Quay_crane.objects.all()
        data = {
            'container_list': container_list,
            'qc_list': qc_list,
            'voyage_info': voyage_info,
        }
        return render(request, 'unloading_planning.html', data)
    else:
        container_list = Container.objects.filter(~Q(qc_id=None), type=0).order_by('bay_id')
        qc_list = Quay_crane.objects.all()
        data = {
            'container_list': container_list,
            'qc_list': qc_list,
            'voyage_info': voyage_info,
        }
        return render(request, 'unloading_planning.html', data)


def loading_planning_page(request):
    """
    装船计划页面
    :param request:
    :return:
    """
    qc_id = request.GET.get('qc')
    voy_id = request.GET.get('voy_id')
    voyage_info = Voyage.objects.get(id=voy_id)
    if qc_id:
        container_list = Container.objects.filter(~Q(qc_id=None), type=1, qc_id=qc_id).order_by('bay_id')
        qc_list = Quay_crane.objects.all()
        data = {
            'container_list': container_list,
            'qc_list': qc_list,
            'voyage_info': voyage_info,
        }
        return render(request, 'loading_planning.html', data)
    else:
        container_list = Container.objects.filter(~Q(qc_id=None), type=1).order_by('bay_id')
        qc_list = Quay_crane.objects.all()
        data = {
            'container_list': container_list,
            'qc_list': qc_list,
            'voyage_info': voyage_info,
        }
        return render(request, 'loading_planning.html', data)


def loading_plan_manage(request):
    return render(request, 'loading_plan_manage.html')


def loading_planning(request):
    return render(request, 'loading_planning.html')


def handling_planning(request):
    """
    添加装卸船计划号
    :param request:
    :return:
    """
    # handling_type   0 卸船  1 装船
    print(request.POST)
    ck_list = request.POST.getlist('ck_list', None)
    # 判断装船还是卸船
    handling_type = request.POST.get('handling_type', None)
    result = Handling_check(ck_list, handling_type)
    data = {
        'code': result['code'],
        'msg': result['msg']
    }
    return JsonResponse(data)


def delete_plan(request):
    """
    删除卸船计划
    :param request:
    :return:
    """
    print(request.POST)
    plan_list = request.POST.getlist('plan_ids')
    Plan_unloading.objects.filter(plan_id__in=plan_list).delete()
    data = {
        'code': 0,
        'msg': '删除成功！'
    }
    return JsonResponse(data)
