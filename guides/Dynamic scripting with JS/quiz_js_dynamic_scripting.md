# 🧠 Practice Quiz: Dynamic Scripting with JS

## Section 1: Arrays & Conditionals

### Question 1: Accessing Array Bounds

Consider the following array:

```js
const stack = ["Gold", "Silver", "Platinum", "Bronze"];
```

What is the result of accessing `stack[stack.length]` and what is the last valid index for this array?

- A) `"Bronze"`; Index 4
- B) `undefined`; Index 3
- C) `null`; Index 4
- D) `ReferenceError`; Index 3

<details>
<summary><b>Hint</b></summary>
Array length is a count of items, while indexing is zero-based. What happens when you try to access a count that points past the last item?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** In JavaScript, arrays are zero-indexed. The `length` property returns the count of items (4), but the last item is at index `length - 1` (3). Accessing an index equal to the length (`stack[4]`) results in `undefined` because that position does not exist in the array's memory map.
- **Why A is incorrect:** Index 4 is out of bounds; the last item is at index 3.
- **Why C is incorrect:** JavaScript returns `undefined` for missing keys/indexes, not `null` (which represents intentional absence).
- **Why D is incorrect:** Accessing an out-of-bounds index doesn't throw a `ReferenceError`; it simply returns the primitive value `undefined`.
</details>

---

### Question 2: The `push()` Method Return Value

A developer runs the following code:

```js
const colors = ["Red", "Green"];
const result = colors.push("Blue", "Yellow");
```

What is the value of `result`?

- A) `["Red", "Green", "Blue", "Yellow"]`
- B) `["Blue", "Yellow"]`
- C) `4`
- D) `True`

<details>
<summary><b>Hint</b></summary>
Mutating methods like `push()` and `pop()` have specific return values. Does `push()` return the array itself or information about its size?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The `push()` method adds elements to the end of an array and returns the **new length** of that array as an integer. Since we added two elements to an array of two, the new length is 4.
- **Why A is incorrect:** This is the resulting state of the `colors` array, but not the value returned by the method call.
- **Why B is incorrect:** This would be a subset of the added items, but `push` does not return the items added.
- **Why D is incorrect:** `push()` returns a number, not a boolean.
</details>

---

### Question 3: Logical OR Short-circuiting

Evaluate the following condition:

```js
const x = 0;
const y = "Default";
const result = x || y;
```

What is the value of `result`, and why?

- A) `0`; because the first item in an OR operation is always returned.
- B) `false`; because 0 evaluates to false.
- C) `"Default"`; because 0 is a falsy value and the operator moves to the next truthy value.
- D) `undefined`; because OR requires booleans on both sides.

<details>
<summary><b>Hint</b></summary>
JavaScript's logical OR (`||`) doesn't just return true/false; it returns the value of the first "truthy" expression it finds.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** In JavaScript, `0` is one of the six falsy values. The `||` operator evaluates from left to right. When it hits a falsy value (0), it "short-circuits" and moves to the second operand. Since `"Default"` (a non-empty string) is truthy, it is returned.
- **Why A is incorrect:** OR returns the first _truthy_ value, not just the first value.
- **Why B is incorrect:** While 0 evaluates to false in a boolean context, the operator returns the actual value of the second operand in this shortcut pattern.
- **Why D is incorrect:** Logical operators in JS can operate on any data types through type coercion (truthy/falsy logic).
</details>

---

### Question 4: Array Mutation via `const`

Why is the following code technically valid in JavaScript?

```js
const items = [1, 2, 3];
items.pop();
items[0] = 99;
```

- A) `const` only prevents the variable itself from being reassigned, but the underlying object/array can still be mutated in place.
- B) Arrays are primitives and `const` doesn't apply to primitives.
- C) `pop()` creates a new array automatically, bypassing the `const` restriction.
- D) The code is actually invalid and will throw a `TypeError`.

<details>
<summary><b>Hint</b></summary>
Think about the difference between a variable "pointing" to a box and the "contents" of that box.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** In JavaScript, `const` creates a read-only reference to a value. However, it does not make the value itself immutable if that value is an object or an array. You cannot reassign the variable `items` to a new array (`items = []`), but you can modify the properties or elements of the existing array referenced by `items`.
- **Why B is incorrect:** Arrays are reference types (objects), not primitives.
- **Why C is incorrect:** `pop()` mutates the original array; it does not return a new one.
- **Why D is incorrect:** The code is standard, valid JavaScript.
</details>

---

### Question 5: `switch` Statement Fall-through

What will be logged to the console by the following code?

```js
const grade = "B";
let result = "";

switch (grade) {
  case "A":
    result = "Excellent";
  case "B":
    result = "Good";
  case "C":
    result = "Average";
  default:
    result = "Failed";
}
console.log(result);
```

- A) `"Good"`
- B) `"Failed"`
- C) `"GoodAverageFailed"`
- D) `""`

<details>
<summary><b>Hint</b></summary>
Look closely for the `break` keyword. What happens in a `switch` when a case matches but there's nothing to stop the execution?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is a classic example of **fall-through**. The switch matches `case "B"`, setting `result` to `"Good"`. However, because there is no `break` statement, the execution continues into `case "C"` (overwriting result with `"Average"`) and finally into the `default` block (overwriting result with `"Failed"`).
- **Why A is incorrect:** This would only be true if a `break` was placed after the "B" case.
- **Why C is incorrect:** This would only happen if we were using `result +=` (concatenation), not `=` (reassignment).
- **Why D is incorrect:** The switch does match "B," so the variable is definitely assigned.
</details>

---

### Question 6: Truthy/Falsy with Empty Containers

In the following conditional check, will the code inside the block execute?

```js
const list = [];
if (list) {
  console.log("Found items!");
}
```

- A) No, because empty arrays are considered falsy.
- B) No, because `[].length` is 0.
- C) Yes, because all objects (including arrays) are truthy, even if they are empty.
- D) Only if the array is converted to a string first.

<details>
<summary><b>Hint</b></summary>
Which specific values are "falsy" in JavaScript? Is an empty array `[]` on that list?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** In JavaScript, the only falsy values are `false`, `0`, `""`, `null`, `undefined`, and `NaN`. An empty array `[]` is an object, and all objects (even `{}`, `[]`, or `new Boolean(false)`) are **truthy**. Therefore, the conditional evaluates to true and the code executes.
- **Why A is incorrect:** This is a common misconception; while `""` is falsy, `[]` is not.
- **Why B is incorrect:** While the length is 0, the array _itself_ is truthy. To check for content, you must explicitly check `list.length > 0`.
- **Why D is incorrect:** Type conversion happens automatically in an `if` condition, but it converts to Boolean, not string.
</details>

---

### Question 7: String to Array via `split()`

A string contains `"2024-04-13"`. Which method call converts this into the array `["2024", "04", "13"]`?

- A) `dateString.join("-")`
- B) `Array.from(dateString, "-")`
- C) `dateString.split("-")`
- D) `dateString.splice("-")`

