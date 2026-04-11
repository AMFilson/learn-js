# 🌳 JavaScript DOM Scripting — Exam Study Guide
**Source:** [MDN Web Docs — DOM scripting introduction](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/DOM_scripting)

---

## Executive Summary

The **Document Object Model (DOM)** is a tree-structured representation of an HTML page that the browser builds when it loads a document, enabling JavaScript to read and dynamically modify every element, attribute, and piece of text on the page. Four fundamental skill areas are tested: **selecting nodes** (querySelector, getElementById), **creating and inserting new nodes** (createElement, appendChild), **removing nodes** (removeChild, remove), and **manipulating styles** (via `element.style` properties or `classList`). The article culminates in a real-world shopping list exercise that combines all four skills — querying the DOM, creating elements programmatically, appending them to the tree, and removing them with event-driven delete buttons.

---

## Core Pillars

### 1. The Browser's Three Key Objects

JavaScript interacts with the browser through three major API objects:

| Object | Represents | Key Uses |
|---|---|---|
| **`Window`** | The browser tab / window | `Window.innerWidth`, `Window.innerHeight`, storing client-side data, attaching window-level events |
| **`Navigator`** | The browser's identity and state | User's preferred language, accessing webcam/media stream |
| **`Document`** | The actual HTML page (DOM) | Selecting elements, creating nodes, modifying content and styles |

> For DOM scripting, **`Document` is the one you use most.** The global `document` object is always available in browser JS — it's the entry point to every element on the page.

---

### 2. The DOM as a Tree

- The browser parses HTML and builds a **tree structure** of **nodes**.
- Each element, text string, attribute, and comment is a **node**.
- The two most common node types are **element nodes** (`<p>`, `<div>`, `<a>`) and **text nodes** (the actual text content inside elements).

**DOM vocabulary you must know:**

| Term | Definition |
|---|---|
| **Root node** | The top of the tree — always `<html>` in an HTML document |
| **Child node** | A node **directly** inside another node (`<img>` is a child of `<section>`) |
| **Descendant node** | Any node inside another, at any nesting depth (`<img>` is a descendant of `<body>`) |
| **Parent node** | The node that directly contains another (`<body>` is the parent of `<section>`) |
| **Sibling nodes** | Nodes at the **same level** under the same parent (`<img>` and `<p>` are siblings if both are children of `<section>`) |

```
HTML tree diagram:
  HTML
  ├── HEAD
  │   └── META, TITLE, ...
  └── BODY
      └── SECTION
          ├── IMG         ← child of SECTION, sibling of P
          └── P           ← child of SECTION, sibling of IMG
              └── A       ← child of P
```

---

### 3. Selecting DOM Nodes — Querying the DOM

Before you can manipulate an element, you need a **reference** to it stored in a variable.

```js
// ── MODERN METHODS (preferred) ─────────────────────────────────────

// Select the FIRST element matching a CSS selector
const link = document.querySelector("a");
const box  = document.querySelector("#container");
const btn  = document.querySelector(".submit-btn");

// Select ALL elements matching a CSS selector → returns a NodeList
const allParas = document.querySelectorAll("p");
// allParas is array-like — iterate with for...of or forEach

// ── OLDER METHODS (still valid, seen in legacy code) ───────────────

// Select by id attribute
const el = document.getElementById("myId");

// Select all elements of a given tag → returns HTMLCollection
const paras = document.getElementsByTagName("p");
```

> **`querySelector()` is the recommended modern approach** — it accepts any CSS selector, is versatile, and replaces most use cases of `getElementById` and `getElementsByTagName`.

---

### 4. Modifying Existing Nodes — Text Content and Attributes

Once you have a node reference, you can read and write its properties:

```js
const link = document.querySelector("a");

// Reading/writing text content
link.textContent;                           // get the text inside the element
link.textContent = "Mozilla Developer Network";  // set text (overwrites all children)

// Reading/writing HTML attributes (as regular JS properties)
link.href = "https://developer.mozilla.org";  // updates the href attribute
link.href;                                     // reads the current href
```

---

### 5. Creating and Inserting New Nodes

