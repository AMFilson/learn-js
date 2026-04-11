# 🐛 JavaScript Debugging & Error Handling — Exam Study Guide
**Source:** [MDN Web Docs — JavaScript debugging and error handling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Debugging_JavaScript)

---

## Executive Summary

JavaScript is **not permissive** like HTML or CSS — the JS engine throws errors on mistakes, which means you need a structured strategy for finding and fixing them. This article covers four key layers of defence: **linting** (catching errors before running code), **the browser console and Console API** (observing what your code is doing at runtime), **the JavaScript debugger** (pausing execution and inspecting your program's exact state with breakpoints), and **error handling in code** (using conditionals, `throw`, and `try...catch` to manage errors gracefully at runtime). Mastering all four gives you a complete toolkit for writing robust JavaScript.

---

## Core Pillars

### 1. Two Types of JavaScript Error

Before debugging, identify what *kind* of error you have:

| Error Type | Description | Example |
|---|---|---|
| **Syntax Error** | Code that cannot be parsed — the engine rejects it before running | Missing bracket, mismatched quotes |
| **Logic Error** | Code that runs but produces a wrong result | Using `+` when you meant `*`; off-by-one index |

- **Syntax errors** are caught immediately by linters and the console (red error with a line number).
- **Logic errors** are harder — the code runs without crashing but behaves incorrectly. These require `console.log()` or the debugger to hunt down.

---

### 2. Linting — Catch Errors Before Running

**Linting** is the process of running a static analysis tool over your code to detect errors *before* you run it in a browser.

- **JavaScript linter:** [ESLint](https://eslint.org/play/) — the industry standard.
- **HTML validator:** [W3C Markup Validation Service](https://validator.w3.org/)
- **CSS validator:** [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)

**Best practice:** Install ESLint as a **VS Code extension** so errors are highlighted in real time as you type — no copy/pasting into web tools.

> Always lint first. Fix linting errors before trying to debug runtime behaviour — you may already be done.

---

### 3. Common JavaScript Problems to Watch For

These recurring bugs account for a large proportion of real-world JavaScript errors:

- **Scope errors** — variables used outside their declared scope, or naming conflicts between variables in different scopes.
- **`this` confusion** — `this` changes value depending on the call site. Inside a nested function or event handler, `this` may not be what you expect.
- **`var` in loops (classic gotcha)** — using `var` in a loop and referencing it in an inner function. Because `var` is function-scoped, all iterations share the same variable:
  ```js
  // Bug: all event handlers see i = 11 (final value after loop ends)
  for (var i = 0; i < 10; i++) {
    btn.addEventListener("click", () => console.log(i)); // always logs 11
  }

  // Fix: use let — block-scoped, unique per iteration
  for (let i = 0; i < 10; i++) {
    btn.addEventListener("click", () => console.log(i)); // logs 0–9 correctly
  }
  ```
- **Async not awaited** — using the result of a `fetch()` or other async call without `await`ing it gives you a pending Promise, not the value.
- **Wrong data types** — passing a string where a number is expected. JS may silently coerce it, producing subtle bugs.

---

### 4. The Browser JavaScript Console

**Open DevTools:** `F12` (or `Ctrl+Shift+I` / `Cmd+Option+I`) → **Console** tab.

**What the console gives you:**
- **Error messages** in red with the file name and line number of the error.
- **A call stack** when you click the arrow next to an error — shows the sequence of function calls that led to the crash.
- **Your own `console.log()` output** to inspect values at key points in code.

**Reading an error message:**
```
Uncaught TypeError: heroes is not iterable
    at showHeroes (index.js:25)
    at onload (index.js:10)
```
- **Error type:** `TypeError` — `heroes` is the wrong type (e.g., `undefined` instead of an array).
- **Location:** `index.js` line 25, inside the function `showHeroes`.
- **Call stack:** `showHeroes` was called from the `onload` handler at line 10.

---

### 5. The Console API — Key Methods

The `console` object has several methods you should know:

| Method | Purpose |
|---|---|
| **`console.log(value)`** | Prints a value to the console for inspection. The go-to debugging tool. |
| **`console.error(value)`** | Prints a value styled as an error (red), and **generates a call stack** even if no error was thrown. Useful for flagging problems manually. |
| **`console.warn(value)`** | Prints a warning (yellow). |
| **`console.table(array)`** | Displays an array of objects as a formatted table. |
| **`console.group()` / `console.groupEnd()`** | Groups related console logs together. |

**Using `console.log()` to diagnose a Promise bug:**
```js
// Bug: response is a Promise, not data
const response = fetch(requestURL);
console.log(`Response value: ${response}`);
// → "Response value: [object Promise]"
// ↑ This tells you response is a Promise, not data — you forgot await or .then()
```

---

### 6. The JavaScript Debugger — Breakpoints

The **Debugger** is the most powerful built-in debugging tool. It lets you **pause code execution mid-run** and inspect the exact state of all variables.

**Accessing it:**
- Firefox: DevTools → **Debugger** tab
- Chrome: DevTools → **Sources** tab
- Safari: Web Inspector → **Debugger**

**Three key panels in the Debugger:**
| Panel | What It Shows |
|---|---|
| **Left** | File list — select the script to debug |
| **Centre** | The source code — click a line number to set a breakpoint |
| **Right** | Live information: **Breakpoints**, **Call Stack**, **Scopes** |

**How to use breakpoints:**
1. Click a **line number** in the centre panel → a blue arrow appears = **breakpoint set**.
2. **Refresh the page** (`Ctrl/Cmd+R`) — execution pauses when it reaches that line.
3. Inspect the **Scopes** panel on the right — see the exact value of every variable at that moment.
4. Use the call stack to trace back which functions called which.

**What the Scopes panel reveals:**
```
showHeroes scope:
  heroes = undefined     ← bug! should be an array
  jsonObj = Response { } ← bug! should be a JS object, not a Response
```
Seeing `heroes = undefined` and `jsonObj = Response {}` immediately tells you:
- `jsonObj["members"]` returned `undefined` because `jsonObj` is not parsed JSON — it's still the raw `Response` object from fetch.
- The fix: call `await response.json()` to parse the body first.

---

### 7. Error Handling with Conditionals

**Defensive programming** — check your inputs before using them.

```js
function inchesToMeters(num) {
  // Guard clause: validate the input FIRST
  if (typeof num !== "number" || Number.isNaN(num)) {
    console.log("A number was not provided. Please correct the input.");
    return undefined;   // exit early with a safe value
  }

  // Safe to proceed
  const mVal = (num * 2.54) / 100;
  return mVal.toFixed(2);
}
```

**Why `typeof num !== "number" || Number.isNaN(num)`?**
- `typeof NaN === "number"` returns `true` — NaN paradoxically has type `"number"`.
- So `typeof` alone is not enough to catch NaN — you need `Number.isNaN()` as a second check.
- Both conditions together guard against all bad numeric input.

---

### 8. Throwing Custom Errors — `throw` + `Error()`

Instead of silently returning `undefined` on bad input, **throw an error** — this is more explicit and gives you a call stack.

```js
function inchesToMeters(num) {
  if (typeof num !== "number" || Number.isNaN(num)) {
    throw new Error("A number was not provided. Please correct the input.");
    // ↑ Immediately halts the function and propagates the error up the call stack
  }
  const mVal = (num * 2.54) / 100;
  return mVal.toFixed(2);
}
```

- `throw` can be used with any value, but `throw new Error("message")` is the standard.
- When thrown, JavaScript stops executing the current function and walks up the call stack looking for a `catch` block.
- The error appears in the console with a useful call stack, marked as "uncaught" if not handled by `try...catch`.

---

### 9. `try...catch` — Handling Errors Gracefully

`try...catch` wraps code that might throw, allowing you to **handle** the error instead of crashing the application.

```js
try {
  // Code that might throw an error
  console.log(inchesToMeters(height));
} catch (error) {
  // Runs ONLY if an error was thrown in the try block
  console.error(error);                  // logs the Error object with its call stack
  console.log("Insert error handling"); // tell the user, re-prompt, etc.
}
```

**Key properties of `try...catch`:**
- The `catch` block receives the **`Error` object** as its parameter (typically named `error` or `err`).
- `error.message` — the human-readable message from `throw new Error("...")`.
- `error.name` — the type of error (`"TypeError"`, `"ReferenceError"`, etc.).
- Once wrapped in `try...catch`, errors are **handled** — they no longer crash the app, and the console no longer shows "Uncaught".
- You can combine `if...else` inside the `catch` block to handle different error types differently.

**Pattern: `throw` + `try...catch` working together:**
```js
// Function throws on bad data:
function inchesToMeters(num) {
  if (typeof num !== "number" || Number.isNaN(num)) {
    throw new Error("Invalid input: expected a number.");
  }
  return ((num * 2.54) / 100).toFixed(2);
}

// Caller handles the error gracefully:
try {
  const result = inchesToMeters(height);  // might throw
  console.log(result);                    // only runs if no error
} catch (error) {
  console.error(error.message);           // "Invalid input: expected a number."
  // Re-prompt the user, use a default value, etc.
}
```

---

### 10. Feature Detection

**Feature detection** is a technique for safely using APIs that may not be available in all browsers. Check if the feature exists before using it:

```js
// Check if geolocation is supported before calling it:
if ("geolocation" in navigator) {
  navigator.geolocation.getCurrentPosition((position) => {
    // show location data
  });
} else {
  // Fallback: show a static map instead
}
```

- Test for the feature's **existence** using `"property" in object` or simply checking if `navigator.geolocation` is truthy.
- This prevents `TypeError: Cannot read properties of undefined` when calling APIs that don't exist in the current browser.

---

### 11. Finding Help — Resources

When stuck, know where to look:

| Resource | Best For |
|---|---|
| **MDN** | Authoritative reference for any web API, with syntax, examples, browser compatibility |
| **Stack Overflow** | Searching for solutions to specific problems; always search before posting |
| **caniuse.com** | Checking whether a CSS/JS feature is supported in a given browser version |
| **Search engine + error message** | Copy the exact error text — someone has likely had the same issue |

**MDN search tip:** Search engine query + "mdn" (e.g., _"fetch api mdn"_) reliably surfaces the right reference page.

---

## Technical Deep-Dive

### Logic Walkthrough: Diagnosing the Fetch Promise Bug Using `console.log()`

**Buggy code:**
```js
// Bug 1: Missing await — response is a Promise, not a Response object
const response = fetch(requestURL);
populateHeader(response);  // ← receives a Promise, not data
showHeroes(response);      // ← "heroes is not iterable" because response is a Promise
```

**Step 1 — Use `console.log()` to inspect `response`:**
```js
const response = fetch(requestURL);
console.log(`Response value: ${response}`);
// Output: "Response value: [object Promise]"
// → response is a Promise, not data ← bug identified
```

**Step 2 — Fix: chain `.then()` (still buggy):**
```js
fetch(requestURL).then((response) => {
  populateHeader(response);
  showHeroes(response);    // still fails — response is a Response object, not parsed JSON
});
```

**Step 3 — Use the debugger: inspect `jsonObj` in the Scopes panel:**
```
showHeroes scope:
  heroes  = undefined        ← accessing .members on a Response returns undefined
  jsonObj = Response { ... } ← bug! should be a JS object, not a Response
```

**Step 4 — Full fix:**
```js
fetch(requestURL)
  .then((response) => response.json())   // ← parse the body FIRST
  .then((data) => {
    populateHeader(data);  // ← now receives a JS object
    showHeroes(data);      // ← works correctly
  });
```

> **Lesson:** `console.log()` revealed a Promise where an object was expected; the debugger confirmed `jsonObj` was a `Response` rather than parsed JSON. Two tools, two layers of insight.

---

### Logic Walkthrough: `throw` → `catch` Execution Flow

```js
function inchesToMeters(num) {
  if (typeof num !== "number" || Number.isNaN(num)) {
    throw new Error("Invalid input");   // ← Step 2: Error object created and thrown
  }
  return ((num * 2.54) / 100).toFixed(2);  // ← SKIPPED if throw runs
}

try {
  console.log(inchesToMeters("tall"));   // ← Step 1: bad argument passed
                                          //   throw fires inside the function
                                          //   execution jumps DIRECTLY to catch
  console.log("This never runs");        // ← SKIPPED — throw already jumped past here
} catch (error) {
  // ← Step 3: error object received here
  console.error(error.message);  // "Invalid input"
  // programme continues normally after the catch block
}

console.log("Programme continues...");  // ← Step 4: runs normally after catch
```

**Flow summary:**
```
inchesToMeters("tall")
  → typeof "tall" !== "number"  → true
      → throw new Error(...)
          → JS searches call stack for nearest catch
              → found in try...catch block
                  → catch(error) runs
                      → programme recovers and continues
```

---

### Logic Walkthrough: Why `typeof NaN === "number"` Requires a Separate Check

```js
typeof 42           // → "number"   ✅ correct
typeof "hello"      // → "string"
typeof NaN          // → "number"   ⚠️ surprise! NaN is technically type "number"
Number.isNaN(NaN)   // → true
Number.isNaN(42)    // → false
Number.isNaN("hi")  // → false  (unlike global isNaN(), which coerces first)

// So to properly guard against bad numeric input:
if (typeof num !== "number" || Number.isNaN(num)) { ... }
// First check: is it not a number type at all? (catches strings, arrays, null…)
// Second check: is it NaN? (catches NaN, which deceives the typeof check)
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Syntax Error** | An error where code cannot be parsed because it violates JS syntax rules. Caught before execution. |
| **Logic Error** | An error where syntactically valid code runs but produces an incorrect result. Requires debugging to find. |
| **Linting** | Static analysis of source code to detect errors and style issues without running the code. ESLint is the standard JS linter. |
| **ESLint** | The industry-standard JavaScript linting tool. Can be installed as a VS Code extension for real-time error highlighting. |
| **`console.log(value)`** | Prints a value to the browser's JavaScript console for debugging inspection. |
| **`console.error(value)`** | Prints a value styled as an error and generates a call stack trace. |
| **Call Stack** | The ordered list of function calls that led to the current point in execution. Shown in console errors and the debugger. Top of the stack = current function; lower entries = callers. |
| **Breakpoint** | A marker set on a specific line in the debugger. Execution pauses there, allowing you to inspect variables. |
| **Scopes panel** | Section of the browser debugger showing all variables and their current values at the paused breakpoint. |
| **`throw`** | Statement that creates and throws an error, immediately stopping the current function and jumping to the nearest `catch` block. |
| **`new Error("message")`** | Creates an Error object with a `.message` property. Typically used with `throw`. |
| **`try...catch`** | Statement that wraps code that might fail (`try`) and provides a block to handle any errors (`catch`). Prevents application crashes. |
| **`error.message`** | Property on an `Error` object containing the human-readable error description passed to `new Error()`. |
| **`typeof`** | Operator returning a string identifying a value's type. Note: `typeof NaN` returns `"number"`. |
| **`Number.isNaN(value)`** | Returns `true` only if `value` is exactly `NaN`. More reliable than the global `isNaN()` because it doesn't coerce its argument. |
| **Guard Clause** | A conditional at the top of a function that validates input and returns early (or throws) if the data is invalid, preventing the main logic from running with bad data. |
| **Feature Detection** | A pattern for checking whether a browser API exists before using it, to safely handle environments where it isn't supported. |
| **Defensive Programming** | The practice of writing code that anticipates and handles bad input, edge cases, and failure modes before they cause crashes. |

---

## Watch Out For...

1. **`typeof NaN === "number"` — NaN deceives `typeof`.** To properly guard against NaN, you must check BOTH `typeof num !== "number"` AND `Number.isNaN(num)`. Using `typeof` alone will let NaN pass through.

2. **`throw` skips all code below it in the `try` block.** Once `throw` fires, execution immediately jumps to the nearest `catch`. Any lines after the `throw` in the same block are unreachable.

3. **Unhandled `throw` (without `try...catch`) marks the error "Uncaught".** An error only becomes "handled" when it is caught by a `catch` block. Without one, the browser shows "Uncaught Error" and halts script execution.

4. **`console.error()` does NOT throw an error — it just styles one.** Calling `console.error("oops")` logs a red message and a call stack but does NOT stop execution or trigger a `catch` block. Only `throw` does that.

5. **The debugger pauses on the breakpoint LINE, before it executes.** Variables set on that line are not yet updated — you see the state just before the line runs.

6. **A `var` loop variable is shared across all iterations' inner functions.** All click handlers created inside a `var`-based loop will close over the same `i` — its final value. Use `let` for block-scoped loop variables.

7. **When `fetch()` returns `[object Promise]`** — you've forgotten `await` or `.then()`. The function is asynchronous; the data arrives later. You must chain `.then()` or `await` the Promise before using the result.

8. **A `Response` object is not parsed JSON.** Even after correctly awaiting `fetch()`, you still have a `Response` — you must call `response.json()` (or `response.text()`) to get the body data.

9. **`error.message` vs. `error` — don't confuse the Error object with its message.** `console.error(error)` logs the full Error object (with stack). `console.error(error.message)` logs just the string message. Both are useful; know the difference.

10. **Feature detection uses `"property" in object`, not calling the method.** Write `"geolocation" in navigator`, NOT `navigator.geolocation()` — calling a non-existent method throws `TypeError`.

11. **Linting catches syntax and style errors, not logic errors.** ESLint can tell you a variable is undeclared, but it cannot tell you that your algorithm gives the wrong answer. Logic errors still require console logging or the debugger.

12. **`try...catch` does NOT catch errors in asynchronous callbacks by default.** A `try...catch` wrapping an async function call without `await` will not catch errors thrown inside the Promise. For async error handling, use `.catch()` on the Promise or `async/await` with `try...catch`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the difference between a **syntax error** and a **logic error**? Which is easier to find and why?

**Q2.** You run the following code and the console logs `"Response value: [object Promise]"`. What is wrong, and how do you fix it?
```js
const response = fetch("data.json");
console.log(`Response value: ${response}`);
showHeroes(response);
```

**Q3.** Explain what a **breakpoint** is and the three key things the debugger's **right-hand panel** shows you when execution is paused.

**Q4.** What is the output and execution order of this code? Trace through step by step.
```js
function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero.");
  }
  return a / b;
}

try {
  console.log("Start");
  console.log(divide(10, 0));
  console.log("End");
} catch (error) {
  console.error(error.message);
}

console.log("After try-catch");
```

**Q5.** Why must you write `typeof num !== "number" || Number.isNaN(num)` to guard against invalid numeric input? What would happen if you only wrote `typeof num !== "number"`?

---

## Answer Key

---

**A1.**

| | Syntax Error | Logic Error |
|---|---|---|
| **What it is** | Violates JS grammar rules; the engine can't parse the code | Syntactically valid code that produces the wrong result |
| **When caught** | Immediately — before any code runs | Only when the code executes and produces unexpected output |
| **Examples** | Missing `)`, unclosed string, `let let x = 1` | Using `+` instead of `*`; off-by-one index; wrong variable name |

**Syntax errors are easier to find** because the engine reports them immediately with a line number. Logic errors require actively running the code, inspecting intermediate values with `console.log()` or the debugger, and reasoning about what the correct output should be.

---

**A2.**

**Problem:** `fetch()` is asynchronous and returns a **Promise**, not the data. Assigning it to `response` without `await` or `.then()` gives you a pending Promise object, not the fetched JSON. `showHeroes(response)` receives a Promise, causing a `TypeError` when it tries to iterate over it.

**Fix using `.then()`:**
```js
fetch("data.json")
  .then((response) => response.json())   // parse the body
  .then((data) => {
    showHeroes(data);                   // now receives the actual JS object
  });
