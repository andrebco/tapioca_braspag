# coding: utf-8

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)

from tapioca.tapioca import TapiocaClient, TapiocaClientExecutor

from resource_mapping import RESOURCE_MAPPING


class BraspagClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://apisandbox.braspag.com.br/'
    api_get_root = 'https://apiquerysandbox.braspag.com.br/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(BraspagClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self,
            iterator_request_kwargs, response_data, response):
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


class TapiocaBraspagInstantiator(object):

    def __init__(self, adapter_class):
        self.adapter_class = adapter_class

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


Braspag = TapiocaBraspagInstantiator(BraspagClientAdapter)
