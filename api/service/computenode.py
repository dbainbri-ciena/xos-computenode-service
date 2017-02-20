from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework import status
from core.models import *
from services.computenode.models import ComputeNodeService
from django.forms import widgets
from django.conf.urls import patterns, url
from api.xosapi_helpers import PlusModelSerializer, XOSViewSet, ReadOnlyField
from django.shortcuts import get_object_or_404
from xos.apibase import XOSListCreateAPIView, XOSRetrieveUpdateDestroyAPIView, XOSPermissionDenied
from xos.exceptions import *
import json
import subprocess

class ComputeNodeServiceSerializer(PlusModelSerializer):
    id = ReadOnlyField()

    nodeId = serializers.CharField(required=True)
    hostname = serializers.CharField(required=True)
    management_address = serializers.CharField(required=True)
    fabric_address = serializers.CharField(required=True)
    hardware_address = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    humanReadableName = serializers.SerializerMethodField('getHumanReadableName')
    class Meta:
        model = ComputeNodeService
        fields = ('humanReadableName', 'id', 'nodeId', 'hostname', 'management_address', 'fabric_address', 'hardware_address', 'role')

    def getHumanReadableName(self, obj):
        return obj.__unicode__()

class ComputeNodeViewSet(XOSViewSet):
    base_name = 'computenode'
    method_name = 'computenode'
    method_kind = 'viewset'

    # these are just because ViewSet needs some queryset and model, even if we don't use the
    # default endpoints
    queryset = ComputeNodeService.get_service_objects().all()
    model = ComputeNodeService
    serializer_class = ComputeNodeServiceSerializer

    custom_serializers = {}

    @classmethod
    def get_urlpatterns(self, api_path='^'):
        patterns = []

        patterns.append( self.detail_url('nodes/$', {'get': 'get_nodes'}, 'computenodes') )
        patterns.append( self.detail_url('node/(?P<computenode>[a-zA-Z0-9\-_]+)/$', {'get': 'get_node'}, 'get_node') )

        patterns = patterns + super(ComputeNodeViewSet,self).get_urlpatterns(api_path)

        return patterns

    def get_nodes(self, request, pk=None):
        return Response(list(ComputeNodeService.objects.all()))

    def get_node(self, request, pk=None):
        return Response(list(ComputeNodeService.objects.filter(hostname=pl)))
