# 🔁 JavaScript Loops — Exam Study Guide
**Source:** [MDN Web Docs — Looping code](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Loops)

---

## Executive Summary

JavaScript **loops** allow a block of code to execute repeatedly without writing it out multiple times — they are the primary tool for automating repetitive tasks and processing collections of data. The four loop types covered are **`for`** (count-controlled), **`for...of`** (collection iteration), **`while`** (condition-controlled), and **`do...while`** (guarantees at least one execution), each suited to a specific scenario. Mastering the **three core components** of a loop (initializer, condition, final-expression), along with **`break`** and **`continue`** for flow control, is the central skill tested in this topic.

---

## Core Pillars

### 1. Why Loops? The Core Motivation

- Without loops, repeating an action 100 times requires writing the same code 100 times — **unscalable and unmaintainable**.
- Loops let you run the same code block repeatedly, with only **one number to change** to scale from 10 to 10,000 iterations.
- Loops are most commonly used to **iterate over collections** (arrays, sets, maps) and **perform a fixed number of operations**.

```js
// Without a loop — repetitive and fragile:
ctx.beginPath(); ctx.arc(...); ctx.fill();
ctx.beginPath(); ctx.arc(...); ctx.fill();
// ... × 100

// With a loop — clean and scalable:
for (let i = 0; i < 100; i++) {
  ctx.beginPath(); ctx.arc(...); ctx.fill();
}
```

---

### 2. `for...of` — Iterating Over a Collection

- The **simplest and preferred** way to loop through every item in an array (or any iterable).
- Syntax: `for (const item of collection) { ... }`
- On each iteration, `item` is automatically assigned the next element — **no index needed**.
- Use `const` for the loop variable (re-assigned each iteration, not mutated).

```js
const cats = ["Leopard", "Serval", "Jaguar", "Tiger", "Caracal", "Lion"];

for (const cat of cats) {
  console.log(cat); // logs each name in order
}
```

---

### 3. `map()` and `filter()` — Functional Alternatives for Collections

- **`map(fn)`**: Calls `fn` on every element and returns a **new array** of results. Use when you want to **transform** every item.
- **`filter(fn)`**: Calls `fn` on every element; includes the item in the new array only if `fn` returns **`true`**. Use when you want to **select a subset**.
- Neither method mutates the original array.

```js
const cats = ["Leopard", "Serval", "Jaguar", "Tiger", "Caracal", "Lion"];

// map — transform each item to uppercase
const upperCats = cats.map((cat) => cat.toUpperCase());
// ["LEOPARD", "SERVAL", "JAGUAR", "TIGER", "CARACAL", "LION"]

// filter — keep only names that start with "L"
const lCats = cats.filter((cat) => cat.startsWith("L"));
// ["Leopard", "Lion"]
```

---

### 4. The Standard `for` Loop — Count-Controlled Iteration

- Best when you need to run code a **specific number of times**, or when you need the **current index** inside the loop body.
- Syntax: `for (initializer; condition; final-expression) { ... }`
- All three header parts are separated by **semicolons**.

| Part | Role | Example |
|---|---|---|
| **Initializer** | Declare & set the counter variable | `let i = 0` |
| **Condition** | Keep looping while this is `true` | `i < 10` |
| **Final-expression** | Run after each iteration (usually increment) | `i++` |

```js
// Prints squares of numbers 1–9
for (let i = 1; i < 10; i++) {
  const newResult = `${i} x ${i} = ${i * i}`;
  results.textContent += `${newResult}\n`;
}
// When i hits 10, condition (i < 10) is false → loop stops
```

---

### 5. Using `for` to Iterate Arrays (vs. `for...of`)

- A `for` loop can replace `for...of` to iterate an array using its **index**: `array[i]`.
- Necessary when you need to **know the index position** (e.g., to handle the last element differently).
- More error-prone than `for...of` — prefer `for...of` unless index access is required.

