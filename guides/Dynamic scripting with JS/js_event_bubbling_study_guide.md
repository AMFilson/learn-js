# 🫧 JavaScript Event Bubbling — Exam Study Guide
**Source:** [MDN Web Docs — Event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling)

---

## Executive Summary

**Event bubbling** is the browser's mechanism by which an event fired on a nested element automatically propagates upward through all of its ancestor elements in the DOM — triggering any matching listeners along the way. Understanding bubbling is essential for both **debugging unexpected handler triggers** (like a child click firing a parent's handler) and **exploiting it intentionally** through **event delegation** — attaching a single listener on a parent to handle events from many child elements efficiently. The critical tools in this module are **`stopPropagation()`** to halt unwanted bubbling, and knowing the difference between **`event.target`** (where the event originated) and **`event.currentTarget`** (where the handler is attached).

---

## Core Pillars

### 1. What Is Event Bubbling?

- When an event fires on an element, it first runs that element's handlers, then moves **up** to the parent, then the grandparent, all the way to the document root.
- The event **"bubbles up"** like a bubble rising through water — from the innermost element outward.
- This happens automatically on almost all events by default — you don't turn it on, it's just how events work.

```
DOM structure:
  <body>
    <div id="container">
      <button>Click me!</button>
    </div>
  </body>

When button is clicked → event fires on:
  1. BUTTON   ← innermost (origin)
  2. DIV      ← parent
  3. BODY     ← grandparent
```

```js
// All three log in order: BUTTON → DIV → BODY
document.body.addEventListener("click", handleClick);
container.addEventListener("click", handleClick);
button.addEventListener("click", handleClick);

function handleClick(e) {
  output.textContent += `You clicked on a ${e.currentTarget.tagName} element\n`;
}
// Output on button click:
// "You clicked on a BUTTON element"
// "You clicked on a DIV element"
// "You clicked on a BODY element"
```

---

### 2. When Bubbling Causes Problems

- If a **child** and a **parent** both have listeners for the same event, clicking the child triggers **both handlers** unexpectedly.
- Classic example: a video inside a `<div>` — clicking the video to play it also triggers the `<div>`'s "hide" handler because the click bubbles up.

```js
// Bug scenario — video player
btn.addEventListener("click", () => box.classList.remove("hidden"));  // show box
video.addEventListener("click", () => video.play());                  // play video
box.addEventListener("click", () => box.classList.add("hidden"));     // hide box

// Problem: clicking the video triggers BOTH:
//   1. video.play()           ← intended
//   2. box.classList.add("hidden")  ← NOT intended (bubbled from video to box)
```

---

### 3. `stopPropagation()` — Halting the Bubble

- Called on the event object inside a handler to **stop the event from propagating further up** the DOM.
- The current handler still completes — only the upward propagation is cut off.
- Prevents parent handlers from being triggered by a child's event.

```js
// Fix — stop the click from bubbling up from video to box
video.addEventListener("click", (event) => {
  event.stopPropagation();  // ← kills the bubble here
  video.play();             // ← still executes normally
});

// Now clicking the video:
//   1. video.play()     ← runs ✅
//   2. box handler      ← NEVER triggered ✅ (propagation stopped)
```

---

### 4. Event Capture — The Opposite Direction

- **Event capture** is the reverse of bubbling — events fire on the **outermost ancestor first**, then travel inward to the target element.
- Disabled by default. To enable it, pass `{ capture: true }` as the third argument to `addEventListener()`.
- Capture phase fires **before** bubbling — so capture handlers run top-down, then bubble handlers run bottom-up.

```js
// Capture mode — event fires: BODY → DIV → BUTTON
document.body.addEventListener("click", handleClick, { capture: true });
container.addEventListener("click", handleClick, { capture: true });
button.addEventListener("click", handleClick);  // no capture — uses bubbling

// Output on button click:
// "You clicked on a BODY element"    ← capture fires first (outermost)
// "You clicked on a DIV element"     ← capture
// "You clicked on a BUTTON element"  ← default bubbling (innermost)
```

