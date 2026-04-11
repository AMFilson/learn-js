# 🧩 JavaScript Functions — Exam Study Guide
**Source:** [MDN Web Docs — Functions: reusable blocks of code](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Functions)

---

## Executive Summary

JavaScript **functions** are named, reusable blocks of code that encapsulate a specific task — defined once, then called as many times as needed with a single command, eliminating repetition and improving maintainability. Functions come in multiple forms: **function declarations** (named, hoisted), **function expressions** (anonymous, not hoisted), and **arrow functions** (concise, modern syntax) — each with distinct behaviour around naming and hoisting. Mastering **parameters vs. arguments**, **default parameters**, **scope**, and the difference between **functions and methods** are the core skills tested in this topic.

---

## Core Pillars

### 1. What Is a Function & Where Are They?

- A function is a **reusable block of code** stored under a name, invoked with parentheses `()`.
- **Any time you see `()` in JavaScript** (outside of `for`, `while`, or `if`), you are calling a function.
- Functions come in two categories:
  - **Built-in browser functions**: Provided by JavaScript or the browser APIs (e.g., `Math.random()`, `Array.join()`, `String.replace()`). Some are written in low-level languages like C++ — not all are pure JavaScript.
  - **Custom functions**: Written by you or included from a library (e.g., `draw()`, `greeting()`).

```js
// Built-in function examples
const newString = myText.replace("string", "sausage");
const randomNum = Math.random();
const joined = myArray.join(" ");
```

---

### 2. Functions vs. Methods

- **Function**: A standalone callable block of code. Example: `myFunction()`.
- **Method**: A function that is a **property of an object**. Called on an object using dot notation. Example: `myArray.join(" ")`.
- The distinction is primarily about **where the function lives** — methods belong to objects; functions stand alone.
- Both use `()` to invoke.

```js
// Function (standalone)
function random(number) {
  return Math.floor(Math.random() * number);
}
random(50);  // invoked directly

// Method (attached to an object)
const myArray = ["I", "love", "chocolate"];
myArray.join(" ");  // join() is a method of the Array object
```

---

### 3. Invoking (Calling) a Function

- **Defining** a function does nothing on its own — it only runs when **invoked**.
- Invoke by writing the function's name followed by `()`. Arguments go inside the parentheses.
- **Function declarations are hoisted** — you can call them before they appear in the code. Function expressions are NOT hoisted.

```js
function myFunction() {
  alert("hello");
}

myFunction();  // invokes the function — runs the code inside
```

---

### 4. Parameters vs. Arguments

- **Parameters**: The variable names listed in the function **definition** — they act as local placeholders.
- **Arguments**: The actual **values passed in** when the function is called.
- Multiple parameters are separated by **commas**.
- Some functions have **no parameters** (e.g., `Math.random()`); some require one or more.

```js
// Definition — "name" is the PARAMETER
function hello(name) {
  console.log(`Hello ${name}!`);
}

// Invocation — "Ari" is the ARGUMENT
hello("Ari");  // Hello Ari!
```

---

### 5. Optional Parameters & Default Values

- **Optional parameters**: Some built-in functions work with or without a parameter (e.g., `array.join()` defaults to `","` if no separator is provided).
- **Default parameters**: In your own functions, set defaults using `= value` in the parameter list. If the caller omits that argument, the default is used.

```js
// Optional parameter (built-in) — comma is the default separator
myArray.join();     // "I,love,chocolate"
myArray.join(" ");  // "I love chocolate"

// Default parameter (custom function)
function hello(name = "Chris") {
  console.log(`Hello ${name}!`);
}
hello("Ari");  // Hello Ari!   ← argument provided, overrides default
hello();       // Hello Chris! ← no argument, default used
```

---

### 6. Anonymous Functions

- A function **without a name**. Cannot be called by name — must be used inline.
- Most commonly passed as **arguments to other functions** (event handlers, callbacks).
- Created with `function () { ... }` syntax.
- This form is a **function expression** — it is **NOT hoisted**.

