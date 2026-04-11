# ⚡ JavaScript Events — Exam Study Guide
**Source:** [MDN Web Docs — Introduction to events](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events)

---

## Executive Summary

JavaScript **events** are signals fired by the browser when something meaningful happens — a click, a keypress, a form submission, a page load — that your code can listen and react to using **event handlers**. The recommended and most powerful mechanism for registering handlers is **`addEventListener()`**, which accepts an event name and a callback function, and allows multiple handlers on the same element. Mastering the three registration methods (and knowing which to avoid), the **event object** and its `target` property, and **`preventDefault()`** are the core skills tested in this topic.

---

## Core Pillars

### 1. What Is an Event?

- An event is a **signal produced by the browser** when something significant happens in the system.
- Events fire inside the **browser window** and are typically attached to a specific element.
- Your code **reacts** to events by attaching an **event listener** — a block of code that waits for a specific event to fire and then calls a **handler function**.
- Setting up code to respond to an event is called **registering an event handler**.

**Common event types:**

| Trigger | Example Events |
|---|---|
| Mouse interaction | `click`, `dblclick`, `mouseover`, `mouseout` |
| Keyboard | `keydown`, `keyup` |
| Form | `submit`, `change`, `focus`, `blur` |
| Page/media | page load, `play`, `pause`, error |
| Window | resize, close |

---

### 2. `addEventListener()` — The Recommended Method

- Called on any element (or the document/window) that can fire events.
- Takes **two required parameters**: the event name (a string) and the handler function (a callback).
- The **recommended** way to set up event handlers — most powerful and scalable.

```js
// Syntax
element.addEventListener("eventName", handlerFunction);

// Example — inline arrow function callback
const btn = document.querySelector("button");
btn.addEventListener("click", () => {
  document.body.style.backgroundColor = "red";
});

// Example — named function reference
function changeBackground() {
  document.body.style.backgroundColor = "blue";
}
btn.addEventListener("click", changeBackground);
```

> ⚠️ **Critical distinction:** Pass `changeBackground` (no parentheses) as the handler reference. Writing `changeBackground()` immediately **calls** the function and passes its return value (`undefined`) — the handler will never fire.

---

### 3. `removeEventListener()` — Unregistering Handlers

- Removes a previously attached event listener.
- Must be called with the **exact same function reference** that was used in `addEventListener()`.
- Anonymous/inline functions **cannot be removed** this way — you must use a named function reference.
- Useful for: preventing memory leaks in complex apps, toggling behaviour on/off.

```js
btn.addEventListener("click", changeBackground);

// Later, to remove it:
btn.removeEventListener("click", changeBackground);
// ✅ Works — same named function reference

// ❌ Cannot remove an anonymous function:
btn.addEventListener("click", () => { ... });
btn.removeEventListener("click", () => { ... });  // different object reference — fails silently
```

---

### 4. Multiple Listeners on One Event

- `addEventListener()` can be called **multiple times** on the same element for the same event.
- All registered handlers will fire — none overwrite the others.
- This is a key advantage over event handler properties (which only support one at a time).

```js
myElement.addEventListener("click", functionA);
myElement.addEventListener("click", functionB);
// Both functionA and functionB run on every click
```

---

### 5. Event Handler Properties (`onclick`, `onkeydown`, etc.)

- A legacy alternative: directly assign a function to a property named `on` + event name.
- Properties exist on element objects (e.g., `btn.onclick`, `input.onkeydown`).
- **Major limitation**: Only one handler can be assigned at a time — assigning a second overwrites the first.
- **Avoid in production** — use `addEventListener()` instead.

```js
btn.onclick = () => {
  document.body.style.backgroundColor = "green";
};

// ❌ Problem: this silently overwrites the handler above
btn.onclick = () => {
  document.body.style.backgroundColor = "yellow";  // only this one runs
};
```

---

### 6. Inline Event Handlers — Never Use These

- The oldest mechanism: JavaScript written directly inside HTML attributes (`onclick="..."`, `onkeydown="..."`).
- **Do not use** — considered bad practice for these reasons:
  - Mixes HTML and JavaScript, making code hard to read and maintain.
  - Doesn't scale — 100 buttons need 100 attributes.
  - Only one handler per element.
  - Many server configurations block inline JavaScript for **security** reasons.

