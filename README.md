![Easy does it!](http://i.imgur.com/N7uilEZ.png)

# easy-expressions 

The world's most gangsta regular expressions library.

## About

_easy-expressions_ is a python regular expressions library with a 'python for humans' philsophy.

Currently in early alpha. More info soon.

## Installation

    pip install easy-expressions

## Examples

```python
from easy_expressions import Easy

regex = Easy 
  .find("$")
  .min(1).digits()
  .then(".")
  .digit()
  .digit()
  .getRegex();

regex.findall("$10.00");
```

## Inspiration

Regexes are hard when they should be easy.

I had this idea while watching Straight Outta Compton. Turns out [@thebinarysearchtree](https://github.com/thebinarysearchtree/) had already [implemented it in JS](https://github.com/thebinarysearchtree/regexpbuilderjs), so this is essentially a port of that.

## License

MIT, 2015.

