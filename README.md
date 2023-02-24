# config_heaven
Python config handling using Pydantic

#### Author: Anders Wiklund

To be able to run this code you need to install the eminent third party [_Pydantic_](https://docs.pydantic.dev/) package.
> 📝 **Note:** Pydantic requires Python v3.7+ to work.

You can install it like this:
```shell
$ pip install pydantic[dotenv]
```

The _configurator.py_ module contains the needed code. _test_config.py_ is a 
small test program that is helpful for testing the response you will get on 
different environment platforms.

Running the _test_conf.py_ program on muy laptop like this:
```shell
$ test_conf.py dev
```

Produces the following result:
```json
$ pip install pydantic[dotenv]
```

To get a deeper and better understanding of what the code does, and what's possible you should read my Mediom article [Lovely Python config handling using Pydantic](https://medium.com/@wilde.consult/lovely-python-config-handling-using-pydantic-852d9be2320f) that this code is developed for.
