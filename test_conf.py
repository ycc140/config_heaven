# -*- coding: utf-8 -*-
"""
Copyright: Wilde Consulting
  License: Apache 2.0

VERSION INFO::
    $Repo: config_heaven
  $Author: Anders Wiklund
    $Date: 2023-07-14 22:54:46
     $Rev: 1
"""

# BUILTIN modules
import os
import argparse
from pprint import pprint


# ---------------------------------------------------------

if __name__ == "__main__":

    Form = argparse.ArgumentDefaultsHelpFormatter
    description = 'A utility script to test the configurator.py file with different environments.'
    parser = argparse.ArgumentParser(description=description, formatter_class=Form)
    parser.add_argument('environment', type=str, choices=['dev','test','prod','stage'],
                        help="Specify ENVIRONMENT to use")
    args = parser.parse_args()

    # To be able to test different environments we need
    # to set this BEFORE we import the config module.
    os.environ['ENVIRONMENT'] = args.environment

    from configurator import config

    pprint(config.model_dump())
