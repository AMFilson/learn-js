# 📚 CSS and JavaScript Accessibility Best Practices — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/CSS_and_JavaScript

---

## Executive Summary

This article covers how CSS and JavaScript, while not as fundamentally tied to accessibility as HTML, can either enhance or significantly harm it depending on usage patterns. The central mechanism is the interplay between visual presentation choices (colour contrast, focus states, hiding techniques) and JavaScript patterns (event types, form validation, unobtrusive enhancement) that either preserve or break access for screen reader and keyboard users. The exam-critical takeaway is that **CSS must never remove interactive state indicators or hide content from ATs unless intentional**, and **JavaScript must use device-independent event handlers and unobtrusive enhancement** — never entirely replacing base HTML functionality.

---

## Core Pillars

### 1. CSS: Correct Semantics and User Expectation

CSS can restyle any element to look like anything — but visual restyling must not destroy the **expected behaviour** that users and ATs rely on.

**The core principle:** You can update the visual styling of an element, but don't change it so much that it no longer *looks or behaves as expected*.

Key concerns by element type:

#### Text Content (`<h1>`–`<h6>`, `<p>`, `<ul>`, `<li>`)
```css
h1 { font-size: 5rem; }
p, li { line-height: 1.5; font-size: 1.6rem; }
```
- Use sensible font sizes, line heights, letter spacing for legibility.
- Headings must *visually look like headings* — big and bold — to match their semantic role.
- Lists must *look like lists*.
- Text colour must contrast well with background.

#### Emphasized Text (`<em>`, `<strong>`)
```css
strong, em { color: #a60000; }
```
- Minor colour adjustments are fine.
- **Do not** radically restyle emphasis elements — bold and italic are the recognized conventions. Changing them causes confusion.

#### Abbreviations (`<abbr>`)
```css
abbr { color: #a60000; }
```
- The recognized convention is a **dotted underline** — do not significantly deviate from this.

#### Links (`<a>`)
```css
a { color: red; }
a:hover,
a:visited,
a:focus { color: #a60000; text-decoration: none; }
a:active { color: black; background-color: #a60000; }
```

**Default link behaviour that must be preserved:**
- Visually distinct from surrounding text (colour + underline by default).
- Different colour when visited (purple by default).
- Pointer cursor on hover.
- **Focus outline/highlight on keyboard focus** — critical for keyboard navigation.

> You can be creative with link styles, but **never remove the pointer cursor or the focus outline** — both are critical accessibility aids.

#### Form Elements
- Style for sizing and layout is fine.
- **Do not remove** focus/hover visual feedback — users depend on these cues to know what is interactive.

#### Tables
- CSS should make tables cleaner and fit the design.
- Bold table headers and zebra striping make data easier to parse.

---

### 2. CSS: Colour and Colour Contrast

**WCAG contrast requirements:**
- Normal text vs background: **4.5:1 minimum**
- Large text (18pt+/14pt+ bold) vs background: **3:1 minimum**
- UI components and graphical objects vs adjacent colours: **3:1 minimum**

**Tools:** WebAIM's [Color Contrast Checker](https://webaim.org/resources/contrastchecker/) — enter foreground and background colours to check WCAG conformance.

**Bonus:** High contrast also benefits users in bright environments (sunlight on glossy screens).

**Colour alone must not convey information:**

| ❌ Wrong | ✅ Correct |
|---|---|
| Required fields marked only in red | Required fields marked with `*` AND in red |
| Error state shown only by red border | Error state shown by red border + error icon + text label |

---

### 3. CSS: Hiding Content

How content is hidden determines whether screen readers can still access it.

| Method | Visually hidden? | Hidden from screen readers? | Use when... |
|---|---|---|---|
| `display: none` | ✅ Yes | ✅ Yes | Content should be fully inaccessible (e.g., truly inactive tab panel) |
| `visibility: hidden` | ✅ Yes | ✅ Yes | Same as above |
| `position: absolute` (off-screen) | ✅ Yes | ❌ No — SR can still read it | Hiding visual content but keeping it AT-accessible (e.g., visually hidden skip links, status messages) |
| CSS background image | ✅ Yes | ❌ N/A | Decorative images that should never enter the AT tree |