```js
const cats = ["Pete", "Biggles", "Jasmine"];
let result = "My cats are called ";

// for...of can't easily detect "last item" — use for instead:
for (let i = 0; i < cats.length; i++) {
  if (i === cats.length - 1) {
    result += `and ${cats[i]}.`;   // last item: add "and" + full stop
  } else {
    result += `${cats[i]}, `;      // all others: add comma + space
  }
}
// "My cats are called Pete, Biggles, and Jasmine."
```

---

### 6. `break` — Exiting a Loop Early

- `break` **immediately terminates** the entire loop and jumps to the code after it.
- Used when you've found what you're looking for and further iterations are unnecessary.
- Works the same in `for`, `for...of`, `while`, and `do...while`.

```js
for (const contact of contacts) {
  const splitContact = contact.split(":");
  if (splitContact[0].toLowerCase() === searchName) {
    para.textContent = `${splitContact[0]}'s number is ${splitContact[1]}.`;
    break;  // ← stop searching once found
  }
}
```

---

### 7. `continue` — Skipping an Iteration

- `continue` **skips the rest of the current iteration** and jumps directly to the next one.
- The loop does **not** stop — it continues from the top with the next value.
- Used to filter out unwanted iterations without restructuring the entire loop body.

```js
for (let i = 1; i <= num; i++) {
  let sqRoot = Math.sqrt(i);
  if (Math.floor(sqRoot) !== sqRoot) {
    continue;  // ← skip non-perfect-squares
  }
  para.textContent += `${i} `;  // only reaches here for perfect squares
}
```

---

### 8. `while` Loop — Condition-Controlled

- Runs as long as the condition is `true`. The **condition is checked BEFORE each iteration**.
- If the condition is `false` from the start, the loop body **never runs**.
- The initializer is declared **outside** the loop; the final-expression is placed **inside** the loop body.

```js
let i = 0;
while (i < cats.length) {
  // loop body
  i++;  // ← final-expression must be inside the body
}
```

---

### 9. `do...while` Loop — Guaranteed First Execution

- Like `while`, but the **condition is checked AFTER each iteration**.
- Guarantees the loop body runs **at least once**, even if the condition is immediately `false`.

```js
let i = 0;
do {
  // loop body — always runs at least once
  i++;
} while (i < cats.length);
```

**Key distinction:**

| Loop | Condition check | Min executions |
|---|---|---|
| `while` | **Before** each iteration | **0** (may never run) |
| `do...while` | **After** each iteration | **1** (always runs once) |
| `for` | **Before** each iteration | **0** (may never run) |

---

### 10. Choosing the Right Loop

| Scenario | Recommended Loop |
|---|---|
| Iterating every item in an array/collection, no index needed | **`for...of`** |
| Transforming every item in a collection → new array | **`map()`** |
| Filtering items from a collection → new array | **`filter()`** |
| Fixed number of repetitions, or index access needed | **`for`** |
| Condition-controlled, may run 0 times | **`while`** |
| Must run at least once before checking condition | **`do...while`** |

---

## Technical Deep-Dive

### Logic Walkthrough: Contact Search with `break`

This shows combining `for...of`, string splitting, conditional logic, and `break` into a real search function:

```js
const contacts = [
  "Chris:2232322",
  "Sarah:3453456",
  "Bill:7654322",
];

btn.addEventListener("click", () => {
  const searchName = input.value.toLowerCase(); // normalize case

  for (const contact of contacts) {
    const splitContact = contact.split(":");     // ["Chris", "2232322"]

    if (splitContact[0].toLowerCase() === searchName) {
      para.textContent = `${splitContact[0]}'s number is ${splitContact[1]}.`;
      break;  // found — stop iterating immediately
    }
  }

  if (para.textContent === "") {
    para.textContent = "Contact not found.";  // post-loop fallback
  }
});
```

**Key logic points:**
- `.toLowerCase()` on both sides makes the search **case-insensitive**.
- `break` prevents wasted iterations after a match — critical for performance at scale.
- The `if (para.textContent === "")` **after** the loop detects the "not found" case — the paragraph only stays empty if no match triggered the `break`.

---

### Logic Walkthrough: Countdown with `while` + Decrement (`i--`)

This exercise demonstrates counting **down** rather than up, and mixing loop logic with DOM manipulation:

```js
let i = 10;

