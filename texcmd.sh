#!/bin/sh

DIRNAME=$(dirname "$0")

python -c \
'import importlib; \
path="'$DIRNAME'/scripts/utils.py"; \
spec = importlib.util.spec_from_file_location("module.name", path); \
util = importlib.util.module_from_spec(spec); \
spec.loader.exec_module(util); \
util.run_cmd("'$1'");'
