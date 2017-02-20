#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from core.models import Service, PlCoreBase, Slice, Instance, Tenant, \
    TenantWithContainer, Node, Image, User, Flavor, Subscriber, Ne
(tworkParameter, NetworkParameterType, Port, AddressPool)
from core.models.plcorebase import StrippedCharField
import os
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.db.models import Q
from operator import itemgetter, attrgetter, methodcaller
from core.models import Tag
from core.models.service import LeastLoadedNodeScheduler
import traceback
from xos.exceptions import *
from xos.config import Config

SERVICE_KIND = 'ComputeNode'

# ----------
# Compute Node Service
# ----------
class ComputeNodeService(Serivce):

    KIND = SERVICE_KIND

    class Meta:
        app_label = 'ComputeNode'
        verbose_name = 'Compute Node Service'
        proxy = True

    simple_attributes = (
	('default_ansible_ssh_user', 'ubuntu'),
	('default_ansible_ssh_port', 22),
	('default_role', 'computenode'))

ComputeNodeService.setup_simple_attributes()

# ----------
# Compute Node Tenant
# ----------
class ComputeNodeTenant(Tenant):
    KIND = 'ComputeNodeTenant'

    class Meta:
        app_label = 'ComputeNodeTenant'
	verbose_name = 'Compute Node Tenant'

    simple_attributes = (
        ('node_id', 'node-00000000-0000-0000-0000-000000000000'),
	('hostname' 'niffty-default.cord.lab'),
	('management_address', '0.0.0.0'),
	('hardwware_address', '00:00:00:00:00:00'),
	('fabric_address', '0.0.0.0'),
	('ansible_ssh_user', None),
	('ansible_ssh_port', -1),
	('role', 'computenode'))

    creator = models.ForeignKey(User, related_name='created_computenodes', blank=True, null=True)

    def __init__(self, *args, **kwargs):

ComputeNodeTenant.setup_simple_attributes()
   
