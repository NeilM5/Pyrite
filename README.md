# Pyrite
A toy programming language made in Python.

## How to Run
Open and run run.py.

You can run single line codes within the run.py's REPL or type `run script_name.pyr` to run Pyrite code from a text file. 

**Make sure text file has .pyr extension**

## Syntax
### Built-In Functions
- `exec("hello world")`
  - prints hello world
- `input("something")`
- `return(something)`
- `type(var`
- `str("")`
- `int(10)`
- `bool(true)`
- `flt(1.1)`
- `abs(-1)`
- `pow(x, y)`
  
### Variables
Variables are assigned using `var`. Example: `var x = 10`.

Variables in Pyrite are dynamic meaning value determines the variable type. Pyrite supports booleans `true or false`, integers, floats, strings `'' or ""`, lists `[]`, and even null types.

Variables cannot be simply changed by name itself and must use the keyword `over`. Example: `over x = 20` is correct while `x = 20` will return an error.

Using the `con` keyword instead of `var` defines a constant. using `over` for them will return an error.

### Loops
#### While Loop
```
while condition
{
  body
}
```
#### For Loop
```
for initialize as condition do update
{
  body
}
```

Example:
```
for var i = 0 as i < 10 do i++
{
  exec(i)
}
```

### Functions
Functions are defined using `func` keyword with parameters and curly braces `{}`.

Example: 

```
func myFunction(x, y) 
{
  return(x + y)
}
```

Note: Making parameters does not require `var` keyword, but changing the value of these parameters requires the `over` keyword.
