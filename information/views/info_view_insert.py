from django.db import transaction
from django.http import JsonResponse

from information.models import VesselInfo, Voyage, Container
from utils.common import data_processing
from plan.models import Bay_position


def vesselInfo_input(request):
    """
    船舶信息入库
    :param request:
    :return:
    """
    print(request.POST)
    en_name = request.POST.get('en_name', None)
    cn_name = request.POST.get('cn_name', None)
    if VesselInfo.objects.filter(en_name=en_name).exists():
        data = {
            'code': -5,
            'msg': '当前英文名的船已存在！'
        }
        return JsonResponse(data)
    else:
        try:
            # 事务回滚
            with transaction.atomic():
                vessel_info = VesselInfo()
                save_id = transaction.savepoint()
                # 保存船信息
                vessel_info.en_name = en_name
                vessel_info.cn_name = cn_name
                vessel_info.save()
        except Exception as err:
            transaction.savepoint_rollback(save_id)
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


def container_input(request):
    """
    进出口箱信息入库
    :param request:
    :return:
    """
    print(request.POST)
    iso_no = request.POST.get('iso_no', None)
    vessel = request.POST.get('vessel', None)
    voy = request.POST.get('voy', None)
    space = request.POST.get('space', None)
    size = request.POST.get('size', None)
    weight = request.POST.get('weight', None)
    type_yn = request.POST.get('type_yn', None)
    voy_type = request.POST.get('voy_type', None)
    bay_id = request.POST.get('bay', None)
    objs = Container.objects.filter(voy=voy, vessel=vessel, bay=bay_id, type=voy_type)
    # 调用数据处理方法
    bay = Bay_position.objects.get(id=bay_id).bay.split(',')
    if space[:2] in bay:
        if data_processing(objs, space, bay):
            try:
                container = Container()
                container.iso_no = iso_no
                container.voy_id = voy
                container.vessel_id = vessel
                container.space = space
                container.size = size
                container.weight = weight
                container.special = type_yn
                container.bay_id = bay_id
                container.type = voy_type
                container.save()
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
            data = {
                'code': -2,
                'msg': '该船当前航次进口的箱位已录入，请重新填写！'
            }
            return JsonResponse(data)
    else:
        data = {
            'code': -3,
            'msg': '箱位号前两位必须在选择的贝位列表中！'
        }
        return JsonResponse(data)


def container_e_Info_input(request):
    """
    出口箱信息入库
    :param request:
    :return:
    """
    print(request.POST)
    iso_no = request.POST.get('ex_iso_no', None)
    voy_ex = request.POST.get('voy', None)
    vessel = request.POST.get('vessel_select', None)
    space = request.POST.get('ex_space', None)
    size = request.POST.get('ex_size', None)
    weight = request.POST.get('ex_weight', None)
    type_yn = request.POST.get('ex_type_yn', None)
    bay_id = request.POST.get('bay', None)
    # objs 要根据船，航次号，大贝，中查询
    objs = Container_e_Info.objects.filter(voy_ex=voy_ex, vessel=vessel, bay=bay_id)
    # 调用数据处理方法
    bay = Bay_position.objects.get(id=bay_id).bay.split(',')
    # 判断 箱位前2位数 是否在选择的大贝中
    if space[:2] in bay:
        if data_processing(objs, space, bay):
            try:
                container_e_Info = Container_e_Info()
                container_e_Info.iso_no = iso_no
                container_e_Info.voy_ex_id = voy_ex
                container_e_Info.vessel_id = vessel
                container_e_Info.space = space
                container_e_Info.size = size
                container_e_Info.weight = weight
                container_e_Info.type = type_yn
                container_e_Info.bay_id = bay_id
                container_e_Info.save()
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
            data = {
                'code': -2,
                'msg': '该船当前航次进口的箱位已录入，请重新填写！'
            }
            return JsonResponse(data)
    else:
        data = {
            'code': -3,
            'msg': '箱位号前两位必须在选择的贝位列表中！'
        }
        return JsonResponse(data)


# def voy_ex_input(request):
#     """
#     添加出口航次信息
#     :param request:
#     :return:
#     """
#     voy_ex = request.POST.get('voy_ex', None)
#     ETB = request.POST.get('ETB', None)
#     ETD = request.POST.get('ETD', None)
#     ATB = request.POST.get('ATB', None)
#     ATD = request.POST.get('ATD', None)
#     vessel = request.POST.get('vessel', None)
#     if Voy_ex.objects.filter(vessel_id=vessel, voy_ex=voy_ex).exists():
#         data = {
#             'code': -1,
#             'msg': '该船以存在当前航次信息！'
#         }
#         return JsonResponse(data)
#     else:
#         try:
#             voy_ex_info = Voy_ex()
#             voy_ex_info.voy_ex = voy_ex
#             voy_ex_info.ETB = ETB
#             voy_ex_info.ETD = ETD
#             voy_ex_info.ATB = ATB
#             voy_ex_info.ATD = ATD
#             voy_ex_info.vessel_id = vessel
#             voy_ex_info.save()
#         except Exception as err:
#             print(err)
#             data = {
#                 'code': -1,
#                 'msg': '保存出口航次失败！'
#             }
#             return JsonResponse(data)
#         data = {
#             'code': 0,
#             'msg': '保存出口航次成功！'
#         }
#         return JsonResponse(data)


def voy_input(request):
    """
    添加进口航次信息
    :param request:
    :return:
    """
    print(request.POST)
    voy_im = request.POST.get('voy_im', None)
    voy_ex = request.POST.get('voy_ex', None)
    ETB = request.POST.get('b_time_plan', None)
    ETD = request.POST.get('d_time_plan', None)
    vessel = request.POST.get('vessel', None)
    if Voyage.objects.filter(vessel_id=vessel, voy_im=voy_im).exists():
        data = {
            'code': 1,
            'msg': '进口航次已存在！'
        }
        return JsonResponse(data)
    elif Voyage.objects.filter(vessel_id=vessel, voy_ex=voy_ex).exists():
        data = {
            'code': 1,
            'msg': '出口航次已存在！'
        }
        return JsonResponse(data)
    else:
        try:
            voy = Voyage()
            voy.vessel_id = vessel
            voy.voy_im = voy_im
            voy.voy_ex = voy_ex
            voy.ETB = ETB
            voy.ETD = ETD
            voy.save()
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
