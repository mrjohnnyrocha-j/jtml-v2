# JTML Official Documentation

## Table of Contents

 1.  [Introduction to JTML](#1-introduction-to-jtml)
 2.  [Getting Started](#2-getting-started)
         1.  [2.1. Installation](#21-installation)
         2.  [2.2. Hello World Example](#22-hello-world-example)
 3.  [Language Fundamentals](#3-language-fundamentals)
         1.  [3.1. Lexical Conventions](#31-lexical-conventions)
         2.  [3.2. Syntax Overview](#32-syntax-overview)
         3.  [3.3. Data Types](#33-data-types)
         4.  [3.4. Variables and Constants](#34-variables-and-constants)
         5.  [3.5. Operators](#35-operators)
         6.  [3.6. Expressions and Statements](#36-expressions-and-statements)
 4.  [Control Flow](#4-control-flow)
         1.  [4.1. Conditional Statements](#41-conditional-statements)
         2.  [4.2. Loops](#42-loops)
         3.  [4.3. Jump Statements](#43-jump-statements)
 5.  [Functions](#5-functions)
         1.  [5.1. Function Definitions](#51-function-definitions)
         2.  [5.2. Function Calls](#52-function-calls)
         3.  [5.3. Recursion](#53-recursion)
 6.  [Data Structures](#6-data-structures)
         1.  [6.1. Arrays](#61-arrays)
         2.  [6.2. Lists](#62-lists)
         3.  [6.3. Dictionaries](#63-dictionaries)
 7.  [Classes and Objects](#7-classes-and-objects)
         1.  [7.1. Class Definitions](#71-class-definitions)
         2.  [7.2. Object Creation](#72-object-creation)
         3.  [7.3. Inheritance](#73-inheritance)
 8.  [JTML Elements](#8-jtml-elements)
         1.  [8.1. Element Syntax](#81-element-syntax)
         2.  [8.2. Attributes and Properties](#82-attributes-and-properties)
         3.  [8.3. Dynamic Content](#83-dynamic-content)
 9.  [Advanced Features](#9-advanced-features)
         1.  [9.1. Database Interactions](#91-database-interactions)
         2.  [9.2. Quantum Computing Simulation](#92-quantum-computing-simulation)
         3.  [9.3. Cryptography Operations](#93-cryptography-operations)
 10.  [Error Handling](#10-error-handling)
         1.  [10.1. Exception Types](#101-exception-types)
         2.  [10.2. Custom Exceptions](#102-custom-exceptions)
 11.  [Modules and Packages](#11-modules-and-packages)
 12.  [Input/Output Operations](#12-inputoutput-operations)
 13.  [Multithreading and Concurrency](#13-multithreading-and-concurrency)
 14.  [Annotations and Decorators](#14-annotations-and-decorators)
 15.  [Best Practices](#15-best-practices)
 16.  [Glossary](#16-glossary)
 17.  [References](#17-references)
* * *

## 1\. Introduction to JTML

**JTML (JavaScript Template Markup Language)** is a high-level language designed to blend the clarity of markup languages with the computational power of scripting languages. JTML enables developers to write clean, maintainable code that spans frontend (markup-like) components and backend logic, integrating advanced features like database queries, quantum simulations, and cryptography.

**Key Features:**

-   **Readable Syntax:** Combines markup familiarity with scripting capabilities.
-   **Full-Stack Integration:** Seamlessly handle data from databases, simulate quantum circuits, perform secure cryptographic operations.
-   **Modular and Scalable:** Classes, modules, and packages to manage complexity.

## 2\. Getting Started

### 2.1. Installation

**Prerequisites:**

-   Python 3.8+
-   Node.js (optional, for JS code generation)
-   Database engines (optional, if needed)
**Install JTML Compiler:**

```
pip install jtml-compiler
```

**Verify Installation:**

```
jtml --version
```

### 2.2. Hello World Example

Create `hello_world.jtml`:

```
#p: "Hello, World!" #
```

Run:

```
jtml run hello_world.jtml
```

**Expected Output:**

```
<p>Hello, World!</p>
```

## 3\. Language Fundamentals

### 3.1. Lexical Conventions

JTML uses Unicode. Comments:

-   Single-line: `// comment`
-   Multi-line: `/* ... */`

### 3.2. Syntax Overview

Statements end with `\\`. Blocks also use `\\` to mark start/end.

```
define x = 10\\if (x > 5) \\    show "Greater"\\\\
```

### 3.3. Data Types

Primitives: `int`, `float`, `string`, `bool`
Composites: `list`, `dict`

```
define count: int = 0\\define name: string = "JTML"\\
```

### 3.4. Variables and Constants

Define variables with `define`, optionally provide types.

```
define x = 5\\define y: float = 3.14\\
```

Constants (if supported):

```
const PI: float = 3.1415\\
```

### 3.5. Operators

**Arithmetic:** + - \* / %
**Assignment:** = += -= \*= /= %=
**Comparison:** == != < > <= >=
**Logical:** && || !

### 3.6. Expressions and Statements

Expressions combine variables and operators. Statements perform actions and end with `\\`.

```
x += 1\\show x\\
```

## 4\. Control Flow

### 4.1. Conditional Statements

```
if (score >= 90) \\    grade = "A"\\else \\    grade = "B"\\\\
```

### 4.2. Loops

**While Loop:**

```
while (count < 5) \\    show count\\    count += 1\\\\
```

**For Loop (over collections):**

```
for (item in items) \\    show item\\\\
```

### 4.3. Jump Statements

`break`, `continue`, `return` to manage flow.

## 5\. Functions

### 5.1. Function Definitions

```
function add(a:int,b:int):int \\    return a+b\\\\
```

### 5.2. Function Calls

```
define result = add(3,4)\\
```

### 5.3. Recursion

```
function factorial(n:int):int \\    if (n <= 1) \\        return 1\\    else \\        return n * factorial(n-1)\\    \\\\
```

## 6\. Data Structures

### 6.1. Arrays

(If supported) Fixed-size arrays:

```
define arr: array[int] = new array[int](5)\\arr[0] = 10\\
```

### 6.2. Lists

```
define fruits: list[string] = ["Apple","Banana"]\\fruits.append("Cherry")\\
```

### 6.3. Dictionaries

```
define capitals: dict[string,string] = {    "France":"Paris",    "Italy":"Rome"}\\show capitals["France"]\\
```

## 7\. Classes and Objects

### 7.1. Class Definitions

```
class Person \\    define name: string\\    define age: int\\    function constructor(name:string,age:int):void \\        self.name = name\\        self.age = age\\    \\\\
```

### 7.2. Object Creation

```
define alice = new Person("Alice",30)\\
```

### 7.3. Inheritance

```
class Employee derive Person \\    define employeeId:int\\    function constructor(name:string,age:int,employeeId:int):void \\        super(name,age)\\        self.employeeId = employeeId\\    \\\\
```

## 8\. JTML Elements

### 8.1. Element Syntax

```
#tagName: "Content" #
```

### 8.2. Attributes and Properties

```
#div class:"container", id:"main": "Hello" #
```

### 8.3. Dynamic Content

```
define userName = "Alice"\\#p: "Welcome, {{userName}}" #
```

## 9\. Advanced Features

### 9.1. Database Interactions

```
connect to "sqlite:///mydb.db" as db\\define users = query on db:"SELECT * FROM users"\\
```

### 9.2. Quantum Computing Simulation

```
define q1 as qubit\\define q2 as qubit\\apply H on q1\\apply CNOT on q1,q2\\define r = measure q1\\
```

### 9.3. Cryptography Operations

```
define privateKey = generate_key type:"RSA", size:2048\\define publicKey = derive_public_key from privateKey\\define enc = encrypt data: message with key:publicKey algorithm:"RSA"\\define dec = decrypt data: enc with key:privateKey algorithm:"RSA"\\
```

## 10\. Error Handling

### 10.1. Exception Types

JTML provides exceptions like `Exception`, `ArithmeticException`, etc.

### 10.2. Custom Exceptions

```
class MyError derive Exception \\    function constructor(msg:string):void \\        super(msg)\\    \\\\throw new MyError("Custom error")\\
```

Try-Catch-Finally:

```
try \\    define res = 10/0\\catch (DivisionByZeroException e) \\    show e.message\\finally \\    show "Done"\\\\
```

## 11\. Modules and Packages

Modularize code into separate files and `import` them:

```
import "utilities.jtml"\\helperFunction()\\
```

## 12\. Input/Output Operations

```
define text = read_file("input.txt")\\write_file("output.txt", text)\\
```

## 13\. Multithreading and Concurrency

```
define t = new Thread(someFunction)\\t.start()\\lock(resource) \\    // critical section \\\\
```

## 14\. Annotations and Decorators

```
@Deprecated("Use newFunc instead")function oldFunc(): void \\    // ...\\
```

## 15\. Best Practices

-   **Readability:** Consistent indentation, naming, and commenting.
-   **Security:** Validate input, use parameterized queries for DB operations.
-   **Performance:** Use efficient data structures, avoid unnecessary computations.
-   **Error Handling:** Anticipate and gracefully handle exceptions.
-   **Documentation:** Comment complex logic and maintain a reference guide.

## 16\. Glossary

-   **JTML:** JavaScript Template Markup Language.
-   **Qubit:** Basic unit of quantum information.
-   **Hashing:** Converting data into a fixed-size hash.
-   **Encryption:** Encoding data to secure it from unauthorized access.
-   **Decryption:** Decoding encrypted data to its original form.

## 17\. References

-   **Official JTML Site:** [www.jtml.org](http://www.jtml.org)
-   **Quantum Computing:** [Qiskit Documentation](https://qiskit.org/documentation/)
-   **Cryptography Guidelines:** [OWASP](https://owasp.org/)
-   **SQL Reference:** [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)
