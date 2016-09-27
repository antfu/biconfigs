# BiConfigs
[![Build Status](https://img.shields.io/travis/antfu/biconfigs.svg)](https://travis-ci.org/antfu/biconfigs)
[![Coverage](https://img.shields.io/codecov/c/github/antfu/biconfigs.svg)](https://codecov.io/gh/antfu/biconfigs)

A file-object two way configures get/set helper

## Install
```sh
pip install git+https://github.com/antfu/biconfigs.git
```

## Dependencies
Not dependencies required.

## Get Started
```python
>>> from biconfigs import BiConfigs
>>> configs = BiConfigs('configs.json')
# Simply change the dict will update file "configs.json" automatically
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

## License
MIT
