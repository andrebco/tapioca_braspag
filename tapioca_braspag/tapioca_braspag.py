# coding: utf-8

from tapioca import (
    TapiocaAdapter, JSONAdapterMixin)

from tapioca.tapioca import TapiocaClient, TapiocaClientExecutor,\
     TapiocaInstantiator

from tapioca.exceptions import ResponseProcessException, ClientError,\
     ServerError

from resource_mapping import RESOURCE_MAPPING


class BraspagClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://apisandbox.braspag.com.br/'
    api_get_root = 'https://apiquerysandbox.braspag.com.br/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(BraspagClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        import ipdb; ipdb.set_trace()

        if 'headers' in api_params:
            params['headers'] = api_params['headers']

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def process_response(self, response):
        if str(response.status_code).startswith('5'):
            raise ResponseProcessException(ServerError, None)

        if str(response.status_code).startswith('4'):
            raise ResponseProcessException(ClientError, response)

        data = self.response_to_native(response)

        return data


class TapiocaBraspagInstantiator(TapiocaInstantiator):

    def __call__(self, *args, **kwargs):
        return TapiocaBraspagClient(self.adapter_class(), api_params=kwargs)


class TapiocaBraspagClient(TapiocaClient):

    def _wrap_in_tapioca_executor(self, data, *args, **kwargs):
        return TapiocaBraspagClientExecutor(self._api.__class__(),
            data=data, api_params=self._api_params, *args, **kwargs)


class TapiocaBraspagClientExecutor(TapiocaClientExecutor):

    def get(self, *args, **kwargs):
        kwargs.update({'url': self._api.api_get_root,})
        import ipdb; ipdb.set_trace()
        return self._make_request('GET', *args, **kwargs)

def generate_wrapper_from_adapter(adapter_class):
    return TapiocaBraspagInstantiator(adapter_class)

Braspag = generate_wrapper_from_adapter(BraspagClientAdapter)
