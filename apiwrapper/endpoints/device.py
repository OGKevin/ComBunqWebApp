from apiwrapper.endpoints.endpoint import Endpoint


class Device(Endpoint):

    __endpoint_device = "device"

    @classmethod
    def _get_base_endpoint(cls, device_id=None):
        endpoint = "/%s" % cls.__endpoint_device
        if device_id is not None:
            endpoint += "/%d" % device_id
        return endpoint

    def get_all_devices(self):
        endpoint = self._get_base_endpoint()

        return self._make_get_request(endpoint)

    def get_device_by_id(self, device_id):
        endpoint = self._get_base_endpoint(device_id)

        return self._make_get_request(endpoint)
