from django.db import models

from equipment.models import *
from information.models import *
from plan.models import *


# Create your models here.


# 卸船作业表
class Job_unloading(models.Model):
    job_id = models.AutoField(primary_key=True, verbose_name="卸船作业编号")
    plan = models.OneToOneField('plan.Plan_unloading', verbose_name="卸船计划编号", on_delete=models.DO_NOTHING,
                                related_name="plan_job_u")
    voy = models.ForeignKey('information.Voyage', on_delete=models.CASCADE)
    qc = models.ForeignKey('equipment.Quay_crane', on_delete=models.CASCADE)
    agv = models.ForeignKey(to='equipment.AGV', on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="作业开始时间", null=True, blank=True)
    middle_time_p = models.DateTimeField(verbose_name="计划至中转平台时间", null=True, blank=True)
    middle_time_a = models.DateTimeField(verbose_name="实际至中转平台时间", null=True, blank=True)
    start_time_after = models.DateTimeField(verbose_name="后吊具作业开始时间", null=True, blank=True)
    end_time_qc_p = models.DateTimeField(verbose_name="岸桥作业计划结束时间", null=True, blank=True)
    end_time_qc = models.DateTimeField(verbose_name="岸桥作业结束时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="卸船作业结束时间", null=True, blank=True)


# 装船作业表
class Job_loading(models.Model):
    job_id = models.AutoField(primary_key=True, verbose_name="卸船作业编号")
    plan = models.OneToOneField('plan.Plan_unloading', verbose_name="卸船计划编号", on_delete=models.DO_NOTHING,
                                related_name="plan_job_l")
    voy = models.ForeignKey('information.Voyage', on_delete=models.CASCADE)
    qc = models.ForeignKey('equipment.Quay_crane', on_delete=models.CASCADE)
    agv = models.ForeignKey(to='equipment.AGV', on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="作业开始时间", null=True, blank=True)
    start_time_after = models.DateTimeField(verbose_name="后吊具作业开始时间", null=True, blank=True)
    middle_time_p = models.DateTimeField(verbose_name="计划至中转平台时间", null=True, blank=True)
    middle_time_a = models.DateTimeField(verbose_name="实际至中转平台时间", null=True, blank=True)
    end_time_qc_p = models.DateTimeField(verbose_name="岸桥作业计划结束时间", null=True, blank=True)
    end_time_qc = models.DateTimeField(verbose_name="岸桥作业结束时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="装船作业结束时间", null=True, blank=True)
