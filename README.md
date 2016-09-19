# Bilateral-Configs.py
A file-object two way configures get/set helper

## Get Started
```python
>>> from bcfg import BilateralConfigs
>>> configs = BilateralConfigs('configs.json')
# This statement will update file "configs.json" as well
>>> configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

>>> configs['options']['list'].append('example')

>>> with open('configs.json','r') as f:
...     print(f.read())

{
  "options": {
    "debug": true,
    "list": [
      "example"
    ],
    "username": "Anthony"
  }
}
```