```

**Or using `async/await`:**
```js
async function load() {
  const response = await fetch("data.json");   // wait for HTTP response
  const data = await response.json();          // wait for body parsing
  showHeroes(data);
}
load();
```

---

**A3.**

A **breakpoint** is a marker set on a specific line in the debugger. When the browser reaches that line during execution, it **pauses** before executing it, allowing you to inspect the program's current state.

**Three key things shown in the right-hand panel when paused:**

1. **Breakpoints** — a list of all breakpoints you have set, with the line number and file.

2. **Call Stack** — the ordered list of functions that were called to reach the current point. The top entry is the function currently executing; each entry below it is the caller of the entry above. Clicking a stack entry shows the code at that point.

3. **Scopes** — every variable in every currently active scope (local function scope, block scope, global `Window`), with its current value. This is where you can spot `heroes = undefined` or `jsonObj = Response {}` and instantly identify the bug.

---

**A4.**

```
"Start"
↓
divide(10, 0) is called
  b === 0 → true
  throw new Error("Cannot divide by zero.")
  ← execution jumps DIRECTLY to catch — "End" is skipped
↓
catch receives the Error object
  console.error("Cannot divide by zero.")   ← logged
↓
"After try-catch"                           ← still runs, programme recovered
```

**Console output in order:**
1. `"Start"`
2. `"Cannot divide by zero."` (as an error)
3. `"After try-catch"`

Note: `"End"` is **never logged** because `throw` jumped execution immediately to `catch` before that line was reached. `"After try-catch"` runs because it is **outside** the `try...catch` block — the block was exited cleanly via the `catch`.

---

**A5.**

**Just `typeof num !== "number"` is not enough** because `typeof NaN === "number"` returns `true`. NaN has the data type `"number"` in JavaScript, even though it is "Not a Number" semantically. So a value of `NaN` would pass the `typeof` check and slip into the calculation, producing a result of `NaN` — which would silently corrupt any output.

**Why you need both conditions:**
```js
typeof NaN !== "number"   // → false! (NaN passes the typeof check)
Number.isNaN(NaN)         // → true   (correctly identifies NaN)

// Combined:
typeof NaN !== "number" || Number.isNaN(NaN)
// false || true → true ← correctly rejected
```

The `||` means "reject if EITHER the type is wrong OR the value is NaN", giving a complete guard against all non-numeric inputs including NaN.
