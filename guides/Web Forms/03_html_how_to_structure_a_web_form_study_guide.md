# 🏗️ How to Structure a Web Form — Exam Study Guide
**Source:** [MDN Web Docs — How to structure a web form](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/How_to_structure_a_web_form)

---

## Executive Summary

This article covers the semantic HTML elements used to give a web form meaningful structure — going beyond just collecting data to ensuring forms are usable, accessible, and logically organised. The four core structural elements are `<form>` (the mandatory wrapper), `<fieldset>` + `<legend>` (grouping related controls), and `<label>` (the critical link between text descriptions and their controls). The most exam-critical takeaway is that **correct structure is not optional** — it directly determines whether assistive technologies like screen readers can interpret and announce your form correctly.

---

## Core Pillars

### 1. The `<form>` Element — The Mandatory Wrapper

- Every HTML form **must** start with a `<form>` element — all controls nest inside it.
- `<form>` formally defines the form and its submission behaviour (`action`, `method`).
- Assistive technologies and browser plugins specifically detect `<form>` elements to provide enhanced interaction (e.g., autofill, form navigation shortcuts).
- A form control can live **outside** `<form>` tags — but must be explicitly linked using the `form` attribute (pointing to the form's `id`):

```html
<form id="myForm" action="/submit" method="post">
  <!-- controls inside -->
</form>

<!-- This input is outside the form but still associated with it -->
<input type="text" name="extra" form="myForm" />
```

> ⚠️ **NEVER** nest a `<form>` inside another `<form>`. This is strictly forbidden — it causes **unpredictable behaviour**. Browsers do not support nested forms.

---

### 2. `<fieldset>` and `<legend>` — Grouping Related Controls

**`<fieldset>`** groups related form controls together for both **styling** and **semantic** purposes.
**`<legend>`** is placed immediately after the opening `<fieldset>` tag and provides a text description of the group.

```html
<form>
  <fieldset>
    <legend>Fruit juice size</legend>
    <p>
      <input type="radio" name="size" id="size_1" value="small" />
      <label for="size_1">Small</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_2" value="medium" />
      <label for="size_2">Medium</label>
    </p>
    <p>
      <input type="radio" name="size" id="size_3" value="large" />
      <label for="size_3">Large</label>
    </p>
  </fieldset>
</form>
```

**How screen readers use `<legend>`:**
- Screen readers (e.g., JAWS, NVDA) read the `<legend>` text as a **prefix to every label inside the `<fieldset>`**.
- The above example is read as: `"Fruit juice size small"`, `"Fruit juice size medium"`, `"Fruit juice size large"`.
- Without `<fieldset>` + `<legend>`, the screen reader would just say `"small"`, `"medium"`, `"large"` — completely ambiguous.

**Two primary use cases for `<fieldset>`:**
1. **Radio button groups** — the most important use case. Every set of radio buttons should be wrapped in a `<fieldset>`.
2. **Long form sectioning** — if a form is too long for multiple pages, split related fields into `<fieldset>` sections to improve usability.

> `<fieldset>` is one of the **key elements for building accessible forms**. Don't abuse it — only use it where it adds genuine semantic grouping.

---

### 3. The `<label>` Element — The Accessibility Cornerstone

`<label>` is the **formal, standard way** to associate descriptive text with a form control. It is the most important element for accessibility.

**Two ways to associate a label with a control:**

#### Method 1 — Explicit (Recommended)
```html
<label for="name">Name:</label>
<input type="text" id="name" name="user_name" />
```
- `for` on `<label>` must exactly match the `id` on the `<input>`.
- Screen reader announces: `"Name, edit text"`.

#### Method 2 — Implicit (Nesting)
```html
<label for="name">
  Name:
  <input type="text" id="name" name="user_name" />
</label>
```
- The control is nested inside `<label>` — the association is implicit.
- Even when nesting, **best practice is to still include `for`** to ensure all assistive technologies understand the relationship.

**What happens without a label:**
- Screen reader announces: `"Edit text blank"` — completely uninformative.
- The control is functionally unusable for screen reader users.

#### Labels Are Clickable

A properly associated label **expands the click/tap target** for its control:
- Clicking the label text focuses/activates the linked input.
- Critical for **radio buttons and checkboxes** — their native hit area is tiny. Making the label clickable dramatically improves usability, especially on mobile.

```html
<form>
  <p>
    <input type="checkbox" id="taste_1" name="taste_cherry" value="cherry" />
    <label for="taste_1">I like cherry</label>
  </p>
  <p>
    <input type="checkbox" id="taste_2" name="taste_banana" value="banana" />
    <label for="taste_2">I like banana</label>
  </p>
</form>
```
Clicking "I like cherry" toggles the checkbox — the label is part of the interactive area.

---

### 4. Multiple Labels — What to Avoid and What to Do Instead

Technically, you can put multiple `<label>` elements on one control — but **don't**. Some assistive technologies struggle to handle multiple labels on a single widget.

**Bad practice — two separate labels for one input:**
```html
<!-- DON'T do this -->
<div>
  <label for="username">Name:</label>
  <input id="username" type="text" name="username" required />
  <label for="username">*</label>   <!-- second label — avoid -->
</div>
```

**Better — nest everything in one label:**
```html
<!-- Better, but still complex -->
<div>
  <label for="username">
    <span>Name:</span>
    <input id="username" type="text" name="username" required />
    <span>*</span>
  </label>
</div>
```

**Best — include the required marker inside the single label text:**
```html
<!-- Best practice -->
<div>
  <label for="username">Name *:</label>
  <input id="username" type="text" name="username" required />
</div>
```

The `*` convention must be **explained before it is first used**:
```html
<p>Please complete all required (*) fields.</p>
```
This explanation must come before any `*`-marked field so sighted and AT users understand it before they encounter it.

---

### 5. Common HTML Structures Used With Forms

Form markup is regular HTML — use all standard HTML elements to structure it. Common patterns:

| Structure | Use case |
|---|---|
| `<p>` wrapping `<label>` + `<input>` | Single label/input pairs (most common) |
| `<ul>` / `<ol>` with `<li>` items | Lists of checkboxes or radio buttons |
| `<div>` wrapping `<label>` + `<input>` | General-purpose grouping |
| `<section>` with `<h2>` | Major logical sections of a longer form |
| `<fieldset>` + `<legend>` | Radio/checkbox groups; form section grouping |
| `<h1>` at top of form | Form title (e.g., "Payment form") |

**General rule:** Each separate section of functionality → its own `<section>`. Radio button groups → inside `<fieldset>`.

---

### 6. Building a Real Form — The Payment Form Example

The article builds a **payment form** demonstrating all structural principles together. Full structure:

```html
<form>
  <h1>Payment form</h1>
  <p>Please complete all required (*) fields.</p>

  <!-- SECTION 1: Contact Information -->
  <section>
    <h2>Contact information</h2>

    <!-- Radio group in <fieldset> -->
    <fieldset>
      <legend>Title</legend>
      <ul>
        <li>
          <label for="title_1">
            <input type="radio" id="title_1" name="title" value="A" />
            Ace
          </label>
        </li>
        <li>
          <label for="title_2">
            <input type="radio" id="title_2" name="title" value="K" />
            King
          </label>
        </li>
        <li>
          <label for="title_3">
            <input type="radio" id="title_3" name="title" value="Q" />
            Queen
          </label>
        </li>
      </ul>
    </fieldset>

    <!-- Text inputs in <p> wrappers -->
    <p>
      <label for="name">Name *:</label>
      <input type="text" id="name" name="username" required />
    </p>
    <p>
      <label for="mail">Email *:</label>
      <input type="email" id="mail" name="user-mail" required />
    </p>
    <p>
      <label for="pwd">Password *:</label>
      <input type="password" id="pwd" name="password" required />
    </p>
  </section>

  <!-- SECTION 2: Payment Information -->
  <section>
    <h2>Payment information</h2>
    <p>
      <label for="card">
        <span>Card type:</span>
      </label>
      <select id="card" name="user-card">
        <option value="visa">Visa</option>
        <option value="mc">Mastercard</option>
        <option value="amex">American Express</option>
      </select>
    </p>
    <p>
      <label for="number">Card number *:</label>
      <!-- type="tel" used instead of "number" to avoid spinner UI -->
      <input type="tel" id="number" name="card-number" required />
    </p>
    <p>
      <label for="expiration">Expiration date *:</label>
      <input
        type="text"
        id="expiration"
        name="expiration"
        required
        placeholder="MM/YY"
        pattern="^(0[1-9]|1[0-2])\/([0-9]{2})$" />
    </p>
  </section>

  <!-- SECTION 3: Submit -->
  <section>
    <p>
      <button type="submit">Validate the payment</button>
    </p>
  </section>
</form>
```

**Key decisions in this form:**
- Radio buttons grouped in `<fieldset>` + `<legend>` for screen reader context.
- Each radio wrapped in `<li>` inside a `<ul>` — semantic list structure.
- Each `<label>`/`<input>` pair wrapped in `<p>` for simple spacing.
- `type="tel"` for card number (not `type="number"`) — avoids the unwanted spinner control.
- `pattern` attribute on expiration validates MM/YY format client-side.
- `required` on all mandatory fields for client-side validation.

---

## Technical Deep-Dive

### Logic Walkthrough: Screen Reader Behaviour With and Without `<fieldset>`

**Scenario:** A form asks the user to pick a fruit juice size — Small, Medium, or Large.

**Without `<fieldset>` + `<legend>`:**
```html
<p>
  <input type="radio" name="size" id="s1" value="small" />
  <label for="s1">Small</label>
</p>
<p>
  <input type="radio" name="size" id="s2" value="medium" />
  <label for="s2">Medium</label>
</p>
```
Screen reader announces each control independently:
```
Radio button, Small, not selected
Radio button, Medium, not selected
```
The user has no idea what question these radios are answering.

**With `<fieldset>` + `<legend>`:**
```html
<fieldset>
  <legend>Fruit juice size</legend>
  <p>
    <input type="radio" name="size" id="s1" value="small" />
    <label for="s1">Small</label>
  </p>
  <p>
    <input type="radio" name="size" id="s2" value="medium" />
    <label for="s2">Medium</label>
  </p>
</fieldset>
```
Screen reader announces:
```
Fruit juice size, Radio button, Small, not selected
Fruit juice size, Radio button, Medium, not selected
```
The `<legend>` text is prepended to every label — the question and the answer are always announced together.

---

### Logic Walkthrough: The Required Field Asterisk Pattern

**The problem:** Marking required fields with `*` is a common visual convention — but how do you communicate it to screen reader users?

**Step 1 — Explain the convention BEFORE the first required field:**
```html
<p>Please complete all required (*) fields.</p>
```
This line must appear at the top of the form — before any `*` appears. Screen reader users encounter the explanation first.

**Step 2 — Include `*` in the label itself (best approach):**
```html
<label for="name">Name *:</label>
<input type="text" id="name" name="username" required />
```
The screen reader reads: `"Name star, edit text"` — the asterisk is part of the announced label text.

**The wrong approach — a second `<label>` for the asterisk:**
```html
<!-- DON'T: two labels on one input -->
<label for="username">Name:</label>
<input id="username" type="text" name="username" required />
<label for="username">*</label>
```
- Some AT handles two labels poorly.
- The `*` alone as a label sounds like punctuation out of context.
- Fix: consolidate into one label: `Name *:`.

---

### Logic Walkthrough: `type="tel"` vs `type="number"` for Card Numbers

The payment form uses `type="tel"` for card numbers, not `type="number"`. Why?

```html
<!-- USED in the example: -->
<input type="tel" id="number" name="card-number" required />

<!-- NOT used — and here's why: -->
<input type="number" id="number" name="card-number" required />
```

| Feature | `type="number"` | `type="tel"` |
|---|---|---|
| Spinner arrows (increment/decrement) | ✅ Shows — unwanted for card numbers | ❌ No spinner |
| Mobile keyboard | Numeric keyboard | Phone/numeric keyboard |
| Leading zeros | May strip leading zeros | Preserved as text |
| Semantic meaning | "A mathematical quantity" | "A telephone-style number string" |

Card numbers are **strings of digits**, not mathematical values. `type="tel"` gives the right mobile keyboard without the unwanted number-picker UI. This is a design decision about semantics over convenience.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`<form>`** | The mandatory wrapper element for all form controls. Defines `action` (destination URL) and `method` (HTTP method). Must not be nested inside another `<form>`. |
| **`<fieldset>`** | Groups related form controls together for semantic and styling purposes. Essential for radio button groups and optional for sectioning long forms. |
| **`<legend>`** | Placed as the first child of `<fieldset>`. Provides a text description of the group. Screen readers prepend its content to each label inside the fieldset. |
| **`<label>`** | Associates a text description with a form control. Essential for accessibility — without it, screen readers cannot identify the control's purpose. |
| **`for` attribute** | On `<label>`. Must exactly match the `id` of the associated control. Creates an explicit label association. |
| **Explicit label** | Label associated via matching `for` (on label) and `id` (on input). The recommended pattern. |
| **Implicit label** | Control nested inside `<label>` tags — association is inferred. Still best practice to include `for`. |
| **`form` attribute** | On a form control. Associates the control with a `<form>` element (by the form's `id`) even if the control is outside the `<form>` tags in the DOM. |
| **`required` attribute** | Boolean attribute on a form control. Prevents form submission if the field is empty. Triggers client-side validation. |
| **`pattern` attribute** | Specifies a regex that the field's value must match for the form to submit. Used for format validation (e.g., MM/YY date format). |
| **`placeholder` attribute** | Grey hint text shown inside a field when empty. Describes the expected format. NOT a substitute for a `<label>`. Disappears when user starts typing. |
| **`<section>`** | Used to group a major logical part of a complex form, paired with a heading (`<h2>`). Each distinct area of functionality should be in its own `<section>`. |
| **`<select>`** | A dropdown menu element. Children are `<option>` elements. Used for selecting one item from a predefined list. |
| **`<option>`** | Child of `<select>`. Defines one item in a dropdown. The `value` attribute is what gets submitted; the text content is what the user sees. |
| **`type="tel"`** | Input type for telephone-style numeric strings. Shows numeric keyboard on mobile without the spinner UI of `type="number"`. Preserves leading zeros. |
| **`type="number"`** | Input type for mathematical quantities. Renders increment/decrement arrows (spinner). Not appropriate for card numbers or codes. |
| **`type="password"`** | Masks typed characters. UI-only feature — data still transmitted as plain text unless served over HTTPS. |
| **Nested forms** | Placing a `<form>` inside another `<form>`. Strictly forbidden — causes unpredictable behaviour. |
| **Hit area** | The physical region on screen that responds to a click or tap. Associating a `<label>` with a control expands the hit area to include the label text. |
| **Assistive technology (AT)** | Software that helps people with disabilities use computers — e.g., screen readers (JAWS, NVDA), voice control software. |
| **`<legend>` as label prefix** | The accessibility behaviour where screen readers announce the `<legend>` text before each control label inside the `<fieldset>`: e.g., "Fruit juice size, small". |

---

## Watch Out For...

1. **Nested `<form>` elements are forbidden.** Many beginners try to embed forms within forms. This is invalid HTML and causes unpredictable, browser-specific behaviour. There is no scenario where nesting forms is correct.

2. **`<legend>` must be the FIRST child of `<fieldset>`.** Placing `<legend>` anywhere else (e.g., after some inputs) is invalid. The browser may render it elsewhere or ignore its accessible role. Always put `<legend>` immediately after `<opening-fieldset-tag>`.

3. **Implicit labels (nesting) still need the `for` attribute.** Even if the control is nested inside `<label>`, some assistive technologies still benefit from an explicit `for`/`id` pairing. Always include `for` as best practice, even when nesting.

4. **`placeholder` is NOT a label.** A common UX mistake is removing the `<label>` and relying solely on `placeholder` to describe a field. Placeholder text disappears when the user types — the user can no longer see what the field requires. It is also not reliably announced by all screen readers. Always include a `<label>`.

5. **Multiple `<label>` elements on one control causes AT problems.** If you need to add extra information (like a required `*`), incorporate it into the single `<label>` text (`Name *:`) rather than adding a second `<label for="...">*</label>`.

6. **Explain `*` notation BEFORE the first required field — not after.** The explanation paragraph (`Please complete all required (*) fields.`) must appear at the top of the form, before any `*`-marked input. A screen reader reading top-to-bottom would encounter the `*` before the explanation if it's placed anywhere else.

7. **`type="number"` is wrong for card numbers, phone numbers, and codes.** `type="number"` is for mathematical quantities — it adds a spinner UI and may strip leading zeros. Use `type="tel"` for numeric strings that are telephone-style (card numbers, PINs, verification codes).

8. **Form controls outside `<form>` are submitted only if linked via the `form` attribute.** A control placed outside the `<form>` tags with no `form` attribute is completely disconnected from the form and will never be submitted. If you intend to place a control outside the form, you MUST use `form="[form-id]"`.

9. **`<fieldset>` for radio buttons is mandatory for accessibility, not just nice-to-have.** Without a `<fieldset>` and `<legend>`, screen reader users hear individual radio labels with no context for what choice they're making. This is a WCAG accessibility failure.

10. **`for` is case-sensitive and must be an exact match.** `for="Name"` will NOT link to `id="name"`. JavaScript's DOM is case-sensitive for `id` matching. A mismatch silently breaks both the label click behaviour and screen reader association.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the four main structural elements covered in this article and what is each one's role? Name them from outermost/largest scope to innermost.

**Q2.** Write the HTML for an accessible radio button group asking "What is your preferred contact method?" with options: Email, Phone, Post. Use all correct structural elements.

**Q3.** What is the difference between an explicit label association and an implicit label association? Which is preferred, and what additional step is best practice even when using the implicit method?

**Q4.** A developer is building a credit card form. They use `<input type="number">` for the card number field. What two specific problems does this cause, and what `type` value should they use instead?

**Q5.** A form has a large number of fields covering three topics: personal info, shipping address, and payment details. Describe the recommended HTML structure for this form, naming every structural element layer and explaining why each is used.

---

## Answer Key

---

**A1.** The four structural elements, from largest to smallest scope:

| Element | Role |
|---|---|
| **`<form>`** | The mandatory outermost wrapper. Defines `action` (where data goes) and `method` (HTTP verb). All controls must be inside this (or linked to it via `form` attribute). |
| **`<fieldset>`** | Groups related controls together. Provides semantic structure and is essential for radio/checkbox groups. Can also section long forms. |
| **`<legend>`** | Provides a text description for the `<fieldset>` group. Must be the first child of `<fieldset>`. Screen readers prepend it to every label inside the group. |
| **`<label>`** | Associates descriptive text with a single form control. The most important element for accessibility — without it, controls are unidentifiable to screen reader users. |

---

**A2.** Accessible radio button group:

```html
<form>
  <fieldset>
    <legend>What is your preferred contact method?</legend>
    <ul>
      <li>
        <input type="radio" id="contact_email" name="contact" value="email" />
        <label for="contact_email">Email</label>
      </li>
      <li>
        <input type="radio" id="contact_phone" name="contact" value="phone" />
        <label for="contact_phone">Phone</label>
      </li>
      <li>
        <input type="radio" id="contact_post" name="contact" value="post" />
        <label for="contact_post">Post</label>
      </li>
    </ul>
  </fieldset>
</form>
```

Key elements used:
- `<fieldset>` — groups all three radios as one semantic unit
- `<legend>` — provides the question text, announced by screen readers before each option
- `<ul>` + `<li>` — semantic list structure for the options
- Same `name="contact"` on all radios — creates the mutually exclusive group
- Explicit labels via `for`/`id` pairs — enables label clicking and screen reader announcements

---

**A3.**

**Explicit label:** The `<label>` element has a `for` attribute matching the control's `id`. They are separate elements:
```html
<label for="email">Email:</label>
<input type="email" id="email" name="user_email" />
```

**Implicit label:** The control is nested inside the `<label>`. The association is inferred from the nesting:
```html
<label>
  Email:
  <input type="email" name="user_email" />
</label>
```

**Preferred:** Explicit association (separate elements with `for`/`id`).

**Best practice for implicit:** Even when nesting, still include the `for` attribute — and the control must still have a matching `id`. Some assistive technologies handle the relationship more reliably with explicit `for`/`id` even when nesting is used:
```html
<label for="email">
  Email:
  <input type="email" id="email" name="user_email" />
</label>
```

---

**A4.**

**Problem 1 — Unwanted spinner UI:** `type="number"` renders increment/decrement arrow buttons (a "spinner") on the input. For a credit card number, these arrows are meaningless and visually cluttering. There is no use case for incrementing a card number by 1.

**Problem 2 — Leading zeros stripped:** Some browsers may strip or reject leading zeros from `type="number"` inputs, since mathematically `0123` equals `123`. Card numbers and similar codes must preserve their exact string representation.

**Correct `type` value:** `type="tel"` — designed for telephone-style numeric strings. It triggers a full numeric keyboard on mobile devices, has no spinner, and treats the value as a string, preserving leading zeros.

```html
<!-- WRONG -->
<input type="number" id="number" name="card-number" required />

<!-- CORRECT -->
<input type="tel" id="number" name="card-number" required />
```

---

**A5.** Recommended structure for a multi-section form:

```html
<form action="/submit" method="post">
  <!-- Form title + required field explanation -->
  <h1>Order Form</h1>
  <p>Please complete all required (*) fields.</p>

  <!-- Section 1: Personal Info -->
  <section>
    <h2>Personal Information</h2>
    <p>
      <label for="name">Full name *:</label>
      <input type="text" id="name" name="full_name" required />
    </p>
    <!-- more fields... -->
  </section>

  <!-- Section 2: Shipping Address -->
  <section>
    <h2>Shipping Address</h2>
    <p>
      <label for="street">Street *:</label>
      <input type="text" id="street" name="street" required />
    </p>
    <!-- more fields... -->
  </section>

  <!-- Section 3: Payment Details -->
  <section>
    <h2>Payment Details</h2>
    <!-- Radio group for payment type -->
    <fieldset>
      <legend>Payment method</legend>
      <ul>
        <li>
          <input type="radio" id="pay_card" name="payment" value="card" />
          <label for="pay_card">Credit card</label>
        </li>
        <li>
          <input type="radio" id="pay_paypal" name="payment" value="paypal" />
          <label for="pay_paypal">PayPal</label>
        </li>
      </ul>
    </fieldset>
    <!-- more payment fields... -->
  </section>

  <!-- Submit section -->
  <section>
    <p>
      <button type="submit">Place order</button>
    </p>
  </section>
</form>
```

**Why each layer:**
- **`<form>`** — mandatory wrapper, defines submission target and method
- **`<h1>`** — form title for orientation
- **`<p>` + explanation** — required field convention explained before any `*` appears
- **`<section>` + `<h2>`** — separates each distinct area of the form into navigable, labelled regions
- **`<fieldset>` + `<legend>`** — specifically wraps the radio group, giving screen readers question context for each option
- **`<ul>` + `<li>`** — semantically appropriate list structure for multiple-choice options
- **`<p>` wrapping `<label>` + `<input>`** — simple, clean grouping for individual text fields
- **`<button type="submit">`** — preferred over `<input type="submit">` for flexibility
