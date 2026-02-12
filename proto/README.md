# GILL Prototype (Python Interpreter)

This directory contains the **prototype implementation** of the GILL interpreter written in Python. It exists to validate language design decisions, runtime behavior, and core execution semantics before a production implementation is developed.

## Purpose

The Python version is intended for:

* Rapid experimentation with language features
* Testing syntax and parsing decisions
* Prototyping the runtime model (env, modules, native functions, etc.)
* Validating stdlib design
* Debugging interpreter semantics

It is **not** intended to be:

* A final implementation
* Performance-optimized
* Used in production environments

## Scope of the Prototype

This prototype currently includes:

* Lexer and parser
* AST node system
* Environment model (variables, functions, modules)
* Module loading (Python-backed native modules)
* Scope resolution (`::`)
* Function execution (user-defined + native)
* Early stdlib experimentation

Some areas are intentionally incomplete or unstable as language design evolves.

## Performance Expectations

Because this version is implemented in Python:

* Execution speed is not representative of the final interpreter
* Module loading and runtime dispatch are intentionally simple
* Optimization has not been a priority

Performance work will happen in the production implementation.

## Contributing / Exploration

This directory is meant for:

* exploring language mechanics
* reviewing interpreter structure
* experimenting with features

Feel free to:

* modify existing code
* add new features
* test different language behaviors
* create forks of this repository
* submit issues
* propose changes

If something looks unfinished, unstable, or inconsistent, that is expected at this stage.

## Long-Term Direction

The Python prototype serves as a reference model. Once the language design stabilizes:

* a new interpreter/runtime will be implemented
* performance, memory model, and architecture will be reconsidered
* stdlib and all other prepackaged components will be formalized

Until then, `/proto` is the authoritative sandbox for GILL language experimentation.

## Running The Prototype

cd proto/src
python main.py