> **Historical note:** Netscape used only capture; Internet Explorer used only bubbling. The W3C standard includes both. In practice, **almost all handlers should use the default bubbling phase** — capture is rarely needed.

---

### 5. Event Delegation — Using Bubbling Intentionally

- A powerful pattern that **exploits bubbling** for efficiency.
- Instead of attaching one listener to each child element, attach **one listener on the parent** — events from all children will bubble up to it.
- The handler uses **`event.target`** to identify which child was actually clicked.
- Especially useful when there are **many child elements** or when children are **dynamically added**.

```js
// ❌ Naive approach — 16 listeners for 16 tiles
tile1.addEventListener("click", colorize);
tile2.addEventListener("click", colorize);
// ... × 16

// ✅ Event delegation — 1 listener handles all 16 tiles
const container = document.querySelector("#container");
container.addEventListener("click", (event) => {
  event.target.style.backgroundColor = bgChange();
  // event.target = the specific tile the user clicked
});
```

---

### 6. `event.target` vs `event.currentTarget`

- These two properties both reference elements, but they answer **different questions**:

| Property | Answers | Changes during bubbling? |
|---|---|---|
| **`event.target`** | "Which element was originally clicked?" | **No** — stays the same throughout all handlers as the event bubbles |
| **`event.currentTarget`** | "Which element's handler is currently running?" | **Yes** — changes with each handler as the event propagates |

```js
// HTML: <body> > <div id="container"> > <button>
// Listeners on button, div, and body all using handleClick:

function handleClick(e) {
  console.log(`target: ${e.target.tagName}, currentTarget: ${e.currentTarget.tagName}`);
}

// Output when button is clicked:
// target: BUTTON, currentTarget: BUTTON   ← button's own handler
// target: BUTTON, currentTarget: DIV      ← div's handler (bubbled)
// target: BUTTON, currentTarget: BODY     ← body's handler (bubbled)
```

> **Key insight:** `event.target` is **always the button** (where the user clicked), even as the event bubbles up. `event.currentTarget` changes to reflect **where the current handler lives**.

---

## Technical Deep-Dive

### Logic Walkthrough: Bubbling Order — Bottom to Top

```
Given this HTML:
<body>
  <div id="container">
    <button>Click me!</button>
  </div>
</body>

Listeners attached to: button, div#container, body

User clicks the button → browser fires events in this order:

Phase 1 — EVENT TARGET:
  ▶ button's "click" handler runs
    e.currentTarget = BUTTON
    e.target        = BUTTON

Phase 2 — BUBBLING (upward):
  ▶ div's "click" handler runs
    e.currentTarget = DIV
    e.target        = BUTTON   ← still the original click target

  ▶ body's "click" handler runs
    e.currentTarget = BODY
    e.target        = BUTTON   ← still unchanged
```

**The mental model:** Imagine dropping a stone in a pond. The stone enters at the `target` (innermost element). The ripples (the event) spread outward (upward through parents). Every element in the path feels the ripple, in order, from center out.

---

### Logic Walkthrough: Video Player Bug & Fix

This is the classic bubbling problem — understanding it is exam-critical.

**The structure:**
```
<button> → shows <div>
<div>    → hides itself when clicked
  └── <video> → plays when clicked
```

**The bug:**
```js
btn.addEventListener("click", () => box.classList.remove("hidden"));
video.addEventListener("click", () => video.play());
box.addEventListener("click", () => box.classList.add("hidden"));

// User clicks video:
// Step 1: video handler fires → video.play() ✅
// Step 2: event bubbles to box → box handler fires → box hides ❌
// Result: video starts playing but box disappears immediately
```

**The fix:**
```js
video.addEventListener("click", (event) => {
  event.stopPropagation();  // ← intercepts the bubble at the video level
  video.play();
});

// User clicks video:
// Step 1: video handler fires → event.stopPropagation() + video.play() ✅
// Step 2: bubble HALTED — box handler never fires ✅
// Result: video plays, box stays visible ✅
```

---