```js
// Named function — defined separately, then referenced
function logKey(event) {
  console.log(`You pressed "${event.key}".`);
}
textBox.addEventListener("keydown", logKey);

// Anonymous function — defined inline, passed directly
textBox.addEventListener("keydown", function (event) {
  console.log(`You pressed "${event.key}".`);
});
```

---

### 7. Arrow Functions (`=>`)

- A **concise alternative syntax** for anonymous functions. Preferred in modern JavaScript.
- Syntax: replace `function(params)` with `(params) =>`.
- Three progressively shorter forms:

| Form | When to use |
|---|---|
| `(params) => { ... }` | Multiple statements in the body |
| `param => { ... }` | Only **one** parameter — parentheses optional |
| `param => expression` | Body is a **single return expression** — omit `{}` and `return` |

```js
// Full arrow function
textBox.addEventListener("keydown", (event) => {
  console.log(`You pressed "${event.key}".`);
});

// Single param — no parentheses needed
textBox.addEventListener("keydown", event => {
  console.log(`You pressed "${event.key}".`);
});

// Concise body — implicit return (no {} or return keyword)
const doubled = [1, 2, 3].map(item => item * 2);
// [2, 4, 6]
```

---

### 8. Callback Functions

- A function passed as an **argument to another function**, to be called at a later time.
- The function receiving the callback decides **when** to call it.
- Anonymous functions and arrow functions are the most common forms of callbacks.

```js
// logKey is a callback — addEventListener calls it when keydown fires
function logKey(event) {
  console.log(`You pressed "${event.key}".`);
}
textBox.addEventListener("keydown", logKey);

// Inline arrow function callback — same result, more concise
textBox.addEventListener("keydown", (event) => {
  console.log(`You pressed "${event.key}".`);
});
```

---

### 9. Function Scope

- Variables declared **inside a function** are in **local/function scope** — they are only accessible within that function. Code outside cannot see them.
- Variables declared **outside all functions** are in **global scope** — accessible from anywhere in the code.
- Scope prevents naming conflicts between scripts and isolates logic for security and organisation.

```js
const x = 1;        // global scope — available everywhere

function a() {
  const y = 2;      // function scope — only accessible inside a()
  console.log(x);   // OK: can access global x from inside a()
}

console.log(y);     // ❌ ReferenceError: y is not defined (locked inside a())
```

---

### 10. Block Scope (`let`/`const` vs. `var`)

- Variables declared with **`let`** or **`const`** inside `if`, `for`, or other blocks (`{ }`) are **block-scoped** — only accessible within that block.
- Variables declared with **`var`** inside blocks (but NOT functions) are **hoisted to the global scope** — a source of bugs and the reason `var` is avoided.
- Variables declared with `var` inside a **function** are still function-scoped.

```js
if (x === 1) {
  const c = 4;   // block-scoped — invisible outside
  var d = 5;     // hoisted to global — accessible outside (dangerous!)
}

console.log(c);  // ❌ ReferenceError
console.log(d);  // ✅ 5 — var leaks out of the block (avoid this!)
```

---

## Technical Deep-Dive

### Logic Walkthrough: Function Declaration vs. Expression vs. Arrow

These three forms all define reusable functions but behave differently:

```js
// ── 1. FUNCTION DECLARATION ────────────────────────────────────────
// - Has a name
// - Hoisted: can be called BEFORE the declaration in the code
greet("Alice");  // ✅ works even before the function definition

function greet(name) {
  console.log(`Hello, ${name}!`);
}


// ── 2. FUNCTION EXPRESSION ─────────────────────────────────────────
// - Anonymous function assigned to a variable
// - NOT hoisted: cannot be called before the assignment
sayBye("Bob");  // ❌ ReferenceError: Cannot access 'sayBye' before initialization

const sayBye = function(name) {
  console.log(`Bye, ${name}!`);
};


// ── 3. ARROW FUNCTION (EXPRESSION FORM) ───────────────────────────
// - Concise, no own 'this', always anonymous
// - NOT hoisted
const double = num => num * 2;
console.log(double(5));  // 10
```

---

### Logic Walkthrough: Scope & Naming Conflicts

This demonstrates why scope matters — two scripts with the same variable names cause a crash:

