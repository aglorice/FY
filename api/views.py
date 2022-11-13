from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from FY import FY
from api.models import Fy


def getareadata(request):
    areas = []
    areas_count = []

    data_2 = []
    sells = []
    sell = Fy.objects.values('issell')
    for i in sell:
        sells.append(i['issell'])
    sells = list(set(sells))
    if "地块" in sells:
        sells.remove("地块")
    for i in sells:
        sell = {
            'value': Fy.objects.filter(issell=i).count(),
            'name': i
        }
        data_2.append(sell)

    area = Fy.objects.values('area')
    for i in area:
        areas.append(i['area'])

    areas = list(set(areas))
    for i in areas:
        areas_count.append(Fy.objects.filter(area=i).count())

    data = {
        'areas': areas,
        'areasnumber': areas_count,
        'sell': data_2

    }
    return JsonResponse(data, safe=False)


def getall(request):
    data = []
    result = Fy.objects.all()
    for i in result:
        adata = {
            'name': i.name,
            'url': i.url,
            'address': i.address,
            'addressurl': i.addressurl,
            'price': i.price,
            'issell': i.issell,
            'phone': i.phone,
            'area': i.area,
            'size': i.size
        }
        data.append(adata)

    return JsonResponse(data, safe=False)


def update(request):
    city = request.GET.get('city')
    area = request.GET.get('area')
    data = {
        'code': 200
    }
    # 删除数据库
    try:
        Fy.objects.all().delete()
    except Exception as e:
        print(e)
        data = {
            'code': 300
        }
    # 爬取数据
    try:
        fy = FY(area, city)
        fy.getAreas()  # 获取有哪些数据
        fy.getAllArea()  # 获取所有区域的房源数据
    except Exception as e:
        print(e)
    return JsonResponse(data, safe=False)


