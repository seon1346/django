from django.shortcuts import render
import requests
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework import  status
from rest_framework.views import APIView
from  django.http import HttpResponse,JsonResponse
from haversine import haversine
import json

#from rest_framework.decorators import api_view, renderer_classes
#from rest_framework.request import Request

# Create your views here.


class Customer_register(APIView):
    """
        고객 등록 API
        ---
        # request json
            - username : 고객 이름
            - password : 비밀번호
            - address : 주소(지번 or 도로명 주소까지)
            - detail : 상세주소
        # response
            - 200 : 성공
            - 501, msg-주소변환오류 : 주소변환오류
    """
    def post(self,request):
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        address=data['address']
        try:
            new_address,old_address,x ,y=get_both_address(address)
        except:
            return HttpResponse(json.dumps({'msg':'주소변환오류'}),status=status.HTTP_501_NOT_IMPLEMENTED)
        detail = data['detail']
        Customer.objects.create(username=username, password=password, new_address=new_address,old_address=old_address, detailed_address=detail,x=x,y=y).save()
        return HttpResponse(status=status.HTTP_200_OK)


class Deliveryman_register(APIView):
    """
        배달원 등록 API
        ---
        # request json
            - name : 배달원 이름
            - address : 주소(지번 or 도로명 주소까지)
            - detail : 상세주소
        # response
            - 200 : 성공
            - 501, msg-주소변환오류 : 주소변환오류
    """
    def post(self,request):
        data = JSONParser().parse(request)
        name = data['name']
        address=data['address']
        try:
            new_address,old_address,x ,y=get_both_address(address)
        except:
            return HttpResponse(json.dumps({'msg':'주소변환오류'}),status=status.HTTP_501_NOT_IMPLEMENTED)
        detail = data['detail']
        Del_man.objects.create(name=name, new_address=new_address,old_address=old_address, detailed_address=detail,x=x,y=y).save()
        return HttpResponse(status=status.HTTP_200_OK)

#appkey 재발급
appkey=	'KakaoAK 1d5339e9d072f392889105c67104f95f'
def get_both_address(address):
    headers = {'Authorization': appkey}
    url = "https://dapi.kakao.com/v2/local/search/address.json?page=1&size=10&query="+address
    result = json.loads(str(requests.get(url, headers=headers).text))
    old_address=result['documents'][0]['address']['address_name']
    new_address=result['documents'][0]['road_address']['address_name']
    x=result['documents'][0]['address']['x']
    y=result['documents'][0]['address']['y']
    return new_address, old_address, x, y




class item_assign(APIView):
    """
        상품 할당 API(주문 정보생성)
        ---
        # request json
            - c_id : 고객 id값
            - s_id : 고객사 id값
            - item_list : 구매 아이템 id값 list
            - num_list : 구매 아이템의 수량 list
        # response
            - 200 : 성공
            - 501, msg-고객사 정보 없음 : 고객사 정보 없음
            - 501, msg-상품 정보 오류 : 상품 정보 오류
            - 501, msg-고객사 상품 보유 정보 오류 : 고객사 상품 보유 정보 오류
            - 501, msg-고객사 재고 미달 : 고객사 재고 미달

    """
    del_num = 0
    def post(self,request):
        item_assign.del_num+=1
        delivery_number=item_assign.del_num
        data = JSONParser().parse(request)
        c_id=data['c_id']
        try:
            customer=Customer.objects.get(id=c_id)
        except:
            return HttpResponse(json.dumps(json.dumps({'msg':'고객 정보 없음'})),status=status.HTTP_501_NOT_IMPLEMENTED)
        store_id=data['s_id']
        item_list=data['item_list']
        num_list = data['num_list']
        try:
            store = Store.objects.get(id=store_id)
        except:
            return HttpResponse(json.dumps(json.dumps({'msg':'고객사 정보 없음'})),status=status.HTTP_501_NOT_IMPLEMENTED)
        return_val=[]
        for i in range(len(item_list)):
            try:
                item=Item.objects.get(id=item_list[i])
            except:
                return HttpResponse(json.dumps(json.dumps({'msg': '상품 정보 오류'})), status=status.HTTP_501_NOT_IMPLEMENTED)

            try:
                item_store=Item_Store.objects.get(item=item,store=store)
            except:
                return HttpResponse(json.dumps(json.dumps({'msg': '고객사 상품 보유 정보 오류'})), status=status.HTTP_501_NOT_IMPLEMENTED)

            if item_store.num-num_list[i]<0:
                return HttpResponse(json.dumps(json.dumps({'msg': '고객사 재고 미달'})), status=status.HTTP_501_NOT_IMPLEMENTED)
            item_store.num-=num_list[i]
            item.total-=num_list[i]
            item_store.save()
            item.save()

            delivery = Delivery.objects.create(assigned_customer=customer, del_num=delivery_number,Item_Store=item_store)
            del_serial = DeliverySerializer(delivery)
            return_val.append(del_serial.data)
        return HttpResponse(return_val,status=status.HTTP_200_OK)




class del_assign(APIView):
    """
        배달원 할당 API
        ---
        # request json
            - del_num : 주문번호
        # response
            - 200 : 성공
            - 501, msg-주문정보없음 : 주문정보없음
            - 501, msg-고객 정보 없음 : 고객 정보 없음
            - 501, msg-배달원 없음 : 배달원 없음

    """
    def put(self,request):
        data = JSONParser().parse(request)
        del_num=data['del_num']
        deliverys=Delivery.objects.filter(del_num=del_num)
        if len(deliverys)==0:
            return HttpResponse(json.dumps({'msg': '주문정보없음'}), status=status.HTTP_501_NOT_IMPLEMENTED)
        try:
            customer=deliverys[0].assigned_customer
        except:
            return HttpResponse(json.dumps({'msg':'고객 정보 없음'}),status=status.HTTP_501_NOT_IMPLEMENTED)
        del_man_list = Del_man.objects.all()
        if len(del_man_list)==0:
            return HttpResponse(json.dumps({'msg':'배달원 없음'}),status=status.HTTP_501_NOT_IMPLEMENTED)

        c_gps=(customer.y,customer.x)
        choiced_del_man=None
        km_min=500
        for del_man in del_man_list:
            d_gps = (del_man.y,del_man.x)
            km=haversine(c_gps, d_gps)
            if km_min > km:
                km_min=km
                choiced_del_man=del_man
        return_val=[]
        for d in deliverys:
            d.assigned_del_man= choiced_del_man
            d.save()
            del_serial = DeliverySerializer(d)
            return_val.append(del_serial.data)

        return HttpResponse(return_val,status=status.HTTP_200_OK)



class complete(APIView):
    """
        배달 완료처리 API
        ---
        # request json
            - del_num : 주문번호
        # response
            - 200 : 성공
            - 501, msg-주문정보오류 : 주문정보오류

    """
    def put(self,request):
        data = JSONParser().parse(request)
        del_num=data['del_num']
        deliverys=Delivery.objects.filter(del_num=del_num)
        if len(deliverys)==0:
            return HttpResponse(json.dumps({'msg':'주문정보 오류'}),status=status.HTTP_501_NOT_IMPLEMENTED)
        for d in deliverys:
            d.complete= True
            d.save()
        return HttpResponse(status=status.HTTP_200_OK)




