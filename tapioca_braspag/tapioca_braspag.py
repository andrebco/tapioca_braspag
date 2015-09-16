# coding: utf-8

from tapioca import (
    TapiocaAdapter, JSONAdapterMixin)

from tapioca.tapioca import TapiocaClient, TapiocaClientExecutor,\
     TapiocaInstantiator

from resource_mapping import RESOURCE_MAPPING


class BraspagClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://apisandbox.braspag.com.br/'
    api_get_root = 'https://apiquerysandbox.braspag.com.br/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(BraspagClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        if 'headers' in api_params:
            params['headers'] = api_params['headers']

        return params

    def get_iterator_list(self, response_data):
        return response_data


class TapiocaBraspagInstantiator(TapiocaInstantiator):

    def __call__(self, *args, **kwargs):
        return TapiocaBraspagClient(self.adapter_class(), api_params=kwargs)


class TapiocaBraspagClient(TapiocaClient):

    def _wrap_in_tapioca_executor(self, data, *args, **kwargs):
        return TapiocaBraspagClientExecutor(self._api.__class__(),
            data=data, api_params=self._api_params, *args, **kwargs)


class TapiocaBraspagClientExecutor(TapiocaClientExecutor):

    def get(self, *args, **kwargs):
        kwargs.update({'url': self._api.api_get_root})
        return self._make_request('GET', *args, **kwargs)


        return TapiocaClient(self.adapter_class(), api_params=kwargs)

def generate_wrapper_from_adapter(adapter_class):
    return TapiocaBraspagInstantiator(adapter_class)

Braspag = generate_wrapper_from_adapter(BraspagClientAdapter)
