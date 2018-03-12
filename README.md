# speciPy
Data document descriptor;

# How to use:

## build doc spec
``` 
# sample from open api v3.0.1 
# Default create
openapi_spec = specipy.spec()
# root entity
openapi_spec.expect(keys='openapi', datatype=str, required=True)
# simpler
openapi_infospec = openapi_spec.expect('info')
openapi_infospec.expect('title', str, True)
openapi_infospec.expect('description', str)
openapi_infospec.expect('contact', object)
...
```
### simplified
```
openapi_spec = specipy.spec()
openapi_spec.expects('/openapi', str, '...', True)
# autofill
openapi_spec.expects('/info/title', str, True)
openapi_spec.expects('/info/description', str)

# or

openapi_spec = specipy.spec([
    ('/openapi', str, '...'),
    ('/info/title', str),
    ('/info/description', str),
    ('/info/contact', object),
    ...
])
```

## Data loading
```
import json
import yaml

with open('specs/openapi.v3.json') as spec :
    openapi_spec = specipy(spec)
    with open('example/openapi.v3/petshop.yaml') as data_in :
        petshop_app = openapi_spec.build(yaml.load(data_in))
        # is this document valid?
        if petshop_app.is_valid() :
            print(petshop_app.info.title) ### 'Petshop'
```
## Pretty print view of schema
```
petshop_app.print_spec() 
    - openapi (str): v3.0.1
    + info (object):
        - title (str): 'Petshop'

```

## fill
newapp = openapi_spec.build()
newapp.openapi = '3.0'
...

if newapp.is_valid() :
    newapp.dump(yaml, './newapp.yaml')

