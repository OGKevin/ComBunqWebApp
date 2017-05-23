#  my init_api
```python
from apiwrapper.clients.api_client import ApiClient as API2  # noqa

self.init_api = API2(
    privkey=f['privateKey'],
    api_key=f['API'],
    installation_token=f['Token']['token'],
    server_pubkey=f['ServerPublicKey']['server_public_key']
)

```

# the callback

```python
r = self.init_api.endpoints.device_server.create_new_device_server('ComBunqWebApp').json()  # noqa
return r

```

# will return None with

`ApiClient is not yet properly set up! Variables missing!`

# Because of no session token according to

```python

def client_is_setup(self):
  return self.session_token is not None and self.privkey is not None
```
    
# so if've changed it to just return True

```python
def client_is_setup(self):
  # return self.session_token is not None and self.privkey is not None
  return True

```

# which will now return

`Insufficient authentication.`
