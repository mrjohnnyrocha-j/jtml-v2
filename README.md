# JTML Compiler and Interpreter

JTML is a domain-specific language designed for integrating markup-like syntax with powerful scripting capabilities. It excels as both a general-purpose language—with features like strong typing, classes, modules, concurrency, and cryptography—and as a web development scripting language, enabling the generation of HTML elements, interaction with databases, and dynamic user interfaces.

Every statement in JTML ends with a backslash (`\\`). Blocks conclude with a standalone backslash line. This uniform approach simplifies parsing and ensures a visually distinctive code structure.

## Table of Contents

1. [Introduction to JTML](#1-introduction-to-jtml)
2. [Getting Started](#2-getting-started)
   - [2.1. Installation](#21-installation)
   - [2.2. Hello World Example](#22-hello-world-example)
3. [Language Fundamentals](#3-language-fundamentals)
   - [3.1. Lexical Conventions](#31-lexical-conventions)
   - [3.2. Syntax Overview](#32-syntax-overview)
   - [3.3. Data Types](#33-data-types)
   - [3.4. Variables and Constants](#34-variables-and-constants)
   - [3.5. Operators](#35-operators)
   - [3.6. Expressions and Statements](#36-expressions-and-statements)
4. [Control Flow](#4-control-flow)
   - [4.1. Conditional Statements](#41-conditional-statements)
   - [4.2. Loops](#42-loops)
   - [4.3. Jump Statements](#43-jump-statements)
5. [Functions](#5-functions)
   - [5.1. Function Definitions](#51-function-definitions)
   - [5.2. Function Calls](#52-function-calls)
   - [5.3. Recursion](#53-recursion)
6. [Data Structures](#6-data-structures)
   - [6.1. Arrays and Lists](#61-arrays-and-lists)
   - [6.2. Dictionaries](#62-dictionaries)
7. [Classes and Objects](#7-classes-and-objects)
   - [7.1. Class Definitions](#71-class-definitions)
   - [7.2. Object Creation](#72-object-creation)
   - [7.3. Inheritance](#73-inheritance)
8. [JTML Elements](#8-jtml-elements)
   - [8.1. Element Syntax](#81-element-syntax)
   - [8.2. Attributes and Properties](#82-attributes-and-properties)
   - [8.3. Dynamic Content](#83-dynamic-content)
9. [Advanced Features](#9-advanced-features)
   - [9.1. Database Interactions](#91-database-interactions)
   - [9.2. Quantum Computing Simulation](#92-quantum-computing-simulation)
   - [9.3. Cryptography Operations](#93-cryptography-operations)
10. [Error Handling](#10-error-handling)
11. [Modules and Packages](#11-modules-and-packages)
12. [Input/Output Operations](#12-inputoutput-operations)
13. [Multithreading and Concurrency](#13-multithreading-and-concurrency)
14. [Annotations and Decorators](#14-annotations-and-decorators)
15. [Best Practices](#15-best-practices)
16. [Glossary](#16-glossary)
17. [References](#17-references)

---

## 1. Introduction to JTML

JTML integrates markup-like syntax with powerful scripting capabilities. It serves dual purposes:

- **General-Purpose Language**: Offers strong typing, classes, modules, concurrency, and cryptography, making it suitable for a wide range of applications.
- **Web Development Scripting Language**: Facilitates the generation of HTML elements, interaction with databases, and creation of dynamic user interfaces through a concise and expressive syntax.

**Key Characteristics:**

- **Uniform Statement Termination**: Every statement ends with a backslash (`\\`). Blocks conclude with a standalone backslash line. This consistent structure simplifies parsing and enhances code readability.
- **Visual Distinction**: The use of backslashes ensures that code blocks are visually distinct, aiding in maintaining and navigating complex codebases.

---

## 2. Getting Started

### 2.1. Installation

To get started with JTML, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/jtml_compiler.git
   cd jtml_compiler
   ```
Install Dependencies:

Ensure you have Python 3.7 or higher installed. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
Verify Installation:

Check the installed version of JTML:

```bash
jtml --version
```

Expected Output:

```mathematica
JTML Compiler and Interpreter Version 0.1.0
```

2.2. Hello World Example
Create a simple JTML program to display "Hello, World!" in a paragraph element.

Create a File:

Create a file named hello_world.jtml with the following content:

```jtml
#p "Hello, World!" #p\\
\\
```
Run the Program:

Execute the JTML program using the interpreter:

```bash
jtml run hello_world.jtml
```

Output:

```html
<p>Hello, World!</p>
```

This output demonstrates JTML's ability to generate HTML elements seamlessly.

## 3. Language Fundamentals
Understanding the core aspects of JTML is essential for effective programming. This section covers the basic building blocks of the language.

### 3.1. Lexical Conventions
Identifiers:

Composed of letters (a-z, A-Z), digits (0-9), and underscores (_).
Must not start with a digit.
Case-sensitive.
Strings:

Enclosed in double quotes (").
Support escape sequences, such as \n for newline and \" for double quotes within strings.
Comments:

Single-Line Comments: Begin with // and continue until the end of the line.

```jtml
// This is a single-line comment
```

Multi-Line Comments: Enclosed within /* and */.

```jtml
/*
  This is a multi-line comment.
  It spans multiple lines.
*/
```

Keywords:

All keywords are in lowercase.
Examples include define, const, function, class, if, else, while, for, return, try, catch, finally, throw, etc.
### 3.2. Syntax Overview
JTML emphasizes a clean and visually distinct syntax by enforcing consistent statement termination and block delineation.

Statement Termination: Every statement ends with a backslash (\\).

```jtml
define x = 10\\
show x\\
```

Block Delineation: Blocks (such as those following control structures or function definitions) conclude with a standalone backslash line.

```jtml
if (x > 5) \\
    show "Greater"\\
else \\
    show "Not greater"\\
\\
```

No Semicolons: Unlike some other languages, JTML does not use semicolons to terminate statements, relying instead on backslashes for clarity.

### 3.3. Data Types
JTML supports a variety of data types, both primitive and composite, facilitating versatile programming paradigms.

Primitive Types:

int: Integer numbers.
float: Floating-point numbers.
string: Textual data.
bool: Boolean values (true or false).
void: Represents the absence of a value, primarily used in function return types.
Composite Types:

list: Ordered collections of elements.
dict: Key-value pair mappings.
User-Defined Types:

Classes allow the creation of custom types, enabling object-oriented programming.
### 3.4. Variables and Constants
Variables and constants are fundamental for storing and managing data within JTML programs.

Variable Declaration:

```jtml
define count = 0\\
```

Constant Declaration:

```jtml
const PI: float = 3.1415\\
```

Guidelines:

Variables: Mutable and can be reassigned.
Constants: Immutable once defined; attempting to reassign will result in an error.

### 3.5. Operators
JTML includes a comprehensive set of operators for performing various operations.

Arithmetic Operators:

Addition: +
Subtraction: -
Multiplication: *
Division: /
Comparison Operators:

Equal to: ==
Not equal to: !=
Less than: <
Greater than: >
Less than or equal to: <=
Greater than or equal to: >=
Logical Operators:

Logical AND: &&
Logical OR: ||
Logical NOT: !
Assignment Operators:

Simple assignment: =
Addition assignment: +=
Subtraction assignment: -=
Multiplication assignment: *=
Division assignment: /=

### 3.6. Expressions and Statements
Expressions compute values, while statements perform actions.

Expressions:

Combine literals, variables, and operators to compute values.

```jtml
define x = (y + 3) * 2\\
```

Statements:

Perform actions such as variable declarations, function calls, control flow operations, etc.

```jtml
show x\\
```

## 4. Control Flow
Control flow constructs enable the execution of code based on conditions and repetition, fostering structured and readable programs.

### 4.1. Conditional Statements
Conditional statements execute code blocks based on evaluated conditions.

Syntax:

```jtml
if (condition) \\
    // Statements to execute if condition is true\\
else \\
    // Statements to execute if condition is false\\
\\
```

Example:

```jtml
if (x > 5) \\
    show "Greater"\\
else \\
    show "Not greater"\\
\\
```

### 4.2. Loops
Loops facilitate the repeated execution of code blocks.

While Loop:

Executes as long as a specified condition is true.

```jtml
while (count < 5) \\
    show count\\
    count += 1\\
\\
```

For Loop:

Iterates over elements in a collection.

```jtml
for (item in items) \\
    show item\\
\\
```

### 4.3. Jump Statements
Jump statements alter the normal flow of control within loops and functions.

break: Exits the nearest enclosing loop.

```jtml
while (true) \\
    if (condition) \\
        break\\
    \\
\\
```

continue: Skips the current iteration and proceeds to the next one.

```jtml
for (item in items) \\
    if (item == "skip") \\
        continue\\
    show item\\
\\
```

return: Exits a function and optionally returns a value.

```jtml
function getNumber():int \\
    return 42\\
\\
```

throw: Raises an exception, triggering error handling mechanisms.

```jtml
throw "An error occurred"\\
```

## 5. Functions
Functions encapsulate reusable logic, promoting modularity and maintainability. JTML supports both synchronous and asynchronous functions.

### 5.1. Function Definitions
Define reusable blocks of code that can be invoked with specific parameters.

Syntax:

```jtml
function functionName(parameter1:type, parameter2:type):returnType \\
    // Function body\\
\\
```

Example:

```jtml
function add(a:int, b:int):int \\
    return a + b\\
\\
```

Asynchronous Functions:

Enable non-blocking operations, ideal for I/O tasks or web interactions.

```jtml
async function fetchData():void \\
    // Asynchronous operations\\
    return\\
\\
```

### 5.2. Function Calls
Invoke functions with the required arguments to perform defined operations.

Syntax:

```jtml
define result = functionName(arg1, arg2)\\
```

Example:

```jtml
define result = add(3, 4)\\
show result\\
\\
```

### 5.3. Recursion
Functions can call themselves, enabling solutions to problems that require iterative deepening or divide-and-conquer strategies.

Example:

```jtml
function factorial(n:int):int \\
    if (n <= 1) \\
        return 1\\
    else \\
        return n * factorial(n - 1)\\
\\
```

## 6. Data Structures
JTML offers robust data structures for organizing and managing data effectively.

### 6.1. Arrays and Lists
Ordered collections that store multiple elements.

Declaration:

```jtml
define numbers: list[int] = [1, 2, 3]\\
```

Operations:

Append: Add an element to the end of the list.

```jtml
numbers.append(4)\\
```

Access: Retrieve an element by its index.

```jtml
show numbers[0]\\
\\
```

### 6.2. Dictionaries
Unordered collections of key-value pairs, ideal for mappings and associative arrays.

Declaration:

```jtml
define capitals: dict[string, string] = {
    "France": "Paris",
    "Italy": "Rome"
}\\
```

Access:

```jtml
show capitals["France"]\\
\\
```

## 7. Classes and Objects
JTML supports object-oriented programming through classes and objects, enabling the creation of complex and scalable applications.

### 7.1. Class Definitions
Define blueprints for objects, encapsulating data and behavior.

Syntax:

```jtml
class ClassName \\
    define property1: type\\
    define property2: type\\
    
    function constructor(parameter1:type, parameter2:type):void \\
        self.property1 = parameter1\\
        self.property2 = parameter2\\
    \\
\\
```

Example:

```jtml
class Person \\
    define name: string\\
    define age: int\\
    
    function constructor(name:string, age:int):void \\
        self.name = name\\
        self.age = age\\
    \\
\\
```

### 7.2. Object Creation
Instantiate objects based on class definitions.

Syntax:

```jtml
define objectName = new ClassName(arg1, arg2)\\
```

Example:

```jtml
define alice = new Person("Alice", 30)\\
\\
```

### 7.3. Inheritance
Allow classes to inherit properties and methods from other classes, promoting code reuse and hierarchical structuring.

Syntax:

```jtml
class SubClass derive SuperClass \\
    define subProperty: type\\
    
    function constructor(arg1:type, arg2:type, subArg:type):void \\
        super(arg1, arg2)\\
        self.subProperty = subArg\\
    \\
\\
```

Example:

```jtml
class Employee derive Person \\
    define employeeId: int\\
    
    function constructor(name:string, age:int, employeeId:int):void \\
        super(name, age)\\
        self.employeeId = employeeId\\
    \\
\\
```

## 8. JTML Elements
JTML's unique #tag syntax allows seamless integration of markup within JTML code, enabling dynamic HTML generation.

### 8.1. Element Syntax
Define HTML elements using the #tag syntax.

Basic Example:

```jtml
#p "Hello, World!" #p\\
\\
```

Alternate Form for Readability:

```jtml
#p "Hello, World!" #p\\
\\
```

Both forms are valid, with the second form enhancing readability by repeating the opening tag name before the closing hash.

### 8.2. Attributes and Properties
Add attributes to JTML elements to define properties such as classes, IDs, styles, etc.

Example:

```jtml
#div class:"container" id:"main" \\
    #p "Hello" #p\\
#div\\
```

Explanation:

#div Element:
class:"container": Assigns the container class.
id:"main": Sets the ID to main.
Nested #p Element: Contains the text "Hello".

### 8.3. Dynamic Content
Integrate dynamic data within JTML elements using interpolation.

Example:

```jtml
define userName = "Alice"\\
#p "Welcome, #(userName)" #p\\
\\
```

Output:

```html
<p>Welcome, Alice</p>
```

Explanation:

#(userName): Interpolates the value of the userName variable into the string.

## 9. Advanced Features
JTML extends beyond basic scripting with advanced capabilities, making it suitable for complex applications and specialized tasks.

### 9.1. Database Interactions
JTML provides built-in support for interacting with databases, enabling data storage, retrieval, and manipulation directly within JTML scripts.

Connecting to a Database:

```jtml
connect to "sqlite:///mydb.db" as db\\
\\
```

Executing a Query:

```jtml
define users = query on db:"SELECT * FROM users"\\
show users\\
\\
```

Features:

Parameterized Queries: Prevent SQL injection by using placeholders.
Transactions: Ensure data integrity with commit and rollback operations.
Seamless UI Integration: Display query results dynamically in the user interface.

### 9.2. Quantum Computing Simulation
Leverage quantum computing concepts within JTML to simulate quantum algorithms and operations.

Defining Qubits:

```jtml
define q1 as qubit\\
define q2 as qubit\\
\\
```

Applying Quantum Gates:

```jtml
apply H on q1\\
apply CNOT on q1, q2\\
\\
```

Measuring Qubits:

```jtml
define r = measure q1\\
show r\\
\\
```

Capabilities:

Quantum Gates: Implement fundamental gates like Hadamard (H), CNOT, etc.
Quantum Algorithms: Simulate algorithms such as Grover's or Shor's.
Integration: Combine quantum operations with classical data processing for hybrid applications.

### 9.3. Cryptography Operations
Ensure data security through built-in cryptographic functions, enabling encryption, decryption, hashing, and signing within JTML scripts.

Generating Keys:

```jtml
define privateKey = generate_key type:"RSA", size:2048\\
define publicKey = derive_public_key from privateKey\\
\\
```

Encrypting Data:

```jtml
define enc = encrypt data:"message" with key:"publicKey" algorithm:"RSA"\\
\\
```

Decrypting Data:

```jtml
define dec = decrypt data: enc with key:"privateKey" algorithm:"RSA"\\
\\
```

Additional Operations:

Hashing: Convert data into fixed-size hashes for integrity checks.

```jtml
define hashed = hash data:"myData" algorithm:"SHA256"\\
\\
```

Signing and Verification: Sign data and verify signatures to ensure authenticity.

```jtml
define signature = sign data:"message" with key:"privateKey" algorithm:"SHA256"\\
define isValid = verify signature:"signature" data:"message" with key:"publicKey" algorithm:"SHA256"\\
\\
```

## 10. Error Handling
Robust error handling mechanisms ensure that JTML programs can gracefully handle unexpected situations and maintain stability.

Try/Catch/Finally Structure:

```jtml
try \\
    define res = 10 / 0\\
catch (DivisionByZeroException e) \\
    show e.message\\
finally \\
    show "Operation Completed"\\
\\
```

Explanation:

try: Contains code that may throw exceptions.
catch: Handles specific exceptions, allowing for targeted error responses.
finally: Executes code regardless of whether an exception was thrown, useful for cleanup tasks.
Throwing Exceptions:

```jtml
throw "An unexpected error occurred"\\
\\
```

Best Practices:

Granular Catch Blocks: Catch specific exceptions to handle different error types appropriately.
Resource Management: Use finally blocks to release resources like file handles or database connections.
Custom Exceptions: Define custom exception types for more descriptive error handling.

## 11. Modules and Packages
Organize and modularize JTML codebases by splitting code into multiple files and grouping related modules into packages.

Importing Modules:

```jtml
import "utils/math.jtml"\\
define answer = add(40, 2)\\
show answer\\
\\
```

Package Structure:

```lua
utils/
├── math.jtml
└── helpers.jtml
```

Benefits:

Code Reusability: Reuse functions and classes across different parts of the application.
Maintainability: Simplify navigation and management of large codebases.
Namespace Management: Avoid naming conflicts by logically grouping related modules.

## 12. Input/Output Operations
JTML provides primitives for file handling and data input/output, facilitating interactions with the file system and external data sources.

Reading from a File:

```jtml
define data = read_file("input.txt")\\
\\
```

Writing to a File:

```jtml
define data = data + " More info"\\
write_file("output.txt", data)\\
\\
```

Usage Scenarios:

Generating Static Content: Create HTML files or reports based on dynamic data.
Configuration Management: Read and write configuration files to manage application settings.
Data Processing Pipelines: Combine I/O operations with cryptographic or database interactions for secure and efficient data handling.

## 13. Multithreading and Concurrency
Enhance performance and responsiveness by executing multiple tasks in parallel through multithreading and concurrency features.

Creating and Starting Threads:

```jtml
define t = new Thread(fetchData)\\
t.start()\\
\\
```

Synchronization with Locks:

```jtml
lock(resource) \\
    // Critical section code\\
\\
```

Use Cases:

Scalable Servers: Handle multiple client requests concurrently.
Parallel Computations: Execute computationally intensive tasks without blocking the main thread.
Asynchronous I/O Operations: Perform non-blocking file or network operations to improve application responsiveness.
Best Practices:

Thread Safety: Ensure that shared resources are accessed in a thread-safe manner to prevent race conditions.
Resource Management: Properly manage thread lifecycles to avoid resource leaks.
Concurrency Control: Use synchronization primitives like locks judiciously to balance performance and safety.

## 14. Annotations and Decorators
Enhance code functionality and metadata through annotations and decorators, allowing for advanced programming paradigms like aspect-oriented programming.

Annotations:

Add metadata to classes, functions, or properties to provide additional information or instructions.

Example:

```jtml
@Deprecated("Use newFunc instead")
function oldFunc():void \\
    // Deprecated function logic\\
    return\\
\\
```

Decorators:

Wrap additional behavior around functions or classes, enabling features like logging, caching, or access control.

Example:

```jtml
@LogExecution
function compute():int \\
    // Function logic\\
    return 42\\
\\
```

Future Expansions:

Custom Decorators: Implement decorators for validation, security checks, performance monitoring, and more.
Chaining Decorators: Apply multiple decorators to a single function or class for compounded behavior enhancements.

## 15. Best Practices
Adhering to best practices ensures that JTML codebases remain clean, efficient, and maintainable.

Consistent Syntax:

End every statement with \\.
Close blocks with a standalone \\ line.
Maintain uniform indentation for readability.
Descriptive Names:

Use meaningful and descriptive identifiers for variables, functions, and classes.
Avoid ambiguous names that can lead to confusion.
Modularity:

Organize code into modules and packages to promote reusability and manageability.
Separate concerns by isolating UI logic from core business logic.
Security and Performance:

Validate all user inputs to prevent security vulnerabilities like SQL injection or cross-site scripting (XSS).
Use parameterized queries when interacting with databases.
Handle exceptions gracefully to maintain application stability.
Leverage concurrency responsibly to enhance performance without introducing race conditions.
Testing and Documentation:

Write comprehensive unit tests to ensure code correctness and facilitate future modifications.
Document complex logic and functions to aid understanding and collaboration.
Maintain a reference guide, such as this documentation, to provide quick access to language features and usage examples.

## 16. Glossary
JTML: JavaScript Template Markup Language—a domain-specific language integrating markup with scripting.
Qubit: The basic unit of quantum information, analogous to a classical bit but capable of representing multiple states simultaneously.
Hashing: The process of converting data into a fixed-size string of characters, typically for data integrity verification.
Encryption: Securely encoding data to prevent unauthorized access.
Decryption: Decoding encrypted data back to its original form.
Decorator: A design pattern that allows behavior to be added to individual objects or functions without modifying their structure.
Concurrency: The ability of a system to handle multiple tasks simultaneously.
Asynchronous Operations: Tasks that occur independently of the main program flow, allowing for non-blocking execution.

## 17. References
Official JTML Site
Qiskit - Quantum Computing Framework
OWASP - Open Web Application Security Project
W3Schools SQL Tutorial
Python PLY (Python Lex-Yacc)
Docker Documentation
MkDocs - Project Documentation with Markdown
Python Official Documentation