<details>
<summary><b>Hint</b></summary>
One of these methods belongs to the `String` object and "breaks" a string apart into a list based on a separator.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `split()` is a method on the `String` prototype. It takes a separator string (in this case `"-"`) and returns an array of substrings created by cutting the original string at every occurrence of that separator.
- **Why A is incorrect:** `join()` is an **Array** method used to combine a list back into a single string.
- **Why B is incorrect:** `Array.from()` converts iterables like NodeLists into arrays, but its second argument is a mapping function, not a separator string.
- **Why D is incorrect:** `splice()` is an **Array** method used to add/remove elements at specific indexes; it does not exist on the `String` prototype.
</details>

---

### Question 8: The Ternary Operator for Assignment

Which code block is functionally identical to the following ternary?

```js
const status = age >= 18 ? "Adult" : "Minor";
```

- A) `let status; if (age >= 18) { status = "Adult" } else { status = "Minor" }`
- B) `const status = age >= 18 && "Adult" || "Minor"`
- C) `const status = if (age >= 18) "Adult" else "Minor"`
- D) Both A and B.

<details>
<summary><b>Hint</b></summary>
Ternaries are expressions that return a value. Standard `if` statements are blocks of code.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** D

**Rationale:**

- **Why D is optimal/correct:** Option A is the standard `if...else` equivalent of a ternary. Option B is a "shortcut" pattern using logical short-circuiting: if `age >= 18` is true, the `&&` returns `"Adult"`. Since `"Adult"` is truthy, the `||` stops and returns it. If `age >= 18` is false, the `&&` stops at the falsy value, and the `||` moves to `"Minor"`.
- **Why C is incorrect:** `if` statements cannot be used as expressions on the right side of a `const` assignment in vanilla JavaScript.
</details>

---

### Question 9: Removing Specific Items with `splice()`

Given the array `const fruits = ["Apple", "Banana", "Cherry", "Date"]`, what is the correct code to remove `"Banana"` and `"Cherry"` from the middle?

- A) `fruits.splice(1, 2)`
- B) `fruits.splice(1, 1)`
- C) `fruits.slice(1, 3)`
- D) `fruits.pop(1, 2)`

<details>
<summary><b>Hint</b></summary>
The `splice()` method takes two main parameters: the *starting index* and the *count* of items to remove.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** `"Banana"` is at index 1. To remove both it and the following item (`"Cherry"`), we start at index 1 and provide a count of 2. `splice(1, 2)` performs this mutation in place.
- **Why B is incorrect:** This would only remove `"Banana"`.
- **Why C is incorrect:** `slice()` (with a 'c') returns a copy of a portion of the array; it does not modify the original array.
- **Why D is incorrect:** `pop()` does not take index or count arguments; it only ever removes the single last item.
</details>

---

### Question 10: Strict Equality with Primitives

What does the expression `(10 == "10" && 10 === "10")` evaluate to?

- A) `true`
- B) `false`
- C) `undefined`
- D) `TypeError`

<details>
<summary><b>Hint</b></summary>
Loose equality (`==`) performs type coercion, while strict equality (`===`) requires the types to be identical.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** The first part `10 == "10"` is true because loose equality converts the string to a number for comparison. The second part `10 === "10"` is false because strict equality checks the type, and `Number` is not equal to `String`. Since one side of the `&&` is false, the whole expression is **false**.
- **Why A is incorrect:** Requires both sides of the AND to be true.
- **Why C/D are incorrect:** These are standard comparisons that return a Boolean, not an error or undefined.
</details>

---

### Question 11: `while` vs `do...while` Execution

Consider a loop where the condition is **immediately false** upon initialization. Which statement correctly describes the behavior of `while` and `do...while`?

- A) Both loops will execute exactly zero times.
- B) Both loops will execute exactly one time.
- C) `while` will execute zero times, while `do...while` will execute one time.
- D) `while` will execute one time, while `do...while` will execute zero times.

<details>
<summary><b>Hint</b></summary>
When does the browser check the condition? Before the block runs, or after?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** A `while` loop is a **pre-test loop**; it checks the condition _before_ running the body. If the condition is false initially, the body never runs. A `do...while` loop is a **post-test loop**; it runs the body once _before_ checking the condition for the first time.
- **Why A/B are incorrect:** These fail to account for the difference in when the condition check takes place.
- **Why D is incorrect:** This reverses the actual logic of the two loop types.
</details>

---

### Question 12: Loop Flow Control with `continue`

What will be the output of the following loop?

```js
for (let i = 0; i < 5; i++) {
  if (i === 2) {
    continue;
  }
  process.stdout.write(i.toString());
}
```

- A) `01234`
- B) `01`
- C) `0134`
- D) `2`

<details>
<summary><b>Hint</b></summary>
Does `continue` stop the whole loop, or just skip the rest of the current turn?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The `continue` statement skips the remainder of the _current_ iteration and jumps immediately to the next one. When `i` is 0 and 1, they are printed. When `i` is 2, the `if` condition is met and `continue` triggers, skipping the print statement for that turn. The loop then resumes for `i` values 3 and 4.
- **Why A is incorrect:** This would occur if there was no `if` check or `continue`.
- **Why B is incorrect:** This describes the behavior of `break`, which would exit the entire loop at `i === 2`.
- **Why D is incorrect:** This describes a logic where _only_ the matched item is processed, the opposite of `continue`.
</details>

---

### Question 13: The Infinite Loop Trap

What is the primary cause of the infinite loop in the following code?

```js
let i = 10;
while (i > 0) {
  console.log(i);
  i++;
}
```

- A) The initializer is declared with `let` instead of `var`.
- B) The condition `i > 0` is mathematically impossible to reach.
- C) The final-expression `i++` increments the counter away from the termination condition.
- D) `while` loops do not support the `++` operator.

<details>
<summary><b>Hint</b></summary>
The loop starts at 10 and wants to stop when `i` is 0 or less. But `i` is getting larger every time it runs...
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** To stop the loop, `i` needs to become 0 or negative. However, the code uses `i++`, which makes `i` larger (11, 12, 13...) on every iteration. Since `i` will always be greater than 0, the condition `i > 0` will always be true, and the loop will never terminate.
- **Why A is incorrect:** `let` is the correct way to declare a reassignable counter.
- **Why B is incorrect:** The condition is reached immediately, but the logic inside ensures we никогда exit.
- **Why D is incorrect:** The `++` operator is perfectly valid inside a `while` loop body.
</details>

---

### Question 14: Function Definition Types & Hoisting

Which of the following functions can be successfully called **above** the line where it is defined in the source code?

- A) `const greet = () => { console.log("Hi"); }`
- B) `function greet() { console.log("Hi"); }`
- C) `let greet = function() { console.log("Hi"); }`
- D) Both B and C.

<details>
<summary><b>Hint</b></summary>
Only one form of function definition is "hoisted" by the JavaScript engine, meaning the entire function is moved to the top of its scope before execution.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is a **function declaration**. Function declarations are fully hoisted, meaning the JavaScript engine makes them available everywhere within their containing scope, even before the line they are written on.
- **Why A/C are incorrect:** These are **function expressions** (specifically an arrow function and an anonymous function assigned to a variable). Function expressions are not hoisted; if you call them before the variable is initialized, a `ReferenceError` is thrown.
</details>

