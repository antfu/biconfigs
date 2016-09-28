# Biconfigs
[![Build Status](https://img.shields.io/travis/antfu/biconfigs.svg?style=flat-square)](https://travis-ci.org/antfu/biconfigs)
[![Coverage](https://img.shields.io/codecov/c/github/antfu/biconfigs.svg?style=flat-square)](https://codecov.io/gh/antfu/biconfigs)
[![License](https://img.shields.io/github/license/antfu/biconfigs.svg?style=flat-square)](https://github.com/antfu/biconfigs/blob/master/LICENSE)

📜⇄🛠 Two way configurations mapping helper for Python.

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

## Doc
### High frequency update
Normally, Biconfigs will write the changes to file immediately. But sometime you
will need to update values frequently, which will result in IO bottleneck. So you
can use `with` statement to prevent auto saving for a while.
```python
with configs:
  for i in range(1000):
    configs['some_key'] = i
# This statement will fire saving process only when exiting "with" scope
```

## License
MIT
