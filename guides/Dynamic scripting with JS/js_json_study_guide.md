# 🗂️ JavaScript JSON (Working with JSON) — Exam Study Guide
**Source:** [MDN Web Docs — Working with JSON](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON)

---

## Executive Summary

**JSON (JavaScript Object Notation)** is a standard text-based format for representing structured data, modelled on JavaScript object syntax, and is the most common format for transmitting data between a server and a web application. Once JSON is received as a string, it must be **deserialized** into a JavaScript object using `JSON.parse()` before you can access its values; conversely, a JavaScript object must be **serialized** into a JSON string using `JSON.stringify()` before it can be transmitted. When using the Fetch API, `response.json()` handles the parsing step automatically — but knowing `JSON.parse()` and `JSON.stringify()` is essential for all other scenarios where JSON arrives as raw text or needs to be prepared for sending.

---

## Core Pillars

### 1. What Is JSON?

- **JSON** stands for **JavaScript Object Notation**.
- It is a **text-based data format** — at its core, JSON is just a specially-formatted string.
- It closely resembles JavaScript object/array literal syntax but has stricter rules.
- It is **language-independent** — virtually every programming language can read and write JSON.
- It is the standard format for transmitting data in web apps (client ↔ server).
- JSON files use the `.json` extension and the MIME type `application/json`.

> Think of JSON as a **photograph of a JavaScript object** — it captures the structure as text so it can be sent over a network, then reconstructed on the other side.

---

### 2. JSON Structure — What Valid JSON Looks Like

JSON can be a **single object**, a **top-level array**, or even a **single primitive value**.

**JSON as an object:**
```json
{
  "squadName": "Super hero squad",
  "homeTown": "Metro City",
  "formed": 2016,
  "active": true,
  "members": [
    {
      "name": "Molecule Man",
      "age": 29,
      "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
    },
    {
      "name": "Madame Uppercut",
      "age": 39,
      "powers": ["Million tonne punch", "Damage resistance"]
    }
  ]
}
```

**JSON as a top-level array:**
```json
[
  { "name": "Molecule Man", "age": 29 },
  { "name": "Madame Uppercut", "age": 39 }
]
```

**JSON as a primitive:**
```json
29
"Hello"
true
```

---

### 3. JSON Syntax Restrictions — What's Different from JS Objects

JSON is stricter than JavaScript object literal syntax. These are the rules you MUST know:

| Rule | JSON | Regular JS Object |
|---|---|---|
| **String keys** | Keys MUST be in double quotes | Keys can be unquoted identifiers |
| **String values** | Values MUST use double quotes | Can use single or double quotes |
| **Allowed primitives** | `string`, `number`, `true`, `false`, `null` | Any JS value |
| **Forbidden primitives** | `undefined`, `NaN`, `Infinity` | Allowed |
| **Functions** | ❌ NOT allowed | Allowed |
| **Special objects** | ❌ `Date`, `Set`, `Map` not allowed | Allowed |
| **Trailing commas** | ❌ NOT allowed | Allowed in modern JS |
| **Comments** | ❌ NOT allowed | Allowed |
| **Number notation** | Decimal only | Hex, octal etc. allowed |

```json
// ❌ INVALID JSON — these are common mistakes:
{
  name: "Bob",           // key must be in double quotes
  'city': 'London',      // single quotes not allowed
  score: undefined,      // undefined is not valid JSON
  getValue: function(){} // functions not allowed
}

// ✅ VALID JSON:
{
  "name": "Bob",
  "city": "London",
  "score": null,
  "active": true
}
```

