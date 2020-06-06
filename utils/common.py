from datetime import datetime

from information.models import Container
from plan.models import Plan_unloading
from equipment.models import Quay_crane


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def data_processing(objs, number, bay):
    """
    objs: 查询出来的queryset集合， number： 要比对的前2位数  bay: 贝位列表
    :param objs:
    :param number:
    :return:
    """
    # 创建一个前两位数的列表
    space_top2_list = list()
    # 后四位列表
    space_after4_list = list()
    # 后四位相同列表
    space_number_4 = list()
    # 前2位相同后四位的列表
    space_number_2 = list()
    if objs:
        # 循环出所以符合条件的 已有的前2位数
        for obj in objs:
            space_top2_list.append(obj.space[:2])
            space_after4_list.append(obj.space[-4:])
            if obj.space[-4:] == number[-4:]:
                space_number_2.append(obj.space[:2])
                space_number_4.append(obj.space[-4:])

        # 如果数据有前两位一样的数据存在
        if number[-4:] in space_number_4:
            if bay[1] in space_number_2:
                return False
            elif bay[0] in space_number_2:
                if number[:2] == bay[2]:
                    return True
                else:
                    return False
            elif bay[2] in space_number_2:
                if number[:2] == bay[1]:
                    return True
                else:
                    return False
        else:
            return True
    else:
        return True


def Handling_check(ck_list, handling_type):
    """
    卸船校验
    :param ck_list:
    :return:
    """
    print(ck_list)
    ck_len = len(ck_list)
    if ck_len > 2 or ck_list == []:
        data = {
            'code': -1,
            'msg': '箱子最多选择2个，最少选择1个！'
        }
        return data
    else:
        container_list = Container.objects.filter(id__in=ck_list, type=handling_type)
        space_dict = dict()  # 组装成字典 比对时候用 {'030484': {'space': '030484', 'bay': 1}, '010484': {'space': '010484', 'bay': 1}}
        space_list = list()  # space 列表  箱位
        for container in container_list:
            if container.plan_id:
                data = {
                    'code': -1,
                    'msg': '当前货箱已生成计划！'
                }
                return data
            else:
                space_d = dict()
                space_d['space'] = container.space
                space_d['bay'] = container.bay_id
                space_d['qc_id'] = container.qc_id
                space_d['vessel_id'] = container.vessel_id
                space_d['voy_id'] = container.voy_id
                space_list.append(container.space)
                space_dict[container.space] = space_d

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        qc_id = space_dict[space_list[0]]['qc_id']  # 岸桥编号
        vessel_id = space_dict[space_list[0]]['vessel_id']  # 船id
        voy_id = space_dict[space_list[0]]['voy_id']  # 航次id
        plan_id = str(date) + str(qc_id)  # 生成计划号

        # 获取吊具信息
        qc_info = Quay_crane.objects.get(qc_id=qc_id)
        # 选择的箱重之和
        weight_count = 0

        if ck_len == 2:

            sqace_1_4 = space_dict[space_list[0]]['space'][-4:]   # 箱位后四位
            sqace_2_4 = space_dict[space_list[1]]['space'][-4:]   # 箱位后四位
            sqace_1_bay = space_dict[space_list[0]]['bay']  # bay位
            sqace_2_bay = space_dict[space_list[1]]['bay']  # bay位

            if sqace_1_4 == sqace_2_4 and sqace_1_bay == sqace_2_bay:
                # 判断是否有特殊箱
                for container in container_list:
                    if container.special == True and ck_len > 1:
                        data = {
                            'code': -1,
                            'msg': '选择的箱子中有特殊箱，特殊箱一次之能选择一个！'
                        }
                        return data
                    weight_count +=int(container.weight)

                #  判断承重
                if weight_count > int(qc_info.weight_max):
                    data = {
                        'code': -1,
                        'msg': '当前选择的箱重大于吊具的最大承重！ 当前吊具最大承重为[%skg]'%qc_info.weight_max
                    }
                    return data
                else:
                    # 如果没有特殊性，重量符合的情况下 直接入库
                    try:
                        # 添加Plan_unloading 表信息
                        plan_un = Plan_unloading()
                        plan_un.plan_id = plan_id
                        plan_un.vessel_id = vessel_id
                        plan_un.voy_id = voy_id
                        plan_un.qc_id = qc_id
                        plan_un.state = 1
                        plan_un.handling_type = handling_type
                        plan_un.save()
                        # 更新箱信息表，卸船计划号
                        for container in container_list:
                            container.plan_id = plan_un.plan_id
                            container.save()
                    except Exception as err:
                        print(err)
                        data = {
                            'code': 0,
                            'msg': '添加失败！%s' % err
                        }
                        return data
                    data = {
                        'code': 0,
                        'msg': '计划添加成功！'
                    }
                    return data
            else:
                data = {
                    'code': -1,
                    'msg': '当前双相非邻箱！'
                }
                return data
        elif ck_len == 1:
            for container in container_list:
                weight_count += int(container.weight)

            #  判断承重
            if weight_count > int(qc_info.weight_max):
                data = {
                    'code': -1,
                    'msg': '当前选择的箱重大于吊具的最大承重！ 当前吊具最大承重为[%skg]' % qc_info.weight_max
                }
                return data
            else:
                # 如果没有特殊性，重量符合的情况下 直接入库
                try:
                    # 添加Plan_unloading 表信息
                    plan_un = Plan_unloading()
                    plan_un.plan_id = plan_id
                    plan_un.vessel_id = vessel_id
                    plan_un.voy_id = voy_id
                    plan_un.qc_id = qc_id
                    plan_un.state = 1
                    plan_un.handling_type = handling_type
                    plan_un.save()
                    # 更新箱信息表，卸船计划号
                    for container in container_list:
                        container.plan_id = plan_un.plan_id
                        container.save()
                except Exception as err:
                    print(err)
                    data = {
                        'code': 0,
                        'msg': '添加失败！%s'%err
                    }
                    return data
                data = {
                    'code': 0,
                    'msg': '计划添加成功！'
                }
                return data


