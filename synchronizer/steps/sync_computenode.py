from synchronizers.base.SyncUsingAnsible import SyncUsingAnsible
from services.computenode.models import ComputeNodeService
from xos.logger import Logger, logging
from django.db.models import F, Q
import json
import os
import sys

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)

class SyncComputeNodeService(SyncUsingAnsible):

    provides = [ComputeNodeService]

    observes = ComputeNodeService

    requested_interval = 0

    template_name = "compute_node_playbook.yaml"

    def get_node_key(self, n):
	return "/opt/cord/orchestration/service-profile/cord-pod/id_rsa"

    def __init__(self, *args, **kwargs):
        super(SyncComputeNodeService, self).__init__(*args, **kwargs)

    def get_connection_info(self, o):
        return {
            'hostname'         : o.hostname,
            'instance_name'    : o.hostname,
            'instance_id'      : o.hostname,
            'ansible_ssh_user' : 'ubuntu',
            'ansible_ssh_port' : 22,
            'ssh_ip'   : o.hostname,
            'ssh_key'          : 'file:///opt/xos/synchronizers/computenode/steps/cord_rsa'
        }

    def fetch_pending(self, deleted):
	logger.error("IN PENDING: %s" % deleted)
	logger.error(ComputeNodeService.get_service_objects().all())

        if (not deleted):
            objs = ComputeNodeService.get_service_objects().filter(
                Q(enacted__lt=F('updated')) | Q(enacted=None), Q(lazy_blocked=False))
        else:
            # If this is a deletion we get all of the deleted tenants..
            objs = [] #ComputeNodeService.get_deleted_service_objects()
        logger.error("RETURNING: " + str(objs))

        return objs

    def get_computenodeservice(self, o):
        logger.error("IN GET " + o)
        if not o.provider_service:
            return None

        computenodeservice = ComputeNodeService.get_service_objects().filter(id=o.provider_service.id)

        if not computenodeservice:
            return None

        logger.error("HERE IS WHAT I HAVE: " + str(computenodeservice))

        return computenodeservice[0]

    # Gets the attributes that are used by the Ansible template but are not
    # part of the set of default attributes.
    def get_extra_attributes(self, o):
        fields = {}
        return fields