```js
// first.js
const name = "Chris";
function greeting() {
  alert(`Hello ${name}: welcome to our company.`);
}

// second.js (loaded after first.js)
const name = "Zaptec";  // ❌ SyntaxError: 'name' already declared (global scope clash)
function greeting() {   // ← second.js fails to load entirely
  alert(`Our company is called ${name}.`);
}
```

**What happens:**
1. `first.js` runs fine — `name` = "Chris", `greeting()` defined.
2. `second.js` **crashes** immediately — `name` is already declared in global scope.
3. Because `second.js` fails, its `greeting()` is never defined either.

**The lesson:** Keeping variables and functions inside **function scope** prevents this. The global scope belongs to no one — polluting it invites conflicts.

---

### Logic Walkthrough: Arrow Function Shorthand — Three Levels

```js
// Level 1: Full anonymous function expression
const doubled = originals.map(function(item) {
  return item * 2;
});

// Level 2: Arrow function — same body, just shorter syntax
const doubled = originals.map((item) => {
  return item * 2;
});

// Level 3: Concise arrow — 1 param, 1 return expression → omit (), {}, return
const doubled = originals.map(item => item * 2);
// [2, 4, 6]
```

All three are functionally equivalent. Level 3 is modern standard; only use Level 1 if you need maximum clarity for beginners reading your code.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Function** | A named, reusable block of code defined once and invoked (called) as many times as needed using `functionName()`. |
| **Method** | A function that is a property of an object, called with dot notation: `object.method()`. |
| **Invoke / Call** | To execute a function by writing its name followed by `()`, optionally passing arguments. |
| **Parameter** | A named placeholder variable in a function's **definition**. Receives the value of the corresponding argument when called. |
| **Argument** | The actual **value passed to** a function when it is invoked. Arguments map to parameters by position. |
| **Default parameter** | A parameter with a fallback value (`param = value`) used when no argument is provided for that parameter. |
| **Optional parameter** | A parameter that can be omitted when calling a function — the function handles its absence gracefully. |
| **Function declaration** | The `function name() { }` form. **Hoisted** — can be called before it appears in the source code. |
| **Function expression** | A function (usually anonymous) assigned to a variable: `const fn = function() { }`. **Not hoisted**. |
| **Anonymous function** | A function with no name, typically defined inline and passed as a callback or assigned to a variable. |
| **Arrow function** | A concise function expression using `=>` syntax. Can omit `{}` and `return` for single-expression bodies. |
| **Callback function** | A function passed as an argument to another function, to be called by that function at a later time. |
| **Hoisting** | JavaScript's behaviour of moving `function` declarations (and `var`) to the top of their scope before execution. |
| **Scope** | The context in which a variable is accessible. Variables are only visible within the scope they are declared in. |
| **Global scope** | The outermost scope — code and variables accessible from everywhere in the program. |
| **Function scope / Local scope** | The scope created inside a function's `{ }` — variables declared here are invisible outside. |
| **Block scope** | The narrow scope created by `{ }` in `if`, `for`, etc. Only `let` and `const` are block-scoped; `var` is not. |
| **`var`** | A legacy variable declaration keyword. Function-scoped but **NOT block-scoped**; declared variables leak outside `if`/`for` blocks into global scope. Avoid in modern JavaScript. |
| **`ReferenceError`** | An error thrown when code tries to access a variable that is not defined or not in scope. |

---

## Watch Out For...

1. **Defining vs. calling a function.** `myFunction` (no parentheses) is just a **reference** to the function object. `myFunction()` **calls** it. Passing `myFunction` to an event listener is correct — passing `myFunction()` immediately calls it and passes the return value instead.

2. **Parameters ≠ Arguments.** These words are often used interchangeably in conversation but have distinct technical meanings. Parameters are in the **definition**; arguments are in the **call**. Exams test this distinction.

3. **Function declarations are hoisted; function expressions are not.** Calling a function expression before its assignment throws a `ReferenceError`. Only function declarations can be safely called before they appear in the source.

4. **`var` escapes blocks.** `var` declared inside an `if` or `for` block leaks into the surrounding scope (usually global). `let` and `const` are properly block-scoped. This is one of the most common sources of subtle bugs.

