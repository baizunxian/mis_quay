from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from equipment.models import Quay_crane, AGV
from information.models import Container
from plan.models import Bay_position
from information.models import VesselInfo, Voyage



def qc_equipment(request):
    """
    qc 管理页面
    :param request:
    :return:
    """
    qc_list = Quay_crane.objects.all()
    return render(request, "equipment/qc_equipment.html", {'qc_list': qc_list})


def agv_equipment(request):
    """
    agv 管理页面
    :param request:
    :return:
    """
    agv_list = AGV.objects.all()
    return render(request, "equipment/agv_equipment.html", {'agv_list': agv_list})


def qc_add(request):
    """
    添加 qc
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        qc_id = request.POST.get('qc_id', None)
        sea_state = request.POST.get('sea_state', None)
        land_state = request.POST.get('land_state', None)
        situation = request.POST.get('situation', None)
        middle_space = request.POST.get('middle_space', None)
        weight_max = request.POST.get('weight_max', None)
        if Quay_crane.objects.filter(qc_id=qc_id).exists():
            data = {
                'code': -2,
                'msg': '当前岸桥编号以存在！'
            }
            return JsonResponse(data)
        else:
            try:
                qc_info = Quay_crane()
                qc_info.qc_id = qc_id
                qc_info.sea_state = sea_state
                qc_info.land_state = land_state
                qc_info.situation = situation
                qc_info.middle_space = middle_space
                qc_info.weight_max = weight_max
                qc_info.save()
            except Exception as err:
                data = {
                    'code': -1,
                    'msg': '保存失败！'
                }
                return JsonResponse(data)
            data = {
                'code': 0,
                'msg': '保存成功！'
            }
            return JsonResponse(data)
    else:
        return render(request, 'qc_add.html')


def agv_add(request):
    """
    添加 agv
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        agv_id = request.POST.get('agv_id', None)
        situation = request.POST.get('situation', None)
        state = request.POST.get('state', None)
        if AGV.objects.filter(agv_id=agv_id).exists():
            data = {
                'code': -2,
                'msg': '当前AGV编号以存在！'
            }
            return JsonResponse(data)
        else:
            try:
                agv_info = AGV()
                agv_info.agv_id = agv_id
                agv_info.situation = situation
                agv_info.state = state
                agv_info.save()
            except Exception as err:
                print(err)
                data = {
                    'code': -1,
                    'msg': '保存失败！'
                }
                return JsonResponse(data)
            data = {
                'code': 0,
                'msg': '保存成功！'
            }
            return JsonResponse(data)

    else:
        return render(request, 'agv_add.html')


def qc_edit(request):
    """
    修改 qc
    :param request:
    :return:
    """
    if request.method == "POST":
        print(request.POST)
        qc_id = request.POST.get('qc_id', None)
        sea_state = request.POST.get('sea_state', None)
        land_state = request.POST.get('land_state', None)
        situation = request.POST.get('situation', None)
        middle_space = request.POST.get('middle_space', None)
        weight_max = request.POST.get('weight_max', None)
        qc_info = Quay_crane.objects.get(qc_id=qc_id)
        qc_info.sea_state = sea_state
        qc_info.land_state = land_state
        qc_info.situation = situation
        qc_info.middle_space = middle_space
        qc_info.weight_max = weight_max
        qc_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    else:
        print(request.GET)
        qc_id = request.GET.get('qc_id', None)
        qc_info = Quay_crane.objects.get(qc_id=qc_id)
        return render(request, 'qc_edit.html', {'qc_info': qc_info})


def agv_edit(request):
    """
    agv 编辑
    :param request:
    :return:
    """
    if request.method == "POST":
        agv_id = request.POST.get('agv_id', None)
        situation = request.POST.get('situation', None)
        state = request.POST.get('state', None)
        agv_info = AGV.objects.get(agv_id=agv_id)
        agv_info.situation = situation
        agv_info.state = state
        agv_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    else:
        agv_id = request.GET.get('agv_id', None)
        agv_info = AGV.objects.get(agv_id=agv_id)
        return render(request, 'agv_edit.html', {'agv_info': agv_info})


def qc_delete(request):
    """
    删除 岸桥
    :param request:
    :return:
    """
    qc_id = request.POST.get('qc_id')
    if qc_id:
        Quay_crane.objects.get(qc_id=qc_id).delete()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)


def agv_delete(request):
    """
    删除 agv
    :param request:
    :return:
    """
    agv_id = request.POST.get('agv_id')
    if agv_id:
        AGV.objects.get(agv_id=agv_id).delete()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)


def qc_plan(request):
    print(request.GET)
    v_id = request.GET.get('v_id')
    voy = request.GET.get('voy')
    v_info = VesselInfo.objects.get(id=v_id)
    voy_info = Voyage.objects.get(id=voy)
    bay_list = Bay_position.objects.all()
    qc_list = Quay_crane.objects.filter(sea_state=2, land_state=2, situation=1)
    data ={'v_id': v_id,
           'voy': voy,
           'qc_list': qc_list,
           'bay_list': bay_list,
           'v_info': v_info,
           'voy_info': voy_info,
           }
    return render(request, 'equipment/qc_plan.html', data)


def get_by_bay_id(request):
    print(request.POST)
    v_id = request.POST.get('v_id')
    voy = request.POST.get('voy')
    bay = request.POST.get('bay')
    container_info = Container.objects.filter(vessel_id=v_id, voy_id=voy, bay_id=bay)
    container_list = list()
    if container_info:
        for container in container_info:
            container_dict = dict()
            container_dict['space'] = container.space
            container_dict['type'] = container.type
            container_list.append(container_dict)
        data = {
            'code': 0,
            'container_list': container_list
        }
        return JsonResponse(data)
    else:
        data = {
            'code': 0,
            'container_list': []
        }
        return JsonResponse(data)
