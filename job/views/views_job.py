from django.http import JsonResponse
# Create your views here.


from django.shortcuts import render
from information.models import Voyage, Container
from plan.models import Plan_unloading
from datetime import datetime
from equipment.models import Quay_crane, AGV


# Create your views here.


# def vessel_job(request):
#     voy_list = Voyage.objects.all()
#     return render(request, 'job/vessel_job.html', {'voy_list': voy_list})
from utils.common import get_current_time


# def unloading_control(request):
#     """
#     卸船作业控制
#     :param request:
#     :return:
#     """
#     plan_un_info = Plan_unloading.objects.all()
#     print(plan_un_info)
#     data = {
#         'plan_un_info': plan_un_info
#     }
#     return render(request, 'job/unloading_control.html', data)


# def loading_control(request):
#     """
#     装船作业控制
#     :param request:
#     :return:
#     """
#     plan_un_info = Plan_unloading.objects.all()
#     print(plan_un_info)
#     data = {
#         'plan_un_info': plan_un_info
#     }
#     return render(request, 'job/loading_control.html', data)


def unloading_record(request):
    return render(request, 'job/unloading_record.html')


def unloading_job(request):
    return render(request, 'job/unloading_job.html')


def vessel_job(request):
    """
    船泊管理
    :param request:
    :return:
    """
    voy_list = Voyage.objects.all()
    return render(request, 'job/vessel_job.html', {'voy_list': voy_list})


def search_by_en_name(request):
    print(request.POST)
    en_name = request.POST.get('en_name')
    voy_info = Voyage.objects.filter(vessel__en_name__contains=en_name)
    voy_list = list()
    if voy_info:
        for voy in voy_info:
            voy_dick = dict()
            voy_dick['id'] = voy.id
            voy_dick['vessel_cn'] = voy.vessel.cn_name
            voy_dick['vessel_en'] = voy.vessel.en_name
            voy_dick['voy_im'] = voy.voy_im
            voy_dick['voy_ex'] = voy.voy_ex
            voy_dick['voy_im_state'] = voy.voy_im_state
            voy_dick['voy_ex_state'] = voy.voy_ex_state
            voy_dick['ETB'] = voy.ETB
            voy_dick['ETD'] = voy.ETD
            voy_dick['ATB'] = voy.ATB
            voy_dick['ATD'] = voy.ATD
            voy_list.append(voy_dick)
        data = {
            'code': 0,
            'voy_list': voy_list
        }
        return JsonResponse(data)
    data = {
        'code': 0,
        'voy_list': []
    }
    return JsonResponse(data)


def unloading_control(request):
    """
    卸船作业控制
    :param request:
    :return:
    """
    voy_id = request.GET.get('v_id')
    plan_un_info = Plan_unloading.objects.filter(voy_id=voy_id, handling_type=0)
    data = {
        'plan_un_info': plan_un_info
    }
    return render(request, 'job/unloading_control.html', data)


def loading_control(request):
    """
    裝船作业控制
    :param request:
    :return:
    """
    print(request.GET)
    voy_id = request.GET.get('v_id')
    plan_un_info = Plan_unloading.objects.filter(voy_id=voy_id, handling_type=1)
    data = {
        'plan_un_info': plan_un_info
    }
    return render(request, 'job/loading_control.html', data)


# def unloading_record(request):
#     return render(request, 'job/unloading_record.html')
#
#
# def unloading_job(request):
#     return render(request, 'job/unloading_job.html')


# def loading_plan(request):
#     return render(request, 'job/loading_plan.html')
#
#
# def loading_plan_manage(request):
#     return render(request, 'job/loading_plan_manage.html')
#
#
# def unloading_plan(request):
#     return render(request, 'job/unloading_plan.html')


# def unloading_plan_manage(request):
#     return render(request, 'job/unloading_plan_manage.html')


