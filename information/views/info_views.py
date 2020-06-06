from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

# Create your views here.
from information.models import *
from plan.models import Bay_position


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == "POST":
        user_id = request.POST.get('userid')
        password = request.POST.get('password')
        if user_id and password:
            try:
                # 判断用户在不在
                user_info = UserInfo.objects.get(user_id=user_id)
            except Exception as err:
                data = {
                    'code': -1,
                    'msg': '账号或密码错误！'
                }
                return JsonResponse(data)
            # 判断密码是否匹配
            if user_info.code == password:
                request.session['user_id'] = user_id
                request.session['username'] = user_info.name
                data = {
                    'code': 0,
                    'msg': '登录成功'
                }
                return JsonResponse(data)
            # 不匹配返回
            else:
                data = {
                    'code': -2,
                    'msg': '账号或密码错误！'
                }
                return JsonResponse(data)
    else:
        return render(request, "login.html")


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    # 删除 用户session
    del request.session['user_id']
    del request.session['username']
    return render(request, 'login.html')


def index(request):
    return render(request, "index.html")


def informationinput(request):
    vessel_list = VesselInfo.objects.all()
    bay_list = Bay_position.objects.all()
    return render(request, "info/informationinput.html", {'vessel_list': vessel_list, 'bay_list': bay_list})


def get_voy_info(request):
    """
    获取进出口航次信息
    :param request:
    :return:
    """
    vessel_id = request.GET.get('vessel_id', None)
    if vessel_id:
        voy_info = Voyage.objects.filter(vessel_id=vessel_id)
        voy_info_list = list()
        for voy in voy_info:
            voy_info_dict = dict()
            voy_info_dict['id'] = voy.id
            voy_info_dict['voy_im'] = voy.voy_im
            voy_info_dict['voy_ex'] = voy.voy_ex
            voy_info_dict['vessel_cn'] = voy.vessel.cn_name
            voy_info_dict['vessel_en'] = voy.vessel.en_name
            voy_info_list.append(voy_info_dict)
        data = {
            'code': 0,
            'voy_info_list': voy_info_list
        }
        return JsonResponse(data)
    else:
        data = {
            'code': 0,
            'Voy_im_info_list': []
        }
        return JsonResponse(data)

def get_voy_ex_info(request):
    """
    获取出口航次信息
    :param request:
    :return:
    """
    vessel_id = request.GET.get('vessel_id', None)
    if vessel_id:
        voy_ex_info = Voy_ex.objects.filter(vessel_id=vessel_id)
        voy_ex_info_list = list()
        for voy_ex in voy_ex_info:
            Voy_ex_info_dict = dict()
            Voy_ex_info_dict['id'] = voy_ex.id
            Voy_ex_info_dict['voy_ex'] = voy_ex.voy_ex
            Voy_ex_info_dict['vessel_cn'] = voy_ex.vessel.cn_name
            Voy_ex_info_dict['vessel_en'] = voy_ex.vessel.en_name
            voy_ex_info_list.append(Voy_ex_info_dict)
        data = {
            'code': 0,
            'voy_ex_info_list': voy_ex_info_list
        }
        return JsonResponse(data)
    else:
        data = {
            'code': 0,
            'voy_ex_info_list': []
        }
        return JsonResponse(data)


def vesselinfo_maintain(request):
    vesselinfo_list = VesselInfo.objects.all()
    return render(request, "info/vesselinfo_maintain.html", {'vesselinfo_list': vesselinfo_list})


def container_maintain(request):
    container_list = Container.objects.all()
    return render(request, "info/container_maintain.html", {'container_list': container_list})


def container_e_info_maintain(request):
    container_e_list = Container_e_Info.objects.all()
    return render(request, "info/container_info_maintain.html", {'container_e_list': container_e_list})


def container_add(request):
    vessel_list = VesselInfo.objects.all()
    bay_list = Bay_position.objects.all()
    return render(request, "info/container_add.html", {'vessel_list': vessel_list, 'bay_list': bay_list})


def vessel_add(request):
    return render(request, "info/vessel_add.html")


def voy(request):
    """
    航次录入页面
    :param request:
    :return:
    """
    vessel_list = VesselInfo.objects.all()
    return render(request, 'info/voy.html', {'vessel_list': vessel_list})


def voy_maintain(request):
    """
    进口航次管理页面
    :param request:
    :return:
    """
    voy_list = Voyage.objects.all()
    return render(request, 'info/voy_maintain.html', {'voy_list': voy_list})
