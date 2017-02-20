from django.contrib import admin

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.contrib.contenttypes import generic
from suit.widgets import LinkedSelect
from core.admin import ServiceAppAdmin,SliceInline,ServiceAttrAsTabInline, ReadOnlyAwareAdmin, XOSTabularInline, ServicePrivilegeInline, TenantRootTenantInline, TenantRootPrivilegeInline
from core.middleware import get_request

from services.vtn.models import *

from functools import update_wrapper
from django.contrib.admin.views.main import ChangeList
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import quote

class ComputeNodeServiceForm(forms.ModelForm):
    nodeId = forms.CharField(required=True)
    hostname = forms.CharField(required=True)
    management_address = forms.CharField(required=True)
    fabric_address = forms.CharField(required=True)
    hardward_address = forms.CharField(required=True)
    role = forms.CharField(required=True)

    def __init__(self,*args,**kwargs):
        super (ComputeNodeServiceForm, self).__init__(*args,**kwargs)
        if self.instance:
            self.fields['nodeId'].initial = self.instance.nodeId
            self.fields['hostname'].initial = self.instance.hostname
            self.fields['management_address'].initial = self.instance.management_address
            self.fields['fabric_address'].initial = self.instance.fabric_address
            self.fields['hardward_address'].initial = self.instance.hardward_address
            self.fields['role'].initial = self.instance.role

    def save(self, commit=True):
        self.instance.nodeId = self.cleaned_data.get('nodeId')
        self.instance.hostname = self.cleaned_data.get('hostname')
        self.instance.management_address = self.cleaned_data.get('management_address')
        self.instance.fabric_address = self.cleaned_data.get('fabric_address')
        self.instance.hardward_address = self.cleaned_data.get('hardward_address')
        self.instance.role = self.cleaned_data.get('role')
        return super(ComputeNodeServiceForm, self).save(commit=commit)

    class Meta:
        model = ComputeNodeService
        fields = '__all__'

class ComputeNodeServiceAdmin(ReadOnlyAwareAdmin):
    model = ComputeNodeService
    form = ComputeNodeServiceForm
    verbose_name = 'Compute Node Service'
    verbose_name_plural = 'Compute Node Services'
    list_display = ('backend_status_icon', 'name', 'enabled')
    list_display_links = ('backend_status_icon', 'name', )
    fieldsets = [(None, {'fields': ['backend_status_text', 'name','enabled','versionNumber','description','view_url','icon_url',
                                    'nodeId', 'hostname', 'management_address', 'fabric_address', 'hardward_address', 'role'],
                                    'classes':['suit-tab suit-tab-general']})]
    readonly_fields = ('backend_status_text', )
    inlines = [SliceInline,ServiceAttrAsTabInline,ServicePrivilegeInline]

    extracontext_registered_admins = True

    user_readonly_fields = ['name', 'enabled', 'versionNumber', 'description']

    suit_form_tabs =(('general', 'Compute Node Service Details'),
#        ('administration', 'Administration'),
        ('slices','Slices'),
        ('serviceattrs','Additional Attributes'),
        ('serviceprivileges','Privileges'),
    )

    suit_form_includes = ( # ('computenodeadmin.html', 'top', 'administration'),
                           ) #('hpctools.html', 'top', 'tools') )

    def get_queryset(self, request):
        return ComputeNodeService.get_service_objects_by_user(request.user)

admin.site.register(ComputeNodeService, ComputeNodeServiceAdmin)
