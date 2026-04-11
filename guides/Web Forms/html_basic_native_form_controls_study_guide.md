# 🎛️ Basic Native Form Controls — Exam Study Guide
**Source:** [MDN Web Docs — Basic native form controls](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Basic_native_form_controls)

---

## Executive Summary

This article covers the **original set of form controls** — the `<input>` types, the `<button>` element, and their key attributes — all available since the early days of the web and supported in every browser. The `<input>` element is uniquely polymorphic: a single element that transforms into radically different controls depending on its `type` attribute (`text`, `password`, `hidden`, `checkbox`, `radio`, `submit`, `reset`, `button`, `file`, `image`). Checkable controls (checkboxes and radio buttons) follow a special submission rule — **they are only submitted when checked** — and radio buttons in a group are linked by sharing the **same `name` attribute**. Four universal attributes (`autofocus`, `disabled`, `form`, `name`) apply across all form controls and are essential exam knowledge.

---

## Core Pillars

### 1. The `<input>` Element — The Most Versatile Form Element

> `<input>` is unique in all of HTML — it is a void element that changes its entire appearance and behaviour based on a single attribute: `type`.

```html
<input type="text" />          <!-- single-line text field -->
<input type="password" />      <!-- masked text field -->
<input type="hidden" />        <!-- invisible, still submitted -->
<input type="checkbox" />      <!-- toggle on/off -->
<input type="radio" />         <!-- pick one from a group -->
<input type="submit" />        <!-- submit button -->
<input type="reset" />         <!-- reset button (avoid) -->
<input type="button" />        <!-- generic JS button -->
<input type="file" />          <!-- file picker -->
<input type="image" />         <!-- image submit button -->
```

**Fallback behaviour:** If a browser doesn't recognise a `type` value, it falls back to `type="text"`. This means new HTML5 types like `type="color"` degrade gracefully to a text field in older browsers.

---

### 2. Text Input Fields

**What they are:** Plain text only — no rich formatting (bold, italic, etc.). Rich text editors on the web are custom widgets built with HTML, CSS, and JavaScript — not native form controls.

#### Single-Line Text Field

```html
<input type="text" id="comment" name="comment" value="I'm a text field" />
```

- `type="text"` is the default — `type` can be omitted and it still behaves as text.
- Line breaks are **stripped** if the user somehow types them — single line only.
- Pre-fill the field with the `value` attribute.

#### Password Field

```html
<input type="password" id="pwd" name="pwd" />
```

- Obscures characters with dots or asterisks.
- **IMPORTANT: This is only a UI feature.** The data is still sent in plain text unless the form is submitted over **HTTPS**. Always use `https://` for any page with a password field.
- Does not add extra text constraints — only the visual masking.

#### Hidden Input

```html
<input type="hidden" id="timestamp" name="timestamp" value="1286705410" />
```

- Completely invisible to the user — not rendered, receives no focus, screen readers ignore it.
- Still **submitted with the form** — the server receives its `name=value` pair.
- Common use: sending metadata (timestamps, tokens, session IDs) that the user shouldn't see or edit.
- Value is typically set dynamically via JavaScript.
- **Must not have an associated `<label>`** — there's nothing for the label to describe.

---

### 3. Common Behaviours of All Text Controls

All basic text controls (text, password) share these behaviours:

| Attribute/Feature | What it does |
|---|---|
| `readonly` | User **cannot** modify the value, but it **IS** submitted with the form |
| `disabled` | User cannot modify the value, and it **IS NOT** submitted with the form |
| `placeholder` | Grey hint text inside the box describing its purpose. Disappears when user types. |
| `size` | Sets the physical width of the box (in character widths) |
| `maxlength` | Sets the maximum number of characters the user can enter |
| `spellcheck` | Enables/disables spell-checking for the field |

**`readonly` vs. `disabled` — exam-critical distinction:**

```html
<!-- readonly: shows value, submits value, user can't edit -->
<input type="text" name="locked" value="Cannot change" readonly />

<!-- disabled: grayed out, user can't edit, NOT submitted -->
<input type="text" name="gone" value="Not sent" disabled />
```

---

### 4. Checkable Items — Checkboxes and Radio Buttons

> **The defining rule:** Checkable items are **only submitted when they are checked.** If unchecked, nothing is sent — not even their `name`.

**If checked but no `value` specified → submitted as `name=on`.**