```html
<!-- ❌ Bad practice — never do this -->
<button onclick="bgChange()">Press me</button>
<button onclick="alert('Old-fashioned!');">Press me</button>
```

```js
// ✅ Correct approach — JavaScript in a .js file
const buttons = document.querySelectorAll("button");
for (const button of buttons) {
  button.addEventListener("click", bgChange);
}
// One line handles ALL buttons, no matter how many there are
```

---

### 7. The Event Object

- When an event fires, the browser **automatically passes an event object** as the first argument to the handler function.
- Conventionally named `event`, `evt`, or `e` — any name works, but be consistent.
- The event object contains **information and methods** relevant to the event that occurred.
- **Key universal property: `event.target`** — always points to the element that fired the event.

```js
function bgChange(e) {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  e.target.style.backgroundColor = rndCol;  // ← applies to the button, not the whole page
  console.log(e);                            // ← inspect the full event object
}

btn.addEventListener("click", bgChange);
```

---

### 8. Specialised Event Objects

- Different event types produce **specialised event objects** with additional properties.
- Example: `keydown` fires a **`KeyboardEvent`** which has an `event.key` property identifying the pressed key.
- The base `Event` object is always present; specialised types extend it with extra properties.

```js
textBox.addEventListener("keydown", (event) => {
  output.textContent = `You pressed "${event.key}".`;
  // event.key → "a", "Enter", "ArrowUp", etc.
});
```

| Event type | Object type | Extra properties |
|---|---|---|
| `click`, `mouseover` | `MouseEvent` | `clientX`, `clientY`, `button` |
| `keydown`, `keyup` | `KeyboardEvent` | `key`, `code`, `shiftKey`, `ctrlKey` |
| `submit` | `SubmitEvent` | — |
| All events | `Event` (base) | `target`, `type`, `preventDefault()` |

---

### 9. `preventDefault()` — Blocking Default Browser Behaviour

- Some events have a **default browser action** (e.g., clicking Submit sends a form; clicking a link navigates).
- Call `event.preventDefault()` inside the handler to **stop that default action** from happening.
- Most commonly used for **custom form validation** — prevent submission if inputs are invalid.

```js
const form = document.querySelector("form");

form.addEventListener("submit", (e) => {
  if (fname.value === "" || lname.value === "") {
    e.preventDefault();           // ← stops the form from submitting
    para.textContent = "You need to fill in both names!";
  }
});
```

**How it works:**
1. User clicks Submit → `submit` event fires.
2. Handler checks if fields are empty.
3. If empty → `e.preventDefault()` cancels the browser's default form-send behaviour.
4. Error message is shown instead.

---

## Technical Deep-Dive

### Logic Walkthrough: Three Ways to Register an Event Handler (Compared)

```js
// ── METHOD 1: addEventListener() ── RECOMMENDED ────────────────────
btn.addEventListener("click", () => {
  document.body.style.backgroundColor = "red";
});
// ✅ Supports multiple listeners
// ✅ Can be removed with removeEventListener()
// ✅ Separates HTML and JS


// ── METHOD 2: Event handler property ── AVOID ─────────────────────
btn.onclick = () => {
  document.body.style.backgroundColor = "red";
};
// ❌ Only ONE handler at a time — second assignment overwrites first
// ⚠️ Available as a fallback for very simple scripts


// ── METHOD 3: Inline HTML attribute ── NEVER USE ──────────────────
// <button onclick="doSomething()">Click</button>
// ❌ Mixes HTML and JS
// ❌ Doesn't scale
// ❌ Security risk — many servers block it
```

---

### Logic Walkthrough: Event Object & `e.target`

```js
function bgChange(e) {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;

  // e.target = the element that fired the event (the button)
  e.target.style.backgroundColor = rndCol;
  //           ↑
  //  changes the BUTTON's background, not the page body
}

btn.addEventListener("click", bgChange);
```

**Why `e.target` matters:** Without it, you'd have to hardcode `btn.style.backgroundColor`, which only works for that specific button. Using `e.target` makes the handler **element-agnostic** — the same function can be attached to many buttons and each one will style itself.

```js
// Generic handler works on ALL buttons
const buttons = document.querySelectorAll("button");
for (const button of buttons) {
  button.addEventListener("click", (e) => {
    e.target.style.backgroundColor = "hotpink";
    // e.target is always the specific button that was clicked
  });
}
```