### Logic Walkthrough: Event Delegation with `event.target`

```js
// 16 tile divs inside a container — delegate from parent
const container = document.querySelector("#container");

container.addEventListener("click", (event) => {
  event.target.style.backgroundColor = bgChange();
  //    ↑
  //  This is the TILE the user clicked, not the container
  //  Even though the listener is on the container,
  //  event.target tells us exactly which tile was clicked
});
```

**Why this works:**
1. User clicks tile #7.
2. `click` event fires on tile #7 (`event.target = tile#7`).
3. Event bubbles up to `#container`.
4. Container's handler fires — `event.target` still = tile#7.
5. Handler colours tile#7 specifically.

**Why this is better:**
- 1 event listener instead of 16.
- If new tiles are dynamically added to the container later, they automatically work — no need to attach new listeners.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Event bubbling** | The automatic upward propagation of an event through ancestor elements after being fired on a child element. Events bubble from innermost to outermost by default. |
| **Event propagation** | The general process of an event travelling through the DOM. Includes both the capture phase (downward) and the bubbling phase (upward). |
| **Bubbling phase** | The phase of event propagation in which the event travels upward from the target element through its ancestors. The default phase for most event handlers. |
| **Event capture** | The opposite of bubbling — events fire on the outermost ancestor first, then travel inward to the target. Enabled by passing `{ capture: true }` to `addEventListener()`. |
| **`stopPropagation()`** | A method on the event object that halts the event's upward bubbling (or downward capture). The current handler still completes; only propagation to other elements is stopped. |
| **Event delegation** | A pattern where a single event listener is placed on a parent element to handle events from many child elements, relying on bubbling to bring child events to the parent. |
| **`event.target`** | The element on which the event was **originally fired** (the innermost clicked element). Does not change as the event bubbles up. Used in event delegation to identify which child was clicked. |
| **`event.currentTarget`** | The element whose **event handler is currently executing**. Changes with each handler as the event bubbles. Always refers to the element the listener is attached to. |
| **Capture phase** | The first phase of event propagation where the event travels from the root down to the target. Handlers registered with `{ capture: true }` fire in this phase. |
| **`{ capture: true }`** | The options object passed as the third argument to `addEventListener()` to register a listener in the capture phase instead of the default bubbling phase. |

---

## Watch Out For...

1. **Bubbling is ON by default — you don't enable it.** Every click event automatically bubbles unless stopped. This catches students who expect events to be contained to the clicked element only.

2. **`stopPropagation()` stops the bubble, not the handler.** Calling `event.stopPropagation()` does not stop the current handler from finishing — it only prevents the event from propagating to parent elements. The code after the call still executes.

