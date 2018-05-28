#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = "Rémi ALLAIN"
__copyright__ = "Copyright 2018, Cyberprotect - SDN International"
__credits__ = ["Rémi ALLAIN"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Rémi ALLAIN"
__email__   = "rallain@cyberprotect.fr"
__status__  = "Production"

import json, requests
from thehive4py.api import TheHiveApi, BearerAuth

"""Cortex jobs automation for TheHive."""
class CortexRunner:

    """String: Observable Id""" 
    observable_id = None

    """Dict: Observable information"""
    observable = None
    
    """Dict: Rules"""
    rules = None

    """Dict: Configuration"""
    config = None

    """Object: TheHiveApi"""
    thehive4py = None

    """List of dict: jobs created"""
    jobs = None

    def __init__(self, observable_id, rules, config):
        """Cortex jobs automation for TheHive."""
        # Register the configuration
        self.set_config(config)
        # Check the observable id and retrieve information
        self.set_observable_id(observable_id)
        # Register the rules
        self.set_rules(rules)
        # Instanciate thehive4py
        self.thehive4py = TheHiveApi(self.config['thehive']['url'], self.config['thehive']['key'], proxies=self.proxies, cert=self.cert)
        
    def set_observable_id(self, observable_id):
        """Store the observable Id only if length is correct (32) and retrieve the information about the observable."""
        # Check length
        if(len(observable_id) != 32):
            raise CortexRunnerException('Observable Id seems to be invalid. Not a 32 character Id.')
        # Store Id
        self.observable_id = observable_id
        # Retrieve information
        self.get_observable_data()

    def set_rules(self, rules):
        """Store the rules."""
        self.rules = rules
        # Check structure
        if not isinstance(rules, dict):
            raise CortexRunnerException('"rules" parameter is not a dictionnary.')
        for key in rules:
            if not isinstance(key, basestring):
                raise CortexRunnerException('dataType in rules must be a string. Invalid value = {}'.format(key))
            for rule in rules[key]:
                if not rule.get('analyzer'):
                    raise CortexRunnerException('rule for {} must contain an "analyzer" key-value.'.format(key))

    def set_config(self, config):
        """Store the configuration"""
        # Check the structure
        if config.get('thehive') and config['thehive'].get('url') and config['thehive'].get('key'):
            # Store configuration items
            self.config = config
            self.proxies = config['thehive'].get('proxies')
            self.auth = BearerAuth(self.config['thehive'].get('key'))
            self.cert = config['thehive'].get('cert')
        else:
            raise CortexRunnerException('Configuration not valid. The configuration dictionnary must have at least the keys : "thehive.url" and "thehive.key"')

    def launch(self):
        """Create jobs based on dataType rules for the selected observable"""
        # Reset the created job list
        self.jobs = []
        # Get the rules for the dataType of the current observable
        if self.rules.get(self.observable.get('dataType')):
            for rule in self.rules.get(self.observable.get('dataType')):
                # Create job for each analyzer
                job = self.launch_job(rule.get('analyzer'))
                # Report the response and the matching rule into the list
                self.jobs += [{
                    "rule": rule,
                    "job": job
                }]
        return self.jobs

    def launch_job(self, analyzer_id):
        """Create job for the observable id and the given analyzer id"""
        # Send request
        response = self.thehive4py.run_analyzer(None, self.observable_id, analyzer_id)
        # If job was created report information about it
        if(response.status_code == 200):
            return response.json()
        return {}

    def get_observable_data(self):
        """Get the observable information"""
        # Build url
        req = "{}/api/case/artifact/{}".format(self.config['thehive']['url'], self.observable_id)
        try:
            # Send request
            response = requests.get(req, proxies=self.proxies, auth=self.auth, verify=self.cert)
            if response.status_code == 200:
                # Store the data
                self.observable = response.json()
            else: 
                raise CortexRunnerException('Unable to get the observable : {}'.format(response.text))
        except requests.exceptions.RequestException as e:
            raise CortexRunnerException('Unable to get the observable : {}'.format(e))

class CortexRunnerException(Exception):
    pass