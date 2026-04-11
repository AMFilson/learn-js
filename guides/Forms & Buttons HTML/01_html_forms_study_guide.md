# 📋 HTML Forms & Buttons — Exam Study Guide
**Source:** [MDN Web Docs — Forms and buttons in HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_forms)

---

## Executive Summary

HTML forms are the primary mechanism for **two-way communication** on the web — they allow users to submit data to a server rather than passively consuming content. A basic form is built from three structural components: a `<form>` wrapper (which defines *where* and *how* data is sent), `<label>`/input control pairs (which collect individual pieces of data), and a `<button>` (which triggers submission). Form data is transmitted as **name/value pairs**, so every control that should submit data must have a `name` attribute, and proper `<label>` associations (via matching `for` and `id` attributes) are essential for both accessibility and usability.

---

## Core Pillars

### 1. Why Forms Exist — Two-Way Web Interaction

- Links and media create **one-way interactions** — users consume content passively.
- **Forms and buttons** enable two-way interaction: users submit preferences, orders, searches, feedback, payment details, and more.
- Two key interactive elements:
  - **`<button>`** — triggers actions (via JavaScript or form submission).
  - **`<form>`** — collects structured data and sends it to a server.

---

### 2. The Three Parts of a Basic Form

Every form has exactly three core ingredients:

```html
<form action="./submit_page" method="get">

  <!-- ① label + input pair — collects one piece of data -->
  <p>
    <label for="name">Name (required):</label>
    <input type="text" name="name" id="name" required />
  </p>

  <p>
    <label for="email">Email (required):</label>
    <input type="email" name="email" id="email" required />
  </p>

  <!-- ② Submit button — sends the form -->
  <p>
    <button>Sign me up!</button>
  </p>

</form>
```

| Part | Element | Purpose |
|---|---|---|
| **Wrapper** | `<form>` | Groups all controls; defines where/how data is sent |
| **Controls** | `<input>`, `<select>`, `<textarea>` | Collect individual pieces of user data |
| **Labels** | `<label>` | Describe what each control expects |
| **Submit** | `<button>` | Triggers data submission |

---

### 3. The `<form>` Element — `action` and `method`

The `<form>` element controls **where** data goes and **how** it travels:

```html
<form action="./submit_page" method="get">
```

| Attribute | Purpose | Example |
|---|---|---|
| **`action`** | The URL the form data is sent to when submitted | `action="./submit_page"` |
| **`method`** | The HTTP method used to send the data | `method="get"` (appended to URL) or `method="post"` (in request body) |

**`method="get"` in action:**
- Submitted data is appended to the URL as query parameters:
  ```
  /submit_page?name=Bob&email=bob%40bob.com
  ```
- This is visible in the address bar — useful for debugging, but not for passwords.

---

### 4. The `<input>` Element — Key Attributes

`<input>` is a **void element** (self-closing) and the most versatile form control.

```html
<input type="text" name="name" id="name" required />
```

| Attribute | Purpose |
|---|---|
| **`type`** | What kind of control to render (text, email, radio, checkbox, etc.) |
| **`name`** | The key in the submitted name/value pair — **required for submission** |
| **`id`** | Used to associate the control with its `<label>` via the label's `for` attribute |
| **`required`** | The field must be filled before the form can submit (client-side validation) |
| **`value`** | Pre-fills the field with a default value; for radio/checkbox, sets the submitted value |
| **`checked`** | Pre-selects a radio button or checkbox on page load |
| **`disabled`** | Grays out the control and prevents interaction and submission |

**Specialized `type` values:**

| `type` | Creates | Notes |
|---|---|---|
| `text` | Single-line text field | Accepts any text |
| `email` | Email text field | Browser validates email format |
| `password` | Masked text field | Characters hidden |
| `number` | Numeric field | Only allows numbers |
| `tel` | Telephone field | Optimises mobile keyboard |
| `radio` | Radio button | Choose one from a set — same `name` links the group |
| `checkbox` | Checkbox | Toggle on/off — each has a unique `name` |
| `color` | Color picker widget | Value is a hex color string |
| `submit` | Submit button via `<input>` | Use `<button>` instead — more flexible |
| `reset` | Reset button via `<input>` | Avoid — clears form accidentally |
| `button` | Generic button via `<input>` | Use `<button>` instead |

---

### 5. The `<label>` Element — Explicit vs. Implicit

**Explicit label (recommended):**
- Control has `id="name"`, label has `for="name"` — these must match exactly.
```html
<label for="name">Name (required):</label>
<input type="text" name="name" id="name" required />
```

