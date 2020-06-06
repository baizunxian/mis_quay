from django.db import models

from plan.models import *
from job.models import *


class Base(models.Model):
    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


# 船舶信息表
class VesselInfo(Base):
    class Meta:
        verbose_name = '船舶信息表'
        db_table = 'info_vesselInfo'

    en_name = models.CharField(max_length=18, verbose_name="英文船名", unique=True)
    cn_name = models.CharField(max_length=18, verbose_name="中文船名")


# 进口航次信息表
class Voyage(Base):
    class Meta:
        verbose_name = '进出口航次表'
        db_table = 'info_voyage'

    vessel = models.ForeignKey(to="VesselInfo", on_delete=models.CASCADE, verbose_name="船信息")
    voy_im = models.CharField(max_length=10, verbose_name="进口航次编号")
    voy_ex = models.CharField(max_length=10, verbose_name="出口航次编号")
    voy_im_state = models.IntegerField(verbose_name="进口航次状态", default=0)  # 0 未靠港 1 靠港
    voy_ex_state = models.IntegerField(verbose_name="出口航次状态", default=0)  # 0 未出港 1 以出港
    ETB = models.DateTimeField(verbose_name="计划靠泊时间")
    ETD = models.DateTimeField(verbose_name="计划离泊时间")
    ATB = models.DateTimeField(blank=True, null=True, default=None, verbose_name="实际靠泊时间")
    ATD = models.DateTimeField(blank=True, null=True, default=None, verbose_name="实际离泊时间")
    unloading_im = models.BooleanField(verbose_name="是否卸货完成", default=False)
    unloading_ex = models.BooleanField(verbose_name="是否装货完成", default=False)
    current_state = models.IntegerField(verbose_name='航次当前状态', default=0)  # 0进口， 1 出口


# 进出口口箱信息表
class Container(Base):
    class Meta:
        verbose_name = '船舶信息表'
        db_table = 'info_Container'

    size_choices = (
        (1, "20ft"),
        (2, "40ft"))
    voy = models.ForeignKey('Voyage', on_delete=models.CASCADE, verbose_name='进口航次信息')
    vessel = models.ForeignKey('VesselInfo', on_delete=models.CASCADE, verbose_name='船信息')
    iso_no = models.CharField(max_length=11, verbose_name="箱号")
    space = models.CharField(max_length=6, verbose_name="箱位")
    size = models.SmallIntegerField(verbose_name="尺寸", choices=size_choices)
    weight = models.CharField(max_length=10, verbose_name="重量")
    special = models.BooleanField(verbose_name="是否特殊箱", default=False)
    type = models.IntegerField(verbose_name="进出口类型", null=False)  # 0 进口， 1出口
    state = models.IntegerField(verbose_name="装卸状态", null=False, default=0)  # 0 未装卸， 1装卸完成
    plan = models.ForeignKey("plan.Plan_unloading", verbose_name="卸箱计划编号", on_delete=models.SET_NULL, null=True)
    # job = models.ForeignKey('job.Job_unloading', verbose_name="卸箱作业编号", on_delete=models.SET_NULL, null=True)
    agv = models.ForeignKey('equipment.AGV', verbose_name="AGV", on_delete=models.SET_NULL, null=True)
    qc = models.ForeignKey('equipment.Quay_crane', verbose_name="卸箱岸桥", on_delete=models.SET_NULL, null=True)
    bay = models.ForeignKey('plan.Bay_position', verbose_name="贝位", on_delete=models.SET_NULL, null=True)


# 用户信息表
class UserInfo(Base):
    user_id = models.AutoField(max_length=6, primary_key=True, verbose_name="工号")
    name = models.CharField(max_length=20, verbose_name="姓名")
    code = models.CharField(max_length=20, verbose_name="密码")
