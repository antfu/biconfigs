# Biconfigs
[![Build Status](https://img.shields.io/travis/antfu/biconfigs.svg)](https://travis-ci.org/antfu/biconfigs)
[![Coverage](https://img.shields.io/codecov/c/github/antfu/biconfigs.svg)](https://codecov.io/gh/antfu/biconfigs)
[![License](https://img.shields.io/github/license/antfu/biconfigs.svg)](https://github.com/antfu/biconfigs/blob/master/LICENSE)

📜↔🛠 A file-object two way configures get/set helper

## Get Started
```python
>>> from biconfigs import Biconfigs
>>> configs = Biconfigs('configs.json')

# Simply change the dict, and it will automatically save the changes to file.
>>> configs['options'] = {'debug': True,
                          'username': 'Anthony',
                          'list': [] }

# Access with simple 'x.y.z' style
>>> configs.options.list.append('example')

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

## Install
```sh
pip install git+https://github.com/antfu/biconfigs.git
```

## Dependencies
Not dependencies required.

## License
MIT