**Implicit label (nesting):**
- The input is nested inside the label — no `id`/`for` needed, but less reliable with screen readers.
```html
<label>
  Name (required):
  <input type="text" name="name" required />
</label>
```

**Why labels matter:**
1. **Screen readers** announce the label text when the user focuses the control — essential accessibility.
2. **Clicking the label** focuses the input — bigger hit area, especially important on mobile.

> **Always use explicit labels** (`for` + `id`). Implicit labels are not always handled correctly by assistive technology.

---

### 6. The `<button>` Element — Three Types

Inside a `<form>`, `<button>` defaults to submitting the form. The `type` attribute changes this:

```html
<button type="submit">Submit</button>   <!-- ← default, same as no type -->
<button type="reset">Reset</button>    <!-- ← clears all field values -->
<button type="button">Click me</button> <!-- ← does nothing without JS -->
```

| `type` | Behaviour | Notes |
|---|---|---|
| `submit` (default) | Submits the form if valid | Don't need to specify unless clarifying |
| `reset` | Clears all form fields instantly | **Avoid** — causes accidental data loss |
| `button` | Does nothing by default | Requires JavaScript to be useful |

> **Use `<button>` not `<input type="submit">`.** `<button>` is more flexible — it can contain HTML content (icons, rich text), not just plain text.

---

### 7. Form Structuring — Organising Controls

Form controls are **inline by default** — wrap them in block elements to put each on its own line:

```html
<form>
  <h2>Subscribe</h2>            <!-- heading to describe the form -->

  <p>                           <!-- <p> separates each label/input pair -->
    <label for="name">Name:</label>
    <input type="text" name="name" id="name" />
  </p>

  <p>
    <button>Submit</button>
  </p>
</form>
```

**Acceptable structural wrappers:** `<p>`, `<div>`, `<section>`, `<li>` — anything that makes semantic sense.

**`<fieldset>` and `<legend>` — grouping related controls:**
```html
<fieldset>
  <legend>Preferred contact method:</legend>
  <input type="radio" id="byEmail" name="contact" value="email" />
  <label for="byEmail">Email</label>
  <input type="radio" id="byPhone" name="contact" value="phone" />
  <label for="byPhone">Phone</label>
</fieldset>
```
- `<fieldset>` groups related controls visually and semantically.
- `<legend>` labels the entire group — read by screen readers before each control.
- `disabled` on `<fieldset>` disables **every control inside** it at once.

---

### 8. Radio Buttons — Choose One from Many

```html
<fieldset>
  <legend>Choose hotel room type:</legend>
  <input type="radio" id="economy" name="hotel" value="economy" checked />
  <label for="economy">Economy (+$0)</label>

  <input type="radio" id="superior" name="hotel" value="superior" />
  <label for="superior">Superior (+$50)</label>

  <input type="radio" id="penthouse" name="hotel" value="penthouse" disabled />
  <label for="penthouse">Penthouse (+$150)</label>
</fieldset>
```

**Rules for radio buttons:**
- All buttons in a group share the **same `name`** — this links them so only one can be selected.
- Each button must have a unique **`value`** — this is what gets submitted.
- Submitted as a single `name=value` pair: `hotel=economy`
- `checked` pre-selects a button on load — once a radio is selected, you can't deselect it without selecting another.
- `disabled` grays out a button, making it unselectable.

---

### 9. Checkboxes — Choose Zero or More

```html
<fieldset>
  <legend>Choose classes to attend:</legend>
  <input type="checkbox" id="yoga" name="yoga" />
  <label for="yoga">Yoga (+$10)</label>

  <input type="checkbox" id="coffee" name="coffee" />
  <label for="coffee">Coffee roasting (+$20)</label>
</fieldset>
```

**How checkboxes differ from radio buttons:**
- Each checkbox has a **unique `name`** — they are independent.
- No `value` needed (default submitted value is `on`): `yoga=on`, `coffee=on`
- You **can** specify `value` to customise: `<input type="checkbox" name="yoga" value="yes" />` → `yoga=yes`
- Multiple can be checked simultaneously.
- Unchecked boxes are **not included** in the submitted data at all.

---

### 10. Drop-Down Menus — `<select>` and `<option>`

```html
<label for="transport">How are you getting here:</label>
<select name="transport" id="transport">
  <option value="">--Please choose an option--</option>
  <option value="plane">Plane</option>
  <option value="bike">Bike</option>
  <option value="train">Train</option>
</select>
```

