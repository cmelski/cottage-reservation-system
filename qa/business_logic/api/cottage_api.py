class CottageAPI:

    def __init__(self, api_client):
        self.api_client = api_client
        self.get_cottage_endpoint = api_client.config["get_cottage_endpoint"]

    def get_cottage(self):
        cottage = self.api_client.call_api_with_retry(f'{self.get_cottage_endpoint}',
                                                      'GET')
        return cottage