> A single misplaced comma or missing double quote makes the entire JSON invalid. Use [JSONLint](https://jsonlint.com/) to validate.

---

### 4. Accessing Data in a Parsed JSON Object

Once JSON has been parsed into a JavaScript object, you access its data **exactly like any other JavaScript object** — using dot notation or bracket notation:

```js
// Parsed JSON object stored in superHeroes variable:
// {
//   "squadName": "Super hero squad",
//   "members": [
//     { "name": "Molecule Man", "powers": ["Radiation resistance", "Turning tiny"] },
//     { "name": "Madame Uppercut", "powers": ["Million tonne punch"] }
//   ]
// }

superHeroes.squadName;             // "Super hero squad"  — dot, simple property
superHeroes["homeTown"];           // bracket notation — same result
superHeroes.members[0];            // first member object
superHeroes.members[0].name;       // "Molecule Man"
superHeroes.members[1].powers[0];  // "Million tonne punch"
// Chain: variable → property → array index → property → array index
```

> **Key insight:** After parsing, there is nothing special about JSON data. It's just a normal JavaScript object — all dot/bracket notation rules apply.

---

### 5. `JSON.parse()` — String → JavaScript Object (Deserialization)

- Takes a **JSON string** as input.
- Returns a **JavaScript object/array** (or primitive).
- Called **deserialization** — taking serialized text and reconstructing a native object.
- Throws a `SyntaxError` if the string is not valid JSON.

```js
// Suppose we received this raw JSON string from a server:
const jsonString = '{"name": "Chris", "age": 38}';

// Parse it into a usable JS object:
const myObj = JSON.parse(jsonString);

myObj.name;   // → "Chris"
myObj.age;    // → 38

// Works on arrays too:
const jsonArray = '[1, 2, 3]';
const myArray = JSON.parse(jsonArray);
myArray[0];   // → 1

// Throws SyntaxError on invalid JSON:
JSON.parse("{'bad': 'json'}");  // ❌ single quotes → SyntaxError
```

---

### 6. `JSON.stringify()` — JavaScript Object → String (Serialization)

- Takes a **JavaScript object** (or array/primitive) as input.
- Returns a **JSON string**.
- Called **serialization** — converting a native object into a portable text format for transmission.
- Properties with values of `undefined`, functions, or symbols are **silently dropped**.

```js
const myObj = { name: "Chris", age: 38 };

const myString = JSON.stringify(myObj);
// → '{"name":"Chris","age":38}'     (a string, not an object)

typeof myObj;      // "object"
typeof myString;   // "string"

// Sending an object to a server — must stringify first:
fetch("/api/data", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(myObj)    // ← must be a string, not an object
});

// Things that get dropped by stringify:
const obj = { name: "Alice", fn: function() {}, score: undefined };
JSON.stringify(obj);  // → '{"name":"Alice"}'   (fn and score silently dropped)
```

---

### 7. `response.json()` — The Fetch Shortcut

When using the Fetch API, `response.json()` combines the `response.text()` + `JSON.parse()` steps into one:

```js
// Manual approach — using response.text() + JSON.parse():
fetch("superheroes.json")
  .then((response) => response.text())
  .then((text) => {
    const data = JSON.parse(text);  // ← manually parse the string
    render(data);
  });

// Shortcut — response.json() does both steps:
fetch("superheroes.json")
  .then((response) => response.json())  // ← parses automatically
  .then((data) => render(data));
```

---

### 8. `async/await` with Fetch + JSON — Modern Syntax

The MDN example uses `async/await` instead of `.then()` chains. This is equally valid and increasingly preferred for readability:

```js
async function populate() {
  // 1. Build the request
  const requestURL = "https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json";
  const request = new Request(requestURL);

  // 2. Await the HTTP response
  const response = await fetch(request);

  // 3. Await JSON parsing of the body
  const superHeroes = await response.json();
  //  ↑ superHeroes is now a plain JS object — treat it like any object

  // 4. Use the data
  populateHeader(superHeroes);
  populateHeroes(superHeroes);
}

populate();
```

> **`async`/`await` is syntactic sugar over Promises.** `await` pauses execution inside the `async` function and waits for the Promise to resolve, then returns the resolved value directly. The code reads like synchronous code but still executes asynchronously.

---

### 9. Full End-to-End Pattern — Fetch JSON and Render into the DOM

This is the complete pattern: fetch → parse → loop → DOM insertion.

```js
async function populate() {
  const response = await fetch("superheroes.json");
  const superHeroes = await response.json();  // JS object

  // Access top-level properties
  const header = document.querySelector("header");
  const h1 = document.createElement("h1");
  h1.textContent = superHeroes.squadName;     // dot access on parsed object
  header.appendChild(h1);

  // Access the members array — loop with for...of
  const section = document.querySelector("section");
  const heroes = superHeroes.members;         // array of hero objects

  for (const hero of heroes) {
    const article = document.createElement("article");
    const h2 = document.createElement("h2");
    h2.textContent = hero.name;

    const pID = document.createElement("p");
    pID.textContent = `Secret identity: ${hero.secretIdentity}`;

    // Access the nested powers array — inner for...of loop
    const ul = document.createElement("ul");
    for (const power of hero.powers) {
      const li = document.createElement("li");
      li.textContent = power;
      ul.appendChild(li);
    }

    article.appendChild(h2);
    article.appendChild(pID);
    article.appendChild(ul);
    section.appendChild(article);
  }
}

populate();
```

---

## Technical Deep-Dive

### Logic Walkthrough: Chained Property Access on Parsed JSON

Understanding how to navigate deep JSON structures is a core exam skill. Read each step of the chain:

```js
// JSON structure:
// {
//   "members": [                       ← array
//     { "powers": ["power A", "power B"] },  ← [0]
//     { "powers": ["power C", "power D"] }   ← [1]
//   ]
// }

superHeroes.members[1].powers[2];
// Step 1: superHeroes         → the top-level object
// Step 2: .members            → accesses the 'members' property → array of objects
// Step 3: [1]                 → second object in the array (index 1)
// Step 4: .powers             → accesses the 'powers' property → array of strings
// Step 5: [2]                 → third string in the powers array (index 2)

// If the top-level JSON IS an array (not an object):
// [ { "powers": ["X", "Y"] }, { "powers": ["A", "B"] } ]
superHeroes[0].powers[0];
// Step 1: superHeroes[0]  → first object in the top-level array
// Step 2: .powers         → accesses the 'powers' property
// Step 3: [0]             → first string in that array
```

---

### Logic Walkthrough: `JSON.parse()` vs. `JSON.stringify()` — Direction Matters

```
JavaScript Object  ──── JSON.stringify() ────►  JSON String (for sending/storing)
JSON String        ──── JSON.parse()     ────►  JavaScript Object (for using)

fetch response     ──── response.json() ─────►  JavaScript Object
                        (= response.text() + JSON.parse() combined)
```

```js
// Round-trip demonstration:
const original = { name: "Alice", score: 100 };

const serialized = JSON.stringify(original);
// → '{"name":"Alice","score":100}'   (a string)

const deserialized = JSON.parse(serialized);
// → { name: "Alice", score: 100 }   (an object again)

// Verify round-trip:
deserialized.name;   // "Alice"
deserialized.score;  // 100
```

---

### Logic Walkthrough: What Gets Lost in `JSON.stringify()`

```js
const data = {
  name: "Alice",
  age: 30,
  greet: function() { return "Hello!"; },  // function — DROPPED
  city: undefined,                          // undefined — DROPPED
  score: null,                              // null — KEPT  (null is valid JSON)
  active: true,                             // boolean — KEPT
  tags: ["js", "web"],                      // array — KEPT
};

JSON.stringify(data);
// → '{"name":"Alice","age":30,"score":null,"active":true,"tags":["js","web"]}'
// greet and city are silently dropped — no error, no warning
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **JSON** | JavaScript Object Notation — a text-based, language-independent data format based on JavaScript object literal syntax. Used to transmit structured data between systems. |
| **JSON string** | A JSON value stored as a string (e.g., `'{"name":"Bob"}'`). Must be parsed before it can be used as a JS object. |
| **Serialization** | Converting a JavaScript object into a JSON string (for sending/storing). Done with `JSON.stringify()`. |
| **Deserialization** | Converting a JSON string back into a native JavaScript object (for using). Done with `JSON.parse()`. |
| **`JSON.parse(jsonString)`** | Converts a JSON string into a JavaScript object/array. Throws `SyntaxError` if the input is invalid JSON. |
| **`JSON.stringify(object)`** | Converts a JavaScript object into a JSON string. Functions, `undefined`, and symbols are silently dropped. |
| **`response.json()`** | Fetch API method that reads the response body and automatically parses it as JSON. Returns a Promise resolving to the JavaScript object. |
| **`.json` file** | A text file containing valid JSON, served with MIME type `application/json`. |
| **MIME type** | A label identifying the format of content — JSON uses `application/json`. |
| **Double quotes** | JSON requires all string keys and string values to be wrapped in double quotes (`"`). Single quotes are invalid JSON. |
| **`null`** | A valid JSON primitive representing the intentional absence of a value. Note: `undefined` is NOT valid JSON. |
| **Trailing comma** | A comma after the last element in an object or array — valid in modern JavaScript, but INVALID in JSON. |
| **`async` function** | A function declared with the `async` keyword that enables `await` inside it. Used with Fetch to write asynchronous code in a readable, sequential style. |
| **`await`** | Keyword used inside an `async` function to pause execution until a Promise resolves. The resolved value is returned directly. |
| **Nested access** | Accessing data multiple levels deep in an object/array using chained dot/bracket notation: `obj.array[0].property`. |

---

## Watch Out For...

1. **JSON keys and string values MUST use double quotes.** Single quotes (`'`) are valid in JavaScript but cause a `SyntaxError` in JSON. `{"name": "Bob"}` is valid; `{'name': 'Bob'}` is not.

2. **`undefined`, `NaN`, and `Infinity` are NOT valid JSON values.** They are silently converted to `null` during `JSON.stringify()`. When parsing, JSON has no concept of them.

3. **Functions are not valid JSON** — and `JSON.stringify()` silently drops any property whose value is a function. If you expected a function to survive serialization, you'll get `undefined` back after parsing.

4. **Trailing commas are forbidden in JSON.** `[1, 2, 3,]` is valid JavaScript but invalid JSON. This is a very common source of JSON parse errors.

5. **Comments are not allowed in JSON.** `// comment` or `/* comment */` inside a `.json` file will break it entirely.

6. **`JSON.parse()` throws a `SyntaxError` on invalid input — there is no silent failure.** Always wrap manual `JSON.parse()` calls in `try/catch` if the input might be malformed.

7. **`response.json()` is still asynchronous.** Even in an `async` function, you must `await response.json()` to get the object. Forgetting `await` gives you a pending Promise, not an object.

8. **A JSON string is NOT the same as a JavaScript object.** `typeof JSON.stringify({})` is `"string"`. If you try to access `.name` on a JSON string instead of a parsed object, you get `undefined`.

9. **When the top-level JSON is an array, access it with `[0]` first, not with a property name.** If your JSON is `[{"name":"Alice"}, {"name":"Bob"}]`, you access data as `data[0].name`, not `data.name`.

10. **`null`, `true`, `false`, numbers, and strings are all valid top-level JSON.** JSON does not have to be an object or array — a standalone `29` or `"hello"` is technically valid JSON.

11. **`JSON.parse()` and `.json()` produce plain JavaScript objects, NOT JSON.** Once parsed, the data is regular JS — there is no special "JSON object" type. You work with it exactly like any other object.

12. **"Deserialization" is parse; "Serialization" is stringify.** These academic terms appear in exam questions. Deserialization = text → object; Serialization = object → text.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Name **four syntax rules** that make JSON stricter than regular JavaScript object literals. Give a concrete example of each violation.

**Q2.** What is the difference between **serialization** and **deserialization**? Which JavaScript method performs each operation?

**Q3.** Given the following JSON structure (already parsed into `data`), write the expression to access the string `"Teleportation"`:
```js
// data = {
//   "members": [
//     { "name": "Molecule Man", "powers": ["Radiation resistance", "Turning tiny"] },
//     { "name": "Eternal Flame", "powers": ["Immortality", "Heat Immunity", "Teleportation"] }
//   ]
// }
```

**Q4.** What is the difference between `response.json()` and calling `JSON.parse()` manually? When would you use `JSON.parse()` directly?

**Q5.** The following code has a bug — `myObj` is still a string after running. Fix it.
```js
const jsonText = '{"name": "Alice", "score": 99}';
const myObj = jsonText;
console.log(myObj.name);  // undefined
```

---

## Answer Key

---

**A1.**
Four JSON syntax rules (with violation examples):

1. **Keys must be double-quoted.**
   - ❌ `{ name: "Bob" }` — unquoted key
   - ✅ `{ "name": "Bob" }`

2. **String values must use double quotes (not single).**
   - ❌ `{ "name": 'Bob' }` — single quotes
   - ✅ `{ "name": "Bob" }`

3. **No trailing commas.**
   - ❌ `{ "name": "Bob", }` — trailing comma after last property
   - ✅ `{ "name": "Bob" }`

4. **No functions, `undefined`, or `NaN`/`Infinity`.**
   - ❌ `{ "fn": function(){}, "score": undefined, "ratio": Infinity }`
   - ✅ `{ "fn": null, "score": null, "ratio": null }` (or omit them)

Bonus: **No comments** — `// comment` and `/* comment */` are illegal in JSON.

---

**A2.**

| Term | Direction | Method |
|---|---|---|
| **Serialization** | JS object → JSON string | `JSON.stringify(object)` |
| **Deserialization** | JSON string → JS object | `JSON.parse(jsonString)` |

- **Serialization** prepares data for transmission or storage (network, localStorage, file).
- **Deserialization** reconstructs the native object from received text so it can be used in code.

---

**A3.**

```js
data.members[1].powers[2]
```

Chain breakdown:
1. `data` — the top-level object
2. `.members` — the members array
3. `[1]` — second object in the array (Eternal Flame, index 1)
4. `.powers` — the powers array
5. `[2]` — third string (index 2): `"Teleportation"`

---

**A4.**

| | `response.json()` | `JSON.parse(text)` manually |
|---|---|---|
| **How it works** | Reads body + parses JSON in one step — returns `Promise<object>` | You already have the string; you call `JSON.parse()` on it yourself |
| **Used with** | Fetch API Response object | Any raw JSON string (from `response.text()`, `localStorage`, a `<script>` tag, etc.) |
| **Returns** | Promise | The parsed object (synchronous) |

**Use `JSON.parse()` directly when:**
- You received JSON as raw text via `response.text()` (not `.json()`)
- You stored JSON in `localStorage` and are reading it back: `JSON.parse(localStorage.getItem("data"))`
- JSON arrived embedded in the page or from another non-fetch source

---

**A5.**
**Bug:** `jsonText` is a string. It was never parsed into an object — it was just assigned to `myObj` directly. `"string".name` is `undefined`.

**Fix:** Use `JSON.parse()` to deserialize the string into a JavaScript object:

```js
const jsonText = '{"name": "Alice", "score": 99}';
const myObj = JSON.parse(jsonText);  // ← deserialize the string
console.log(myObj.name);  // "Alice"
console.log(myObj.score); // 99
```

Or alternatively, if fetching the data, use `response.json()` which handles parsing automatically.