- `<select>` is the wrapper — it takes `name` and `id` attributes (like `<input>`).
- `<option>` elements are the choices — each has a `value` (what gets submitted).
- If `value` is omitted on `<option>`, the text content is submitted instead.
- Add `selected` to an `<option>` to pre-select it on page load.
- Submitted as: `transport=train`

---

### 11. Multi-line Text — `<textarea>`

```html
<label for="comments">Any other comments:</label>
<textarea id="comments" name="comments" rows="5" cols="33"></textarea>
```

- Like `<input type="text">` but allows **multiple lines**.
- `rows` — default height in lines (default: `2`).
- `cols` — default width in characters (default: `20`).
- Note: `<textarea>` has a **closing tag** — unlike `<input>`, it is not void.
- Browsers render a resize handle in the corner by default.

---

### 12. Form Validation

**Two types of validation — you need BOTH:**

| Type | Where it runs | How | Limitations |
|---|---|---|---|
| **Client-side** | Browser (before submission) | HTML attributes (`required`, `type`) + JavaScript | Easy to bypass — user can disable JS or modify code |
| **Server-side** | Server (after submission) | Backend language | Can't give instant field-level feedback |

**Built-in client-side validation attributes:**
- `required` — field cannot be empty.
- `type="email"` — validates email format automatically.
- `type="number"` — validates numeric input.

> **Never rely on client-side validation alone.** Always validate on the server. They serve different purposes: client-side for UX hints, server-side for security and data integrity.

---

### 13. Accessibility — Use Semantic Elements

- **Always use real form elements** (`<button>`, `<input>`, `<select>`) — not `<div>` or `<span>` styled to look like controls.
- Screen readers understand semantic elements — a `<button>` announces itself as a button; a styled `<div>` does not.
- Semantic form controls are **keyboard-navigable by default** — Tab to move forward, Shift+Tab to move back.
- Focused elements get a **focus outline** (blue ring) — critical for keyboard users to know where they are.
- Re-implementing this behaviour with non-semantic elements requires significant extra code and never fully matches native behaviour.

---

## Technical Deep-Dive

### Logic Walkthrough: How `name` and `value` Become Submitted Data

When the form is submitted, the browser collects all controls inside `<form>` that have a `name` attribute and bundles them as `name=value` pairs in the URL (GET) or request body (POST):

```html
<form action="./submit_page" method="get">
  <input type="text"  name="name"      value="" />   <!-- user types "Bob" -->
  <input type="email" name="email"     value="" />   <!-- user types "bob@bob.com" -->
  <input type="radio" name="hotel"     value="economy" checked />  <!-- selected -->
  <input type="radio" name="hotel"     value="superior" />         <!-- not selected -->
  <input type="checkbox" name="yoga"  />              <!-- checked by user -->
  <select name="transport">
    <option value="train">Train</option>              <!-- selected -->
  </select>
  <button>Submit</button>
</form>
```

**Resulting URL after submit:**
```
/submit_page?name=Bob&email=bob%40bob.com&hotel=economy&yoga=on&transport=train
```

**Key rules:**
- Unsubmitted radio buttons → not included (only the selected one appears).
- Unchecked checkboxes → not included at all.
- `<select>` → the `value` of the chosen `<option>` is submitted.
- The submit `<button>` itself is not included in the data.

---

### Logic Walkthrough: Radio vs. Checkbox — Structural Differences

```
RADIO — choose exactly one:
  All share the SAME name → "hotel"
  Each has a unique value  → "economy", "superior", "penthouse"
  Submitted:               → hotel=economy  (one pair)

CHECKBOX — choose zero or more:
  Each has a UNIQUE name   → "yoga", "coffee", "balloon"
  value defaults to "on"   → customise with value attribute
  Submitted (if checked):  → yoga=on&balloon=on  (separate pairs for each checked)
  Unchecked:               → not submitted at all
```

---

### Logic Walkthrough: Explicit vs. Implicit Label — What Changes