Structure recommendation: wrap related checkables in `<fieldset>` + `<legend>`, with each `<label>`/`<input>` pair in a list item (`<li>`).

#### Checkbox

```html
<fieldset>
  <legend>Choose all the vegetables you like to eat</legend>
  <ul>
    <li>
      <label for="carrots">Carrots</label>
      <input type="checkbox" id="carrots" name="vegetable" value="carrots" checked />
    </li>
    <li>
      <label for="peas">Peas</label>
      <input type="checkbox" id="peas" name="vegetable" value="peas" />
    </li>
  </ul>
</fieldset>
```

**Checkbox rules:**
- Related checkboxes **can share the same `name`** (as in the example above).
- Each one submitted independently: `vegetable=carrots` if checked.
- `checked` pre-selects on page load.
- Clicking the checkbox OR its label toggles it on/off.
- A checked checkbox adds `name=value` to submission; an unchecked one adds nothing.

**CSS pseudo-classes:**
- `:default` — matches any checkbox that had `checked` on page load (even if now unchecked).
- `:checked` — matches any checkbox that is currently checked.

#### Radio Button

```html
<fieldset>
  <legend>What is your favorite meal?</legend>
  <ul>
    <li>
      <label for="soup">Soup</label>
      <input type="radio" id="soup" name="meal" value="soup" checked />
    </li>
    <li>
      <label for="curry">Curry</label>
      <input type="radio" id="curry" name="meal" value="curry" />
    </li>
    <li>
      <label for="pizza">Pizza</label>
      <input type="radio" id="pizza" name="meal" value="pizza" />
    </li>
  </ul>
</fieldset>
```

**Radio button rules:**
- Buttons in the same group **must share the same `name`** — this is what links them and enforces mutual exclusivity.
- Only **one** radio in a same-named group can be checked at a time — selecting one auto-unchecks the others.
- Only the **value of the checked radio** is submitted: `meal=soup`.
- If **none are checked**, no value is sent (unknown state).
- Once a radio in a group is checked, the user **cannot uncheck all buttons** without resetting the form.
- `checked` pre-selects the default choice — always provide one to avoid an ambiguous initial state.

---

### 5. Actual Buttons — `<input>` Types vs. `<button>` Element

There are **three button input types** and the **`<button>` element**, which mirrors them:

| Action | `<input>` version | `<button>` version |
|---|---|---|
| Submit form | `<input type="submit" value="Submit" />` | `<button type="submit">Submit</button>` |
| Reset form | `<input type="reset" value="Reset" />` | `<button type="reset">Reset</button>` |
| No default action (JS) | `<input type="button" value="Click me" />` | `<button type="button">Click me</button>` |

**Why `<button>` is superior:**
- `<input>` is a void element — its label comes from the `value` attribute, which only accepts **plain text**.
- `<button>` has opening and closing tags — it can contain **full HTML content** (icons, bold text, images).

```html
<!-- <input> — plain text label only -->
<input type="submit" value="Submit this form" />

<!-- <button> — HTML content allowed inside -->
<button type="submit">Submit <strong>this form</strong></button>
```

> **Default `<button>` type:** Inside a `<form>`, omitting `type` (or using an invalid `type` value) defaults to `type="submit"`. Outside a `<form>`, it defaults to `type="button"` (no action).

---

### 6. Image Button

```html
<input type="image" alt="Click me!" src="my-img.png" width="80" height="30" />
```