Three-step pattern: **create → configure → append**.

```js
const sect = document.querySelector("section");

// Step 1: Create a new element node
const para = document.createElement("p");

// Step 2: Set its content / attributes
para.textContent = "We hope you enjoyed the ride.";

// Step 3: Add it to the DOM tree as a child of 'sect'
sect.appendChild(para);
// ← para is now the last child of sect in the live DOM
```

**Creating a text node separately:**
```js
// Create a bare text node (no surrounding element)
const text = document.createTextNode(" — the premier source for web development knowledge.");

// Append it to an existing element
const linkPara = document.querySelector("p");
linkPara.appendChild(text);
// ← appends the text to the END of linkPara's children
```

> **`appendChild()` always appends to the end.** The new node becomes the last child of the parent.

---

### 6. Moving Existing Nodes

- `appendChild()` on a node that **already exists in the DOM** will **move** it, not copy it.
- There is only ever **one copy** of any given node in the DOM.
- To create a true duplicate, use `Node.cloneNode()`.

```js
// Moving:
sect.appendChild(linkPara);
// ← linkPara moves to the bottom of sect — it is NOT duplicated

// Cloning:
const copy = linkPara.cloneNode(true);  // true = deep clone (includes children)
sect.appendChild(copy);
// ← now there are two copies — original stays, copy is added
```

---

### 7. Removing Nodes

Two ways to remove a node:

```js
// Method 1: removeChild() — via the parent (works in all browsers)
sect.removeChild(linkPara);
// ← removes linkPara from sect

// Method 2: remove() — directly on the node (modern, cleaner)
linkPara.remove();
// ← self-removal — no need to know the parent

// Legacy fallback for very old browsers (if .remove() unsupported):
linkPara.parentNode.removeChild(linkPara);
// ← walks up to the parent then removes the child
```

---

### 8. Manipulating Styles — Two Approaches

#### Method A: Inline styles via `element.style`

- Directly sets individual CSS properties as **inline styles** on the element.
- JavaScript uses **camelCase** for property names (CSS uses kebab-case).
- Quick for dynamic, one-off changes — but mixes JS and style logic.

```js
para.style.color           = "white";
para.style.backgroundColor = "black";    // ← camelCase! (CSS: background-color)
para.style.padding         = "10px";
para.style.width           = "250px";
para.style.textAlign       = "center";   // ← camelCase! (CSS: text-align)

// Result in HTML:
// <p style="color: white; background-color: black; ...">...</p>
```

#### Method B: `classList` — toggling CSS classes (preferred)

- Keeps **styles in CSS** and only toggles class names from JavaScript.
- Cleaner separation of concerns — more maintainable.
- `classList` has a full API: `add()`, `remove()`, `toggle()`, `contains()`.

```js
// CSS (in a <style> block or stylesheet):
// .highlight { color: white; background-color: black; padding: 10px; }

// JavaScript — just add/remove the class
para.classList.add("highlight");       // applies the CSS class
para.classList.remove("highlight");   // removes it
para.classList.toggle("highlight");   // adds if absent, removes if present
para.classList.contains("highlight"); // → true/false
```

> **Prefer `classList` for anything beyond simple one-off dynamic changes.** Inline `element.style` is fine for quick/temporary values; for app-level styling logic, `classList` keeps CSS and JS properly separated.

---

### 9. Full Pattern — Dynamic Shopping List

This exercise combines all DOM skills together in a real-world workflow:

```js
// References to existing DOM elements
const list   = document.querySelector("ul");
const input  = document.querySelector("input");
const button = document.querySelector("button");

button.addEventListener("click", (event) => {

  // 1. Prevent form from submitting and reloading the page
  event.preventDefault();

  // 2. Capture and clear the input value
  const myItem  = input.value;
  input.value   = "";

  // 3. Create new DOM nodes
  const listItem = document.createElement("li");
  const listText = document.createElement("span");
  const listBtn  = document.createElement("button");

  // 4. Assemble the tree: span + button inside li
  listItem.appendChild(listText);
  listText.textContent = myItem;    // set text from input
  listItem.appendChild(listBtn);
  listBtn.textContent  = "Delete";

  // 5. Attach the new li to the ul
  list.appendChild(listItem);

  // 6. Wire up: delete button removes its parent li
  listBtn.addEventListener("click", () => {
    list.removeChild(listItem);
  });

  // 7. Re-focus input for next entry
  input.focus();
});
```

