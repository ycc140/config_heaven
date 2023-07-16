# config_heaven
Python config handling using Pydantic

#### Author: Anders Wiklund

To be able to run this code you need to install the eminent third party [_Pydantic_](https://docs.pydantic.dev/) package.
> 📝 **Note:** Pydantic requires Python v3.7+ to work.

You can install it like this:
```shell
$ pip install pydantic-settings[dotenv]
```

> 📝 **Note:** Pydantic have just release v2 and it’s not backwards compatible. No worries I have updated this example to be compliant with the new version.

The _configurator.py_ module contains the needed code. _test_config.py_ is a 
small test program that is helpful for testing the response you will get on 
different environment platforms.

Running the _test_conf.py_ program on muy laptop like this:
```shell
$ test_conf.py dev
```

Produces the following result:
```python
{'apiTimeout': (9.05, 60),
 'dbServer': 'ocsemysqlcl:3306',
 'env': 'dev',
 'hdrData': {'Content-Type': 'application/json'},
 'mongoPwd': '>>> missing SECRETS file <<<',
 'mongoUrl': 'mongodb://phoenix:>>> missing SECRETS file <<<@localhost:27017/',
 'mqServer': 'localhost',
 'platform': 'Windows',
 'portalApi': 'http://localhost',
 'routingDbPort': 8012,
 'server': 'CHARON',
 'trackingDbPort': 8006}
```

To get a deeper and better understanding of what the code does, and what's possible you should read my Mediom article [Lovely Python config handling using Pydantic](https://medium.com/@wilde.consult/lovely-python-config-handling-using-pydantic-852d9be2320f) that this code is developed for.
