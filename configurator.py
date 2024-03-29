# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: config_heaven
  $Author: Anders Wiklund
    $Date: 2023-09-26 17:12:37
     $Rev: 1
"""

# BUILTIN modules
import os
import sys
import site
from typing import Union, Type, Tuple

# Third party modules
from pydantic import Field, computed_field
from pydantic_settings import (BaseSettings, SettingsConfigDict,
                               PydanticBaseSettingsSource)

# Constants
USER_BASE = site.getuserbase()
""" This is required when programs are frozen."""
MISSING_ENV = '>>> undefined ENV parameter <<<'
""" Error message for missing environment variables. """
MISSING_SECRET = '>>> missing SECRETS file <<<'
""" Error message for missing secrets file. """
SECRETS_DIR = ('/run/secrets'
               if os.path.exists('/.dockerenv')
               else f'{site.USER_BASE}/secrets')
""" This is where your secrets are stored (in Docker or locally). """
PLATFORM = {'linux': 'Linux', 'linux2': 'Linux',
            'win32': 'Windows', 'darwin': 'MacOS'}
""" Known platforms in my end of the world. """
ENVIRONMENT = os.getenv('ENVIRONMENT', MISSING_ENV)
""" Define environment. """

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
class Common(BaseSettings):
    """ Common configuration parameters shared between all environments.

    Read configuration parameters defined in this class, and from
    ENVIRONMENT variables and from the .env file.

    The source priority is changed (from default) to the following
    order (from highest to lowest):
      - init_settings
      - dotenv_settings
      - env_settings
      - file_secret_settings

    The following environment variables should already be defined:
      - HOSTNAME (on Linux servers only - set by OS)
      - COMPUTERNAME (on Windows servers only - set by OS)
      - ENVIRONMENT (on all servers)

    Path where your <environment>.env file should be placed:
      - linux: /home/<user>/.local
      - darwin: /home/<user>/.local
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python'

    Path where your secret files should be placed:
      - linux: /home/<user>/.local/secrets
      - darwin: /home/<user>/.local/secrets
      - win32: C:\\Users\\<user>\\AppData\\Roaming\\Python\\secrets'
    """
    model_config = SettingsConfigDict(extra='ignore',
                                      secrets_dir=SECRETS_DIR,
                                      env_file_encoding='utf-8',
                                      env_file=f'{USER_BASE}/.env')

    # constant parameters.
    routingDbPort: int = 8012
    trackingDbPort: int = 8006
    mqServer: str = 'P-W-MQ01'
    apiTimeout: tuple = (9.05, 60)

    # Environment depending parameters.
    env: str = ENVIRONMENT
    platform: str = PLATFORM.get(sys.platform, 'other')

    # Secrets depending parameters.
    serviceApiKey: str = Field(MISSING_SECRET, alias='service_api_key')

    @computed_field
    @property
    def hdrData(self) -> dict:
        """ Return updated API header (added serviceApiKey secret).

        :return: Updated API header.
        """
        return {'Content-Type': 'application/json',
                'X-API-Key': f'{self.serviceApiKey}'}

    @computed_field
    @property
    def server(self) -> str:
        """ Return local server name stripped of possible domain part.

        :return: Server name in upper case.
        """
        name = ('COMPUTERNAME' if sys.platform == 'win32' else 'HOSTNAME')
        return os.getenv(name, MISSING_ENV).upper().split('.')[0]

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """ Change source priority order (env trumps environment). """
        return (init_settings, dotenv_settings,
                env_settings, file_secret_settings)


# ------------------------------------------------------------------------
#
class Dev(Common):
    """ Configuration parameters for DEV environment.

    Values from dev.env supersede previous values when the file exists.
    """
    model_config = SettingsConfigDict(env_file=f'{USER_BASE}/{Common().env}.env')

    mqServer: str = 'localhost'
    dbServer: str = 'localhost:3306'
    apiRoot: str = 'http://localhost'
    mongoUrl: str = Field(MISSING_SECRET, alias=f'mongo_url_{Common().env}')


# ------------------------------------------------------------------------
#
class Test(Common):
    """ Configuration parameters for TEST environment.

    Values from test.env supersedes previous values when the file exists.
    """
    model_config = SettingsConfigDict(env_file=f'{USER_BASE}/{Common().env}.env')

    dbServer: str = 't-l-docker01:3306'
    apiRoot: str = 'http://internal_api_test_host'
    mongoUrl: str = Field(MISSING_SECRET, alias=f'mongo_url_{Common().env}')


# ------------------------------------------------------------------------
#
class Stage(Common):
    """ Configuration parameters for STAGE environment.

     Values from stage.env supersede previous values when the file exists.
     """
    model_config = SettingsConfigDict(env_file=f'{USER_BASE}/{Common().env}.env')

    routingDbPort: int = 8013
    trackingDbPort: int = 8007
    dbServer: str = 't-l-docker01:3307'
    apiRoot: str = 'http://internal_api_stage_host'
    mongoUrl: str = Field(MISSING_SECRET, alias=f'mongo_url_{Common().env}')


# ------------------------------------------------------------------------
#
class Prod(Common):
    """ Configuration parameters for PROD environment.

    Values from prod.env supersedes previous values when the file exists.
    """
    model_config = SettingsConfigDict(env_file=f'{USER_BASE}/{Common().env}.env')

    dbServer: str = 'ocsemysqlcl:3306'
    apiRoot: str = 'http://internal_api_prod_host'
    mongoUrl: str = Field(MISSING_SECRET, alias=f'mongo_url_{Common().env}')


# ------------------------------------------------------------------------

# Translation table between ENVIRONMENT value and their classes.
_setup = dict(
    dev=Dev,
    test=Test,
    prod=Prod,
    stage=Stage
)

# Validate and instantiate specified environment configuration.
config: Union[Dev, Test, Prod, Stage] = _setup[ENVIRONMENT]()