---

## Technical Deep-Dive

### Logic Walkthrough: Three-Step DOM Insertion Pattern

Understanding **create → configure → append** is the exam-critical pattern for inserting nodes:

```
Step 1: document.createElement("p")
        ─────────────────────────────
        Creates a detached <p> node.
        It exists in memory but is NOT in the DOM yet.
        The user cannot see it.

Step 2: para.textContent = "Hello!"
        ─────────────────────────────
        Configures the node while it's still detached.
        Set text, attributes, classes, styles before inserting.

Step 3: parent.appendChild(para)
        ─────────────────────────────
        Attaches the configured node to the live DOM tree.
        Browser immediately renders it — user can now see it.
```

```js
// Full example: dynamically add a styled paragraph
const container = document.querySelector("#output");

const msg = document.createElement("p");       // Step 1 — detached
msg.textContent = "Item added!";               // Step 2 — configure text
msg.classList.add("success-message");          // Step 2 — configure class
container.appendChild(msg);                    // Step 3 — attach, render
```

---

### Logic Walkthrough: `querySelector` vs. Older Methods

```js
// ── querySelector / querySelectorAll ──────────────────────────────
// Selector: any valid CSS selector string
// Returns: the FIRST matching element (or null)
document.querySelector("p");               // first <p>
document.querySelector("#nav");            // element with id="nav"
document.querySelector(".btn.primary");    // first element with both classes
document.querySelector("ul > li:first-child"); // CSS combinators work too

// Returns: a STATIC NodeList of all matches
document.querySelectorAll("p");            // all <p> elements
// Iterate with for...of:
for (const p of document.querySelectorAll("p")) {
  p.style.color = "blue";
}

// ── getElementById ─────────────────────────────────────────────────
// Only matches id — no CSS selector syntax needed
// Returns: the element, or null
document.getElementById("myId");          // equivalent to querySelector("#myId")
// Advantage: very slightly faster — a direct id lookup

// ── getElementsByTagName ───────────────────────────────────────────
// Returns: a LIVE HTMLCollection (updates automatically as DOM changes)
document.getElementsByTagName("p");       // all <p> elements (live collection)
// ⚠️ Quirk: it's live — if you add a <p> mid-loop, the collection updates
```

---

### Logic Walkthrough: CSS Style Property Casing

JavaScript's `element.style` API uses **camelCase** equivalents of CSS's **kebab-case** property names:

| CSS property (kebab-case) | JS `element.style` (camelCase) |
|---|---|
| `background-color` | `backgroundColor` |
| `text-align` | `textAlign` |
| `font-size` | `fontSize` |
| `border-radius` | `borderRadius` |
| `padding-top` | `paddingTop` |
| `z-index` | `zIndex` |
| `flex-direction` | `flexDirection` |

