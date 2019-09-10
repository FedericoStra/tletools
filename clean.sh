#!/bin/bash

rm -r .pytest_cache/ TLE_tools.egg-info/ build/ docs/_build
find . -name __pycache__ -exec rm -r {} +