**Key rule:** `visibility: hidden` and `display: none` hide content from **both** sighted users and screen readers. Do not use these to hide content that screen reader users still need.

**Absolute positioning is the preferred approach** for visually hiding content while keeping it AT-accessible — such as error boxes that screen readers need to announce even when visually repositioned.

---

### 4. CSS: Accept User Style Overrides

Users with disabilities may apply custom stylesheets (via browser extensions like Stylus/Stylish or browser settings) to:
- Increase font sizes globally.
- Apply high-contrast colour schemes.

**Design implication:** Your layouts must be **flexible** enough to handle these overrides. Main content areas should scroll or expand to accommodate larger text — they must not clip or hide content.

---

### 5. JavaScript: The Accessibility Baseline

JavaScript doesn't have an inherent negative impact on accessibility, but misuse causes significant problems.

**The two key requirements apply regardless of how complex the JS is:**
1. **Good semantics** — use the right HTML element (`<button>`, `<a>`, `<input>`, not `<div>` for everything).
2. **Text alternatives** — all content must be available as text: good labels, `alt` attributes, ARIA attributes where needed.

**Complexity vs. accessibility expectation:**
- Simple content (text, images, forms, buttons) — fully accessible is a reasonable expectation.
- Complex content (`<canvas>`-based 3D games) — full accessibility is unreasonable; implement what is possible (keyboard controls, sufficient colour contrast).

---

### 6. JavaScript: The Problem with Too Much JavaScript

**Anti-pattern:** Everything done in JavaScript — HTML generated by JS, CSS generated by JS, no server-side fallback.

**The principle:** Use the **right technology for the right job**. Before reaching for JavaScript, ask:
- Do I need a complex JS-powered information box, or would plain text serve?
- Do I need a custom non-standard form widget, or would a standard `<input>` do?
- Must all HTML be generated by JavaScript, or can the server/HTML template do it?

JavaScript-generated HTML has no semantic fallback, breaks no-JS scenarios, and is harder to test with AT.

---

### 7. JavaScript: Unobtrusive JavaScript

**Unobtrusive JavaScript** = JavaScript that *enhances* existing functionality, not replaces it.

**The principle:** Basic functions should ideally work without JavaScript. JS is used to improve the experience for users who have it, not to gatekeep functionality for those who don't.

**Good examples of unobtrusive JS:**

| Use case | Without JS | With JS |
|---|---|---|
| Form validation | Form submits to server; server validates and returns errors | Client-side validation provides instant error feedback |
| `<video>` controls | Browser default controls (not keyboard-accessible in most browsers) | Custom accessible keyboard-navigable controls + direct video link fallback |

**Form validation pattern (unobtrusive):**
```js
form.onsubmit = validate;

function validate(e) {
  errorList.textContent = "";            // Clear previous errors
  for (const testItem of formItems) {
    if (testItem.input.value === "") {   // Check for empty fields
      errorField.style.left = "360px";  // Show error container
      createLink(testItem);             // Create descriptive error link
    }
  }
  if (errorList.hasChildNodes()) {
    e.preventDefault();                 // Stop submission only if errors exist
  }
}
```

**Error link pattern (each error links back to the problematic field):**
```js
function createLink(testItem) {
  const listItem = document.createElement("li");
  const anchor = document.createElement("a");
  const name = testItem.input.name;
  anchor.textContent = `${name} field is empty: fill in your ${name}.`;
  anchor.href = `#${name}`;             // Links directly to the input element
  listItem.appendChild(anchor);
  errorList.appendChild(listItem);
}
```

**Why absolute positioning for the error box (not `display:none` / `visibility:hidden`):**
```html
<!-- Error container uses absolute positioning to hide/show -->
<div class="errors" role="alert" aria-relevant="all">
  <ul></ul>
