# Easy

## Really, really easy regular expressions.

## Examples

regex = easy 
  .find("$")
  .min(1).digits()
  .then(".")
  .digit()
  .digit()
  .getRegExp();

regex.test("$10.00"); // true

## Inspiration

https://github.com/thebinarysearchtree/regexpbuilderjs
