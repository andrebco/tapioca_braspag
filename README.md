# Tapioca Braspag

## Installation
```
pip install tapioca-braspag
```

## Documentation
Braspag has two different endpoints. One is intentded to POST and PUT methods
and the othrer is designed to perform GET operations.

You can consult these operations in the api docs [here](http://apidocs.braspag.com.br/)

For that reason, you'll need a different adapter for each endpoint:

``` python
from tapioca_braspag import Braspag, BraspagConsult


# POST to and PUT to api
api = Braspag(merchant_id='your-merchant-id', merchant_key='your_merchant_key')

# GET from api
api_query = BraspagConsult(merchant_id='your-merchant-id',
                           merchant_key='your_merchant_key')
```

#### homolog and sandbox

if you want to post to homolog or sandbox, pass it as an api_param:
```
api_homolog = Braspag(merchant_id='your-merchant-id', merchant_key='your_merchant_key',
                   homolog=True)

test_sandbox = Braspag(merchant_id='your-merchant-id', merchant_key='your_merchant_key',
                   sandbox=True)
```
No more documentation needed.

- Learn how Tapioca works [here](http://tapioca-wrapper.readthedocs.org/en/latest/quickstart/)
- Explore this package using iPython
- Have fun!