```js
// ❌ Wrong — hyphenated doesn't work in JS property access
para.style.background-color = "red";    // SyntaxError — JS reads - as minus

// ✅ Correct — camelCase
para.style.backgroundColor = "red";
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **DOM (Document Object Model)** | A tree-structured representation of an HTML page created by the browser, which JavaScript uses to read and dynamically modify any element, attribute, or text on the page. |
| **Node** | A single entry in the DOM tree. Can be an element node, text node, comment node, etc. |
| **Element node** | A DOM node representing an HTML element (e.g., `<p>`, `<div>`, `<a>`). |
| **Text node** | A DOM node containing only text content — the actual string inside an element. Created with `document.createTextNode()`. |
| **`document`** | The global `Document` object — the entry point to all DOM manipulation. Represents the entire loaded page. |
| **`document.querySelector(selector)`** | Returns the **first** element in the document matching the given CSS selector. Returns `null` if none found. Recommended modern approach. |
| **`document.querySelectorAll(selector)`** | Returns a **static NodeList** of all elements matching the CSS selector. Can be iterated with `for...of`. |
| **`NodeList`** | An array-like object returned by `querySelectorAll`. Not a true array, but can be iterated. |
| **`document.getElementById(id)`** | Returns the element with the specified `id` attribute. Older approach, but still common and fast. |
| **`document.createElement(tagName)`** | Creates a new, **detached** element node of the given type (e.g., `"p"`, `"li"`). Must be appended to be visible. |
| **`document.createTextNode(text)`** | Creates a new, detached text node containing the given string. |
| **`node.appendChild(child)`** | Appends a node as the **last child** of a parent node, inserting it into the live DOM. If the child already exists in the DOM, it is **moved**, not copied. |
| **`node.textContent`** | Gets or sets the text content of a node and all its descendants. Setting it replaces all child nodes with a single text node. |
| **`node.removeChild(child)`** | Removes a specified child node from the parent and returns it. |
| **`element.remove()`** | Removes the element directly from the DOM without needing to reference its parent. Not supported in very old browsers. |
| **`node.cloneNode(deep)`** | Creates a copy of a node. Pass `true` for a deep clone (includes all descendants). |
| **`node.parentNode`** | A reference to the parent node of the current node. Used in the legacy removal pattern: `node.parentNode.removeChild(node)`. |
| **`element.style`** | An object exposing the element's inline CSS styles as JavaScript properties. Property names use camelCase (e.g., `backgroundColor`). |
| **`element.classList`** | An object providing methods to add, remove, toggle, and check CSS classes on an element. `add()`, `remove()`, `toggle()`, `contains()`. |
| **`classList.add(className)`** | Adds a CSS class to an element. |
| **`classList.remove(className)`** | Removes a CSS class from an element. |
| **`classList.toggle(className)`** | Adds the class if absent; removes it if present. |
| **`element.focus()`** | Programmatically gives keyboard focus to an element (e.g., puts the cursor in an `<input>`). |
| **`Window`** | Browser API object representing the current browser tab — provides window size, storage, and window-level events. |
| **`Navigator`** | Browser API object representing the browser's identity and capabilities — language, media devices, etc. |

---

## Watch Out For...

1. **CSS kebab-case → JavaScript camelCase for `element.style`.** `background-color` becomes `backgroundColor`, `text-align` becomes `textAlign`. Using hyphens in JS property access causes a `SyntaxError`.

2. **`appendChild()` moves, not copies, existing nodes.** If a node is already in the DOM and you `appendChild()` it elsewhere, it is **moved** from its current position. No duplicate is created. Use `cloneNode(true)` if you need a copy.

3. **`createElement()` creates a detached node.** The element exists in memory but is invisible until you attach it to the DOM with `appendChild()` or a similar method. Forgetting the append step is a very common bug.

4. **`querySelector()` returns the first match only.** If you need all matching elements, use `querySelectorAll()`. Using `querySelector()` when you expect multiple results silently ignores all but the first.

5. **`querySelectorAll()` returns a NodeList, not an Array.** You can iterate it with `for...of`, but built-in array methods like `.map()` or `.filter()` are not available unless you convert it first: `Array.from(nodeList)`.

6. **`getElementsByTagName()` returns a live collection; `querySelectorAll()` returns a static snapshot.** Modifying the DOM while looping over a live `getElementsByTagName` result can cause infinite loops or skipped elements.

7. **`textContent` vs. `innerHTML`.** `textContent` sets/gets plain text — it **escapes HTML**. `innerHTML` parses and renders HTML inside the string, which is a security risk (XSS) if used with user input. Prefer `textContent` for plain text.

8. **`element.style` only reflects inline styles, not stylesheet-applied styles.** If a style is applied via a CSS class or external stylesheet, `element.style.color` returns `""` (empty). Use `getComputedStyle(element)` to get the effective computed value.

9. **The `classList` approach is preferred over `element.style` for most styling.** Inline styles mix JS and CSS, have high specificity, are hard to override, and make codebases harder to maintain. Toggle CSS classes instead.

10. **`remove()` is not supported in very old browsers.** If legacy support is needed, use the `node.parentNode.removeChild(node)` pattern. In modern projects, `remove()` is universally available.

11. **`input.value` captures the current text; setting it to `""` clears the field.** This is the standard pattern for reading then resetting form inputs — always clear after capturing the value.

12. **`event.preventDefault()` is required in form-related button clicks.** Without it, clicking a `<button>` inside a `<form>` submits the form and reloads the page, destroying all dynamically added DOM content.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Name the **three browser objects** central to web development. What does each represent and what is each primarily used for in JavaScript?

**Q2.** What is the difference between a **child node** and a **descendant node** in the DOM tree? Give an example using HTML nesting.

**Q3.** Explain the **three-step pattern** to create and display a new element on the page. Write code that creates a `<p>` element with the text "Hello, world!" and appends it to a `<div id="output">`.

**Q4.** What is the difference between `querySelector()` and `querySelectorAll()`? What type does each return, and how do you iterate over the result of `querySelectorAll()`?

**Q5.** The following code is supposed to make a paragraph's background red and text white, but it doesn't work. Identify and fix the bug.
```js
const para = document.querySelector("p");
para.style.background-color = "red";
para.style.color = "white";
```

---

## Answer Key

---

**A1.**

| Object | Represents | Primary JS Use |
|---|---|---|
| **`Window`** | The browser tab/window | `window.innerWidth`, data storage, window-level events |
| **`Navigator`** | The browser's identity and state | `navigator.language`, accessing webcam/media |
| **`Document`** | The actual HTML page (the DOM) | Selecting, creating, modifying, and deleting HTML elements |

`Document` (accessed as the global `document`) is the object used most in everyday DOM scripting.

---

**A2.**
- A **child node** is a node **directly inside** another node — one level deep only.
- A **descendant node** is a node **anywhere inside** another node — any number of levels deep.

```html
<body>
  <section>           ← child of body (also a descendant of body)
    <img>             ← child of section, descendant of section AND body
    <p>
      <a>Link</a>     ← child of p, descendant of p, section, AND body
    </p>
  </section>
