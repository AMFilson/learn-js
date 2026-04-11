# 📚 JavaScript Arrays — Exam Study Guide
**Source:** [MDN Web Docs — Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays)

---

## Executive Summary

JavaScript **arrays** are ordered, list-like objects that store multiple values of any type under a single variable name, accessible via a **zero-based integer index**. They expose a rich set of built-in methods — such as `push()`, `pop()`, `splice()`, `map()`, and `filter()` — that make adding, removing, searching, and transforming data efficient and expressive. Arrays are a foundational data structure used constantly in JavaScript, especially in combination with loops, to process collections of data without repetitive code.

---

## Core Pillars

### 1. What is an Array?

- An array is a **single object** that holds **multiple values** in an ordered list.
- Why use them? Without arrays, you'd need a separate variable for every item — 100 products = 100 variables. Arrays collapse that to **one**.
- Arrays are **indexed collections**: items are numbered starting at **index 0**.
- Arrays can store **mixed data types**: strings, numbers, objects, even other arrays.

```js
const shopping = ["bread", "milk", "cheese", "hummus", "noodles"];
const mixed    = ["tree", 795, [0, 1, 2]]; // mixed types + nested array
```

---

### 2. Creating Arrays

- Use **square bracket literal syntax**: `[]` with items separated by commas.
- Declared with `const` — the variable reference can't be reassigned, but the **array contents can still be mutated**.

```js
const sequence = [1, 1, 2, 3, 5, 8, 13]; // numbers
const random   = ["tree", 795, [0, 1, 2]]; // mixed
```

---

### 3. The `length` Property

- `array.length` returns the **count of items** (not the last index).
- Last valid index = `array.length - 1`.

```js
const shopping = ["bread", "milk", "cheese", "hummus", "noodles"];
console.log(shopping.length); // 5  ← count of items
console.log(shopping[4]);     // "noodles" ← last item (index 4, not 5)
```

---

### 4. Accessing & Modifying Items (Bracket Notation)

- **Read**: `array[index]` — returns the value at that index.
- **Write**: `array[index] = newValue` — directly reassigns a specific item.
- **Multidimensional arrays**: chain bracket notation — `array[2][1]` accesses the element at index 1 of the nested array at index 2.

```js
const shopping = ["bread", "milk", "cheese", "hummus", "noodles"];
console.log(shopping[0]); // "bread"
shopping[0] = "tahini";
console.log(shopping);    // ["tahini", "milk", "cheese", "hummus", "noodles"]

const random = ["tree", 795, [0, 1, 2]];
console.log(random[2][2]); // 2  ← nested array access
```

---

### 5. Finding an Item's Index — `indexOf()`

- `array.indexOf(item)` returns the **index** of the first match.
- Returns **`-1`** if the item is **not found** — this is a critical sentinel value.
- Always check `!== -1` before using the result to manipulate the array.

```js
const birds = ["Parrot", "Falcon", "Owl"];
birds.indexOf("Owl");    // 2
birds.indexOf("Rabbit"); // -1  ← not found
```

---

### 6. Adding Items

| Method | Where Added | Mutates Original? | Returns |
|---|---|---|---|
| `push(item)` | **End** | ✅ Yes | New length |
| `unshift(item)` | **Start** | ✅ Yes | New length |

```js
const cities = ["Manchester", "Liverpool"];

cities.push("Cardiff");           // end   → ["Manchester", "Liverpool", "Cardiff"]
cities.push("Bradford","Brighton"); // multiple at once
cities.unshift("Edinburgh");      // start → ["Edinburgh", "Manchester", ...]

const newLen = cities.push("Bristol"); // capture returned length
```

> **Key detail:** `push()` returns the **new length** of the array, not the array itself.

---

### 7. Removing Items

| Method | Where Removed | Mutates Original? | Returns |
|---|---|---|---|
| `pop()` | **Last** item | ✅ Yes | The removed item |
| `shift()` | **First** item | ✅ Yes | The removed item |
| `splice(start, count)` | **Any position** | ✅ Yes | Array of removed items |

```js
const cities = ["Manchester", "Liverpool"];

const removed = cities.pop();   // returns "Liverpool"; cities = ["Manchester"]
cities.shift();                 // removes "Manchester"; cities = []

// splice: remove by index
const arr = ["Manchester", "Liverpool", "Edinburgh", "Carlisle"];
const idx = arr.indexOf("Liverpool");
if (idx !== -1) {
  arr.splice(idx, 1); // remove 1 item at idx → ["Manchester", "Edinburgh", "Carlisle"]
  arr.splice(idx, 2); // remove 2 items → ["Manchester", "Carlisle"]
}
```

---

### 8. Iterating Over Arrays

