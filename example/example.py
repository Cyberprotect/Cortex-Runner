#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cortexrunner.api import CortexRunner
import yaml, json

# function to dump yaml file in a dict
def file_get_yaml(filename):
    with open(filename) as f:
        return yaml.safe_load(f)

# get the config
config = file_get_yaml('./config.yaml')

# get the rules
rules = file_get_yaml('./rules.yaml')

# set the observable id
observable = "1234abcd1234abcd1234abcd1234abcd"

# instanciate the runner
runner = CortexRunner(observable, rules, config)

# create the jobs
result = runner.launch()

# output jobs information
print(json.dumps(result, indent=4))
