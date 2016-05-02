# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pecan import abort
from pecan.rest import RestController
import six
from mongoengine import ValidationError

from st2common import log as logging
from st2common.exceptions.keyvalue import CryptoKeyNotSetupException
from st2common.models.api.keyvalue import KeyValuePairAPI
from st2common.models.api.base import jsexpose
from st2common.persistence.keyvalue import KeyValuePair
from st2common.services import coordination

http_client = six.moves.http_client

LOG = logging.getLogger(__name__)

__all__ = [
    'PackConfigController'
]


class PackConfigController(RestController):
    """
    Implements the REST endpoint for managing pack config values in the datastore.
    """

    @jsexpose(arg_types=[str], status_code=http_client.OK)
    def get_all(self, pack_ref_or_id):
        """
        Retrieve all the configuration item for the provided pack.

        Handles requests:

            GET /packs/config/<pack_ref_or_id>
        """
        pack_db = self._get_by_ref_or_id(ref_or_id=pack_ref_or_id)

        if not pack_db:
            msg = 'Pack with ref_or_id "%s" does not exist' % (ref_or_id)
            raise StackStormDBObjectNotFoundError(msg)

        kvp_dbs = get_datastores_items_for_pack(pack_name=pack_db.name)
        kvp_apis = []

        for kvp_db in kvp_dbs:
            kvp_api = KeyValuePairAPI.from_model(kvp_db)
            kvp_apis.append(kvp_db)
        return kvp_apis

    @jsexpose(arg_types=[str])
    def get_one(self, pack_ref_or_id, config_item_name):
        """
        Retrieve a single configuration value.

        Handles requests:

            GET /packs/config/<pack_ref_or_id>/<config_item_name>
        """
        pass

    @jsexpose(arg_types=[str, str], body_cls=KeyValuePairAPI)
    def put(self, pack_ref_or_id, config_item_value):
        """
        Set a value for a particular configuration item.

        Handles requests:

            PUT /packs/config/<pack_ref_or_id>/<config_item_name>
        """
        pass

    @jsexpose(arg_types=[str], status_code=http_client.NO_CONTENT)
    def delete(self, pack_ref_or_id, config_item_name):
        """
        Delete a value for a particular configuration item.

        Handles requests:

            DELETE /packs/config/<pack_ref_or_id>/<config_item_name>
        """
        pass

