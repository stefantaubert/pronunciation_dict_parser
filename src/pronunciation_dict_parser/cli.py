import argparse
import logging
from argparse import ArgumentParser
from logging import INFO, getLogger
from typing import Callable, Dict, Generator, Tuple

__version__ = "0.0.1"

INVOKE_HANDLER_VAR = "invoke_handler"


def formatter(prog):
  return argparse.ArgumentDefaultsHelpFormatter(prog, max_help_position=40)


def _init_parser():
  main_parser = ArgumentParser(
    formatter_class=formatter,
    description="This program handles pronunciation dictionaries.",
  )

  main_parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
  subparsers = main_parser.add_subparsers(help="description")
  methods = (
    ("download", "download a public pronunciation dictionary", None),
  )

  for command, description, method in methods:
    method_parser = subparsers.add_parser(
      command, help=description, formatter_class=formatter)
    method_parser.set_defaults(**{
      INVOKE_HANDLER_VAR: method(method_parser),
    })

  return main_parser


def main():
  parser = _init_parser()
  received_args = parser.parse_args()
  params = vars(received_args)

  if INVOKE_HANDLER_VAR in params:
    invoke_handler: Callable = params.pop(INVOKE_HANDLER_VAR)
    invoke_handler(**params)
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