#### `for...of` Loop — Simple Iteration
```js
const birds = ["Parrot", "Falcon", "Owl"];
for (const bird of birds) {
  console.log(bird); // logs each item
}
```

#### `map()` — Transform Every Item → New Array
- Calls a function on **each item**, returns a **new array** of results.
- **Does not mutate** the original array.

```js
function double(number) { return number * 2; }
const numbers = [5, 2, 7, 6];
const doubled = numbers.map(double); // [10, 4, 14, 12]
```

#### `filter()` — Select Items That Pass a Test → New Array
- Calls a function on each item; keeps items where the function returns **`true`**.
- **Does not mutate** the original array.

```js
function isLong(city) { return city.length > 8; }
const cities = ["London", "Liverpool", "Totnes", "Edinburgh"];
const longer = cities.filter(isLong); // ["Liverpool", "Edinburgh"]
```

---

### 9. Converting Between Strings and Arrays

#### `split()` — String → Array *(technically a String method)*
- Splits a string at a specified **separator character**, returning an array of substrings.

```js
const data = "Manchester,London,Liverpool,Birmingham";
const cities = data.split(","); // ["Manchester", "London", "Liverpool", "Birmingham"]
```

#### `join()` — Array → String *(inverse of `split()`)*
- Joins all elements into a string with a specified **separator**.

```js
const commaSep = cities.join(",");  // "Manchester,London,Liverpool,Birmingham"
const dashSep  = cities.join(" - "); // "Manchester - London - ..."
```

#### `toString()` — Array → String (always comma-separated)
- Simpler than `join()` but **always uses a comma** — no custom separator.

```js
const dogs = ["Rocket", "Flash", "Bella"];
dogs.toString(); // "Rocket,Flash,Bella"
```

---

## Technical Deep-Dive

### Logic Walkthrough: "Printing Those Products" Exercise

This exercise demonstrates combining `split()`, `Number()`, `for...of`, and string templates into a real-world pattern.

**Goal:** Parse an array of `"name:price"` strings, total the prices, and render an invoice.

```js
const products = [
  "Underpants:6.99",
  "Socks:5.99",
  "T-shirt:14.99",
  "Trousers:31.99",
  "Shoes:23.99",
];
let total = 0;

for (const product of products) {
  // Step 1: split "name:price" → ["name", "price"]
  const subArray = product.split(":");

  // Step 2: isolate name and convert price string → Number
  const name  = subArray[0];
  const price = Number(subArray[1]);

  // Step 3: accumulate total
  total += price;

  // Step 4: build display string
  const itemText = `${name} — $${price}`;

  // Step 5: DOM manipulation (create <li> and append)
  const listItem = document.createElement("li");
  listItem.textContent = itemText;
  list.appendChild(listItem);
}

totalBox.textContent = `Total: $${total.toFixed(2)}`;
```

**Why `Number(subArray[1])`?** `split()` always returns **strings**. Without explicit conversion, `total += price` would concatenate strings instead of adding numbers.

---

### Logic Walkthrough: "Storing the Previous 5 Searches" Exercise

This demonstrates a **fixed-size sliding window** pattern using `unshift()` and `pop()`.

```js
const myHistory = [];
const MAX_HISTORY = 5;

// On each new search:
myHistory.unshift(searchInput.value); // ← add newest to FRONT

if (myHistory.length >= MAX_HISTORY) {
  myHistory.pop(); // ← remove oldest from BACK
}
```

**Why `unshift` + `pop` and not `push` + `shift`?**
- `unshift` keeps the **most recent** item at index `[0]` (top of list).
- `pop` removes the **oldest** item from the end, controlling total size.
- This is an efficient **LIFO-style bounded queue** pattern.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Array** | An ordered, list-like object in JavaScript that stores multiple values under a single variable, accessed by integer index. |
| **Index** | The integer position of an element in an array. JavaScript arrays are **zero-indexed** (first element = index `0`). |
| **`length`** | A property of every array that returns the **total count** of elements. Always one greater than the last valid index. |
| **`push()`** | Adds one or more items to the **end** of an array. Returns the new array length. Mutates the original array. |
| **`pop()`** | Removes and **returns** the last item from an array. Mutates the original array. |
| **`unshift()`** | Adds one or more items to the **beginning** of an array. Returns the new length. Mutates the original array. |
| **`shift()`** | Removes and **returns** the first item from an array. Mutates the original array. |
| **`splice(start, count)`** | Removes `count` elements starting at index `start`. Mutates the original array; returns an array of removed elements. |
| **`indexOf(item)`** | Returns the first index where `item` is found, or **`-1`** if not present. |
| **`map(fn)`** | Creates and returns a **new array** by calling `fn` on every element of the original. Non-mutating. |
| **`filter(fn)`** | Creates and returns a **new array** of elements for which `fn` returns `true`. Non-mutating. |
| **`for...of`** | A loop construct that iterates over each **value** in an iterable (e.g., array), one by one. |
| **`split(separator)`** | A **String** method that divides a string at each `separator` and returns an **array** of substrings. |
| **`join(separator)`** | An **Array** method that combines all elements into a string, separated by the given `separator`. |
| **`toString()`** | Converts an array to a comma-separated string. Less flexible than `join()` — separator cannot be customized. |
| **Multidimensional Array** | An array where one or more elements are themselves arrays. Accessed via chained bracket notation: `arr[i][j]`. |
| **Mutation** | Modifying an array **in place** (the original array changes). Methods like `push`, `pop`, `splice` are mutating. |
| **Non-mutating** | Returning a new array without altering the original. `map()` and `filter()` are non-mutating. |