---

### Question 15: Parameters vs. Arguments

In the following code snippet, identify which terms represent **parameters** and which represent **arguments**.

```js
function calculate(total, tax) {
  return total * tax;
}
const result = calculate(100, 0.08);
```

- A) `total, tax` are parameters; `100, 0.08` are arguments.
- B) `100, 0.08` are parameters; `total, tax` are arguments.
- C) All four are considered arguments in modern JavaScript.
- D) `result` is the parameter; `total` is the argument.

<details>
<summary><b>Hint</b></summary>
One set of names lives in the **definition** (the blueprint), while the other set of values is provided during the **call** (the execution).
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** **Parameters** are the variable names listed in the function definition (`total`, `tax`). They act as local placeholders. **Arguments** are the actual values or variables passed into the function when it is invoked (`100`, `0.08`).
- **Why B is incorrect:** This reverses the technical definition.
- **Why C is incorrect:** While related, they have distinct technical roles in the execution stack.
- **Why D is incorrect:** `result` is the variable storing the return value, not a parameter.
</details>

---

### Question 16: Arrow Function Implicit Return

Which of the following arrow functions will correctly return the square of a number?

- A) `const sq = n => { n * n };`
- B) `const sq = n => n * n;`
- C) `const sq = (n) => { return n * n };`
- D) Both B and C.

<details>
<summary><b>Hint</b></summary>
If you use curly braces `{}` in an arrow function, you **must** use the `return` keyword. If you omit the braces, the single expression is returned automatically.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** D

**Rationale:**

- **Why B is optimal/correct:** This is the "concise body" form. Because there are no curly braces, the expression `n * n` is implicitly returned.
- **Why C is optimal/correct:** This is the "block body" form. It uses curly braces and an explicit `return` statement, which is also correct.
- **Why A is incorrect:** Because it uses curly braces but lacks the `return` keyword, this function will execute the math but ultimately return `undefined`.
</details>

---

### Question 17: Global vs Local Scope Conflict

What value will be logged to the console?

```js
let x = 10;
function transform() {
  let x = 20;
  x += 5;
}
transform();
console.log(x);
```

- A) `10`
- B) `20`
- C) `25`
- D) `ReferenceError`

<details>
<summary><b>Hint</b></summary>
Note that `let x = 20` is declared *inside* the function. Does a internal variable with the same name change the external one?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** This is an example of **shadowing**. By declaring `let x = 20` inside the function, we create a new, local variable named `x` that exists only within the scope of `transform()`. The math `x += 5` modifies this local `x`. The global `x` (declared outside) remains unchanged at 10.
- **Why B/C are incorrect:** These would only be true if the function updated the global variable (which it would have done if there was no `let` inside).
- **Why D is incorrect:** `x` is defined in both scopes correctly; there is no reference error.
</details>

---

### Question 18: `var` and Block Scoping

Consider the following block of code. What is accessible at the final console log?

```js
if (true) {
  var a = "Visible";
  let b = "Hidden";
}
console.log(a);
console.log(b);
```

- A) Both `"Visible"` and `"Hidden"` are logged.
- B) `"Visible"` is logged, then a `ReferenceError` for `b`.
- C) Both throw a `ReferenceError`.
- D) `"Hidden"` is logged, then a `ReferenceError` for `a`.

<details>
<summary><b>Hint</b></summary>
Legacy `var` is function-scoped but ignores blocks like `if` and `for`. Modern `let` and `const` respect those blocks.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Variables declared with `var` are not block-scoped. They "leak" out of `if` statements and loops into the surrounding function or global scope. Therefore, `a` is accessible outside the `if` block. Variables declared with `let` (and `const`) are strictly block-scoped and cannot be accessed outside the `{}` they were defined in.
- **Why A is incorrect:** `let b` is properly hidden by the block scope.
- **Why C is incorrect:** `var` hoisting and scoping rules ensure `a` is visible.
</details>

---

### Question 19: Default Parameter Activation

Given the function `function greet(name = "User")`, in which scenario will the default value `"User"` be applied?

- A) `greet()`
- B) `greet(undefined)`
- C) `greet(null)`
- D) Both A and B.

<details>
<summary><b>Hint</b></summary>
Default parameters are only triggered when the argument is literally missing or specifically set to `undefined`.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** D

**Rationale:**

- **Why D is optimal/correct:** Default parameters trigger when the argument for that parameter is either omitted entirely (`greet()`) or passed as `undefined`.
- **Why C is incorrect:** Passing `null` is considered an intentional assignment of an empty value. JavaScript treats `null` as a value, so it overrides the default parameter with `null`.
- **Why A/B are partially correct:** Both trigger the default, so D is the only complete answer.
</details>

---

### Question 20: Functions vs. Methods Distinction

What is the primary technical difference between a function and a method in JavaScript?

- A) Methods can return values; functions cannot.
- B) Methods are functions that are properties of an object.
- C) Functions require parameters; methods do not.
- D) Methods are always anonymous, while functions must be named.

<details>
<summary><b>Hint</b></summary>
Think about `Math.random()` vs `alert()`. One is "on" an object, the other is "standalone."
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** The term "method" is used for a function that is stored as a property inside an object. For example, `toUpperCase()` is a method of the `String` object. A standard function is a standalone callable block.
- **Why A is incorrect:** Both can and usually do return values.
- **Why C is incorrect:** Both can accept parameters.
- **Why D is incorrect:** Both can be named or anonymous depending on how they are defined.
</details>

---

## Section 2: Events & Bubbling

### Question 21: Correct Event Listener Registration

Which of the following is the correct (and recommended) way to attach a function named `updateUI` to a button's click event?

- A) `btn.addEventListener("onclick", updateUI)`
- B) `btn.addEventListener("click", updateUI())`
- C) `btn.addEventListener("click", updateUI)`
- D) `btn.onclick = updateUI()`

<details>
<summary><b>Hint</b></summary>
When using `addEventListener`, you don't use the "on" prefix for the event name, and you pass a *reference* to the function, not a call.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `addEventListener` requires the event name _without_ the "on" prefix (so `"click"`, not `"onclick"`) and a reference to the handler function (`updateUI`). By passing the reference without parentheses, you ensure the function only runs when the event actually fires.
- **Why A is incorrect:** The event name should be `"click"`.
- **Why B is incorrect:** `updateUI()` with parentheses calls the function _immediately_ and passes its return value to the listener, which is almost never what you want.
- **Why D is incorrect:** This uses a legacy property and also suffers from the "immediate call" bug mentioned in B.
</details>

---

### Question 22: Identifying the Original Event Source

Inside an event handler, which property of the event object always points to the **specific element that originally fired the event**, even if the event bubbled up from a nested child?

- A) `event.currentTarget`
- B) `event.srcElement` (legacy)
- C) `event.target`
- D) `event.origin`

