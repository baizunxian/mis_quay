from django.db import models

from equipment.models_eq import *
from information.models_info import *
from plan.models_plan import *


# Create your models here.

# 卸船作业表
class Job_unloading(models.Model):
    job_id = models.CharField(verbose_name="卸船作业编号", null=True, blank=True)
    plan = models.OneToOneField('Plan_unloading', verbose_name="卸船计划编号", on_delete=models.DO_NOTHING,
                                related_name="plan_job_u")
    voy_im = models.ForeignKey('Voyage', on_delete=models.DO_NOTHING, related_name="job_unloading_voy")
    qc = models.ForeignKey('Quay_crane', on_delete=models.DO_NOTHING, related_name="job_unloading_qc")
    agv = models.ForeignKey(to='AGV', on_delete=models.DO_NOTHING, related_name="job_unloading_agv")
    start_time = models.DateTimeField(verbose_name="作业开始时间", null=True, blank=True)
    middle_time = models.DateTimeField(verbose_name="至中转平台时间", null=True, blank=True)
    start_time_land = models.DateTimeField(verbose_name="陆侧吊具作业开始时间", null=True, blank=True)
    end_time_qc = models.DateTimeField(verbose_name="岸桥作业结束时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="卸船作业结束时间", null=True, blank=True)


# 装船作业表
class Job_loading(models.Model):
    job_id = models.CharField(verbose_name="卸船作业编号", null=True, blank=True)
    plan = models.OneToOneField('Plan_unloading', verbose_name="卸船计划编号", on_delete=models.DO_NOTHING,
                                related_name="plan_job_l")
    voy_ex = models.ForeignKey('Voyage', on_delete=models.DO_NOTHING, related_name="job_loading_voy")
    qc = models.ForeignKey('Quay_crane', on_delete=models.DO_NOTHING, related_name="job_loading_qc")
    agv = models.ForeignKey(to='AGV', on_delete=models.DO_NOTHING, related_name="job_loading_agv")
    start_time = models.DateTimeField(verbose_name="作业开始时间", null=True, blank=True)
    start_time_after = models.DateTimeField(verbose_name="岸桥作业开始时间", null=True, blank=True)
    middle_time = models.DateTimeField(verbose_name="至中转平台时间", null=True, blank=True)
    start_time_sea = models.DateTimeField(verbose_name="海侧吊具作业开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="装船作业结束时间", null=True, blank=True)
