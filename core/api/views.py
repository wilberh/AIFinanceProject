from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.decorators import api_view, schema
from django.http import JsonResponse
from rest_framework.schemas import AutoSchema
from rest_framework import permissions
from django.http import Http404
from .trending import get_stock_price, trending_by_country
from datetime import datetime, date, timedelta


class GoogleTrendApiDetail(APIView):
    def post(self, request):
        data = request.data
        # Example of API body/payload:
        # {"task": "quote", "ticker": "AAPL" [OPTIONAL: ,"strt_dt": "2023-06-29", "end_dt": "2023-07-28"]}
        # {"task": "trend", "company": "Apple", "country": "us" [OPTIONAL: ,"strt_dt", "2023-06-29", "end_dt": "2023-07-28"]}

        task = data["task"]

        # NOTE: Hardcoded start and end dates to qualify for free-tier NewsAPI access (last 30 days)
        end_dt = date.today()
        strt_dt = end_dt - timedelta(days=29)
        strt_dt = data.get("strt_dt", strt_dt.isoformat())
        end_dt = data.get("end_dt", end_dt.isoformat())  

        if task == "quote":
            sp_close = get_stock_price(data["ticker"], strt_dt, end_dt)
            if "error" in sp_close:
                return Response(sp_close, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(sp_close, status=status.HTTP_200_OK)
        elif task == "trend":
            trend_resp = trending_by_country(data["company"], data["country"], strt_dt, end_dt)
            if "error" in trend_resp:
                return Response(trend_resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(trend_resp, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


    # def Index(request):
    #     return HttpResponse("AIFinance backend app page")
    #     # raise Http404("Poll does not exist")