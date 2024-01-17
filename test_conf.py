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
import json
import argparse

# Third party modules
import colorama


# ---------------------------------------------------------
#
def _display_status(env: str, secret: str, json_dump: str) -> str:
    """ Show valid parameters in green and missing values in RED.

    :param json_dump: The config object as a json string.
    """
    lines = []
    color = {env: f'{colorama.Fore.RED}{env}{colorama.Fore.GREEN}',
             secret: f'{colorama.Fore.RED}{secret}{colorama.Fore.GREEN}'}

    for row in json_dump.split('\n'):
        lines.append(
            (
                f'{colorama.Fore.GREEN}{row}{colorama.Style.NORMAL}'
                .replace(secret, color[secret])
                .replace(env, color[env])
            ))

    return '\n'.join(lines)


# ---------------------------------------------------------
#
def run():
    """ A utility script to test the configuration with different environments.

    Usage: verify_config [-h] [{dev,test,prod,stage}]

    If no environment is given, the defined operating system environment
    variable "ENVIRONMENT" will be used.

    A check that it's defined in the operating system is also done.
    """
    form = argparse.ArgumentDefaultsHelpFormatter
    description = (
        'A utility script to test the configurator with different '
        'environments. Default value is current the ENVIRONMENT.')
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=form)
    parser.add_argument(dest='environment', nargs='?',
                        help="Specify environment to use",
                        choices=['dev', 'test', 'prod', 'stage'])
    args = parser.parse_args()

    # Make sure an environment is already defined.
    if not os.getenv('ENVIRONMENT'):
        print("ERROR: Environment variable 'ENVIRONMENT' "
              "is not defined for this user!")
        sys.exit(1)

    # To be able to test different environments, we need
    # to set this BEFORE we import the config module.
    if args.environment:
        os.environ['ENVIRONMENT'] = args.environment

    from configurator import config
    from configurator import MISSING_ENV
    from configurator import MISSING_SECRET

    # Show valid values in green and missing values in RED.
    print(_display_status(
        MISSING_ENV, MISSING_SECRET,
        json.dumps(indent=4, sort_keys=True,
                   obj=config.model_dump())))


# ---------------------------------------------------------

if __name__ == "__main__":
    run()