---

### Logic Walkthrough: Form Validation with `preventDefault()`

```js
const form   = document.querySelector("form");
const fname  = document.getElementById("fname");
const lname  = document.getElementById("lname");
const para   = document.querySelector("p");

form.addEventListener("submit", (e) => {
  // Check both fields
  if (fname.value === "" || lname.value === "") {
    e.preventDefault();   // ← kills default submit → page doesn't reload/redirect
    para.textContent = "You need to fill in both names!";
    // Error message shown to user instead
  }
  // If both fields have values, we fall through without calling preventDefault()
  // → default submit behaviour proceeds normally
});
```

**The pattern:** The event listener on `"submit"` intercepts the submission before it reaches the server. `e.preventDefault()` is only called conditionally — if validation passes, the default action (send the form) proceeds untouched.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Event** | A signal fired by the browser when something significant happens (click, keypress, page load, etc.). |
| **Event listener** | The code feature that "listens" for a specific event and triggers a handler function when the event fires. |
| **Event handler** | The function that runs in response to an event. Also called a **handler function** or **callback**. |
| **Registering an event handler** | The act of attaching an event listener to an element so the handler runs when the event fires. |
| **`addEventListener(eventName, handler)`** | The recommended method to register an event handler. Accepts the event name string and a callback function. |
| **`removeEventListener(eventName, handler)`** | Removes a previously registered event listener. Requires the same named function reference used in `addEventListener()`. |
| **Event handler property** | An element property named `on` + event (e.g., `btn.onclick`). Accepts one handler function at a time; second assignments overwrite the first. |
| **Inline event handler** | JavaScript written directly in an HTML attribute (e.g., `onclick="..."`). Outdated and should never be used. |
| **Event object** | An object automatically passed to the handler function containing information about the event. Conventionally named `e`, `evt`, or `event`. |
| **`event.target`** | A property of the event object that always references the **specific element** the event was fired on. |
| **`KeyboardEvent`** | A specialised event object produced by keyboard events (`keydown`, `keyup`). Has an `event.key` property for the key pressed. |
| **`MouseEvent`** | A specialised event object for mouse events. Contains coordinates (`clientX`, `clientY`) and button info. |
| **`event.preventDefault()`** | A method called on the event object to cancel the browser's default behaviour for that event (e.g., stops form submission). |
| **Default behavior** | The browser's built-in response to an event — e.g., navigating on link click, submitting on form submit. Cancelable with `preventDefault()`. |
| **Event bubbling** | (Preview) When an event fires on a nested element, it also propagates up through its parent elements. Covered in the next module. |

---

## Watch Out For...

1. **Passing vs. calling the handler.** `btn.addEventListener("click", changeBackground)` is correct. `btn.addEventListener("click", changeBackground())` immediately calls the function and passes its return value (`undefined`) — the click will never trigger anything. **No parentheses on the handler reference.**

2. **`e.target` vs. hardcoded element reference.** `e.target` refers to the element that fired the event — it's dynamic and reusable. Hardcoding the element reference works only for that one specific element and breaks as soon as you reuse the handler on another element.

3. **Event handler properties only support one handler.** `btn.onclick = fn1; btn.onclick = fn2` — only `fn2` runs. `addEventListener()` stacks them. This is why `addEventListener()` is preferred.

4. **You cannot remove an anonymous function.** `removeEventListener` requires the **exact same function reference**. An arrow function written inline creates a new anonymous object each time — `removeEventListener` cannot match it. Always store functions in named variables if you intend to remove them later.

5. **Inline event handlers are a security risk.** Most Content Security Policies (CSPs) block inline JavaScript execution by default. Code that relies on `onclick="..."` attributes will silently fail in secure environments.

6. **`preventDefault()` doesn't stop the handler from running.** It only cancels the browser's _default action_ for that event. Your handler code still executes fully before and after the call.

7. **`event.key` vs. `event.keyCode`.** `event.key` returns a human-readable string like `"Enter"` or `"a"`. The older `event.keyCode` returns a numeric code — it is deprecated. Always use `event.key`.

8. **The event object is only available inside the handler.** It's automatically provided by the browser as the first argument — you don't create it manually. If your handler doesn't declare an `e` parameter, you can't access it.