</div>
```
- `display:none` would hide the content **from screen readers too**.
- Absolute positioning moves the box off-screen visually but keeps it accessible to AT.
- `role="alert"` causes the SR to immediately announce new content inserted into this container.
- `aria-relevant="all"` instructs the SR to announce all changes to the live region.

**Validation timing — validate on submit, not on every keystroke:**
- Updating the UI on every keystroke is disruptive and confusing for screen reader users.
- Submit-time validation is less noisy and gives the user time to complete fields before errors appear.

---

### 8. JavaScript: Mouse-Specific vs. Device-Independent Events

**The problem:** Some JavaScript event handlers only fire for mouse users, locking out keyboard and touch users.

**Mouse-only events (problematic in isolation):**

| Event | Problem |
|---|---|
| `mouseover` | Fires when mouse enters element — keyboard users never trigger this |
| `mouseout` | Fires when mouse leaves element — same issue |
| `dblclick` | Double-click — no keyboard equivalent |

**Solution:** **Double up** with device-independent equivalents:

| Mouse event | Device-independent pair |
|---|---|
| `mouseover` | `focus` |
| `mouseout` | `blur` |

**Pattern — accessible image zoom on hover/focus:**
```js
imgThumb.onmouseover = showImg;   // Mouse hover → show enlarged image
imgThumb.onmouseout = hideImg;    // Mouse leave → hide enlarged image
imgThumb.onfocus = showImg;       // Keyboard focus → show enlarged image
imgThumb.onblur = hideImg;        // Keyboard blur → hide enlarged image
```

The image thumbnail must also have `tabindex="0"` to be keyboard-focusable, since `<img>` is not natively focusable.

**The `click` event is special:**
- Despite sounding mouse-specific, `click` events fire on `<a>` and `<button>` via `Enter`/`Return` and on touchscreen taps.
- `click` **does not** automatically fire via `Enter` on elements made focusable with `tabindex="0"` (like a `<div>`) — a separate `keydown` handler is needed for those.

---

## Technical Deep-Dive

### Logic Walkthrough: Accessible Form Validation

**Full flow from submission to error display:**

**HTML Setup:**
```html
<form id="myForm">
  <div>
    <label for="name">Enter your name:</label>
    <input type="text" name="name" id="name" />
  </div>
  <div>
    <label for="age">Enter your age:</label>
    <input type="text" name="age" id="age" />
  </div>
  <button type="submit">Submit</button>
</form>

<!-- Error container — visually positioned off-screen when empty,
     positioned on-screen when errors exist. role="alert" announces
     new content to screen readers immediately. -->
<div class="errors" role="alert" aria-relevant="all">
  <ul id="error-list"></ul>
</div>
```

**JavaScript validation flow:**
```js
const form = document.getElementById("myForm");
const errorList = document.getElementById("error-list");
const errorField = document.querySelector(".errors");

const formItems = [
  { input: document.getElementById("name") },
  { input: document.getElementById("age") },
];

form.onsubmit = validate;

function validate(e) {
  // Step 1: Clear previous errors
  errorList.textContent = "";

  // Step 2: Check each field
  for (const testItem of formItems) {
    if (testItem.input.value === "") {
      errorField.style.left = "360px"; // Move error box into view
      createLink(testItem);           // Generate descriptive error link
    }
  }

  // Step 3: If errors exist, stop submission
  if (errorList.hasChildNodes()) {
    e.preventDefault(); // Block form submission
  }
  // If no errors, form submits normally
}

function createLink(testItem) {
  const listItem = document.createElement("li");
  const anchor = document.createElement("a");
  const name = testItem.input.name;
  // Human-readable error message + link back to the field
  anchor.textContent = `${name} field is empty: fill in your ${name}.`;
  anchor.href = `#${name}`;
  listItem.appendChild(anchor);
  errorList.appendChild(listItem);
}
```

**What happens at each step for AT users:**
1. User submits the form.
2. `validate()` clears old errors first (prevents duplicate announcements).
3. Errors are generated and inserted into the `role="alert"` container.
4. Screen reader **immediately announces** the new error list content without user interaction (due to `role="alert"`).
5. Each error is a clickable/activatable link — keyboard users can `Tab` to the link and press `Enter` to jump directly to the unfilled field.
6. `e.preventDefault()` stops form submission — the user stays on the page.
7. Server-side validation must also exist because client-side validation can be bypassed (JS disabled, devtools, etc.).

---

### Logic Walkthrough: Device-Independent Event Pairing

**Scenario:** Thumbnail image that shows a larger version on hover.

**Inaccessible (mouse-only):**
```js
imgThumb.onmouseover = showImg;
imgThumb.onmouseout = hideImg;
// Keyboard users cannot trigger mouseover/mouseout — enlarged image is inaccessible
```

**Accessible (device-independent):**
```html
<!-- tabindex="0" makes the image keyboard-focusable -->
<img src="thumbnail.jpg" alt="Product thumbnail" tabindex="0" id="thumb" />
<img src="fullsize.jpg" alt="Full-size product image" id="full" style="display:none" />
```

```js
const imgThumb = document.getElementById("thumb");
const imgFull = document.getElementById("full");