def leave_and_stop(request):
    """
    靠港，离岗
    :param request:
    :return:
    """
    print(request.POST)
    v_id = request.POST.get('v_id')
    type = request.POST.get('type')
    voyage_info = Voyage.objects.get(id=v_id)
    if type == 'leave':
        if voyage_info.ATD:
            data = {
                'code': -1,
                'msg': '当前航次已经离港！'
            }
            return JsonResponse(data)
        else:
            voyage_info.ATD = datetime.now()
            voyage_info.voy_ex_state = 1
            voyage_info.save()
            data = {
                'code': 0,
                'msg': '离港成功！'
            }
            return JsonResponse(data)
    else:
        if voyage_info.ATB:
            data = {
                'code': -1,
                'msg': '当前航次已经靠港！'
            }
            return JsonResponse(data)
        else:
            voyage_info.ATB = datetime.now()
            voyage_info.voy_im_state = 1
            voyage_info.save()
            data = {
                'code': 0,
                'msg': '靠港成功！'
            }
            return JsonResponse(data)


def distribution_qc(request):
    """
    分配岸桥
    :param request:
    :return:
    """
    print(request.POST)
    qc1_id = request.POST.get('qc1', None)
    qc1_start = request.POST.get('qc1_start')
    qc1_end = request.POST.get('qc1_end')
    qc2_id = request.POST.get('qc2', None)
    qc2_start = request.POST.get('qc2_start')
    qc2_end = request.POST.get('qc2_end')
    v_id = request.POST.get('v_id')
    voy = request.POST.get('voy')
    container_info = Container.objects.filter(vessel__id=v_id, voy__id=voy, qc_id=None)
    print(container_info)
    if container_info:
        for container in container_info:
            print(container)
            if container.qc_id == None:
                if qc1_id and qc2_id:
                    if int(qc1_start) <= container.bay_id <= int(qc1_end):
                        container.qc_id = qc1_id
                        container.save()
                    elif int(qc2_start) <= container.bay_id <= int(qc2_end):
                        container.qc_id = qc2_id
                        container.save()
                elif qc1_id and not qc2_id:
                    if int(qc1_start) <= container.bay_id <= int(qc1_end):
                        container.qc_id = qc1_id
                        container.save()
                elif qc2_id and not qc1_id:
                    if int(qc2_start) <= container.bay_id <= int(qc2_end):
                        container.qc_id = qc2_id
                        container.save()
        data = {
            'code': 0,
            'msg': '分配成功！'
        }
        return JsonResponse(data)
    else:
        data = {
            'code': -1,
            'msg': '当前批次的货箱都以分配岸桥！'
        }
        return JsonResponse(data)


def grab_box(request):
    """
    卸船抓箱操作
    :param request:
    :return:
    """
    print(request.POST)
    box = request.POST.get('box')
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    data_time = datetime.now().strftime('%Y%m%d')
    job_id = data_time+str(plan_id)
    print(job_id)
    # 获取岸桥信息
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    # 获取卸船计划信息
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    # 卸船计划编号对应的箱数量
    container_count = Container.objects.filter(plan_id=plan_id).count()
    if box == '1':
        if plan_un_info.state_time:
            data = {
                'code': -1,
                'msg': '当前环节以操作完成！',
            }
            return JsonResponse(data)
        else:
            if qc_info.sea_state == 2:
                try:
                    plan_un_info.job_id = job_id
                    plan_un_info.state_time = get_current_time()
                    plan_un_info.save()
                    qc_info.sea_state = 1
                    qc_info.save()
                except Exception as err:
                    data = {
                        'code': -1,
                        'msg': '操作失败！',
                    }
                    return JsonResponse(data)
                data = {
                    'code': 0,
                    'msg': '操作成功！',
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '海侧吊具运行中,请稍后重试！',
                }
                return JsonResponse(data)
    elif box == '2':
        if plan_un_info.state_time_land:
            data = {
                'code': -1,
                'msg': '当前环节以操作完成！',
            }
            return JsonResponse(data)
        else:
            if qc_info.land_state == 2:
                if plan_un_info.middle_time:
                    qc_info.land_state = 1
                    qc_info.middle_space += container_count
                    qc_info.save()
                    plan_un_info.state_time_land = get_current_time()
                    plan_un_info.save()
                    data = {
                        'code': 0,
                        'msg': '操作成功！',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'code': -1,
                        'msg': '上一工作环境未完成！',
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '陆侧吊具运行中,请稍后重试！',
                }
                return JsonResponse(data)