<details>
<summary><b>Hint</b></summary>
One property changes as the event travels up the DOM, but the other stays fixed on the element where the interaction happened.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `event.target` refers to the "target" of the event—the innermost element that was actually interacted with. This property is stable and does not change as the event propagates (bubbles) through the DOM.
- **Why A is incorrect:** `event.currentTarget` refers to the element whose listener is _currently_ running. As the event bubbles up, `currentTarget` changes to each ancestor.
- **Why B is incorrect:** `srcElement` is a legacy Microsoft-specific property and is not part of the modern standard.
- **Why D is incorrect:** `event.origin` is used in message events (like `postMessage`), not local DOM events.
</details>

---

### Question 23: Canceling Default Browser Behavior

A developer wants to prevent a search form from actually sending a GET request and reloading the page so they can handle the search with JavaScript instead. Which line of code should be added to the `submit` listener?

- A) `event.stopPropagation()`
- B) `event.cancelBubble = true`
- C) `event.preventDefault()`
- D) `return false`

<details>
<summary><b>Hint</b></summary>
You want to "prevent" the "default" action of the browser.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** Many events have a "default" browser action (forms submit, links navigate, etc.). Calling `event.preventDefault()` tells the browser to skip that default action. The event handler code itself still finishes running.
- **Why A/B are incorrect:** These methods stop the event from traveling up to parents (propagation/bubbling), but they do not stop the browser's own built-in response to the event.
- **Why D is incorrect:** While `return false` worked as a shorthand in some legacy libraries (like jQuery) to both stop propagation and prevent default, it is not the standard or explicit way to do it in vanilla modern JavaScript listeners.
</details>

---

### Question 24: Event Bubbling Direction

Given the following structure:

```html
<section id="outer">
  <div id="inner">
    <button id="target">Click Me</button>
  </div>
</section>
```

If all three elements have click listeners (with default settings), what is the order in which they will fire when the button is clicked?

- A) `target` → `inner` → `outer`
- B) `outer` → `inner` → `target`
- C) `target` only
- D) Randomly, depending on browser speed.

<details>
<summary><b>Hint</b></summary>
JavaScript events "bubble up" like air bubbles in water. Do they go from inside to outside, or outside to inside?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** Standard JavaScript events follow the "bubbling" model. The event is first captured (usually ignored by most listeners) and then it bubbles from the **innermost** element (`target`) to the surface (`outer`).
- **Why B is incorrect:** This describes "event capturing," which is disabled by default and requires the `{ capture: true }` option.
- **Why C is incorrect:** Events automatically bubble up the entire hierarchy unless explicitly stopped.
- **Why D is incorrect:** The bubbling order is deterministic and strictly defined by the DOM tree structure.
</details>

---

### Question 25: Halting Event Propagation

What is the effect of calling `event.stopPropagation()` inside a child element's handler?

- A) The browser's default action (like following a link) is canceled.
- B) The current handler stops running immediately.
- C) The event is prevented from triggering handlers on any ancestor elements (parents, grandparents).
- D) The event is deleted from memory.

<details>
<summary><b>Hint</b></summary>
Think about what "propagation" means—spreading from one thing to another.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `stopPropagation()` "kills" the event at its current level in the DOM tree. It prevents the event from "bubbling up" to parents. If a parent also had a click listener, it would not know the click happened.
- **Why A is incorrect:** This is the job of `preventDefault()`.
- **Why B is incorrect:** The current handler function completes its execution fully; `stopPropagation()` only affects _future_ handlers in the propagation chain.
- **Why D is incorrect:** This is too broad; the event object still exists for the duration of the current handler.
</details>

---

### Question 26: Event Delegation Logic

What is the primary benefit of **Event Delegation**?

- A) It allows you to run multiple functions for a single event.
- B) It allows a single listener on a parent element to handle events for many existing (or future) child elements.
- C) It makes event listeners run faster by avoiding the bubbling phase.
- D) It prevents memory leaks by automatically deleting elements after clicks.

<details>
<summary><b>Hint</b></summary>
If you had 1,000 buttons in a list, would you rather attach 1,000 listeners or just 1?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Event delegation leverages bubbling. By putting one listener on a container (parent), you can catch events from all its children. This is memory efficient and also works for items added to the list _after_ the listener is attached.
- **Why A is incorrect:** This is a feature of `addEventListener` generally, not specific to delegation.
- **Why C is incorrect:** Delegation actually _uses_ the bubbling phase to work.
- **Why D is incorrect:** Delegation has no effect on element deletion; it only manages how listeners interact with elements.
</details>

---

### Question 27: Identifying keys in KeyboardEvents

Which property of the `KeyboardEvent` object is recommended for identifying which key was pressed (e.g., "Enter", "a", or "ArrowUp")?

- A) `event.keyCode`
- B) `event.which`
- C) `event.key`
- D) `event.char`

<details>
<summary><b>Hint</b></summary>
While there are numeric codes representing keys, the modern standard uses a human-readable string.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `event.key` is the modern, standard property that returns a string representing the key character (like `"a"`) or the key name (like `"Enter"`).
- **Why A/B are incorrect:** `keyCode` and `which` are deprecated legacy properties. They return numbers (e.g., 13 for Enter), which are less readable and harder to maintain.
- **Why D is incorrect:** `event.char` was proposed in early drafts but is not supported in the final standard for most browsers.
</details>

---

### Question 28: Removing Event Listeners

To successfully use `removeEventListener()`, what condition must be met?

- A) The event handler must have been defined as an anonymous arrow function.
- B) The listener must have been attached using `onclick = ...`.
- C) You must provide the exact same function reference that was used to add the listener.
- D) You can only remove listeners from the `window` object.

<details>
<summary><b>Hint</b></summary>
If you registered an "anonymous" function, how would the browser know which one you're trying to remove later?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `removeEventListener` requires the exact same function object that was passed to `addEventListener`. If you used an anonymous function (`() => {}`), you didn't save a reference to that specific object, and therefore cannot remove it later.
- **Why A is incorrect:** Anonymous functions are the _hardest_ to remove because you don't have a variable pointing to them.
- **Why B is incorrect:** `removeEventListener` is the companion to `addEventListener`, not property assignments.
- **Why D is incorrect:** Listeners can be removed from any valid EventTarget (elements, document, window, etc.).
</details>

---

### Question 29: `event.currentTarget` vs. `event.target`

If a click listener is attached to a `<div>` containing a `<button>`, and the user clicks the button, what does `event.currentTarget` represent?

- A) The `<button>` (the origin).
- B) The `<div>` (the element where the listener is attached).
- C) The `<body>` (the root).
- D) `null`.

<details>
<summary><b>Hint</b></summary>
The "target" is where the event started; the "current target" is where the code is currently running.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `event.currentTarget` always refers to the element that the event listener is **attached to**. In this case, the code is executing a listener defined on the `<div>`, so `currentTarget` is the `<div>`.
- **Why A is incorrect:** This is `event.target`.
- **Why C is incorrect:** The event has not bubbled up to the body yet (or may never if propagation is stopped).
- **Why D is incorrect:** The property is always populated during event execution.
</details>

