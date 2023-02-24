# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: fastapi_mongo
  $Author: Anders Wiklund
    $Date: 2023-02-18 00:27:47
     $Rev: 1
"""

# BUILTIN modules
import os
import sys
import site
from typing import Union

# Third party modules
from pydantic import BaseSettings, validator

# Constants
MISSING_SECRET = '>>> missing SECRETS file <<<'
""" Error message for missing secrets file. """
MISSING_ENV = '>>> undefined ENV parameter <<<'
""" Error message for missing environment variables. """
SECRETS_DIR = ('/run/secrets'
               if os.path.exists('/.dockerenv')
               else f'{site.USER_BASE}/secrets')
""" This is where your secrets are stored, either in Docker or locally. """
PLATFORM = {'linux': 'Linux', 'linux2': 'Linux',
            'win32': 'Windows', 'darwin': 'MacOS'}
""" Known platforms in my end of the world. """


# --------------------------------------------------------------
# This needs to be done before the Base class gets evaluated, and
# to avoid getting five UserWarnings that the path does not exist.
#
# Create the directory if it does not already exist. When running
# inside Docker, skip it (Docker handles that just fine on its own).
#
if not os.path.exists('/.dockerenv'):
    os.makedirs(SECRETS_DIR, exist_ok=True)


# ------------------------------------------------------------------------
#
class Base(BaseSettings):
    """ Common configuration parameters shared between all environments.

    The following environment variables should already be defined::
      - HOSTNAME (on Linux servers only - set by OS)
      - COMPUTERNAME (on Windows servers only - set by OS)
      - ENVIRONMENT (on all servers - "dev" is default when missing)

    Path where your <environment>.env file should be placed::
      - linux: /home/<user>/.local
      - darwin: /home/<user>/.local
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python'

    Path where your secret files should be placed::
      - linux: /home/<user>/.local/secrets
      - darwin: /home/<user>/.local/secrets
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python\\secrets'

    You know you are running in Docker when the "/.dockerenv" file exists.
    """

    class Config:
        """ Enable the usage of secrets. """
        secrets_dir = SECRETS_DIR

    # secrets...
    mongoPwd: str = MISSING_SECRET

    # Normal stuff.
    routingDbPort = 8012
    trackingDbPort = 8006
    mqServer = 'P-W-MQ01'
    apiTimeout = (9.05, 60)
    env: str = os.getenv('ENVIRONMENT', 'dev')
    hdrData = {'Content-Type': 'application/json'}
    platform: str = PLATFORM.get(sys.platform, 'other')
    server: str = os.getenv(('COMPUTERNAME'
                             if sys.platform == 'win32'
                             else 'HOSTNAME'), MISSING_ENV)

    @validator('server', always=True, pre=True)
    def remove_domain(cls, value) -> str:
        """ Return server name stripped of possible domain part. """
        return value.upper().split('.')[0]


# ------------------------------------------------------------------------
#
class Dev(Base):
    """ Configuration parameters for DEV environment. """

    mqServer: str = 'localhost'
    dbServer: str = 'localhost:3306'
    portalApi: str = 'http://localhost'
    mongoUrl: str = f'mongodb://phoenix:{Base().mongoPwd}@localhost:27017/'

    class Config:
        """ Context aware env file. """
        env_file_encoding = 'utf-8'
        env_file = f'{site.USER_BASE}/dev.env'


# ------------------------------------------------------------------------
#
class Test(Base):
    """ Configuration parameters for TEST environment. """

    dbServer: str = 't-l-docker01:3306'
    mongoUrl: str = f'mongodb://phoenix:{Base().mongoPwd}@t-l-docker01:27017/'

    class Config:
        """ Context aware env file. """
        env_file_encoding = 'utf-8'
        env_file = f'{site.USER_BASE}/test.env'


# ------------------------------------------------------------------------
#
class Stage(Base):
    """ Configuration parameters for STAGE environment. """

    routingDbPort = 8013
    trackingDbPort = 8007
    dbServer: str = 't-l-docker01:3307'
    mongoUrl: str = f'mongodb://phoenix:{Base().mongoPwd}@t-l-docker01:27117/'

    class Config:
        """ Context aware env file. """
        env_file_encoding = 'utf-8'
        env_file = f'{site.USER_BASE}/stage.env'


# ------------------------------------------------------------------------
#
class Prod(Base):
    """ Configuration parameters for PROD environment. """

    dbServer: str = 'ocsemysqlcl:3306'
    mongoUrl: str = f'mongodb://phoenix:{Base().mongoPwd}@t-l-webtools01:27017/'

    class Config:
        """ Context aware env file. """
        env_file_encoding = 'utf-8'
        env_file = f'{site.USER_BASE}/prod.env'


# ------------------------------------------------------------------------

_setup = dict(
    dev=Dev,
    test=Test,
    prod=Prod,
    stage=Stage
)
""" Translation table between ENVIRONMENT value and their classes. """

config: Union[Dev, Test, Prod, Stage] = \
    _setup[os.getenv('ENVIRONMENT', 'dev').lower()]()
""" Instantiate the required platform environment. """
