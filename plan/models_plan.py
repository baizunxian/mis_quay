from django.db import models

# Create your models here.

from information.models_info import *
from equipment.models_eq import *
from job.models_job import *


# 卸船计划表
class Plan_unloading(models.Model):
    state_choices = (
        (1, "计划"),
        (2, "执行"),
        (3, "完成"))
    plan_id = models.AutoField(primary_key=True, verbose_name="卸箱计划编号")
    vessel = models.ForeignKey("VesselInfo", verbose_name="英文船名", on_delete=models.CASCADE,
                               related_name="plan_u_vessel")
    voy = models.ForeignKey("Voyage", verbose_name="进口航次", on_delete=models.CASCADE, related_name="plan_u_voy")
    qc = models.ForeignKey("Quay_crane", verbose_name="岸桥信息", on_delete=models.CASCADE, related_name="plan_u_qc")
    state = models.SmallIntegerField(verbose_name="计划完成情况", choices=state_choices)


# 装船计划表
class Plan_loading(models.Model):
    state_choices = (
        (1, "计划"),
        (2, "执行"),
        (3, "完成"))
    plan_id = models.AutoField(primary_key=True, verbose_name="卸船计划号")
    vessel = models.ForeignKey("VesselInfo", verbose_name="英文船名", on_delete=models.CASCADE,
                               related_name="plan_l_vessel")
    voy = models.ForeignKey("Voyage", verbose_name="出口航次", on_delete=models.CASCADE, related_name="plan_l_voy")
    qc = models.ForeignKey("Quay_crane", verbose_name="岸桥信息", on_delete=models.CASCADE, related_name="plan_l_qc")
    state = models.SmallIntegerField(verbose_name="计划完成情况", choices=state_choices)