function showImg() { imgFull.style.display = "block"; }
function hideImg() { imgFull.style.display = "none"; }

// Mouse users
imgThumb.onmouseover = showImg;
imgThumb.onmouseout = hideImg;

// Keyboard users (Tab focuses the thumbnail, Shift+Tab unfocuses it)
imgThumb.onfocus = showImg;
imgThumb.onblur = hideImg;
```

**What changes:**
- Keyboard user presses `Tab` → thumbnail receives focus → `onfocus` fires → enlarged image appears.
- Keyboard user presses `Shift+Tab` or `Tab` away → `onblur` fires → enlarged image hidden.
- Mouse user hovers → `onmouseover` fires → enlarged image appears.
- Both control pathways produce identical UX.

---

### Logic Walkthrough: CSS Hiding Methods Decision Tree

```
Do screen reader users need access to this content?
  └─ YES →
      Does it need to be visually hidden?
        └─ YES → Use absolute positioning (e.g., left: -9999px; or clip-path: inset(100%))
                 OR use the "visually-hidden" CSS utility class:
                 .visually-hidden {
                   position: absolute;
                   width: 1px; height: 1px;
                   padding: 0; margin: -1px;
                   overflow: hidden;
                   clip: rect(0,0,0,0);
                   border: 0;
                 }
        └─ NO → Leave it visible in the normal flow
  └─ NO →
      Use display: none OR visibility: hidden
      (Both remove content from both visual rendering AND the accessibility tree)
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Colour contrast ratio** | A numeric measure of the luminance difference between foreground and background colours; WCAG requires 4.5:1 for normal text and 3:1 for large text against the background. |
| **`display: none`** | CSS declaration that removes an element from the layout flow and the accessibility tree — screen readers cannot access content hidden this way. |
| **`visibility: hidden`** | CSS declaration that hides an element visually while preserving its space in the layout; also removes content from the accessibility tree, making it inaccessible to screen readers. |
| **Absolute positioning (for hiding)** | Using `position: absolute` with off-screen coordinates to visually hide content while keeping it in the accessibility tree, allowing screen readers to still read it. |
| **`:focus` pseudo-class** | CSS selector that matches an element when it receives keyboard focus; styles applied here provide the visual focus indicator required for keyboard accessibility. |
| **`:hover` pseudo-class** | CSS selector that matches an element when the mouse pointer is over it; must be paired with `:focus` styles if the hover behaviour is also needed for keyboard users. |
| **`outline: none`** | CSS declaration that removes the browser's default focus ring; doing so without providing an alternative `:focus` style is a WCAG violation that harms keyboard users. |
| **Unobtrusive JavaScript** | A JavaScript design philosophy where JS enhances existing HTML functionality rather than building it entirely — base functionality should remain available without JS. |
| **Device-independent event handler** | A JavaScript event that fires regardless of input method (mouse, keyboard, touch) — e.g., `focus`/`blur` as alternatives to `mouseover`/`mouseout`. |
| **`mouseover` / `mouseout`** | Mouse-specific events that fire when the pointer enters or leaves an element; do not fire for keyboard users and must be paired with `focus`/`blur` for accessibility. |
| **`focus` / `blur`** | Device-independent events that fire when an element gains or loses keyboard focus; the accessible equivalent of `mouseover`/`mouseout` for keyboard users. |
| **`click` event** | An event that is largely device-independent — fires on mouse click, `Enter`/`Return` on native focusable elements (`<a>`, `<button>`), and touchscreen tap. Does not automatically fire via `Enter` on elements made focusable with `tabindex` only. |
| **`role="alert"`** | WAI-ARIA live region role that causes screen readers to immediately announce newly inserted content without the user needing to navigate to it; used for error messages and status updates. |
| **`aria-relevant="all"`** | WAI-ARIA attribute on a live region that instructs screen readers to announce all changes (additions and removals) to the region's content. |
| **Client-side form validation** | JavaScript-based validation that checks form data before submission, providing instant user feedback; must not replace server-side validation, which is the authoritative security check. |
| **`e.preventDefault()`** | JavaScript method called on a form submission event to stop the browser from performing the default form submission action, keeping the user on the current page to correct errors. |
| **Zebra striping** | An alternating background colour pattern applied to table rows via CSS to visually separate rows and make tabular data easier to scan — a common CSS accessibility best practice for tables. |
| **Visually hidden utility class** | A CSS class (commonly `.sr-only` or `.visually-hidden`) that positions content off-screen with `position: absolute` and tiny dimensions so it is invisible to sighted users but accessible to screen readers. |
| **`tabindex="0"`** | HTML attribute that makes a non-focusable element (like `<img>` or `<div>`) keyboard-focusable, enabling it to receive `focus` and `blur` events triggered by `Tab` navigation. |
| **WebAIM Color Contrast Checker** | A widely-used online tool that calculates the contrast ratio between two colours and reports whether they pass WCAG AA and AAA conformance levels. |

