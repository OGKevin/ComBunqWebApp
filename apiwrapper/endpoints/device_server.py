from apiwrapper.endpoints.endpoint import Endpoint


class DeviceServer(Endpoint):

    __endpoint_device_server = "device-server"

    @classmethod
    def _get_base_endpoint(cls, server_id=None):
        endpoint = "/%s" % cls.__endpoint_device_server
        if server_id is not None:
            endpoint += "/%d" % server_id
        return endpoint

    def get_all_device_servers(self):
        endpoint = self._get_base_endpoint()

        return self._make_get_request(endpoint)

    def get_device_server_by_id(self, server_id):
        endpoint = self._get_base_endpoint(server_id)

        return self._make_get_request(endpoint)

    def create_new_device_server(self, description, permitted_ips=None):
        endpoint = self._get_base_endpoint()
        payload = {
            'description': description,
            'secret': self._api_client.api_key
        }
        if permitted_ips is not None:
            payload["permitted_ips"] = permitted_ips

        return self._make_post_request(endpoint, payload)