- Renders like an `<img>` element but **acts as a submit button** when clicked.
- Supports all `<img>` attributes (`src`, `alt`, `width`, `height`) plus button attributes.
- **Unique submission behaviour:** Instead of submitting its `value`, it submits the **X and Y coordinates** of where the user clicked on the image (relative to image's top-left corner = (0,0)).
- Coordinates submitted as two pairs: `name.x=123` and `name.y=456`.

```
URL result: https://example.com?pos.x=123&pos.y=456
```

Use case: interactive image maps ("hot maps") where the click location is meaningful.

---

### 7. File Picker

```html
<input type="file" name="file" id="file" accept="image/*" multiple />
```

- Opens the OS native file chooser dialog.
- `accept` — restricts file types the picker shows:
  - `accept="image/*"` — all image types
  - `accept=".pdf,.doc"` — specific extensions
  - `accept="image/*;capture=camera"` — trigger device camera (mobile)
- `multiple` — allows the user to select more than one file.
- File uploads require `method="post"` and `enctype="multipart/form-data"` on the `<form>`.

**Mobile camera capture:**
```html
<input type="file" accept="image/*;capture=camera" />    <!-- camera -->
<input type="file" accept="video/*;capture=camcorder" /> <!-- video -->
<input type="file" accept="audio/*;capture=microphone" /> <!-- audio -->
```

---

### 8. Common Attributes — Universal Across All Form Controls

These four attributes apply to virtually all form controls:

| Attribute | What it does | Notes |
|---|---|---|
| **`autofocus`** | Automatically focuses this control when the page loads | Only one element on the page should have this |
| **`disabled`** | Grays out the control, prevents interaction, and **excludes it from form submission** | Also works on `<fieldset>` to disable all controls inside |
| **`form`** | Associates a control with a `<form>` by the form's `id` | Allows a control to live **outside** the `<form>` element in the HTML |
| **`name`** | The key in the `name=value` submission pair | Required for a control's data to be submitted |
| **`value`** | The data submitted for this control | On text inputs: default/current value. On buttons: label text. On radio/checkbox: what gets submitted when checked. |

**The `form` attribute — frequently overlooked:**
```html
<form id="myForm" action="/submit">
  <!-- ... -->
</form>

<!-- This input is OUTSIDE the <form> tags, but associated via form="myForm" -->
<input type="text" name="extra" form="myForm" />
```

---

## Technical Deep-Dive

### Logic Walkthrough: Checkbox Submission vs. Radio Submission

**Setup:**
```html
<!-- CHECKBOX GROUP (same name) -->
<input type="checkbox" name="vegetable" value="carrots" checked />  <!-- checked -->
<input type="checkbox" name="vegetable" value="peas" />             <!-- unchecked -->
<input type="checkbox" name="vegetable" value="cabbage" checked />  <!-- checked -->

<!-- RADIO GROUP (same name, one selected) -->
<input type="radio" name="meal" value="soup" checked />   <!-- selected -->
<input type="radio" name="meal" value="curry" />           <!-- not selected -->
<input type="radio" name="meal" value="pizza" />           <!-- not selected -->
```

**Submitted data:**
```
vegetable=carrots    ← checked checkbox → submitted
                     ← unchecked "peas" → NOT submitted
vegetable=cabbage    ← checked checkbox → submitted (multiple pairs with same name!)
meal=soup            ← the one selected radio → submitted
                     ← unselected "curry" and "pizza" → NOT submitted
```

**Result string:** `vegetable=carrots&vegetable=cabbage&meal=soup`

---

### Logic Walkthrough: `readonly` vs. `disabled` — Submission Difference

```html
<form action="/submit" method="get">
  <input type="text" name="field_a" value="ReadOnly value" readonly />
  <input type="text" name="field_b" value="Disabled value" disabled />
  <button type="submit">Submit</button>
</form>
```

**After click — URL produced:**
```
/submit?field_a=ReadOnly+value
```

- `field_a` is submitted because `readonly` only prevents editing — the value still travels with the form.
- `field_b` is **absent entirely** — `disabled` means it is not part of the submission at all.

---

### Logic Walkthrough: Password Field — UI Feature Only

```
User sees:  ●●●●●●●●●●  (masked)
Browser sends over HTTP:  pwd=mysecretpassword  (plain text!)
Browser sends over HTTPS: [encrypted payload containing: pwd=mysecretpassword]
```

The `type="password"` masking stops over-the-shoulder reading — it does NOT protect the data in transit. HTTPS encryption is what actually protects the password.

---

### Logic Walkthrough: Image Button Coordinates

```html
<form action="/map" method="get">
  <input type="image" name="pos" src="map.png" alt="Click a location" />
</form>
```

User clicks at position (150, 87) on the image:

```
GET /map?pos.x=150&pos.y=87
```

The `name` attribute (`pos`) is used as the prefix for both coordinate pairs. The image's own `value` attribute is irrelevant — it is not submitted.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`type` attribute** | On `<input>`, determines the entire appearance and behaviour of the control. The most important attribute on `<input>`. Falls back to `text` if unrecognised. |
| **`type="text"`** | Default `<input>` type. Single-line, accepts any text. Strips line breaks before submission. |
| **`type="password"`** | Masks input with dots/asterisks. UI-only feature — data still sent as plain text unless HTTPS is used. |
| **`type="hidden"`** | Invisible form control. Submitted with the form. Used for server metadata. Must not have a `<label>`. |
| **`type="checkbox"`** | Toggle control. Only submitted when checked. If checked with no `value`, submits `name=on`. |
| **`type="radio"`** | One-of-many selector. Buttons with the same `name` form a mutual exclusivity group. Only the checked one submits. |
| **`type="submit"`** | Button that submits the form. Equivalent to `<button type="submit">`. |
| **`type="reset"`** | Button that resets all form fields to defaults. Avoid — causes accidental data loss. |
| **`type="button"`** | Generic button with no default behaviour. Requires JavaScript. |
| **`type="file"`** | Opens native OS file picker. Use `accept` to filter types and `multiple` to allow multiple files. |
| **`type="image"`** | Image that acts as submit button. Submits click coordinates (`name.x` and `name.y`) instead of a value. |
| **`readonly`** | Prevents user editing the value. Value IS still submitted. Different from `disabled`. |
| **`disabled`** | Prevents interaction AND excludes the control from form submission. Can be applied to `<fieldset>`. |
| **`placeholder`** | Grey hint text in the field that disappears when the user starts typing. Not submitted as a value. |
| **`size`** | Sets the visible width of a text input in character units. Does not limit input length. |
| **`maxlength`** | Sets the maximum number of characters a user can type into a text input. |
| **`spellcheck`** | Enables/disables spell-checking on a text input. |
| **`checked`** | Boolean attribute. Pre-selects a checkbox or radio button when the page loads. |
| **`autofocus`** | Automatically moves keyboard focus to this control when the page loads. Only one per page. |
| **`form`** | Associates a control with a specific `<form>` by its `id`. Allows the control to live outside `<form>` tags. |
| **`accept`** | On `type="file"`. Restricts which file types appear in the picker (e.g., `image/*`, `.pdf`). |
| **`multiple`** | On `type="file"`. Allows the user to select more than one file. |
| **Checkable item** | A form control whose state changes by clicking: checkboxes and radio buttons. |
| **Void element** | Element with no content and no closing tag. `<input>` is void — label text goes in `value`, not between tags. |
| **`:default` pseudo-class** | Matches form controls that were checked/selected at page load (via `checked` attribute). |
| **`:checked` pseudo-class** | Matches form controls that are currently checked/selected. |
| **Hot map** | A use case for `type="image"` — submitting click coordinates to identify a location on an image. |
| **`name=on` default** | What a checked checkbox submits when no `value` attribute is set: `name=on`. |

---

## Watch Out For...

1. **Unchecked checkboxes and unselected radio buttons send NOTHING.** Not `name=false`, not `name=off` — absolutely nothing. The absence of the key is how the server knows it wasn't checked. Server-side code must handle missing keys gracefully.

2. **`readonly` submits; `disabled` does not.** This is a favourite exam trick. A `readonly` field sends its value to the server. A `disabled` field is completely excluded from submission, as though it doesn't exist.

3. **Radio buttons only work as a mutually exclusive group when they share the same `name`.**  If you accidentally give two radio buttons different `name` values, they become two independent toggles — both can be "selected" simultaneously. The `name` is the group identifier.

4. **If no radio button in a group is checked, no value is sent at all.** The entire group produces no output. This is an "unknown/unselected" state — plan for it server-side. Always add `checked` to a sensible default to prevent this.

5. **`type="password"` is purely visual security.** It hides characters on screen but does NOT encrypt the transmission. The password travels as plain text over HTTP. Use HTTPS. Always.

6. **`type="hidden"` inputs must still have `name` and `value`.** They won't appear on screen, but they need a `name` to be submitted and `value` for that name to mean anything. They should not have a `<label>`.

7. **`type="image"` submits coordinates, not a value.** If you use an image button and expect its `value` attribute to be sent, you'll get nothing — only `name.x` and `name.y` are submitted.

8. **`<button>` inside `<form>` defaults to `type="submit"`.** Even without an explicit `type`. If you want a non-submitting button inside a form (for JS), you MUST write `type="button"`.

9. **`<input type="reset">` clears ALL fields instantly and irreversibly.**  There is no undo. Avoid it on any form where data entry takes effort. Users who accidentally click it lose all their work.

10. **`placeholder` is NOT a default value.** It's hint text — it disappears when the user types and is never submitted. Do not use placeholder as a substitute for a proper `<label>`.

11. **`type="file"` uploads require special form encoding.** To actually send files to a server you need `<form method="post" enctype="multipart/form-data">`. Without this, only the filename (not the file content) may be sent.

12. **`autofocus` should be used on at most one element per page.** Multiple `autofocus` attributes produce unpredictable behaviour. Reserve it for the primary action on the page (e.g., the main search bar).

13. **`size` and `maxlength` are independent.** `size` controls how wide the box looks (visual). `maxlength` controls how many characters the user can type (functional). You can have a narrow box that accepts many characters, or a wide box that only accepts a few.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking back at the guide.

---

**Q1.** What are the ten `<input>` types covered in this article? Group them into three categories: text inputs, checkable inputs, and button inputs.

**Q2.** What is the critical difference between `readonly` and `disabled` in terms of form submission? Write a code example showing one of each, and describe exactly what gets sent to the server for each.

**Q3.** Explain radio button grouping. What makes multiple radio buttons into a mutually exclusive group? What happens if none are selected when the form is submitted?

**Q4.** A developer adds a checkbox like this:
```html
<input type="checkbox" name="newsletter" checked />
```
The checkbox is checked when the user submits. What is submitted to the server? If the user unchecks it before submitting, what is submitted?

**Q5.** Compare `<input type="submit">` to `<button type="submit">`. What is the key reason `<button>` is preferred? Demonstrate with a code example showing something `<button>` can do that `<input>` cannot.

---

## Answer Key

---

**A1.** The ten `<input>` types, grouped:

**Text inputs (single-line):**
- `text` — basic single-line, any text, default type
- `password` — masked single-line text field
- `hidden` — invisible, still submitted, for metadata

**Checkable inputs:**
- `checkbox` — independent toggle (on/off)
- `radio` — mutually exclusive (one-of-group)

**Button inputs:**
- `submit` — submits form
- `reset` — resets all fields (avoid)
- `button` — no action, JS-powered
- `image` — image that submits (sends coordinates)
- `file` — opens OS file picker

---

**A2.**

```html
<form action="/submit" method="get">
  <!-- readonly: user sees and can read, but can't edit -->
  <input type="text" name="ro_field" value="Visible and sent" readonly />

  <!-- disabled: grayed out, can't interact, NOT submitted -->
  <input type="text" name="dis_field" value="Grayed out, not sent" disabled />

  <button type="submit">Submit</button>
</form>
```

**After click — URL produced:**
```
/submit?ro_field=Visible+and+sent
```

`dis_field` is completely absent from the URL — `disabled` controls are excluded from form submission entirely. `readonly` controls ARE submitted. This is the key difference: `readonly` = visible but locked, still sends data. `disabled` = grayed out, does not send data.

---

**A3.**

Radio buttons form a mutually exclusive group when they **all share the same `name` attribute**:

```html
<input type="radio" name="colour" value="red" />
<input type="radio" name="colour" value="blue" checked />
<input type="radio" name="colour" value="green" />
```

- The browser treats all `name="colour"` radios as one group.
- Selecting one **automatically unchecks** all others.
- Only the selected one contributes to submission: `colour=blue`

**If none are selected:** The group produces **no output** — no key, no value. The server receives nothing for that field. Once a radio in a group is selected, the user cannot deselect all of them without resetting the form. Always include a `checked` default to prevent the no-selection state.

---

**A4.**

```html
<input type="checkbox" name="newsletter" checked />
```

- **User submits with the checkbox checked:** `newsletter=on`
  - No `value` attribute is set, so the default submitted value is `on`.
- **User unchecks and submits:** Nothing — the key `newsletter` is completely absent from the submitted data.

There is no `newsletter=off`. The server must infer "not subscribed" from the absence of the `newsletter` key.

---

**A5.**

The key advantage of `<button>` over `<input type="submit">` is that `<button>` can contain **full HTML content** — because it has opening and closing tags. `<input>` is a void element, so its label can only be plain text via the `value` attribute.

```html
<!-- <input type="submit"> — plain text label ONLY -->
<input type="submit" value="Send Message" />

<!-- <button type="submit"> — HTML content inside! -->
<button type="submit">
  <img src="send-icon.svg" alt="" /> <strong>Send</strong> Message
</button>
```

The `<button>` version can include icons, styled text, images, or any inline HTML. The `<input>` version is limited to unformatted text in `value`. Both produce identical functional behaviour — it's purely the label flexibility that differs.