---

## Watch Out For...

1. **Removing `outline: none` without a replacement `:focus` style** — This is one of the most common accessibility violations. The browser's default focus ring is the only visual indicator for keyboard users; removing it without an equally visible custom `:focus` style leaves keyboard users with no way to know which element has focus.

2. **Using `display: none` or `visibility: hidden` to hide content that ATs still need** — Both of these declarations remove content from the accessibility tree, not just from visual rendering. Use absolute positioning (or a `.visually-hidden` class) when content must be visually hidden but accessible to screen readers.

3. **Relying on `mouseover`/`mouseout` without `focus`/`blur` counterparts** — Mouse-only events exclude keyboard users entirely. Every `mouseover` handler must have a corresponding `focus` handler, and every `mouseout` must have a `blur` handler.

4. **Assuming `click` is always device-independent** — `click` fires from `Enter`/`Return` on native focusable elements (`<button>`, `<a>`) but **not** on elements made focusable only via `tabindex`. For `<div tabindex="0">` acting as a button, a `keydown` handler for `Enter` and `Space` is still required.

5. **Using colour alone to convey information** — Marking required fields only in red or showing errors only through a coloured border fails WCAG 1.4.1 (Use of Color). Always pair colour with a text label, icon, or pattern.

6. **Treating client-side validation as a security measure** — Client-side JavaScript validation can be bypassed trivially (JS disabled, devtools, direct POST requests). It is a usability improvement only. Server-side validation is the authoritative security check and must always be implemented.

7. **Validating form fields on every keystroke** — Real-time keystroke validation updates the UI constantly, causing screen readers to announce errors and state changes on every character typed — an extremely disruptive experience. Validate on submit (or at minimum on field blur) instead.

8. **Generating all HTML via JavaScript** — Entirely JS-generated HTML has no fallback for users with JS disabled, creates SEO disadvantages, and is harder to test with AT. Use semantic server-rendered or static HTML as the base; layer JS for enhancement.

9. **Restyling links so they are no longer distinguishable from body text** — Removing the underline and using the same colour as surrounding text makes links undetectable to users who cannot rely on hover/focus states. The 3:1 contrast requirement between link text and surrounding non-link text must be maintained across all link states.

10. **Storing all visual feedback in icons only (without text)** — Icon-only error indicators, icon-only status indicators, and icon-only buttons lack accessible text. Screen readers announce nothing useful for an icon with no `alt` text or `aria-label`. Always provide a text equivalent.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the difference between `display: none` and `position: absolute` (off-screen) as methods of hiding content, in terms of their effect on screen reader accessibility?

**Q2.** A developer builds an image thumbnail that reveals a full-size image on `mouseover`. Write the complete JavaScript needed to make this behaviour accessible to keyboard users as well.

**Q3.** Explain what `role="alert"` does in a form validation error container. Why is it used instead of `display: none` / `display: block` toggling for the error box?