def transfer(request):
    """
    卸船中转操作
    :param request:
    :return:
    """
    print(request.POST)
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)

    # middle_space 中转空间
    middle_space = qc_info.middle_space
    container_count = Container.objects.filter(plan_id=plan_id).count()
    if plan_un_info.middle_time:
        data = {
            'code': -1,
            'msg': '当前环节以操作完成！',
        }
        return JsonResponse(data)
    elif not plan_un_info.state_time:
        data = {
            'code': -1,
            'msg': '上一工作环境未完成！',
        }
        return JsonResponse(data)
    else:
        if plan_un_info.state_time:
            if container_count <= int(middle_space):
                qc_info.sea_state = 2
                qc_info.middle_space = int(middle_space) - container_count
                qc_info.save()
                plan_un_info.middle_time = get_current_time()
                plan_un_info.save()
                data = {
                    'code': 0,
                    'msg': '操作成功！',
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '中转平台空位不足！',
                }
                return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '上一工作环境未完成！',
            }
            return JsonResponse(data)


def discharge_box(request):
    """
    卸船岸桥放箱
    :param request:
    :return:
    """
    print(request.POST)
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    container_info = Container.objects.filter(plan_id=plan_id)
    # agv
    agv_free = AGV.objects.filter(situation=1, state=2)

    if plan_un_info.end_time_qc:
        data = {
            'code': -1,
            'msg': '当前环节以操作完成！',
        }
        return JsonResponse(data)
    elif not plan_un_info.state_time_land:
        data = {
            'code': -1,
            'msg': '上一工作环境未完成！',
        }
        return JsonResponse(data)
    else:
        if agv_free:
            # 获取空闲，且状态良好的agv 第一个
            agv_info = agv_free[0]
            plan_un_info.agv_id = agv_info.agv_id
            plan_un_info.end_time_qc = get_current_time()
            plan_un_info.save()
            for container in container_info:
                container.agv_id = agv_info.agv_id
                container.save()
            data = {
                'code': 0,
                'msg': '操作成功！',
            }
            agv_info.state = 1
            agv_info.save()
            qc_info.land_state = 2
            qc_info.save()
            return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '目前没有空闲的AGV！',
            }
            return JsonResponse(data)


def agv_discharge_box(request):
    """
    卸船agv放箱
    :param request:
    :return:
    """
    print(request.POST)
    plan_id = request.POST.get('plan_id')
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    container_info = Container.objects.filter(plan_id=plan_id)
    # agv
    agv_info = AGV.objects.get(agv_id=plan_un_info.agv_id)
    if plan_un_info.end_time:
        data = {
            'code': -1,
            'msg': '当前环节以操作完成！',
        }
        return JsonResponse(data)
    elif not plan_un_info.end_time_qc:
        data = {
            'code': -1,
            'msg': '上一工作环境未完成！',
        }
        return JsonResponse(data)
    else:
        # 记录结束时间
        plan_un_info.end_time = get_current_time()
        plan_un_info.save()
        # 更改箱状态
        for container in container_info:
            container.state = 1
            container.save()
        data = {
            'code': 0,
            'msg': '操作成功,当前货箱卸船完成！',
        }
        # 更改vag状态
        agv_info.state = 2
        agv_info.save()
        # 箱状态列
        container_info_list = Container.objects.filter(plan_id=plan_id)
        container_state_list = list()
        for container in container_info_list:
            container_state_list.append(container.state)
        container_state = list(set(container_state_list))
        if len(container_state) > 1:
            pass
        else:
            if container_state[0] == 1:
                plan_un_info.state = 3
                plan_un_info.save()
        return JsonResponse(data)