3. **`event.target` ≠ `event.currentTarget`.** `target` = where the event started (fixed, doesn't change). `currentTarget` = the element whose handler is currently running (changes at each step during bubbling). Confusing these is the most common exam error in this topic.

4. **Event delegation uses `event.target`, not `event.currentTarget`.** When delegating from a parent to a child, you want to know *which child was clicked* — that's `event.target`. `event.currentTarget` would always give you the parent (the element with the listener).

5. **Capture is the opposite of bubbling — outer to inner.** Capture fires `BODY → DIV → BUTTON`; bubbling fires `BUTTON → DIV → BODY`. The default (and almost always correct) choice is bubbling.

6. **You can't remove a listener you registered with `{ capture: true }` using a plain `removeEventListener()`.** You must also pass `{ capture: true }` (or `true`) to `removeEventListener()` to match correctly.

7. **`stopPropagation()` is not `preventDefault()`.** `stopPropagation()` halts the event's travel through the DOM. `preventDefault()` cancels the browser's default action (like form submit or link navigation). They are entirely different — one affects propagation, the other affects default behaviour.

8. **Not all events bubble.** Most do (click, keydown, submit), but some do not — for example, `focus` and `blur` do not bubble by default (though their capturing equivalents, `focusin` and `focusout`, do). Attaching a `focus` listener on a parent expecting it to bubble from a child input will not work.

9. **Event delegation is more efficient but can interact badly with `stopPropagation()`.** If a child element calls `stopPropagation()`, its event never reaches the delegated parent listener. Be careful when mixing both techniques.

10. **`event.target` in delegation can be an unexpected element.** If your tile `<div>` contains a `<span>` for text and the user clicks the `<span>`, `event.target` will be the `<span>`, not the `.tile`. You may need to use `.closest()` to walk up to the intended ancestor when delegating.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Describe event bubbling in your own words. When you click a `<button>` that sits inside a `<div>` inside `<body>`, in what order do the click handlers fire?

**Q2.** What does `event.stopPropagation()` do? How is it different from `event.preventDefault()`?

**Q3.** What is the difference between `event.target` and `event.currentTarget`? Given that listeners are attached to a `<button>`, a `<div>`, and `<body>`, and the user clicks the button — what is the value of `event.target` in the `<body>`'s handler?

**Q4.** What is **event delegation** and why is it more efficient than attaching listeners to every child element? Which event object property do you use inside a delegated handler to identify which child was clicked?

**Q5.** The following code has a bubbling bug. The user clicks the video element, and the box disappears unexpectedly. Explain the bug and write the fix.
```js
video.addEventListener("click", () => video.play());
box.addEventListener("click", () => box.classList.add("hidden"));
```

---

## Answer Key

---

**A1.**
Event bubbling is when a browser event that fires on a child element automatically propagates upward through each ancestor element, triggering any matching handlers along the way — from the innermost element outward.

When a `<button>` inside a `<div>` inside `<body>` is clicked, and all three have click handlers:
```
1. BUTTON handler fires first   ← innermost (origin of the click)
2. DIV handler fires next       ← parent
3. BODY handler fires last      ← grandparent
```
The event bubbles outward like rings in water.

---

**A2.**

- **`event.stopPropagation()`**: Halts the event's upward propagation through the DOM. Parent handlers that would have been triggered by bubbling are **no longer called**. The current handler still finishes executing.

- **`event.preventDefault()`**: Cancels the **browser's default action** for the event (e.g., stops a form from submitting, stops a link from navigating). Does not affect propagation at all.

**They are completely separate** — `stopPropagation` controls where the event travels; `preventDefault` controls what the browser does next.

---

**A3.**
- **`event.target`**: The element where the event **originally fired** — the element the user directly interacted with. It **does not change** as the event bubbles.
- **`event.currentTarget`**: The element whose **handler is currently executing**. It changes at each step as the event propagates up the DOM.

In the `<body>`'s handler, when the user clicked the button:
- `event.target` = **`BUTTON`** (where the user clicked — unchanged throughout bubbling)
- `event.currentTarget` = **`BODY`** (the element whose handler is currently running)

---

**A4.**
**Event delegation** is the pattern of attaching a **single event listener on a parent element** to handle events from many child elements, relying on bubbling to carry child events up to the parent.

**Why it's more efficient:**
- 1 listener instead of N listeners (one per child) — lower memory usage.
- Automatically works for dynamically added children — no need to re-attach listeners.

**Property used:** `event.target` — it always refers to the specific child element the user clicked, even though the listener lives on the parent.

```js
container.addEventListener("click", (event) => {
  event.target.style.backgroundColor = randomColor();
  // event.target = the specific tile clicked, not the container
});
```

---

**A5.**
**The bug:** When the user clicks the `<video>`, the `click` event fires the video's handler (`video.play()`), then **bubbles up** to the parent `<div>` (box), triggering the box's handler (`box.classList.add("hidden")`). This makes the box disappear immediately after the video starts playing.

**The fix:** Call `event.stopPropagation()` inside the video's handler to prevent the click from bubbling up to the box:

```js
video.addEventListener("click", (event) => {
  event.stopPropagation();  // ← stops bubble here; box handler never fires
  video.play();
});

box.addEventListener("click", () => box.classList.add("hidden"));
```

Now clicking the video plays it without hiding the box, while clicking elsewhere in the box (outside the video) still hides it correctly.
