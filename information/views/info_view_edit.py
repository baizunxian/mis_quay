from django.shortcuts import render
from django.http import JsonResponse

from information.models import VesselInfo


def vessel_edit(request):
    if request.method == 'POST':
        print(request.POST)
        v_id = request.POST.get('v_id')
        en_name = request.POST.get('en_name')
        cn_name = request.POST.get('cn_name')
        vessel_info = VesselInfo.objects.get(id=v_id)
        vessel_info.en_name = en_name
        vessel_info.cn_name = cn_name
        vessel_info.save()
        data = {
            'code': 0,
            'msg': '修改成功！'
        }
        return JsonResponse(data)
    else:
        v_id = request.GET.get('v_id')
        vessel_info = VesselInfo.objects.get(id=v_id)
        return render(request, 'info/vessel_edit.html', {'vessel_info': vessel_info})


def container_e(request):
    pass


def container_i(request):
    pass