def start_job(request):
    """
    装船开始作业
    :param request:
    :return:
    """
    print(request.POST)
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    container_info = Container.objects.filter(plan_id=plan_id)
    data_time = datetime.now().strftime('%Y%m%d')
    job_id = data_time + str(plan_id)
    print(job_id)
    # agv
    agv_free = AGV.objects.filter(situation=1, state=2)

    if plan_un_info.state_time:
        data = {
            'code': -1,
            'msg': '当前环节以操作完成！',
        }
        return JsonResponse(data)
    else:
        if agv_free:
            # 获取空闲，且状态良好的agv 第一个
            agv_info = agv_free[0]
            plan_un_info.job_id = job_id
            plan_un_info.agv_id = agv_info.agv_id
            plan_un_info.state_time = get_current_time()
            plan_un_info.save()
            for container in container_info:
                container.agv_id = agv_info.agv_id
                container.save()
            data = {
                'code': 0,
                'msg': '操作成功！',
            }
            agv_info.state = 1
            agv_info.save()
            qc_info.land_state = 2
            qc_info.save()
            return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '目前没有空闲的AGV！',
            }
            return JsonResponse(data)


def qc_job(request):
    """
    装船岸桥作业
    :param request:
    :return:
    """
    print(request.POST)
    box = request.POST.get('box')
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    # 获取岸桥信息
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    # 获取卸船计划信息
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    # 卸船计划编号对应的箱数量
    container_count = Container.objects.filter(plan_id=plan_id).count()
    if box == '1':
        if plan_un_info.start_time_qc:
            data = {
                'code': -1,
                'msg': '当前环节以操作完成！',
            }
            return JsonResponse(data)
        else:
            if qc_info.land_state == 2:
                try:
                    plan_un_info.state_time_land = get_current_time()
                    plan_un_info.save()
                    qc_info.land_state = 1
                    qc_info.save()
                except Exception as err:
                    data = {
                        'code': -1,
                        'msg': '操作失败！',
                    }
                    return JsonResponse(data)
                data = {
                    'code': 0,
                    'msg': '操作成功！',
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '海侧吊具运行中,请稍后重试！',
                }
                return JsonResponse(data)
    elif box == '2':
        if plan_un_info.start_time_sea:
            data = {
                'code': -1,
                'msg': '当前环节以操作完成！',
            }
            return JsonResponse(data)
        else:
            if qc_info.sea_state == 2:
                if plan_un_info.middle_time:
                    qc_info.sea_state = 1
                    qc_info.middle_space += container_count
                    qc_info.save()
                    plan_un_info.start_time_sea = get_current_time()
                    plan_un_info.save()
                    data = {
                        'code': 0,
                        'msg': '操作成功！',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'code': -1,
                        'msg': '上一工作环境未完成！',
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '陆侧吊具运行中,请稍后重试！',
                }
                return JsonResponse(data)


def transfer_load(request):
    """
    装船中转操作
    :param request:
    :return:
    """
    print(request.POST)
    plan_id = request.POST.get('plan_id')
    qc_id = request.POST.get('qc_id')
    qc_info = Quay_crane.objects.get(qc_id=qc_id)
    plan_un_info = Plan_unloading.objects.get(plan_id=plan_id)
    # middle_space 中转空间
    middle_space = qc_info.middle_space
    container_count = Container.objects.filter(plan_id=plan_id).count()
    if plan_un_info.middle_time:
        data = {
            'code': -1,
            'msg': '当前环节以操作完成！',
        }
        return JsonResponse(data)
    elif not plan_un_info.state_time_land:
        data = {
            'code': -1,
            'msg': '上一工作环境未完成！',
        }
        return JsonResponse(data)
    else:
        if plan_un_info.state_time:
            if container_count <= int(middle_space):
                qc_info.land_state = 2
                qc_info.middle_space = int(middle_space) - container_count
                qc_info.save()
                plan_un_info.middle_time = get_current_time()
                plan_un_info.save()
                data = {
                    'code': 0,
                    'msg': '操作成功！',
                }
                return JsonResponse(data)
            else:
                data = {
                    'code': -1,
                    'msg': '中转平台空位不足！',
                }
                return JsonResponse(data)
        else:
            data = {
                'code': -1,
                'msg': '上一工作环境未完成！',
            }
            return JsonResponse(data)