```html
<!-- EXPLICIT (recommended) -->
<label for="email">Email:</label>      <!-- for="email" matches id="email" -->
<input type="email" id="email" name="email" />  <!-- separate elements -->

<!-- IMPLICIT (nesting) -->
<label>
  Email:
  <input type="email" name="email" />   <!-- no id or for needed -->
</label>

<!-- NO LABEL (wrong) -->
<input type="email" name="email" />   <!-- screen reader: "edit text, email" — meaningless! -->
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`<form>`** | The wrapper element for all form controls. Defines `action` (submission URL) and `method` (HTTP method). Controls inside it are submitted together on form submission. |
| **`action`** | Attribute on `<form>`. The URL the browser sends form data to when submitted. |
| **`method`** | Attribute on `<form>`. `get` appends data to the URL; `post` sends data in the request body. |
| **`<input>`** | Void (self-closing) element that creates various form controls depending on its `type` attribute. |
| **`type` attribute** | On `<input>`, determines the control type: `text`, `email`, `password`, `radio`, `checkbox`, etc. |
| **`name`** | Attribute on form controls. Becomes the key in the submitted name/value pair. Required for submission. |
| **`value`** | Attribute on form controls. The data submitted when the control is submitted. On `radio`, it's mandatory. |
| **`id`** | Unique identifier for an element. On a form control, used to link it to its `<label>` via the label's `for` attribute. |
| **`required`** | Boolean attribute on `<input>`. Prevents form submission if the field is empty. Built-in client-side validation. |
| **`checked`** | Boolean attribute on `radio`/`checkbox` inputs. Pre-selects the control on page load. |
| **`disabled`** | Boolean attribute on any form control or `<fieldset>`. Grays out the element and excludes it from submission. |
| **`<label>`** | Provides a text description for a form control. Associates with a control via matching `for` and `id` values. |
| **`for` attribute** | On `<label>`. Must match the `id` of the associated form control to create an explicit label association. |
| **Explicit label** | Label association made via `for` + `id` attributes. Recommended approach. |
| **Implicit label** | Label association made by nesting the control inside the `<label>` element. Less reliable with screen readers. |
| **`<button>`** | Clickable button element. Inside a `<form>`, defaults to `type="submit"`. Can contain HTML content. |
| **`<button type="submit">`** | Submits the form. Default behaviour of `<button>` inside a `<form>`. |
| **`<button type="reset">`** | Clears all form fields. Avoid using — causes accidental data loss. |
| **`<button type="button">`** | No default behaviour. Requires JavaScript. Same as `<button>` outside a form. |
| **`<fieldset>`** | Groups related form controls. Can be disabled to disable all contained controls. |
| **`<legend>`** | Child of `<fieldset>`. Provides a label for the entire group, read by screen readers. |
| **`<select>`** | Creates a drop-down menu. Takes `name` and `id` like `<input>`. |
| **`<option>`** | Child of `<select>`. Represents one choice. The `value` attribute sets the submitted data. |
| **`<textarea>`** | Multi-line text input. Takes `rows` and `cols` to set default dimensions. Has a closing tag (not void). |
| **Client-side validation** | Validation in the browser using attributes like `required` and appropriate `type`. Fast but bypassable. |
| **Server-side validation** | Validation on the server. Secure and tamper-resistant, but can't give instant feedback. |
| **Name/value pair** | The format of submitted form data: `name=value` (e.g., `hotel=economy`). Each control contributes one pair. |
| **Focus outline** | The visible blue ring that appears around a focused form element. Critical for keyboard navigation accessibility. |

---

## Watch Out For...

1. **A form control without a `name` attribute is NOT submitted.** This is the #1 cause of "my data isn't sending" bugs. Every control you want submitted must have `name`.

2. **`id` and `name` serve different purposes.** `id` links the control to its `<label>` (via the `for` attribute). `name` is the key in submitted data. They often have the same value, but they are separate attributes with separate jobs.

3. **Radio buttons all share the same `name` but must have different `value` attributes.** If two radio inputs have different `name` values, they become independent — you can "select" both. If they have no `value`, the submitted value defaults to `on`, which is useless for telling options apart.

4. **Unchecked checkboxes are completely absent from submitted data.** There is no `yoga=off` — a checkbox either appears in the URL (when checked) or does not appear at all. Server-side code must account for this.

5. **`<button>` inside `<form>` submits the form by default** — even without `type="submit"`. If you want a button inside a form that does NOT submit (e.g., a JS-powered UI button), you MUST add `type="button"`.

6. **`<input type="submit">` and `<input type="reset">` are inferior to `<button>`.** Prefer `<button type="submit">` and avoid `<button type="reset">` entirely (accidental data loss).

7. **`<textarea>` is NOT a void element** — it requires a closing `</textarea>` tag. Default placeholder text goes between the tags: `<textarea>Default text here</textarea>`.

8. **If `<option>` has no `value` attribute, the text content is submitted.** `<option>Plane</option>` submits `transport=Plane`. Always specify `value` to control what actually gets submitted.

9. **The first `<option>` is selected by default**, even if it's a placeholder like `--Please choose--`. If you don't want a value pre-selected, make the placeholder's `value=""` and add `required` to the `<select>`.

10. **Client-side validation only (`required`, `type="email"`) is NOT sufficient.** Users can disable JavaScript, modify the DOM, or send raw HTTP requests to bypass all client-side validation. Always validate on the server.

11. **`disabled` controls are NOT submitted** — their data is excluded from form submission entirely. This is by design, but can be surprising. Use `readonly` if you want non-editable data that still submits.

12. **Implicit labels (nesting) are less reliable than explicit labels** with screen readers. Prefer `<label for="id">` + `<input id="id">` for maximum accessibility compatibility.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the **three required components** of a basic HTML form? What is each one responsible for?

**Q2.** Explain the difference between the `name` and `id` attributes on an `<input>` element. What happens if `name` is omitted?

**Q3.** Write the HTML for a group of three radio buttons labelled "Small", "Medium", and "Large" where "Medium" is pre-selected and "Large" is disabled. Use proper `<fieldset>` structure.

**Q4.** What is the difference between client-side and server-side form validation? Why do you need both?

**Q5.** Explain the key structural difference between radio buttons and checkboxes in HTML — specifically how `name` and `value` are used differently, and how their submitted data differs.

---

## Answer Key

---

**A1.** The three required components of a basic HTML form:

1. **`<form>` element** — the outer wrapper. Groups all controls together. Defines `action` (where to send data) and `method` (how to send it — GET or POST). Any control inside `<form></form>` is part of the form.

2. **Label/control pairs** — one or more `<label>` + form control (`<input>`, `<select>`, `<textarea>`) pairs. The control collects the user's data; the label describes what data is expected. They are linked via matching `for` and `id` attributes.

3. **`<button>` (submit button)** — when clicked inside a `<form>`, it submits all collected data to the server at the URL specified by `action`.

---

**A2.**

| Attribute | Purpose | What happens if omitted |
|---|---|---|
| **`name`** | The **key** in the submitted `name=value` pair. Sets the data label sent to the server. | The control is **not submitted at all** — its value is silently excluded from the form data. |
| **`id`** | A unique identifier for the element. Used to link the control to its `<label>` via the label's `for` attribute. | The control cannot be associated with an explicit `<label>`. Clicking the label text won't focus the input; screen readers can't announce the label. |

Both often have the same string value (e.g., `id="email" name="email"`), but they serve completely different purposes.

---

**A3.**
```html
<fieldset>
  <legend>Choose a size:</legend>

  <input type="radio" id="small" name="size" value="small" />
  <label for="small">Small</label>

  <input type="radio" id="medium" name="size" value="medium" checked />
  <label for="medium">Medium</label>

  <input type="radio" id="large" name="size" value="large" disabled />
  <label for="large">Large</label>
