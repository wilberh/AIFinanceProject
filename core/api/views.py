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


class GoogleTrendApiDetail(APIView):
    def get(self, request, pk=None):
        return Response({"message": "testing!"}, status=status.HTTP_200_OK)