---

## Watch Out For...

1. **Zero-based indexing trap.** Arrays start at index `0`. A 5-element array's last item is `array[4]`, not `array[5]`. Accessing `array[5]` returns `undefined`, not an error.

2. **`length` ≠ last index.** `array.length` is always 1 more than the last valid index. The last element is always `array[array.length - 1]`.

3. **`push()` returns length, not the array.** A common exam trick: `const result = arr.push("x")` stores the **new length** (a number), not the modified array.

4. **`pop()` and `shift()` return the removed item, not the array.** `const removed = arr.pop()` captures the deleted element, not the remaining array.

5. **`split()` is a String method, not an Array method.** It lives on `String.prototype`. You call it on a string, and it gives you an array — not the other way around.

6. **`map()` and `filter()` do NOT modify the original.** They return a **new array**. If you don't assign the result, it's lost. Example mistake: `arr.map(double);` with no assignment — the result is discarded.

7. **Price strings must be converted explicitly.** After `split()`, all values are strings. Using a price string directly in math (`total += "6.99"`) causes **string concatenation**, not addition. Always use `Number()` or `parseFloat()`.

8. **`indexOf()` returning `-1` is falsy... but not `false`.** The check `if (arr.indexOf("x"))` is **wrong** — index `0` is also falsy! Always use `if (arr.indexOf("x") !== -1)`.

9. **`const` arrays are still mutable.** Declaring with `const` prevents reassigning the variable (`arr = []` fails), but you can still call `arr.push()`, `arr.pop()`, etc.

10. **`splice()` argument 2 is a COUNT, not an end index.** `arr.splice(1, 2)` removes **2 items** starting at index 1 — not "from index 1 to index 2."

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** You have `const arr = ["a", "b", "c", "d"]`. What is `arr[arr.length - 1]`? What does `arr.indexOf("z")` return?

**Q2.** What is the difference between `push()` and `unshift()`? What does each method **return**?

**Q3.** Given the array `["Manchester", "Liverpool", "Edinburgh", "Carlisle"]`, write the code to safely remove `"Liverpool"` using `indexOf()` and `splice()`.

**Q4.** Explain the difference between `map()` and `filter()`. Does either method mutate the original array?

**Q5.** You receive the string `"apple,banana,cherry"`. Write the code to: (a) split it into an array, (b) find the length of the array, and (c) join it back into a string using `" | "` as the separator.

---

## Answer Key

---

**A1.**
- `arr[arr.length - 1]` → `arr[3]` → **`"d"`** (last element).
- `arr.indexOf("z")` → **`-1`** (item not found in the array).

---

**A2.**
- `push(item)` adds to the **end** of the array.
- `unshift(item)` adds to the **beginning** of the array.
- Both return the **new length** of the array (a number), not the modified array.

---

**A3.**
```js
const cities = ["Manchester", "Liverpool", "Edinburgh", "Carlisle"];
const index = cities.indexOf("Liverpool"); // 1
if (index !== -1) {
  cities.splice(index, 1);
}
// cities → ["Manchester", "Edinburgh", "Carlisle"]
```
The `!== -1` guard prevents accidentally calling `splice(-1, 1)` which would remove the last element.

---

**A4.**
- `map(fn)` calls `fn` on **every element** and returns a **new array** of the return values — used to **transform** data.
- `filter(fn)` calls `fn` on each element and returns a **new array** of only those elements where `fn` returned **`true`** — used to **select** a subset.
- **Neither mutates** the original array. Both return brand-new arrays.

---

**A5.**
```js
const str = "apple,banana,cherry";

// (a) Split into array
const fruits = str.split(",");        // ["apple", "banana", "cherry"]

// (b) Find length
console.log(fruits.length);           // 3

// (c) Join with custom separator
const result = fruits.join(" | ");    // "apple | banana | cherry"
```
