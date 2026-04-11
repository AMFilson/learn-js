# 🔀 JavaScript Conditionals — Exam Study Guide
**Source:** [MDN Web Docs — Making decisions in your code: Conditionals](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Conditionals)

---

## Executive Summary

JavaScript **conditional statements** allow a program to execute different blocks of code depending on whether a given condition evaluates to `true` or `false`, enabling dynamic, decision-based logic. The three primary tools covered are **`if...else`** (and its chained `else if` form), **`switch`** statements, and the **ternary operator** — each suited to different scenarios of complexity and readability. Understanding when to use each construct, how **truthy/falsy** values behave, and the correct use of **logical operators** (`&&`, `||`, `!`) are the core skills tested in this topic.

---

## Core Pillars

### 1. The `if...else` Statement

- The **fundamental branching structure** — runs one block of code if a condition is `true`, and a different block if it is `false`.
- The `else` clause is **optional** — omitting it means the second block always runs regardless of the condition.
- **Always use curly braces `{}`** — single-line omission (`if (x) doSomething();`) is valid but error-prone and not recommended.

```js
if (condition) {
  // runs if condition is true
} else {
  // runs if condition is false
}
```

---

### 2. `else if` — Chaining Multiple Conditions

- Chain **as many `else if` blocks as needed** between `if` and the final `else`.
- JavaScript evaluates conditions **top to bottom** and executes only the **first matching block**.
- The final `else` is the **"last resort"** fallback — runs only if all prior conditions are `false`.

```js
if (choice === "sunny") {
  // sunny logic
} else if (choice === "rainy") {
  // rainy logic
} else if (choice === "snowing") {
  // snowing logic
} else {
  // default / catch-all
}
```

---

### 3. Truthy & Falsy Values

- JavaScript evaluates **any value** as a boolean inside a condition.
- **Falsy values** (evaluate as `false`): `false`, `0`, `""` (empty string), `null`, `undefined`, `NaN`
- **Everything else** is **truthy** — including non-zero numbers, non-empty strings, objects, and arrays.
- This allows shorthand checks like `if (cheese)` instead of `if (cheese !== undefined && cheese !== "")`.

```js
let cheese = "Cheddar";
if (cheese) {
  console.log("Cheese is available!"); // runs — non-empty string is truthy
}

if (shoppingDone) {  // equivalent to: if (shoppingDone === true)
  childAllowance = 10;
} else {
  childAllowance = 5;
}
```

---

### 4. Nesting `if...else`

- You can place an `if...else` **inside another** `if...else` block to handle multi-variable conditions.
- Each nested statement is **independent** — the outer condition must be true before the inner one is even evaluated.

```js
if (choice === "sunny") {
  if (temperature < 86) {
    para.textContent = "Nice and sunny — let's go to the beach!";
  } else if (temperature >= 86) {
    para.textContent = "REALLY HOT! Put sunscreen on.";
  }
}
```

---

### 5. Logical Operators: `&&`, `||`, `!`

| Operator | Name | Behaviour |
|---|---|---|
| `&&` | **AND** | Both sides must be `true` for the whole expression to be `true` |
| `\|\|` | **OR** | At least one side must be `true` for the whole expression to be `true` |
| `!` | **NOT** | Inverts / negates the boolean value of the expression |

```js
// AND — both conditions must be true
if (choice === "sunny" && temperature < 86) { ... }

// OR — either condition can be true
if (iceCreamVanOutside || houseStatus === "on fire") { ... }

// NOT — negates the OR result
if (!(iceCreamVanOutside || houseStatus === "on fire")) { ... }

// Complex combinations
if ((x === 5 || y > 3 || z <= 10) && (loggedIn || userName === "Steve")) { ... }
```

---

### 6. `switch` Statements

- Best for cases where **one variable** needs to be matched against **many specific values** — cleaner than a long `else if` chain.
- **Structure:** `switch(expression)` → `case value:` → code → **`break`** → repeat → `default:`
- The `break` keyword is **critical** — without it, execution **falls through** to the next case.
- `default` is the fallback equivalent of a final `else`; it is optional but recommended when unknown values are possible.

```js
switch (choice) {
  case "sunny":
    para.textContent = "It is nice and sunny!";
    break;
  case "rainy":
    para.textContent = "Take a rain coat.";
    break;
  case "snowing":
    para.textContent = "It is freezing!";
    break;
  default:
    para.textContent = "";
}
```

---

### 7. The Ternary Operator

- A **compact, single-line** conditional expression — ideal for **simple two-outcome** decisions.
- Syntax: `condition ? valueIfTrue : valueIfFalse`
- Can be used to assign values **or** execute functions/expressions inline.
- **Avoid nesting** ternaries — it makes code unreadable.

