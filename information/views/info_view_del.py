from django.http import JsonResponse

from information.models import VesselInfo, Container, Voyage


def delete_vessel(request):
    """
    删除船信息
    :param request:
    :return:
    """
    print(request.POST)
    v_id = request.POST.get('v_id')
    VesselInfo.objects.get(id=v_id).delete()
    data = {
        'code': 0,
        'msg': '删除成功!'
    }
    return JsonResponse(data)


def delete_container(request):
    """
    删除出口信息
    :param request:
    :return:
    """
    print(request.POST)
    c_id = request.POST.get('c_id')
    Container.objects.get(id=c_id).delete()
    data = {
        'code': 0,
        'msg': '删除成功!'
    }
    return JsonResponse(data)



def delete_voy(request):
    """
    删除进出口航次
    :param request:
    :return:
    """
    v_id = request.POST.get('v_id')
    Voyage.objects.get(id=v_id).delete()
    data = {
        'code': 0,
        'msg': '删除成功!'
    }
    return JsonResponse(data)