9. **Different events have different event objects.** A `click` gives you a `MouseEvent`; a `keydown` gives you a `KeyboardEvent`. They all inherit from the base `Event`, but the extra properties (like `event.key` or `event.clientX`) are only available on the appropriate specialised type.

10. **Not every event is available on every element.** `click` works on almost anything; `play` and `pause` only fire on media elements (`<video>`, `<audio>`). Attaching a `play` listener to a button silently does nothing.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the **three methods** for registering an event handler in JavaScript? Which is recommended, and why?

**Q2.** What is the **event object**, and what does `event.target` refer to? Give a practical example of why `event.target` is more useful than hardcoding the element reference.

**Q3.** The following code registers a click handler but it doesn't work. Identify the bug and fix it.
```js
const btn = document.querySelector("button");
function handleClick() {
  alert("Clicked!");
}
btn.addEventListener("click", handleClick());
```

**Q4.** Why can't you remove an event listener that was registered with an anonymous/arrow function? How do you fix this?

**Q5.** What does `event.preventDefault()` do? Write a short code example showing its most common use case — form validation.

---

## Answer Key

---

**A1.**
The three methods are:

| Method | Syntax | Status |
|---|---|---|
| **`addEventListener()`** | `btn.addEventListener("click", fn)` | ✅ Recommended |
| **Event handler property** | `btn.onclick = fn` | ⚠️ Limited — use sparingly |
| **Inline HTML attribute** | `<button onclick="fn()">` | ❌ Never use |

`addEventListener()` is recommended because:
- It supports **multiple handlers** for the same event (the others don't).
- It can be **removed** with `removeEventListener()`.
- It keeps **JS and HTML separate**, improving readability and maintainability.

---

**A2.**
The **event object** is an object automatically provided by the browser as the first argument to every handler function. It contains information about the event that occurred (what was clicked, which key was pressed, etc.).

**`event.target`** always refers to the **specific element** that triggered the event — not the element the listener is attached to (which could be a parent in the case of event bubbling).

**Practical example:**
```js
// ✅ Using e.target — handler is reusable across ALL buttons
document.querySelectorAll("button").forEach(button => {
  button.addEventListener("click", (e) => {
    e.target.style.backgroundColor = "hotpink";
    // Each button colours itself — no hardcoded reference needed
  });
});

// ❌ Hardcoded reference — only works for 'btn', not any other button
btn.addEventListener("click", () => {
  btn.style.backgroundColor = "hotpink";
});
```

---

**A3.**
**Bug:** `handleClick()` is called with parentheses, which immediately **invokes the function** and passes its return value (`undefined`) to `addEventListener`. The click event is attached to `undefined`, so nothing ever fires.

**Fix:** Remove the parentheses — pass the **function reference**, not its return value:
```js
btn.addEventListener("click", handleClick);  // ✅ no ()
```

---

**A4.**
`removeEventListener()` works by matching the **exact same function reference** that was passed to `addEventListener()`. An anonymous function (or arrow function written inline) creates a **new function object** every time it's written — so even if the code looks identical, it's a different reference and `removeEventListener` can't match it.

**Fix:** Store the function in a named variable before registering it:
```js
// ❌ Cannot remove — anonymous function, no reference saved
btn.addEventListener("click", () => { doSomething(); });
btn.removeEventListener("click", () => { doSomething(); });  // different object — fails

// ✅ Can remove — named reference saved
const handler = () => { doSomething(); };
btn.addEventListener("click", handler);
btn.removeEventListener("click", handler);  // same reference — works
```

---

**A5.**
`event.preventDefault()` **cancels the browser's built-in default action** for that event. The handler still runs; only the automatic browser response is suppressed.

**Most common use case — form validation:**
```js
const form  = document.querySelector("form");
const fname = document.getElementById("fname");
const lname = document.getElementById("lname");
const para  = document.querySelector("p");

form.addEventListener("submit", (e) => {
  if (fname.value === "" || lname.value === "") {
    e.preventDefault();  // ← stops the form from being sent to the server
    para.textContent = "Please fill in both name fields!";
  }
  // If both fields are filled, no preventDefault() → browser submits normally
});
```

Without `e.preventDefault()`, the form would submit immediately, the page would redirect, and the user would never see the error message.
