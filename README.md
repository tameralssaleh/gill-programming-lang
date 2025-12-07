# General Interpreted Language (GIL)

**GIL** is a lightweight, fast, general-purpose object-oriented programming language.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started) (N/A)
- [Other Useful Information](#other-useful-information)
- [Syntax Examples](#syntax-examples)

---

## Overview
General Interpreted Language (GIL) focuses on:

- **Lightweight**: Minimal runtime and fast interpretation.
- **Speed**: Designed to be fast
- **OOP**: Supports general-purpose object-oriented programming.
- **Readability**: Clean and understandable syntax that is similar enough to other languages
---

## Features
- Built-in REPL
- Object-oriented design.
- Simple, familiar syntax for rapid development.
- Simple, human-readable and understandable syntax for complete beginners.
- Cross-platform support.
---

## Other Useful Information

- GIL currently uses an interpreter built in Python 3.13 & above. There are plans to build the interpreter in C/C++, this Python implementation is not planned to stay for a long time and is solely used to build GIL as a prototype.

---

## Syntax Examples

1) The following GIL code defines two variables `x` and `y`, displays results of these two numbers when mathematical operations are performed on them.

```GIL
define x int 10 ; integer value of 10
define y int 5 ; integer value of 5

out x + y ; displays 15
out x - y ; displays 5
out x / y ; displays 2.0
```

2) The following GIL code defines an integer variable `x` as 0, then reassigns `x` the same value but incremented in a while loop after displaying the current value. The code will then output "done" once `x` reaches 3.

```GIL
define x int 0

while (x < 3) {
    out x
    assign x x + 1
}

if (x == 3) {
    out "done"
} else {
    out "error"
}
```

3) The following GIL code defines integer values `x` and `y` as 9 and 3, then performs increments and decrements using their respective operators. This is the same as writing `assign x x + 1` or `assign y y - 1`.

```GIL
define x int 9
x++
out x ; should display '10'

define y int 3
y--
out y ; should display '2'
```

4) The following GIL code defines two floats and one integer, `pi`, `r`, and `d`. `pi`'s value is the mathematical constant `pi`. `r` = `pi`/2, and `d`'s value is an integer cast of `r` * 180/`pi`. Then these values are casted as strings in the final output.

```GIL
define pi float 3.14159265 ; pi
define r float pi/2 ; pi/2 radians
define d int (int)(r*(180/pi)) ; convert radians to degrees

out (string)r + " radians = " + (string)d + " degrees."
```

5) The following GIL code defines an integer `age` and a string `name`, `age` is then casted as a string while being concatenated in the final output.

```GIL
define age int = 20
define name string "John"

out "Hello, World! My name is " + name + " and I am " + (string)age + " years old."
```

6) The following GIL code simply evaluates if and else statements.

```GIL
if (4 >= 2) {
    out "HURRAY!"
} else {
    out ":("
}

if (4 == 4.0) {
    out "Hey look, you can compare numbers of different types!"
} else {
    out "Nevermind..."
}
```

7) The following GIL code creates a new function with parameters `x` and `y` both being integers.

```GIL
function int add_numbers(int x, int y) {
    return x + y
}
```

8) The following GIL code creates a new function with parameters `x` and `y` both being integers just like in snippet 7, however, this time we allow parameters to default to a specified value in case they are not passed when the function is called..

```GIL
; <type> <parameter> default <value>
function int add_numbers(int x default 0, int y default 0) {
    return x + y
}
```

9) The following GIL code executes `add_numbers(x, y)`. Note that `exec` means execute, and is meant to be used to call functions and methods.

```GIL
exec add_numbers(3, 4)
```

10) The following GIL code creates a new array with type enforcement. An array of 3 integer elements is created by defining `x[3]` meaning integer array of 3. Note that size does not have to be specified and can be determined before runtime. However, size cannot be changed after it is declared and elements are populated into it. If you need to use a collection with a dynamic size, consider using a `List<T>`.

```GIL
define x[3] int [1, 2, 3]
define y[] int [4, 5, 6, 7, 8, 9]
```

11) The following GIL code creates a new array with type enforcement of 3 integers, and then loops through the array with a `foreach` loop to display each element of `x`.
```GIL
define x[3] int [1, 2, 3]
foreach (define num int : x) {
    out x
}
```

12) The following GIL code does the same thing as #11, however this time we are working with nested loops, meaning that we can see some pretty cool mathematical results when adding two elements from two different lists during iteration.
```GIL
define x[5] int [1, 2, 3, 4, 5]
define y[5] int [5, 4, 3, 2, 1]

foreach (define num1 int : x) {
    foreach (define num2 int : y) {
        out num1 + num2
    }
}
```

13) The following GIL code creates a simple for loop, not bound to an array or any other collection. This basically works the same way as a traditional while loop.
```GIL
for (define i int 0, i < 10, i++) {
    out i
}
```

14) The following GIL code creates a simple array and outputs an element from the array by index addressing.
```GIL
define x[] int [1, 2, 3]
out x[2] ; Displays 3 in output
```

15) The following GIL code creates a simple array and then utilizes the try-catch-finally blocks to execute code based on if there were an error or not. The try block will attempt to execute the code within it, if the code executes without an error, then it will terminate and execute the finally block. If there is an error within the try block, then the catch block will execute instead, then lastly it will execute the finally block. The finally block is completely optional, and is there if you want to execute code no matter if an error occurred within the try block.
```GIL
define x[3] int [1, 2, 3]

try {
    out x[5] ; This line will not work as the index is out of range, thus will execute the catch block. 
} catch {
    out "Error"
} finally {
    out "Code finished." ; this will execute no matter if there is an error or if the try block executed without an error.
}
```
