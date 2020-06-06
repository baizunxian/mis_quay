"""mis_quay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from information.views import info_views, info_view_del, info_view_search, info_view_insert, info_view_edit
from equipment.views import eq_views
from plan.views import plan_views
from job.views import views_job

urlpatterns = [
    # ------------------------- info ------------------------
    path('admin/', admin.site.urls),
    path('login/', info_views.login),
    path('logout/', info_views.logout),
    path('index/', info_views.index),

    # 获取航次信息 get
    path('get_voy_info/', info_views.get_voy_info),
    path('get_voy_ex_info/', info_views.get_voy_ex_info),

    # 编辑 edit
    path('vessel_edit/', info_view_edit.vessel_edit),
    path('container_e_edit/', info_view_edit.container_e),
    path('container_i_edit/', info_view_edit.container_i),

    # 删除船信息 del
    path('delete_vessel/', info_view_del.delete_vessel),
    path('delete_container/', info_view_del.delete_container),
    path('delete_voy/', info_view_del.delete_voy),

    # 查询船信息 search
    path('search_vessel/', info_view_search.search_vessel),
    path('search_container/', info_view_search.search_container),

    # 添加进口箱信息, 添加出口箱信息 insert
    path('container_input/', info_view_insert.container_input),
    path('container_e_Info_input/', info_view_insert.container_e_Info_input),
    path('vesselInfo_input/', info_view_insert.vesselInfo_input),
    path('voy_input/', info_view_insert.voy_input),
    # path('voy_ex_input/', info_view_insert.voy_ex_input),

    # 页面返回
    path('informationinput/', info_views.informationinput),
    path('container_add/', info_views.container_add),
    path('vessel_add/', info_views.vessel_add),
    path('voy/', info_views.voy),
    path('voy_maintain/', info_views.voy_maintain),

    path('vesselinfo_maintain/', info_views.vesselinfo_maintain),
    path('container_maintain/', info_views.container_maintain),
    path('container_e_maintain/', info_views.container_e_info_maintain),

    # ------------------------- eq ------------------------
    path('qc_equipment/', eq_views.qc_equipment),
    path('agv_equipment/', eq_views.agv_equipment),
    path('qc_plan/', eq_views.qc_plan),
    path('get_by_bay_id/', eq_views.get_by_bay_id),
    # path('qc_info/', eq_views.qc_info),

    # add
    path('qc_add/', eq_views.qc_add),
    path('agv_add/', eq_views.agv_add),

    # edit
    path('qc_edit/', eq_views.qc_edit),
    path('agv_edit/', eq_views.agv_edit),

    # delete
    path('qc_delete/', eq_views.qc_delete),
    path('agv_delete/', eq_views.agv_delete),

    # ------------------------- plan ------------------------
    # 页面返回
    path('vessel_plan/', plan_views.vessel_plan),
    # path('vessel_chart/', plan_views.vessel_chart),

    # 卸船计划
    path('unloading_plan_manage/', plan_views.unloading_plan_manage),
    path('unloading_planning_page/', plan_views.unloading_planning_page),
    path('handling_planning/', plan_views.handling_planning),
    # 装船计划
    path('loading_plan_manage/', plan_views.loading_plan_manage),
    path('loading_planning_page/', plan_views.loading_planning_page),
    path('loading_planning/', plan_views.loading_planning),

    # delete
    path('delete_plan/', plan_views.delete_plan),

    # 查询
    # path('delete_plan/', plan_views.delete_plan),

    # ------------------------- job ------------------------
    # 查询
    path('search_by_en_name/', views_job.search_by_en_name),

    # 页面
    path('vessel_job/', views_job.vessel_job),

    # 装卸操作
    path('grab_box/', views_job.grab_box),
    path('transfer/', views_job.transfer),
    path('discharge_box/', views_job.discharge_box),
    path('agv_discharge_box/', views_job.agv_discharge_box),

    # 装船操作
    path('start_job/', views_job.start_job),
    path('qc_job/', views_job.qc_job),
    path('transfer_load/', views_job.transfer_load),

    path('loading_control/', views_job.loading_control),
    path('unloading_control/', views_job.unloading_control),
    path('distribution_qc/', views_job.distribution_qc),

    path('leave_and_stop/', views_job.leave_and_stop),
    # path('loading_plan_manage/', views_job.loading_plan_manage),
    # path('loading_plan/', views_job.loading_plan),
    path('unloading_record/', views_job.unloading_record),
    path('unloading_job/', views_job.unloading_job)
]
