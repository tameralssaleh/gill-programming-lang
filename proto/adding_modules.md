# Adding Your Own Modules/Libraries
This document describes how you can add your own modules/libraries to the prototype system. The prototype is designed to be extensible, allowing you to easily integrate additional functionality as needed.
## Steps to Add a Module/Library
Simply create a new file under the `/proto/src/packages` directory. Here we have GILL's very own Standard Library (stdlib) which contains a small collection of useful functions and utilities that can be used in GILL programs. You can create your own module/library by following the same structure and conventions as the stdlib.
### Step 1: Creating The Python File
- The prototyped version of GILL uses Python for its implementation of native prepackaged modules. In the future, we would of course use C, which is the intended language for the final product of this language. 
- In the future, we will add more precise structure to this system to ensure better organization and maintainability. 
- When GILL supports OOP, you will be able to define classes and other constructs as well. 
- GILL is also planned to have a more defined system in place where we can have multiple modules be part of the same library or package.
- For now, you can only just create a Python file and define functions and variables.
### Step 2: Defining Functions and Variables
- You can define functions and variables in your Python file as you normally would. These will be accessible in GILL programs that import your module/library.
### Step 3: Creating a Module Environment (ModuleEnv) Object
- To make your module/library available in GILL, you need to create an instance of the `ModuleEnv` class. This object will hold the functions and variables you defined in your Python file and make them accessible to GILL programs. The GILL interpreter automatically looks for this.
- NOTE: you __must__ name this object `module_env` for the interpreter to recognize it.
### Step 4: Registering Your Module/Library
- Once you have created the `ModuleEnv` object, you need to register each function and variable you defined in your Python file with the `ModuleEnv` instance. This typically involves adding them to the `functions` and `variables` dictionaries of the `ModuleEnv` object. Please see `/src/packages/stdlib.py` for an example of how to do this.
### Step 5: Importing Your Module/Library in GILL Programs
- After you have registered your module/library, you can import it in your GILL programs using the `import` statement. For example, if you created a module called `my_module`, you would import it in a GILL program like this:
```GILL
import my_module
// Now you can use the functions and variables defined in your module/library
exec my_module::my_function(args)
```
## Conclusion
Adding your own modules/libraries to the GILL prototype system is a straightforward process that allows you to extend the functionality of the language. By following the steps outlined above, you can create and integrate your own modules/libraries into GILL programs, enhancing the capabilities of the language and enabling you to tailor it to your specific needs.

Congratulations on taking the initiative to expand the GILL ecosystem! Your contributions will help shape the future of this language and make it more versatile for everyone. 

Please consider submitting your module/library to the GILL repository if you think it would be beneficial for the community. We welcome contributions and are always looking for ways to improve the language and its ecosystem.