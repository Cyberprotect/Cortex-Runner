![](https://www.cyberprotect.fr/wp-content/uploads/2015/12/Logo-340-156-web-noir.png)

> Rémi ALLAIN <rallain@cyberprotect.fr>

# CortexRunner

Cortex jobs automation for TheHive

## Requirements

- thehive4py
- requests

## Installation

```bash
git clone 'https://github.com/Cyberprotect/CortexRunner.git'
cd CortexRunner-master
python setup.py install
```

or

```bash
pip install Cortex-Runner
```

## Usage

```python
from cortexrunner.api import CortexRunner

observable = '1234abcd1234abcd1234abcd1234abcd'
config = {
    'thehive': {
        'url': 'http://127.0.0.1:8080',
        'proxies': None,
        'cert': True,
        'key': '--API-KEY--'
    }
}
rules = {
    'file': [{
        'analyzer': 'Cuckoo_Sandbox_File_Analysis_1_0',
        'scope': 'internal'
    },{
        'analyzer': 'VirusTotal_Report_2_0',
        'scope': 'external'
    }],
    'filename': [{
        'analyzer': 'MISP_2_0',
        'scope': 'internal'
    },{
        'analyzer': 'HybridAnalysis_GetReport_1_0',
        'scope': 'external'
    }],
    'url': [{
        'analyzer': 'Threatcrowd_1_0',
        'scope': 'external'
    }]
}

runner = CortexRunner(observable, rules, config)

result = runner.launch()

print(result)
```

For a more complete and real example, get a look at `example/` directory