---

### Question 30: The `{ capture: true }` Option

What happens if you set the third argument of `addEventListener` to `{ capture: true }`?

- A) The event will fire in the capture phase (outward to inward) instead of the bubbling phase.
- B) The event will be "captured" so no other listeners can hear it.
- C) The event will only fire if the user is holding the "Ctrl" key.
- D) The listener will only run once and then delete itself.

<details>
<summary><b>Hint</b></summary>
Remember that there are two phases of propagation: one goes down the tree, and one goes up. Bubbling is "up." What is the other one?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** Events actually travel down the DOM tree first (Capture phase) before bubbling back up. By default, listeners only listen for the bubbling phase. Setting `capture: true` tells the listener to fire as the event "trickles down" from the root.
- **Why B is incorrect:** Multiple listeners can still listen in both phases.
- **Why C is incorrect:** This is unrelated to modifier keys.
- **Why D is incorrect:** This functionality exists via the `{ once: true }` option, not `{ capture: true }`.
</details>

---

## Section 3: Objects & DOM Scripting

### Question 31: Bracket Notation with Variables

Consider the following object:

```js
const user = { name: "Alice", age: 25, job: "Developer" };
const field = "job";
```

How should you access the "Developer" value using the `field` variable?

- A) `user.field`
- B) `user[field]`
- C) `user."field"`
- D) `user(field)`

<details>
<summary><b>Hint</b></summary>
When the property name is stored inside another variable, dot notation fails because it looks for a literal member with that name.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Bracket notation (`user[field]`) evaluates the expression inside the brackets. In this case, `field` evaluates to `"job"`, so it becomes `user["job"]`, which returns `"Developer"`.
- **Why A is incorrect:** `user.field` literally looks for a key named "field" inside the object, which doesn't exist (returns `undefined`).
- **Why C is incorrect:** This is not valid JavaScript syntax.
- **Why D is incorrect:** Objects are not functions; parentheses are used for invocation, not property access.
</details>

---

### Question 32: The Role of `this` in Methods

What does `this` refer to in the following code?

```js
const car = {
  brand: "Tesla",
  showBrand() {
    console.log(this.brand);
  },
};
car.showBrand();
```

- A) The global `window` object.
- B) The `showBrand` function itself.
- C) The `car` object.
- D) `undefined`

<details>
<summary><b>Hint</b></summary>
Inside a standard object method, `this` is a "shortcut" back to the object that owns the method.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** When a function is called as a method of an object (`car.showBrand()`), `this` is bound to the object the method was called on. This allows the method to access other properties of that same object.
- **Why A is incorrect:** `this` points to `window` in global functions or arrow functions in certain scopes, but not in standard object methods.
- **Why B is incorrect:** `this` rarely refers to the function itself in standard JS (that's usually accessed via the function name or `arguments.callee` in legacy code).
- **Why D is incorrect:** In non-strict mode, `this` defaults to `window`; in strict mode it's `undefined` for standalone functions, but for methods, it's defined.
</details>

---

### Question 33: Creating Instances with Constructors

You have a constructor defined as:

```js
function Person(name) {
  this.name = name;
}
```

Which line correctly creates a new object instance using this template?

- A) `const p = Person("Ari");`
- B) `const p = Create Person("Ari");`
- C) `const p = new Person("Ari");`
- D) `const p = Person.instance("Ari");`

<details>
<summary><b>Hint</b></summary>
There is a specific keyword in JavaScript designed to instantiate objects from constructor functions.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The `new` keyword is used to call a constructor. It handles creating the empty object, binding `this`, and returning the result. By convention, constructors are capitalized to signal that `new` should be used.
- **Why A is incorrect:** Calling a constructor without `new` just executes it as a regular function. `this` will likely refer to `window` (global pollution), and the function returns `undefined` because there is no explicit `return`.
- **Why B/D are incorrect:** These use fake or non-standard syntax that does not exist in the JavaScript language.
</details>

---

### Question 34: Modern Element Selection

Which statement about `document.querySelector()` and `document.getElementById()` is true?

- A) `querySelector` is faster because it only searches for IDs.
- B) `getElementById` can accept any CSS selector like `.my-class`.
- C) `querySelector` is more versatile as it can select by ID, class, tag, or complex CSS relationships.
- D) Both return a `NodeList` of all matches.

<details>
<summary><b>Hint</b></summary>
One method is dedicated to a single attribute; the other is a "Swiss Army knife" that uses the same language as your CSS.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `querySelector()` accepts any valid CSS selector string. This makes it the modern "go-to" for selecting elements, as it replaces the need for separate ID, Class, and Tag selectors.
- **Why A is incorrect:** `getElementById` is actually slightly faster because it uses a direct lookup table, whereas `querySelector` has to parse a CSS string.
- **Why B is incorrect:** `getElementById` _only_ accepts the raw ID string (e.g., `"myId"`, not `"#myId"`).
- **Why D is incorrect:** `getElementById` and `querySelector` both return the **first** matching element only. `querySelectorAll` returns a NodeList.
</details>

---

### Question 35: The Three-Step DOM Insertion Pattern

A developer wants to add a new `<li>` to an existing `<ul>`. What is the correct sequence of operations?

- A) `appendChild()` → `createElement()` → `textContent`
- B) `textContent` → `appendChild()` → `createElement()`
- C) `createElement()` → `textContent` → `appendChild()`
- D) `createElement()` → `appendChild()` → `textContent`

<details>
<summary><b>Hint</b></summary>
Think about the lifecycle of a node: creation (off-screen), population (content), and attachment (on-screen).
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The standard pattern is: 1. `createElement()` to generate the node in memory. 2. `textContent` (and other properties) to configure the node. 3. `appendChild()` (or `prepend`, `insertAfter`, etc.) to attach it to the visible DOM tree.
- **Why A/B are incorrect:** You cannot append a node that hasn't been created yet.
- **Why D is incorrect:** While technically possible, it's less efficient as it causes two "paints" (the empty element, then the text) rather than one complete insertion.
</details>

---

### Question 36: Moving vs. Copying Nodes

You have an existing element `const img = document.querySelector("img")`. If you run `containerB.appendChild(img)`, what happens if the image was already inside `containerA`?

- A) A second identical image is created in `containerB`.
- B) The image is **moved** from `containerA` to `containerB`.
- C) Nothing happens; a node can only ever have one parent.
- D) The browser throws a `DOMException`.

<details>
<summary><b>Hint</b></summary>
In the standard DOM, can one specific node "object" exist in two places at the same time?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** In the DOM, an element node is a unique object. It can only have one parent at a time. Using `appendChild()` on an existing node effectively "re-parents" it, moving it from its current location to the new one.
- **Why A is incorrect:** To copy a node, you must explicitly use `img.cloneNode(true)`.
- **Why C/D are incorrect:** Moving elements is a standard, built-in feature of the DOM.
</details>

---

### Question 37: Style Property Naming in JS

How would you set the CSS `background-color` of an element using the `.style` property in JavaScript?