```js
// Assigning a value
const greeting = isBirthday
  ? "Happy birthday!"
  : "Good morning.";

// Calling a function inline
select.addEventListener("change", () =>
  select.value === "black"
    ? update("black", "white")
    : update("white", "black")
);
```

---

## Technical Deep-Dive

### Logic Walkthrough: Weather App (`if...else if` + Logical Operators)

This is the canonical `else if` chain example from MDN, demonstrating how to handle multiple discrete string values:

```js
function setWeather() {
  const choice = select.value;  // get current dropdown value

  if (choice === "sunny") {
    para.textContent = "Wear shorts!";
  } else if (choice === "rainy") {
    para.textContent = "Take a rain coat.";
  } else if (choice === "snowing") {
    para.textContent = "Stay in with hot chocolate!";
  } else if (choice === "overcast") {
    para.textContent = "Take a rain coat just in case.";
  } else {
    para.textContent = "";  // fallback: clears text if no valid choice
  }
}
```

**Key logic points:**
- Uses **strict equality** (`===`), not loose equality (`==`) — these compare both value AND type.
- The final `else` clears the paragraph — handles the "Make a choice --" placeholder case.
- An event listener on `"change"` fires this function every time the dropdown changes.

---

### Logic Walkthrough: Calendar App (`if...else if` with `||`)

This exercise shows using **OR** to group months with the same number of days, avoiding redundant cases:

```js
function createCalendar(month) {
  let days = 31;  // default: most months have 31 days

  if (month === "February") {
    days = 28;    // specific exception first
  } else if (
    month === "April"     ||
    month === "June"      ||
    month === "September" ||
    month === "November"
  ) {
    days = 30;    // group of 30-day months via OR
  }
  // All other months remain at the default of 31
}
```

**Key logic points:**
- Set the **most common value as the default** above the conditional, then only handle the exceptions.
- Using `||` within a single `else if` is far cleaner than writing four separate `else if` blocks.
- **February** must be checked first as its own specific case (28 days, ignoring leap years here).

---

### Logic Walkthrough: Theme Switcher (Ternary → Switch)

The `switch` version scales the earlier ternary (2 choices) to 5 choices cleanly:

```js
switch (choice) {
  case "black":       update("black", "white");   break;
  case "white":       update("white", "black");   break;
  case "purple":      update("purple", "white");  break;
  case "yellow":      update("yellow", "purple"); break;
  case "psychedelic": update("lime", "purple");   break;
}
```

**Why `switch` over ternary here?** The ternary only supports **two outcomes**. Once you have 3+ branches all testing the same variable, `switch` is the readable choice. The `break` after each `case` is **mandatory** — without it, execution cascades into the next case.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Conditional statement** | A code structure that runs different blocks of code depending on whether a condition evaluates to `true` or `false`. |
| **`if` statement** | The basic conditional keyword. Executes its code block only when the given condition is `true`. |
| **`else`** | An optional clause paired with `if`. Its block runs only when the `if` condition is `false`. |
| **`else if`** | Chains an additional condition to an `if` block, evaluated only if all preceding `if`/`else if` conditions were `false`. |
| **Nested conditional** | An `if...else` statement placed inside the block of another `if...else`, allowing multi-variable decision trees. |
| **Comparison operator** | Operators used to test conditions: `===`, `!==`, `<`, `>`, `<=`, `>=`. All return `true` or `false`. |
| **Strict equality (`===`)** | Checks that two values are identical in both **value AND type**. Preferred over loose equality (`==`). |
| **Truthy value** | Any value that evaluates to `true` in a boolean context. Includes non-zero numbers, non-empty strings, objects, arrays. |
| **Falsy value** | Any value that evaluates to `false` in a boolean context: `false`, `0`, `""`, `null`, `undefined`, `NaN`. |
| **Logical AND (`&&`)** | Returns `true` only if **both** operands are truthy. Short-circuits if the first is falsy. |
| **Logical OR (`\|\|`)** | Returns `true` if **at least one** operand is truthy. Short-circuits if the first is truthy. |
| **Logical NOT (`!`)** | Negates / inverts a boolean expression. `!true` → `false`, `!false` → `true`. |
| **`switch` statement** | A conditional that matches one expression against multiple `case` values and runs the matching block. |
| **`case`** | A keyword in a `switch` block that defines a value to match against the switch expression. |
| **`break`** | Halts execution at the end of a `case` block, preventing fall-through to subsequent cases. |
| **`default`** | The fallback clause in a `switch` statement; runs when no `case` matches. Equivalent to a final `else`. |
| **Fall-through** | The behaviour when a `break` is omitted from a `switch case` — execution continues into the next case unintentionally. |
| **Ternary operator** | A compact 3-part conditional: `condition ? valueIfTrue : valueIfFalse`. Suited for simple two-outcome decisions. |

---