</fieldset>
```

Key points:
- All share `name="size"` — this groups them so only one can be selected.
- Each has a unique `value` — this is what actually gets submitted (`size=small`, etc.).
- `checked` pre-selects Medium.
- `disabled` grays out Large and prevents selection.
- `<fieldset>` + `<legend>` groups and labels the entire set for accessibility.

---

**A4.**

| | Client-side validation | Server-side validation |
|---|---|---|
| **Where** | In the browser, before data is sent | On the server, after data arrives |
| **How** | HTML attributes (`required`, `type="email"`) and JavaScript | Backend code (any server language) |
| **Strength** | Instant feedback to the user | Secure — cannot be disabled by the user |
| **Weakness** | Bypassable — user can disable JS, edit the DOM, or send raw HTTP | Slow feedback — data must travel to server before errors are reported |

**Why you need both:**
- Client-side gives **immediate UX feedback** — "Please fill in this field" appears instantly.
- Server-side provides **security and integrity** — it's the only layer you can trust, because client-side code can always be tampered with.

---

**A5.**

**Radio buttons:**
- All buttons in a group share the **same `name`** — this makes them a single mutually exclusive set.
- Each needs a unique **`value`** — this is mandatory, as it's what gets submitted.
- Exactly **one** name/value pair submitted: `hotel=economy`
- You cannot select more than one at a time.

**Checkboxes:**
- Each checkbox has a **unique `name`** — they are independent controls.
- `value` is optional (defaults to `on`): `yoga=on`
- **Zero or more** name/value pairs submitted — one per checked box.
- Unchecked boxes produce **no entry** in submitted data.

```
Radio:    name="hotel"  value="economy"   → hotel=economy  (one submitted pair for the group)
Radio:    name="hotel"  value="superior"  → (not selected, not submitted)

Checkbox: name="yoga"                     → yoga=on         (checked - submitted)
Checkbox: name="coffee"                   → (unchecked - not submitted at all)
```