- A) `el.style.background-color = "blue";`
- B) `el.style["background-color"] = "blue";`
- C) `el.style.backgroundColor = "blue";`
- D) Both B and C are valid.

<details>
<summary><b>Hint</b></summary>
JavaScript property names cannot contain hyphens unless they are strings inside brackets. Dot notation requires "CamelCase".
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** D

**Rationale:**

- **Why D is optimal/correct:** JavaScript uses **camelCase** for CSS properties accessed via the `.style` object (e.g., `backgroundColor`). However, since `style` is an object, you can also use bracket notation with the literal CSS string (`["background-color"]`).
- **Why A is incorrect:** `el.style.background-color` is parsed as `(el.style.background) minus (color)`, which results in a `ReferenceError` or `NaN`.
</details>

---

### Question 38: Separation of Concerns with `classList`

Between `element.style.color = "red"` and `element.classList.add("error")`, which is generally preferred for scaling a large project and why?

- A) `element.style`, because it is faster to type and execute.
- B) `element.classList`, because it maintains **separation of concerns** by keeping the visual logic in the CSS file.
- C) `element.style`, because it has higher specificity and overrides everything.
- D) `element.classList`, but only if the class name is also in the JavaScript file.

<details>
<summary><b>Hint</b></summary>
If you want to change the "error" color to orange in the future, where would you rather do it: in one CSS file, or in 50 different `.js` files?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Toggling classes is the professional standard. It keeps "how things look" in the CSS and "what things are doing" in the JS. Class based styling is also easier to override and more performant than heavy inline styles.
- **Why A is incorrect:** Maintaining inline styles in JS is a nightmare for maintenance.
- **Why C is incorrect:** High specificity (inline styles) is usually a disadvantage, as it makes CSS overrides (`hover`, `media queries`) difficult or impossible without `!important`.
</details>

---

### Question 39: Nodes vs. Elements

What is the difference between a **Node** and an **Element** in the DOM?

- A) They are synonyms.
- B) An Element is a _type_ of Node. All elements are nodes, but not all nodes are elements (e.g., text nodes).
- C) Nodes are visible, while Elements are hidden storage structures.
- D) Elements are the parents, and Nodes are the children.

<details>
<summary><b>Hint</b></summary>
Think of "Node" as the broad biological category (like "Animal") and "Element" as the specific species (like "Cat").
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** The DOM is a tree of **Nodes**. Common node types include `ELEMENT_NODE` (like `<div>`), `TEXT_NODE` (the text inside), and `COMMENT_NODE`. "Element" specifically refers to the HTML tags.
- **Why A is incorrect:** While often used loosely, they denote different levels of the class hierarchy.
- **Why C/D are incorrect:** These are misunderstandings of tree-structure terminology.
</details>

---

### Question 40: Clearing Input after Submission

After capturing `input.value`, why is it standard practice to run `input.value = ""`?

- A) To prevent the browser from crashing.
- B) To provide a good user experience by clearing the field for the next entry.
- C) To ensure the memory associated with that string is released.
- D) Because the DOM requires fields to be empty before the next event listener can fire.

<details>
<summary><b>Hint</b></summary>
If you type a message in a chat app and hit send, do you want your old message to stay in the box?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is purely about Usability/UX. When a user submits data (like a shopping list item), they expect the interface to reset so they can immediately begin typing the next item without manually deleting their previous input.
- **Why A/C/D are incorrect:** These are technical fabrication; the language does not require this for safety or memory management.
</details>

---

## Section 4: Network Requests & JSON

### Question 41: Understanding the Fetch Promise

What does the `fetch()` function return?

- A) The actual data from the server (e.g., a JSON object).
- B) A Promise that resolves to a `Response` object.
- C) A string containing the raw HTTP response headers.
- D) `undefined`.

<details>
<summary><b>Hint</b></summary>
Network requests take time. Since JavaScript doesn't want to "freeze" while waiting, it returns a placeholder object that represents the future result.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `fetch()` is an asynchronous function. It returns a Promise immediately. This Promise resolves once the browser receives the HTTP headers from the server, providing a `Response` object which contains metadata (status, headers) and methods to read the body.
- **Why A is incorrect:** You cannot get the data immediately because the network request is still in progress when `fetch()` returns.
- **Why C is incorrect:** While headers are part of the `Response` object, `fetch` itself returns the Promise wrapper.
- **Why D is incorrect:** `fetch` consistently returns a Promise.
</details>

---

### Question 42: Handling 404 and 500 Errors in Fetch

A developer notices that their `.catch()` block is not firing even when the server returns a "404 Not Found" error. Why is this happening?

- A) The URL is malformed.
- B) Fetch only catches network failures; HTTP errors like 404 still "resolve" the Promise.
- C) The developer forgot to include an `err` parameter in the catch block.
- D) 404 errors are considered successful in JavaScript.

<details>
<summary><b>Hint</b></summary>
"Success" for the `fetch()` function means "The server sent a response," not "The server gave me the data I wanted."
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is a critical Fetch behavior. The Promise returned by `fetch()` only rejects on **network failures** (like being offline or a DNS error). If the server responds with a 404 or 500, the request "succeeded" at a technical network level, so the Promise resolves.
- **Why A is incorrect:** A malformed URL might cause a network error, but a 404 specifically means the server _was_ reached and replied.
- **Why C is incorrect:** Parameter names don't affect whether the block executes.
- **Why D is incorrect:** While the _Promise_ resolves, the developer should check `response.ok` to see if the HTTP status was successful (200-299).
</details>

---

### Question 43: Correct Use of `response.json()`

Why is a second `.then()` typically needed when fetching JSON data?

- A) Because the server sends the data twice for security.
- B) Because `response.json()` _also_ returns a Promise that must be awaited.
- C) To ensure the `Response` object is deleted from memory.
- D) To handle the headers and body separately.

<details>
<summary><b>Hint</b></summary>
The body of a response can be large and arrives in "chunks." Converting those chunks into a JavaScript object is itself an asynchronous task.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** The first `.then()` receives the `Response` object (headers). The body hasn't been fully downloaded or parsed yet. Methods like `.json()` or `.text()` return a _new_ Promise that resolves once the body has been completely received and converted.
- **Why A/C/D are incorrect:** These are misunderstandings of how HTTP streams and Promises work in JavaScript.
</details>

---

### Question 44: The `response.ok` Property

What is the most reliable way to check if a Fetch request actually succeeded at the HTTP level?

- A) `if (response.status === 200)`
- B) `if (response.ok)`
- C) `if (response.body !== null)`
- D) `if (response.type === "success")`

<details>
<summary><b>Hint</b></summary>
There are several status codes (200, 201, 204) that represent success. Is there a property that covers all of them?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `response.ok` is a boolean property that is `true` if the status code is in the range **200-299**. This is more robust than checking for just `200`, as it correctly handles other success codes like `201` (Created).
- **Why A is incorrect:** It's too narrow; many successful requests use codes other than exactly 200.
- **Why C is incorrect:** An error page (404) still has a body (usually a "Not Found" message).
- **Why D is incorrect:** `response.type` describes the type of response (e.g., "basic", "cors"), not its success status.
</details>