while (i >= 0) {             // condition: keep going until i goes below 0
  const para = document.createElement("p");

  if (i === 10) {
    para.textContent = `Countdown ${i}`;
  } else if (i === 0) {
    para.textContent = "Blast off!";
  } else {
    para.textContent = i;
  }

  output.appendChild(para);
  i--;                       // ← decrement, not increment
}
```

**Key logic points:**
- The condition is `i >= 0` — the loop includes `0` (Blast off!) before stopping.
- `i--` decrements the counter. Forgetting this creates an **infinite loop**.
- This cannot be a `for...of` — there's no collection. A `for` or `while` is appropriate.

---

### Logic Walkthrough: Guest List with `for...of` + `slice()`

This combines a loop with a conditional and a string clean-up trick using `.slice(0, -2)`:

```js
const people = ["Chris", "Anne", "Colin", "Phil", "Lola", "Sam"];

for (const person of people) {
  if (person === "Phil" || person === "Lola") {
    refused.textContent += `${person}, `;   // add to refused list
  } else {
    admitted.textContent += `${person}, `;  // add to admitted list
  }
}

// Clean up trailing ", " and add full stop
refused.textContent  = `${refused.textContent.slice(0, -2)}.`;
admitted.textContent = `${admitted.textContent.slice(0, -2)}.`;
```

**Key logic points:**
- Every item appends `", "` — so after the loop ends, there's an unwanted trailing comma-space.
- `.slice(0, -2)` removes the **last 2 characters** — a clean idiom for trimming trailing delimiters.
- This pattern (build in loop, trim after) is extremely common and exam-testable.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Loop** | A code structure that repeats a block of code multiple times until a specified condition becomes `false`. |
| **Iteration** | A single pass through a loop's code block. Each time the loop body runs once = one iteration. |
| **`for` loop** | A count-controlled loop with three header parts (initializer; condition; final-expression) separated by semicolons. |
| **`for...of` loop** | A loop that iterates over every item in a collection (array, Set, etc.), auto-assigning each item to a variable. |
| **`while` loop** | A condition-controlled loop that checks its condition **before** each iteration. May run 0 times. |
| **`do...while` loop** | Like `while`, but checks its condition **after** each iteration — guarantees at least one execution. |
| **Initializer** | The variable declared at the start of a `for` loop to serve as the counter. Example: `let i = 0`. |
| **Condition** | The boolean expression checked each iteration to decide if the loop should continue. |
| **Final-expression** | The expression run at the end of each `for` loop iteration, typically incrementing/decrementing the counter. |
| **Counter variable** | The variable (usually `i`) used to track how many iterations have occurred. |
| **`break`** | A statement that immediately exits the entire loop and moves to the code following it. |
| **`continue`** | A statement that skips the remainder of the current iteration and jumps to the next one. |
| **Infinite loop** | A loop whose condition never becomes `false`, causing the browser to freeze or crash. Caused by a missing or incorrect final-expression. |
| **`map(fn)`** | An array method that calls `fn` on every element and returns a **new array** of the results. Non-mutating. |
| **`filter(fn)`** | An array method that calls `fn` on every element and returns a **new array** of elements for which `fn` returned `true`. Non-mutating. |
| **Decrement (`i--`)** | Subtracts 1 from a variable. Used in countdown loops where you iterate downward. Opposite of `i++`. |

---

## Watch Out For...

1. **Off-by-one errors with `for` on arrays.** When using a `for` loop on an array, start at `i = 0` (not 1), and use `i < array.length` (not `i <= array.length`). Using `<=` will access `array[array.length]` which is `undefined`.

2. **Forgetting the final-expression → infinite loop.** In a `while` or `do...while` loop, the counter increment/decrement (`i++` or `i--`) must be inside the loop body. Forgetting it means the condition never becomes `false` and the browser hangs.

3. **`break` vs. `continue` confusion.** `break` **exits the loop entirely**. `continue` **skips to the next iteration** — the loop keeps going. They are not interchangeable and each produces different output.

4. **`for...of` can't tell you the current index.** If you need to know whether you're on the last item (e.g., for formatting the final element differently), you **must use a standard `for` loop** with an index variable. `for...of` does not expose the index.

5. **`map()` and `filter()` require you to capture the return value.** These methods return a **new array** — they do not modify the original. Writing `cats.map(toUpper);` on its own discards the result. Always assign: `const result = cats.map(toUpper);`.

6. **`do...while` always runs at least once — even if the condition starts false.** If your logic requires the option of 0 executions, use `while` or `for`. Using `do...while` when the initial condition may be false can cause unintended behaviour.

7. **Counting down needs `i--`, not `i++`.** A countdown loop starting at 10 and going to 0 needs `i--` (decrement) and a condition like `i >= 0`. Using `i++` in a countdown creates an infinite loop going upward.

8. **`while (i >= 0)` vs. `while (i > 0)`.** The `>=` version includes `0` in the loop; `>` does not. This matters in countdowns where `0` is a meaningful value (e.g., "Blast off!").

9. **`filter()` callback must return a boolean.** If your `filter` callback doesn't explicitly return `true`/`false` (or a truthy/falsy value), all items will be excluded (implicit `undefined` return = falsy).

10. **`for` loop initializer must use `let`, not `const`.** The counter variable is reassigned every iteration (`i++`), so it must be declared with `let`. Using `const` will throw a `TypeError`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the **three parts** of a standard `for` loop header, and what does each one do?

**Q2.** What is the **key difference** between `break` and `continue`? What does each one do to the loop?

**Q3.** When would you choose a **`for` loop** over a **`for...of`** loop to iterate over an array? Give a concrete example of a situation where `for...of` can't do the job.

**Q4.** What is the critical difference between a **`while`** loop and a **`do...while`** loop? When is `do...while` the right choice?

**Q5.** The following code has a bug — it produces an infinite loop. Identify the problem and fix it.
```js
let i = 0;
while (i < 5) {
  console.log(i);
}
```

---

## Answer Key

---

**A1.**
The three parts of a `for` loop header are:

| Part | Purpose |
|---|---|
| **Initializer** (`let i = 0`) | Declares and sets the counter variable before the loop starts |
| **Condition** (`i < 10`) | Checked before each iteration — loop continues while `true`, stops when `false` |
| **Final-expression** (`i++`) | Runs at the end of each iteration — typically increments (or decrements) the counter |

```js
for (let i = 0; i < 10; i++) { ... }
//    ↑ initializer  ↑ condition  ↑ final-expression
```

---

**A2.**
- **`break`**: **Exits the entire loop immediately.** Execution jumps to the code following the closing `}` of the loop.
- **`continue`**: **Skips the rest of the current iteration only.** The loop jumps back to the top and checks the condition for the next iteration — the loop itself continues running.

Think of it as: `break` = "stop the whole loop"; `continue` = "skip this round, but keep going".

---

**A3.**
Use a **`for` loop** over `for...of` when you need access to the **current index position** inside the loop body.

The classic example: handling the **last element differently** (e.g., formatting a list with "and" before the final item):

```js
for (let i = 0; i < cats.length; i++) {
  if (i === cats.length - 1) {
    result += `and ${cats[i]}.`;  // only possible because we know i
  } else {
    result += `${cats[i]}, `;
  }
}
```

`for...of` gives you the value but no way to check if it's the last one — you'd need the index for that.

---

**A4.**
- **`while`**: Checks its condition **before** the first iteration. If the condition is `false` from the start, the body **never runs** (0 executions possible).
- **`do...while`**: Checks its condition **after** the first iteration. The body **always runs at least once**, regardless of the starting condition.

Use `do...while` when you have logic that must execute at least once before you know whether to continue — for example, prompting a user for input and only stopping once they give valid data.

---

**A5.**
**Problem:** The loop never increments `i`, so `i` stays at `0` forever, the condition `i < 5` is always `true`, and the loop never ends — this is an **infinite loop**.

**Fix:** Add `i++` inside the loop body:
```js
let i = 0;
while (i < 5) {
  console.log(i);
  i++;  // ← missing final-expression added here
}
```
Alternatively, rewrite as a `for` loop where the final-expression is built into the header and harder to forget:
```js
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```
