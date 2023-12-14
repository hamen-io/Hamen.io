# Style Guide for Hamen.io/docs

## Configuration files

Configuration files ( ending in `.config` ) provide additional relative details for something; they should follow an exact syntax and be parsed with the `HamenAPI.Configuration` API

### Features

The `HamenAPI.Configuration` API supports ;

* Comments (denoted with "//" or "/* ... */")
* Many data types
* Doc-Strings

#### Comments

There are two types of comments;

* Block comments ( denoted with `/* ... */` )
* Line comments ( denoted with `//` )

For example;
```
// My 
MY_KEY = false;
```

#### Doc-Strings

Doc-strings describe a certain key; although you can describe them with a single comment, doc-strings are registered to the actual item

You can define a doc-string as shown below:

```````
KEY = VALUE;
```
Doc Strings; provides additional information about the given declaration;

You can also provide type suggestions for the value:
@type $KEY : string
@type $VALUE : string
```
```````

They are then accessible through the `HamenAPI.Configuration` API through `HamenAPI.Configuration.Declaration(...).docString`; `docString` is a property and will return `str` or `None` ( `None` if it has not been defined )

#### Configuration declarations

Declarations refer to a key-to-value declaration; the syntax is as follows

```
KEY = VALUE;
```

A few things to note:

* **`KEY` should be uppercase and spaces should become commas (DO NOT CONCATENATE WORDS WITHOUT AN UNDERSCORE INDICATING WORD-SEPARATION WHITESPACE; ALSO, DO NOT REPEAT ONE OR MORE UNDERSCORE: YOU SHOULD FOLLOW THIS VALUE-SUB-PATTERN: `/[ ]+/g -> /_/`)**;

* `VALUE` supports the following types:

    * `int`: Integers (just simply write the number!)
    * `float`: Floating-point numbers; works the same way as `int`
    * `string`: Strings; denoted with either `"` or `'`
    * `boolean`: Booleans; defined with the case-sensitive symbols: `true` or `false`
    * `null`: NullType; defined with the case-sensitive symbol: `null`

* Whitespace: whitespace before or after the equal sign does not matter&mdash;it will be parsed the same; however, it is requested that you provide one space before and after the equal sign for consistency and readability

* Line-terminator delimiter: semi-colons are not necessary; you can define a line break with a newline too; however, we strongly recommend a semi-colon for consistency and readability

    * Additionally, line-terminating-semi-colons can also prevent issues when building as sometimes `.config` files are minified making each newline line inline