---

### Question 45: JSON Syntax: Keys and Quotes

Which of the following is a **valid** JSON string?

- A) `{'name': 'Bob'}`
- B) `{"name": "Bob"}`
- C) `{name: "Bob"}`
- D) `{"name": 'Bob'}`

<details>
<summary><b>Hint</b></summary>
JSON is stricter than JavaScript. It requires double quotes for both property names and string values.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** In JSON, keys **must** be double-quoted, and string values **must** also be double-quoted.
- **Why A/D are incorrect:** JSON does not allow single quotes (`'`).
- **Why C is incorrect:** Unquoted keys are allowed in JavaScript object literals, but are illegal in JSON.
</details>

---

### Question 46: Serialization vs. Deserialization

A developer has a JavaScript object and wants to convert it into a string to send it to a server. Which method should they use?

- A) `JSON.parse()`
- B) `JSON.toString()`
- C) `JSON.stringify()`
- D) `JSON.serialize()`

<details>
<summary><b>Hint</b></summary>
"Serialization" means turning a complex structure into a "string" (a sequence of characters).
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `JSON.stringify()` converts (serializes) a JavaScript value or object into a JSON-formatted string.
- **Why A is incorrect:** `JSON.parse()` does the opposite (deserialization)—it turns a JSON string back into a JavaScript object.
- **Why B/D are incorrect:** These are not standard JavaScript methods.
</details>

---

### Question 47: Prohibited Value Types in JSON

Which of the following values is **NOT** allowed in a JSON file?

- A) `null`
- B) `10.5`
- C) `undefined`
- D) `true`

<details>
<summary><b>Hint</b></summary>
JSON is meant to be language-independent. `null` and `true` are universal concepts, but what value is specific to JavaScript's quirkiness?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `undefined` is a JavaScript-specific type and is not supported in the JSON standard. Other forbidden types include functions and symbols.
- **Why A/B/D are incorrect:** `null`, numbers, and booleans are all valid, standard JSON data types.
</details>

---

### Question 48: Accessing Nested JSON Data

Given the following JSON:

```json
{
  "users": [{ "id": 1, "profile": { "username": "ace" } }]
}
```

If this is parsed into a variable `data`, how do you access the string `"ace"`?

- A) `data.users[0].profile.username`
- B) `data.users.profile.username`
- C) `data[users][0][profile][username]`
- D) `data.users[1].profile.username`

<details>
<summary><b>Hint</b></summary>
Follow the path: The object has a "users" array. Pick the first item in that array. Then access the "profile" object inside it.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** This follows the chain correctly: `data` (root object) -> `.users` (the array) -> `[0]` (the first user object) -> `.profile` (nested object) -> `.username`.
- **Why B is incorrect:** `users` is an array; you cannot access `.profile` directly on the array itself.
- **Why C is incorrect:** This is invalid syntax; `users` and others would need to be strings (`["users"]`).
- **Why D is incorrect:** Array indexes start at `0`. `[1]` would look for a second user who doesn't exist.
</details>

---

### Question 49: Fetch Error Handling Pattern

Where will an error be caught if the user's internet disconnects during a `fetch` call?

- A) In the first `.then()` block.
- B) In the second `.then()` block.
- C) In the `.catch()` block.
- D) It won't be caught; it will crash the browser.

<details>
<summary><b>Hint</b></summary>
A network disconnect is a "Rejection" of the Promise. Which block is dedicated to rejections?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** If the network request fails to initiate or complete due to a connection issue, the Promise "rejects." This bypasses all `.then()` blocks and goes directly to the nearest `.catch()` block.
- **Why A/B are incorrect:** `.then()` blocks only run if the request completes and a response object is successfully created.
- **Why D is incorrect:** Well-written Promises with catch blocks prevent application crashes from environmental errors.
</details>

---

### Question 50: Binary Data (Blobs) in Fetch

When fetching an image file to display it in an `<img>` tag, which response method should you use after the initial `fetch`?

- A) `response.json()`
- B) `response.blob()`
- C) `response.text()`
- D) `response.image()`

<details>
<summary><b>Hint</b></summary>
An image is a "Binary Large Object". Is there a method named after that abbreviation?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `.blob()` is the method used to read the response body as binary data. This is necessary for non-text files like images, video, or audio. You can then use `URL.createObjectURL(blob)` to display it.
- **Why A is incorrect:** Images are not text-based JSON objects.
- **Why C is incorrect:** Reading an image as text would result in a string of garbage characters (binary data forced into text encoding).
- **Why D is incorrect:** There is no `.image()` method on the Response object.
</details>

---

## Section 5: Debugging & Integrated Scenarios

### Question 51: Syntax Error vs. Logic Error

A developer writes a program to calculate the average of three numbers, but the result is always higher than expected. The code runs without any red messages in the console. What type of error is this?

- A) Syntax Error
- B) Logic Error
- C) Reference Error
- D) Type Error

<details>
<summary><b>Hint</b></summary>
If the code "runs" (executes) but just gives the "wrong answer," the browser thinks the grammar is fine, but the math is wrong.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** A **Logic Error** occurs when the code is syntactically correct (no grammar mistakes) but the instructions given to the computer don't produce the intended result. Common examples include using the wrong mathematical operator or an off-by-one error in a loop.
- **Why A is incorrect:** A syntax error would prevent the code from running at all and would show a red error in the console.
- **Why C/D are incorrect:** These are specific types of runtime errors that usually crash the script (e.g., calling a variable that doesn't exist).
</details>

---

### Question 52: Using Breakpoints effectively

What happens precisely when the browser reaches a line where you have set a **breakpoint** in the DevTools Debugger?

- A) The browser ignores that line and skips to the next one.
- B) The browser executes the line and then stops.
- C) The browser **pauses** execution _before_ running that specific line.
- D) The browser automatically fixes any errors on that line.

<details>
<summary><b>Hint</b></summary>
A breakpoint is like a "stop sign." Do you stop before the sign or after you've already driven past it?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** Breakpoints allow you to pause the code right before a specific instruction executes. This is incredibly useful because it lets you look at the **Scopes** panel to see exactly what the variables contain at that exact moment in time.
- **Why B is incorrect:** If it stopped _after_, you wouldn't be able to see the state of the world that caused the line to behave a certain way.
- **Why A/D are incorrect:** These are not features of standard breakpoints.
</details>

---

### Question 53: Validating Numbers Safely

Why is it recommended to use `Number.isNaN(val)` instead of just `typeof val !== "number"` when validating user input?

- A) `typeof` is much slower than `Number.isNaN`.
- B) Because `typeof NaN` actually returns `"number"`.
- C) `Number.isNaN` can check for strings too.
- D) `typeof` is deprecated in modern JavaScript.

