# 2. Getting Started
## 2.1. Installation
### Prerequisites:

Python 3.8+
Node.js (Optional for generating JS code)
Database Engines (Optional for DB interactions)
Install the JTML Compiler:

```bash
pip install jtml-compiler
```

Verify Installation:

```bash
jtml --version
```

## 2.2. Hello World Example
Create hello_world.jtml:

```jtml
#p: "Hello, World!" #
```

Run:

```bash
jtml run hello_world.jtml
```

Expected Output:

```html
<p>Hello, World!</p>
```