</body>
```

`<img>` is a child of `<section>` and a descendant of `<body>`, but **not** a child of `<body>` (it's two levels below).

---

**A3.**
The three-step pattern is: **Create** a node → **Configure** it → **Append** it to the DOM.

```js
// Step 1: Create a detached element node (not yet in the DOM/visible)
const para = document.createElement("p");

// Step 2: Configure content and attributes
para.textContent = "Hello, world!";

// Step 3: Append to the DOM (now visible on the page)
const output = document.querySelector("#output");
output.appendChild(para);
```

Without Step 3, the element exists in memory but the user never sees it.

---

**A4.**

| | `querySelector(selector)` | `querySelectorAll(selector)` |
|---|---|---|
| **Returns** | The **first** matching element, or `null` | A **static NodeList** of all matching elements |
| **Count** | Always 0 or 1 element | 0 to N elements |
| **Miss case** | Returns `null` | Returns an empty NodeList |

**Iterating `querySelectorAll()` results:**
```js
const allParas = document.querySelectorAll("p");

// ✅ for...of — cleanest
for (const p of allParas) {
  p.style.color = "blue";
}

// ✅ forEach (NodeList has a built-in forEach)
allParas.forEach(p => p.classList.add("highlight"));

// ✅ Convert to array first to use map/filter
Array.from(allParas).map(p => p.textContent);
```

---

**A5.**
**Bug:** `para.style.background-color` uses kebab-case — in JavaScript, the hyphen is interpreted as the **minus operator** (subtraction), causing a `SyntaxError`. JavaScript's `element.style` API uses **camelCase** property names.

**Fix:**
```js
const para = document.querySelector("p");
para.style.backgroundColor = "red";   // ✅ camelCase — not background-color
para.style.color = "white";           // ✅ already correct
```

Or better yet, use `classList` to keep styles in CSS:
```js
// In CSS: .error-style { background-color: red; color: white; }
para.classList.add("error-style");    // ✅ preferred approach
```
