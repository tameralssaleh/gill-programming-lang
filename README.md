# General Interpreted Language (GIL)

**HawkScript** is a lightweight, fast, general-purpose object-oriented programming language.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started) (N/A)
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
- Simple and familiar syntax for rapid development.
- Cross-platform support.
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