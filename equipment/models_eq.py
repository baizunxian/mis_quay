from django.db import models

from plan.models import *
from information.models import *
from job.models import *


# Create your models here.

# 岸桥信息表
class Quay_crane(models.Model):
    situation_choices = (
        (1, "良好"),
        (2, "待修"))
    sea_state_choices = (
        (1, "作业"),
        (2, "空闲"))
    land_state_choices = (
        (1, "作业"),
        (2, "空闲"))

    qc_id = models.IntegerField(verbose_name="岸桥编号", primary_key=True)
    sea_state = models.IntegerField(verbose_name="海侧吊具运行状态", choices=sea_state_choices)
    land_state = models.IntegerField(verbose_name="陆测吊具运行状态", choices=land_state_choices)
    situation = models.IntegerField(verbose_name="设备情况", choices=situation_choices)
    middle_space = models.IntegerField(verbose_name="中转平台空位")
    weight_max = models.CharField(max_length=10, verbose_name="吊具承重量")
    voy = models.ManyToManyField(to="information.Voyage", through="voyage_qc")


# 岸桥_航次表
class voyage_qc(models.Model):
    start_plan = models.DateTimeField(verbose_name="开始占用时间")
    end_plan = models.DateTimeField(verbose_name="结束占用时间")


# AGV表
class AGV(models.Model):
    situation_choices = (
        (1, "良好"),
        (2, "待修"))
    state_choices = (
        (1, "作业"),
        (2, "空闲"))
    agv_id = models.AutoField(primary_key=True, verbose_name="AGV编号")
    situation = models.IntegerField(verbose_name="设备情况", choices=situation_choices)
    state = models.IntegerField(verbose_name="运行状态", choices=state_choices)
