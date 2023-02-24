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
import argparse
from enum import Enum
from pprint import pprint


# ---------------------------------------------------------
#
class Environment(str, Enum):
    """ Defines available environment platforms. """
    dev = 'dev'
    test = 'test'
    prod = 'prod'
    stage = 'stage'

    def __str__(self):
        return self.value


# ---------------------------------------------------------

if __name__ == "__main__":

    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script to test the configurator.py file with different environments.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument('environment', type=Environment, choices=list(Environment),
                        help="Specify ENVIRONMENT to use")
    args = parser.parse_args()

    # To be able to test different environments we need
    # to set this BEFORE we import the config module.
    os.environ['ENVIRONMENT'] = args.environment

    from configurator import config

    pprint(config.dict())
