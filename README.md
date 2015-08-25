![Easy does it!](http://i.imgur.com/N7uilEZ.png)

# easy-expressions [![Build Status](https://travis-ci.org/Miserlou/easy-expressions.svg)](https://travis-ci.org/Miserlou/easy-expressions)

The world's most gangsta regular expressions library.

It turns this..

```python

regex = re.compile(r'(?:(?:\$){1,1})(?:(?:(?:\d)){1,})(?:(?:\.){1,1})(?:\d)(?:\d)')
```

into this!

```python
from easy_expressions import Easy

regex = Easy() / 
  .find("$") /
  .min(1).digits() /
  .then(".") /
  .digit() /
  .digit() /
  .getRegex()

regex.findall("$10.00");
```

## About

_easy-expressions_ is a python regular expressions library with a [Python for Humans](https://speakerdeck.com/kennethreitz/python-for-humans) philosophy.

Currently in alpha. More info soon.

## Installation

    pip install easy-expressions

## Examples

```python
from easy_expressions import Easy

regex = Easy() / 
  .find("$") /
  .min(1).digits() /
  .then(".") /
  .digit() /
  .digit() /
  .getRegex()

regex.findall("$10.00");
```

More coming soon. Perhaps you'd like to contribute one?

## Inspiration

Regexes are hard when they should be easy.

I had this idea while watching Straight Outta Compton. Turns out [@thebinarysearchtree](https://github.com/thebinarysearchtree/) had already [implemented it in JS](https://github.com/thebinarysearchtree/regexpbuilderjs), so this is essentially a port of that.

## Contributing 

This software is still quite young and I'm certain there are still bugs in it. If you find bugs or want new features included, please create a new Issue and send a pull request, along with an accompanying test. Thanks!

## Other Easy Projects

If you like easy things, you may also enjoy:

  * [django-easy-api](https://github.com/Miserlou/django-easy-api)
  * [django-easy-split](https://github.com/Miserlou/django-easy-split)
  * [django-easy-timezones](https://github.com/Miserlou/django-easy-timezones)
  * [django-knockout-modeler](https://github.com/Miserlou/django-knockout-modeler)
  * [simpleaws](https://github.com/Miserlou/simpleaws)

## License

MIT, 2015.