5. **Arrow functions can't always replace regular functions.** Arrow functions don't have their own `this`, so they behave differently inside class methods or object methods. The MDN article notes this subtlety; it becomes critical in later topics.

6. **Concise arrow functions implicitly return — no `return` needed.** `item => item * 2` already returns the value. Adding `return` inside `{}` is correct, but `item => { item * 2 }` (with braces but no `return`) returns `undefined` — a common mistake.

7. **Global scope pollution.** Variables declared outside any function are global and accessible from everywhere — including other scripts loaded on the page. Name collisions between scripts are a real risk. Always scope variables tightly.

8. **Methods are functions — but not all functions are methods.** A method is only a method because of where it lives (on an object). `myArray.join()` is a method; `join()` alone would be a standalone function call (and would error). The dot notation is the tell.

9. **Default parameters only trigger when the argument is `undefined`.** If you explicitly pass `null`, `0`, or `""` (empty string), the default is **not** used — only omitting the argument or passing `undefined` triggers the default.

10. **Scope rules apply to `if` and `for` blocks too.** A variable declared with `let` inside a `for` loop `{ }` is not accessible after the loop ends. This catches students who expect it to persist.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the difference between a **parameter** and an **argument**? Write a short code example that labels each.

**Q2.** What does **hoisting** mean in the context of functions? How does it differ between a function declaration and a function expression?

**Q3.** The following code throws a `ReferenceError`. Explain why, and what rule it demonstrates.
```js
function a() {
  const y = 2;
}

console.log(y);  // ❌ ReferenceError
```

**Q4.** Rewrite the following named function as: (a) an anonymous function expression, (b) an arrow function, and (c) a concise arrow function.
```js
function double(n) {
  return n * 2;
}
```

**Q5.** Why is `var` considered problematic compared to `let` and `const`? What specific scoping behaviour makes it dangerous?

---

## Answer Key

---

**A1.**
- **Parameter**: The placeholder name in the function **definition**.
- **Argument**: The actual value passed in the function **call**.

```js
function greet(name) {  // ← "name" is the PARAMETER
  console.log(`Hello ${name}!`);
}

greet("Ari");           // ← "Ari" is the ARGUMENT
```

---

**A2.**
**Hoisting** is JavaScript's behaviour of moving certain declarations to the top of their scope before code runs.

- **Function declarations** (`function name() {}`) are **fully hoisted** — the entire function is available before it appears in source code. You can call it before its definition.
- **Function expressions** (`const fn = function() {}` or `const fn = () =>`) are **NOT hoisted** — calling them before their assignment throws a `ReferenceError`.

```js
greet();           // ✅ works — declaration is hoisted
function greet() { console.log("hi"); }

sayBye();          // ❌ ReferenceError — expression is not hoisted
const sayBye = () => console.log("bye");
```

---

**A3.**
The error is caused by **function scope**. The variable `y` is declared with `const` inside the function `a()`, making it **local to that function**. Code outside the function cannot access it.

The rule demonstrated: **Variables declared inside a function are locked in function scope** — they are invisible to any code outside that function, including the global scope.

---

**A4.**

**(a) Anonymous function expression:**
```js
const double = function(n) {
  return n * 2;
};
```

**(b) Arrow function:**
```js
const double = (n) => {
  return n * 2;
};
```

**(c) Concise arrow function (implicit return):**
```js
const double = n => n * 2;
```
Since there is only one parameter and the body is a single return expression, both the parentheses around `n` and the `{}` + `return` can be omitted.

---

**A5.**
`var` is dangerous because it is **not block-scoped** — it is only scoped to the **function** it's in (or global scope if in no function). This means a `var` declared inside an `if` block or `for` loop **leaks out** into the surrounding scope.

```js
if (true) {
  var x = 5;  // leaks into global scope
  let y = 6;  // stays in block scope
}

console.log(x);  // ✅ 5 — var leaked out (unexpected, dangerous)
console.log(y);  // ❌ ReferenceError — let is properly block-scoped
```

This makes it very easy to accidentally overwrite variables from other parts of the code. `let` and `const` respect block boundaries and are predictable, making them the only recommended choice in modern JavaScript.
