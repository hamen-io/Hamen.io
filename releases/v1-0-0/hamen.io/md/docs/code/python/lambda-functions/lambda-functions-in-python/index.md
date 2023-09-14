<doc style="display: none;">
    title: Lambda Functions in Python
    titleID: lambda-functions-in-python
    description: In this article, you will learn about lambda functions/expressions in Python, what they are, their history, and how you can use them
    type: Blog
    tags: Python,Lambda functions,Serverless,AWS Lambda,Function as a Service,Event-driven programming,Cloud computing,Microservices,Serverless architecture,Event processing,Serverless computing,AWS,Python programming,AWS services,Serverless development,Event-driven architecture,Serverless Python,Event handlers,Function deployment,Scalable applications,Serverless deployment,Serverless frameworks,Serverless best practices,AWS cloud,AWS Lambda triggers,AWS Lambda functions,Python scripting,AWS Lambda event sources,Event-driven design,Serverless patterns,Serverless security,AWS serverless architecture,AWS serverless development,Serverless advantages,Serverless challenges,AWS Lambda use cases,AWS Lambda tutorial,Serverless cost optimization,AWS Lambda scalability,AWS Lambda performance,AWS Lambda benefits,AWS Lambda setup,AWS Lambda ecosystem,AWS Lambda automation,AWS Lambda integration,AWS Lambda examples
    author: Daniel Hamen
    authorID: danielhamen
    date: 2023-08-14
    url: blogs/code/python/lambda-functions/lambda-functions-in-python
    category: Code,Python,Lambda Functions
    categorySlug: code,python,lambda-functions
</doc>

# Lambda-Functions in Python

## Introduction

Lambda functions, also known as anonymous functions, are a powerful and concise way to define small, throwaway functions in Python. These functions can be extremely handy when you need a quick function without the formality of a complete function definition. In this article, we'll dive into what lambda functions are, why they're useful, and how to use them effectively.

## Introduction to Lambda Functions

A lambda function is a small, unnamed function in Python that can have any number of arguments but can only have a single expression. It is defined using the lambda keyword, makinglambda arguments: expression it a quick and convenient way to create on-the-fly functions for specific tasks.

## Syntax of Lambda Functions

The basic syntax of a lambda function is as follows:

```python:syntax
lambda arguments: expression
```

Lambda functions consist of three main components:

* The `lambda` keyword
* A list of arguments (similar to a function's parameter list)
* A single expression that gets executed when the lambda function is called

## Using Lambda Functions

### Simple Lambda Functions

Let's start with a simple example. Suppose you want a function to calculate the square of a number. Instead of defining a separate function, you can use a lambda function like this:

```python
square = lambda x: x ** 2

print(square(5))  # Output: 25
```

This example is the exact same as doing the following; just in a condensed, and shorter&mdash;lambda&mdash; notation:

```python
def square(x):
    return x ** 2

print(square(5)) # Output: 25
```

### Lambda Functions with Built-in Functions

Lambda functions are often used in conjunction with built-in functions like `map()`, `filter()`, and `reduce()`. Here's an example using `map()` to double a list of numbers:

```python
numbers = [1, 2, 3, 4, 5]
doubled_numbers = list(map(lambda x: x * 2, numbers))
print(doubled_numbers)  # Output: [2, 4, 6, 8, 10]
```

If you are unfamiliar with the `map`, `filter`, or `reduce` function in Python, check out our other blogs!

- [Tutorial to Python's `map` Function]("https://www.hamen.io/...")
- [Tutorial to Python's `filter` Function]("https://www.hamen.io/...")
- [Tutorial to Python's `reduce` Function]("https://www.hamen.io/...")

Nevertheless, the function-equivalent of the lambda-function above is as follows:

```python
def double_number(x):
    return x * 2

numbers = [1, 2, 3, 4, 5]
doubled_numbers = list(map(double_number))
print(doubled_number)  # Output: [2, 4, 6, 8, 10]
```

Or to simplify this even further, in case you are not familiar with the `map` function, you can achieve the same results in a for-loop:

```python
def double_number(x):
    return x * 2

numbers = [1, 2, 3, 4, 5]
for i,number in enumerate(numbers):
    numbers[i] = double_number(number)
print(numbers)  # Output: [2, 4, 6, 8, 10]
```

Note that in this example, we modified the original list, instead of creating a new one

### Lambda Functions in Sorting

Lambda functions are handy for sorting lists of complex objects based on specific attributes. Let's say you have a list of tuples representing people's names and ages, and you want to sort them by age:

```python
people = [('Alice', 30), ('Bob', 25), ('Charlie', 40)]
people.sort(key=lambda person: person[1])
print(people)  
# Output: [('Bob', 25), ('Alice', 30), ('Charlie', 40)]
```

## Limitations of Lambda Functions

While lambda functions are convenient for simple tasks, they have limitations. They can only contain a single expression, which means complex logic isn't suitable for lambda functions. In such cases, it's better to use regular named functions.

## Conclusion

Lambda functions are a valuable tool in Python's toolbox, providing a concise way to create small, disposable functions. They're particularly useful when you need a quick function for a specific purpose without writing a full function definition. By understanding the syntax and examples provided in this guide, you can start using lambda functions effectively in your Python code.

## Related Articles

If you enjoyed this article, here are some other articles similar to this one:

- [Tutorial to Python's `map` Function]("https://www.hamen.io/...")
- [Tutorial to Python's `filter` Function]("https://www.hamen.io/...")
- [Tutorial to Python's `reduce` Function]("https://www.hamen.io/...")
- [Tutorial to Python's `sort` Function]("https://www.hamen.io/...")
- [Types of Arrays in Python]("https://www.hamen.io/docs/blogs/code/python/data-types/arrays/types-of-arrays-in-python/")

Finally, we recommend checking out our *free* [Python Course]("https://www.hamen.io/...") if you want to learn more about this great language!