from django.http import JsonResponse

from information.models import VesselInfo, Container


def search_vessel(request):
    """
    查询船信息
    :param request:
    :return:
    """
    en_name = request.POST.get('en_name', None)
    vessel_info = VesselInfo.objects.filter(en_name__contains=en_name)
    vessel_list = list()
    for vessel in vessel_info:
        vessel_dict = dict()
        vessel_dict['id'] = vessel.id
        vessel_dict['en_name'] = vessel.en_name
        vessel_dict['cn_name'] = vessel.cn_name
        # vessel_dict['voy_im_x'] = vessel.voy_im_x
        # vessel_dict['voy_ex_x'] = vessel.voy_ex_x
        # vessel_dict['ETB'] = vessel.ETB
        # vessel_dict['ETD'] = vessel.ETD
        vessel_list.append(vessel_dict)
    data = {
        'code': 0,
        'vessel_list': vessel_list
    }
    return JsonResponse(data)


def search_container(request):
    """
    查询进出口信息
    :param request:
    :return:
    """
    print(request.POST)
    voy = request.POST.get('voy', None)
    container_info = Container.objects.filter(voy__voy_im__contains=voy)
    container_list = list()
    for container in container_info:
        container_dict = dict()
        container_dict['id'] = container.id
        container_dict['iso_no'] = container.iso_no
        container_dict['voy_im'] = container.voy.voy_im
        container_dict['voy_ex'] = container.voy.voy_ex
        container_dict['vessel_cn'] = container.vessel.cn_name
        container_dict['vessel_en'] = container.vessel.en_name
        container_dict['space'] = container.space
        container_dict['size'] = container.size
        container_dict['weight'] = container.weight
        container_dict['special'] = container.special
        container_dict['type'] = container.type
        container_list.append(container_dict)
    data = {
        'code': 0,
        'container_list': container_list
    }
    return JsonResponse(data)