## Watch Out For...

1. **`=` vs `==` vs `===`**: In a conditional, always use **`===`** (strict equality). Using `=` inside an `if()` is an assignment, not a comparison — it will always evaluate as truthy (a common bug). Loose `==` causes type coercion surprises (e.g., `0 == false` is `true`).

2. **Missing `break` in `switch`.** Forgetting `break` causes **fall-through**: the matched case runs, then *keeps running* subsequent cases until a `break` is hit or the block ends. This is almost never what you want.

3. **The OR shortcut trap.** `if (x === 5 || 7 || 10)` does NOT check if x equals 5, 7, or 10. It checks `(x === 5)` OR `(7)` OR `(10)` — and since `7` is always truthy, the condition is always `true`. Correct form: `if (x === 5 || x === 7 || x === 10)`.

4. **`else` without braces silently breaks logic.** Code written after a brace-less `if` is not part of the conditional and **always runs**, which can introduce subtle bugs that are hard to trace.

5. **Truthy/falsy confusion with intentional zeroes.** If `0` is a valid meaningful value in your program (e.g., a score), `if (score)` will fail when score is `0` (falsy). Use the explicit check `if (score !== undefined)` instead.

6. **Ternary overuse / nesting.** Ternaries are meant for simple two-outcome assignments. Nested ternaries (`a ? b : c ? d : e`) are nearly unreadable. Use `if...else if` or `switch` instead.

7. **`else if` order matters — first match wins.** Conditions are tested sequentially. If a broader condition is placed before a more specific one, the specific one may never be reached. Order your conditions from most-specific to least-specific.

8. **`switch` uses strict equality (`===`).** Switch cases compare using `===`, not `==`. So `switch("1")` will NOT match `case 1:` (number vs. string mismatch).

9. **Not using `default` in `switch`.** If an unexpected value reaches a switch with no `default`, it silently does nothing. Always add `default` to handle unknown inputs gracefully.

10. **Truthy booleans don't need comparison.** Writing `if (isLoggedIn === true)` is redundant. `if (isLoggedIn)` is equivalent and preferred. Similarly, `if (isLoggedIn === false)` should be written as `if (!isLoggedIn)`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the **six falsy values** in JavaScript? Why does it matter in the context of conditionals?

**Q2.** What is the difference between a **ternary operator** and an `if...else` statement? When would you choose one over the other?

**Q3.** The following code always logs `"You should leave!"` regardless of the value of `x`. Why? How do you fix it?
```js
if (x === 5 || 7 || 10) {
  console.log("You should leave!");
}
```

**Q4.** What happens if you forget to include `break` at the end of a `switch case`? Give a specific term for this behaviour.

**Q5.** Rewrite the following `if...else if` chain as a `switch` statement:
```js
if (day === "Monday")    { console.log("Start of the week."); }
else if (day === "Friday") { console.log("End of the week!"); }
else                     { console.log("Midweek."); }
```

---

## Answer Key

---

**A1.**
The six falsy values are: **`false`**, **`0`**, **`""`** (empty string), **`null`**, **`undefined`**, and **`NaN`**.

It matters because JavaScript implicitly converts values to `true` or `false` inside `if()` conditions. You can use shorthand like `if (username)` to check that a variable exists AND has a non-empty value — without writing multiple explicit comparisons. The danger is when `0` or other falsy values are intentionally valid, in which case you must use an explicit check.

---

**A2.**
- **Ternary**: `condition ? valueIfTrue : valueIfFalse` — a single-line expression, returns a value, best for **simple two-outcome** assignments or inline function calls.
- **`if...else`**: a full statement block, can contain multiple lines of logic, used for **complex branching**, side effects, or more than two outcomes.

Choose **ternary** when assigning a variable or passing an argument with a simple true/false condition. Choose **`if...else`** when the branches contain multi-line code or you have more than two outcomes.

---

**A3.**
The condition `x === 5 || 7 || 10` is parsed as `(x === 5) || (7) || (10)`. Since `7` is always **truthy**, the entire OR expression is always `true`, regardless of `x`.

**Fix:**
```js
if (x === 5 || x === 7 || x === 10) {
  console.log("You should leave!");
}
```
Each side of every `||` must be a **complete, independent comparison**.

---

**A4.**
Without `break`, execution **falls through** into the next `case` block and continues running until it hits another `break` or the end of the `switch`. This behaviour is called **fall-through**. It is almost always a bug, though it can occasionally be used intentionally to share code between cases.

---

**A5.**
```js
switch (day) {
  case "Monday":
    console.log("Start of the week.");
    break;
  case "Friday":
    console.log("End of the week!");
    break;
  default:
    console.log("Midweek.");
}
```
Note: `default` does **not** require a `break` since it is always the last block, but adding one is harmless and consistent.