<details>
<summary><b>Hint</b></summary>
JavaScript has some strange "legacy" behaviors. One of them is that "Not a Number" is technically a type of number.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is a famous JavaScript quirk. `NaN` (Not-a-Number) has a data type of `"number"`. Therefore, if you only check `typeof`, `NaN` will pass through as "valid," likely causing your math to fail later. You must check both the type and that it isn't `NaN`.
- **Why A/C/D are incorrect:** These are technical inaccuracies. `typeof` is still the standard for type checking, and `Number.isNaN` only returns true for the specific value `NaN`.
</details>

---

### Question 54: The `try...catch` Execution Flow

What will be logged to the console in the following scenario?

```js
try {
  console.log("A");
  throw new Error("B");
  console.log("C");
} catch (e) {
  console.log("D");
}
console.log("E");
```

- A) A, B, C, D, E
- B) A, D, E
- C) A, B, D, E
- D) A, D

<details>
<summary><b>Hint</b></summary>
When an error is "thrown," JavaScript stops everything in the `try` block and jumps immediately to the `catch`. Does it stop the whole program, or just that block?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:**
  1. "A" is logged normally.
  2. An error is thrown. This causes JS to **skip** the rest of the `try` block (so "C" is never logged).
  3. The `catch` block catches the error and logs "D".
  4. Since the error was caught, the program recovers and continues with the line after the `try...catch` block, logging "E".
- **Why A/C are incorrect:** Execution never returns to the `try` block after a throw.
- **Why D is incorrect:** `E` is outside the block and will run regardless of whether an error was caught.
</details>

---

### Question 55: The `finally` Block

If a `try...catch` statement also includes a `finally` block, when does the code inside `finally` run?

- A) Only if an error occurs.
- B) Only if NO error occurs.
- C) Always, regardless of whether an error was thrown or caught.
- D) Only if the `catch` block throws a second error.

<details>
<summary><b>Hint</b></summary>
The name "finally" implies it is the very last step in a sequence that happens every time.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The `finally` block is used for cleanup code (like closing a database connection or hiding a loading spinner) that must execute no matter what happens in the `try` or `catch` blocks.
- **Why A/B/D are incorrect:** These describe conditional behavior, but `finally` is unconditional.
</details>

---

### Question 56: Integrated Scenario: Input & DOM

A developer wants to take text from an `<input id="user-in">` and add it as a new paragraph to `<div id="display">` only if the input is not empty. Which logic is correct?

- A) `display.textContent = userIn.value`
- B) `if (userIn.value) { const p = document.createElement("p"); p.textContent = userIn.value; display.appendChild(p); }`
- C) `const p = document.createElement("p"); display.appendChild(p); p.textContent = userIn.value;`
- D) `if (userIn.value == "") { display.appendChild(userIn.value); }`

<details>
<summary><b>Hint</b></summary>
Think about the correct sequence: Check input → Create element → Set text → Append.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This follows the correct integrated pattern: first, it checks if `userIn.value` is truthy (not empty). Then it creates the element, sets the value, and appends it.
- **Why A is incorrect:** This replaces everything in the `div` with plain text rather than adding a new paragraph.
- **Why C is incorrect:** This adds an empty paragraph to the DOM before putting text in it, and it lacks the "not empty" check.
- **Why D is incorrect:** This logic is reversed (it runs when empty) and tries to append a string directly to the DOM (which requires a node).
</details>

---

### Question 57: Integrated Scenario: Fetch & Result Handling

When fetching data from an API, which approach correctly handles both the network request and potential parsing errors?

- A) `fetch(url).then(r => r.json()).catch(err => console.log(err))`
- B) `try { const r = await fetch(url); const d = await r.json(); return d; } catch(e) { console.log(e); }`
- C) `fetch(url).then(r => { if(!r.ok) throw Error(); return r.json(); }).then(d => show(d)).catch(e => error(e))`
- D) `fetch(url).json().then(d => show(d))`

<details>
<summary><b>Hint</b></summary>
A "safe" fetch needs three things: checking `response.ok`, parsing the body, and a `catch` at the end for network failures.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** This represents a complete "gold standard" fetch chain. It checks `response.ok` (to catch 404s/500s), returns the JSON promise, handles the result, and has a `.catch()` for network failures or parsing issues.
- **Why A is incorrect:** It fails to check `response.ok`, meaning it might try to parse a 404 error page as JSON.
- **Why B is incorrect:** While it uses `async/await`, it is incomplete without checking `r.ok`.
- **Why D is incorrect:** `.json()` is a method on the _response_, not the fetch result itself.
</details>

---

### Question 58: Debugging "undefined" in Object Access

You see an error: `TypeError: Cannot read properties of undefined (reading 'name')`. What does this tell you about your code?

- A) The variable you are trying to access is not a string.
- B) The object itself is `undefined`, and you are trying to access the `.name` key on it.
- C) The `.name` property exists but has no value.
- D) You forgot to use double quotes in your JSON.

<details>
<summary><b>Hint</b></summary>
The error says it can't read 'name' *of* undefined. So, what is the thing "before" the dot?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is the most common runtime error in JavaScript. It means a variable (e.g., `user`) is `undefined`, but you wrote `user.name`. Since `undefined` has no properties, the engine throws an error.
- **Why A/C/D are incorrect:** These would either produce no error, return `undefined` silently (if the object existed), or throw a `SyntaxError`.
</details>

---

### Question 59: Integrated Scenario: Event Delegation with Logic

In an event delegation setup on a `<ul>`, you want to delete only the `<li>` that was clicked. Which specific property should you use inside the handler?

- A) `event.currentTarget`
- B) `event.currentTarget.remove()`
- C) `event.target.closest("li").remove()`
- D) `document.querySelector("li").remove()`

<details>
<summary><b>Hint</b></summary>
In delegation, the "currentTarget" is the `<ul>`. The "target" is whatever was clicked (which might be the `<li>` or a `<span>` inside it).
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `event.target` is the specific element clicked. Using `.closest("li")` ensures that even if you clicked a child of the list item (like an icon or text span), you always find the parent `<li>` and remove just that one.
- **Why A/B are incorrect:** `currentTarget` is the `<ul>` where the listener is attached. Removing it would delete the entire list.
- **Why D is incorrect:** This would only ever remove the very first list item on the page, regardless of which one was clicked.
</details>

---

### Question 60: Identifying a Closure/Scope Bug

Why does the following code always log "3" regardless of which button is clicked?

```js
for (var i = 0; i < 3; i++) {
  btns[i].onclick = () => console.log(i);
}
```

- A) Because the index `i` is reset after each click.
- B) Because `var` is function-scoped, so all three buttons share the same `i` variable which ends up as 3.
- C) Because arrow functions cannot see variables from loops.
- D) Because the loop runs too fast for the buttons to register.

<details>
<summary><b>Hint</b></summary>
Compare `var` and `let`. `var` shares its identity across the whole function, whereas `let` creates a new "copy" for every loop iteration.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is a classic "Closure" problem. `var` is not block-scoped. By the time any button is clicked, the loop has already finished and `i` has reached 3. Since all three buttons reference the _same_ `i`, they all log 3. Changing `var` to `let` fixes this.
- **Why A/C/D are incorrect:** These are common misconceptions about how loops and scope work in JavaScript.
</details>
