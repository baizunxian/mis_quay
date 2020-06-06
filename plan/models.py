from django.db import models

# Create your models here.

from information.models import *
from equipment.models import *
from job.models import *


class Bay_position(models.Model):
    bay = models.CharField(max_length=11, verbose_name="贝位号")


# 卸船计划表
class Plan_unloading(models.Model):
    state_choices = (
        (1, "计划"),
        (2, "执行"),
        (3, "完成"))
    plan_id = models.BigIntegerField(primary_key=True, verbose_name="卸箱计划编号")
    vessel = models.ForeignKey("information.VesselInfo", verbose_name="英文船名", on_delete=models.CASCADE,
                               related_name="plan_u_vessel")
    voy = models.ForeignKey("information.Voyage", verbose_name="进口航次", on_delete=models.CASCADE,
                            related_name="plan_u_voy")
    qc = models.ForeignKey("equipment.Quay_crane", verbose_name="岸桥信息", on_delete=models.CASCADE,
                           related_name="plan_u_qc")
    state = models.SmallIntegerField(verbose_name="计划完成情况", choices=state_choices)
    job_id = models.CharField(max_length=255, verbose_name="装/卸船作业编号", null=True, blank=True)
    state_time = models.DateTimeField(verbose_name="装/卸船作业开始时间", null=True, blank=True)
    middle_time = models.DateTimeField(verbose_name="至中转平台时间", null=True, blank=True)
    state_time_land = models.DateTimeField(verbose_name="陆测吊作业开始时间", null=True, blank=True)
    end_time_qc = models.DateTimeField(verbose_name="岸桥作业结束时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="装/卸船结束时间", null=True, blank=True)
    start_time_qc = models.DateTimeField(verbose_name="装船岸桥作业开始时间", null=True, blank=True)
    start_time_sea = models.DateTimeField(verbose_name="装船海侧吊具作业开始时间", null=True, blank=True)
    handling_type = models.IntegerField(verbose_name='装/卸船类型')  # 0 卸船  1 装船
    agv = models.ForeignKey('equipment.AGV', on_delete=models.DO_NOTHING, null=True, blank=True)


# 装船计划表
# class Plan_loading(models.Model):
#     state_choices = (
#         (1, "计划"),
#         (2, "执行"),
#         (3, "完成"))
#     plan_id = models.AutoField(primary_key=True, verbose_name="卸船计划号")
#     vessel = models.ForeignKey("information.VesselInfo", verbose_name="英文船名", on_delete=models.CASCADE,
#                                related_name="plan_l_vessel", null=True)
#     voy = models.ForeignKey("information.Voyage", verbose_name="出口航次", on_delete=models.CASCADE, related_name="plan_l_voy" , null=True)
#     qc = models.ForeignKey("equipment.Quay_crane", verbose_name="岸桥信息", on_delete=models.CASCADE, related_name="plan_l_qc", null=True)
#     state = models.SmallIntegerField(verbose_name="计划完成情况", choices=state_choices, default=1)