**Q4.** What is "unobtrusive JavaScript"? Give one concrete example of a feature implemented unobtrusively and explain why it qualifies.

**Q5.** A designer has set link text to the same shade of blue as the page background. A developer points out this fails WCAG. What are the two distinct colour contrast requirements that apply to links, and against what are they each measured?

---

## Answer Key

---

**A1.**
- **`display: none`** removes the element from both the visual rendering *and* the **accessibility tree**. Screen readers cannot access or announce content hidden this way — it is as if the element does not exist.
- **`position: absolute` with off-screen coordinates** (e.g., `left: -9999px`) removes the element **only from visual rendering**. It remains in the DOM and in the accessibility tree, so screen readers *can* still read it. This is the correct technique for content that must be visually hidden but accessible to AT — such as skip links, visually-hidden status messages, and error containers that use `role="alert"`.

---

**A2.** The image thumbnail element must first be made keyboard-focusable with `tabindex="0"` since `<img>` is not natively focusable. Then `focus` and `blur` events are paired with `mouseover` and `mouseout`:

```html
<img src="thumbnail.jpg" alt="Product thumbnail" tabindex="0" id="thumb" />
<img src="fullsize.jpg" alt="Full-size product image" id="full" style="display:none" />
```

```js
const imgThumb = document.getElementById("thumb");
const imgFull  = document.getElementById("full");

function showImg() { imgFull.style.display = "block"; }
function hideImg() { imgFull.style.display = "none"; }

// Mouse users
imgThumb.onmouseover = showImg;
imgThumb.onmouseout  = hideImg;

// Keyboard users
imgThumb.onfocus = showImg;
imgThumb.onblur  = hideImg;
```

With this, a keyboard user pressing `Tab` to focus the thumbnail triggers `onfocus → showImg()`, and tabbing away triggers `onblur → hideImg()` — identical UX to the mouse path.

---

**A3.** `role="alert"` designates the container as a **WAI-ARIA live region**. Whenever content is *inserted into* this element (even programmatically via JavaScript), screen readers automatically announce the new content to the user **without** the user needing to navigate to it. This is essential for dynamically injected error messages — the user stays on the form but is immediately notified of the error.

The error box uses **absolute positioning** (not `display: none` / `display: block`) because:
- `display: none` hides content from screen readers — toggling it back with `display: block` would technically work for the `role="alert"` announcement, but it's less reliable.
- Absolute positioning keeps the element in the accessibility tree at all times. When error content is inserted, the `role="alert"` fires its announcement regardless of the container's visual position.
- Using `display: none` on an element with `role="alert"` may suppress announcements in some AT/browser combinations, whereas absolutely positioned live regions are more consistently supported.

---

**A4.** **Unobtrusive JavaScript** is a design approach where JavaScript *enhances* existing functionality rather than being required for it to function at all. Base functionality works in HTML/CSS alone; JS layers on improvements for users who have it.

**Example:** Client-side form validation.
- **Without JS:** The form submits to the server, which validates the data and returns an error page or success page — fully functional, just slower.
- **With JS:** Client-side validation intercepts the submit event, checks field values immediately, and displays errors without a round-trip to the server — faster feedback, but not a replacement for server-side validation.

This qualifies as unobtrusive because:
1. The form *works* without JS (server validates it).
2. JS only *improves* the experience (faster error feedback).
3. JS does not *build* the form — it enhances a semantic `<form>` element.

---

**A5.** WCAG applies two distinct contrast requirements to links:

1. **Link text vs. background colour: 4.5:1 minimum** — The link text must have sufficient contrast against the page background to be readable. This is the standard text contrast requirement (WCAG 1.4.3).

2. **Link text vs. surrounding non-link text: 3:1 minimum** — The link must be visually distinguishable from adjacent body text *by colour alone* if the underline is removed. If the underline is preserved, this 3:1 requirement does not strictly apply since underline is a non-colour differentiator. This requirement applies across all link states: default, visited, and focus/active (WCAG 1.4.1, Use of Color).

In the scenario described, a link that is the same blue shade as the page background fails requirement 1 (4.5:1 vs background). It may also fail requirement 2 if the surrounding body text is a different colour. Both must pass independently.
