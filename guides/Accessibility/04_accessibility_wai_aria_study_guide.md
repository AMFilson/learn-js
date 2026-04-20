# 📚 WAI-ARIA Basics — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics

---

## Executive Summary

WAI-ARIA (Web Accessibility Initiative – Accessible Rich Internet Applications) is a W3C specification that fills the gaps left by HTML semantics: specifically, it addresses complex dynamic UIs, custom widget patterns, and live content regions that no native HTML element can adequately describe. The exam-critical principle is **"use WAI-ARIA only when necessary"** — semantic HTML always comes first. When ARIA is warranted, it operates through three constructs: **roles** (what an element *is*), **properties** (what an element *means*), and **states** (what an element's *current condition* is). ARIA attributes have zero visual or DOM effect — they exclusively communicate through the browser's **accessibility API** to assistive technologies.

---

## Core Pillars

### 1. What is WAI-ARIA — and Why Does it Exist?

**The problem ARIA was created to solve:**

Modern web apps broke accessibility in two ways:

1. **Non-semantic structural markup:** Before `<nav>`, `<main>`, `<aside>` etc., developers used `<div class="nav">` — which gave screen readers no structural signposts to navigate by.

2. **Dynamic content:** Screen readers read page content at load time. JavaScript-driven updates (e.g., live search results, chat messages, stock tickers) happen *after* initial load — screen readers have no native mechanism to detect or announce DOM changes.

WAI-ARIA's solution: a set of **additional HTML attributes** (`role`, `aria-*`) that communicate extra semantics to the browser's accessibility API, which in turn surfaces them to screen readers and other AT. These attributes **do not affect DOM, layout, or visual appearance** — they exist solely in the accessibility layer.

---

### 2. The Three Constructors of WAI-ARIA

| ARIA Concept | What it communicates | Example |
|---|---|---|
| **Role** | What an element *is* or *does* | `role="button"`, `role="tablist"`, `role="alert"` |
| **Property** | Fixed extra meaning of an element | `aria-required="true"`, `aria-labelledby="id"`, `aria-describedby="id"` |
| **State** | Current, *changeable* condition of an element | `aria-disabled="true"`, `aria-expanded="false"`, `aria-checked="true"` |

**Key distinction — Properties vs. States:**
- **Properties** don't change during the app's lifecycle (e.g., `aria-required="true"` — a field is either required or it's not).
- **States** change programmatically via JavaScript (e.g., `aria-disabled` starts `true` then flips to `false` when a checkbox is ticked).

---

### 3. The Golden Rule: Use ARIA Only When Necessary

> **"Using the correct HTML elements implicitly gives you the roles that are needed."**

ARIA is a last resort, not a first instinct. The decision hierarchy is:

```
Can I use a native HTML element that already provides the semantics?
  └─ YES → Use the HTML element. Full stop.
  └─ NO (unavoidable legacy code / complex widget) →
      Use WAI-ARIA to provide the missing semantics.
```

**Why this matters:** Adding `role="navigation"` to a `<div>` gives roughly the same AT information as using `<nav>` directly — but `<nav>` also gives keyboard and layout benefits, is handled by browsers natively, and requires no ARIA workaround. Over-use of ARIA on semantic HTML can corrupt the accessibility tree (e.g., `<button role="button">` is redundant; `<button role="heading">` is actively misleading).

---

### 4. The Four Main Use Cases for WAI-ARIA

The article identifies four concrete situations where ARIA is appropriate:

| Use Case | When to use ARIA | Example |
|---|---|---|
| **Signposts / Landmarks** | When a structural element has no HTML semantic equivalent or an existing element needs an explicit landmark role | `role="search"` on a `<form>` (prior to the `<search>` element); `role="tablist"` / `role="tab"` on custom tab UIs |
| **Dynamic content updates** | When JavaScript updates part of the DOM and screen readers need to announce the change | `aria-live="polite"` on a news ticker; `aria-live="assertive"` on an error message container |
| **Keyboard accessibility** | When non-focusable elements need to be made focusable | `tabindex="0"` on a `<div>` acting as an interactive widget |
| **Accessibility of non-semantic controls** | When a series of `<div>`s + CSS/JS forms a complex UI widget with no native HTML equivalent | `role="tabpanel"`, `role="listbox"`, `role="combobox"`, `aria-required`, `aria-posinset` on custom widgets |

---

### 5. Signposts / Landmarks

HTML5 sectioning elements expose landmark roles to AT automatically. **Semantic HTML first:**

| HTML Element | Implicit ARIA Landmark Role |
|---|---|
| `<header>` (as page header) | `banner` |
| `<nav>` | `navigation` |
| `<main>` | `main` |
| `<aside>` | `complementary` |
| `<footer>` | `contentinfo` |
| `<article>` | `article` |
| `<search>` | `search` |

**When ARIA landmarks are necessary:**
- The page uses `<div>`-based layout (legacy or third-party generated).
- A widget type exists in ARIA but has no HTML equivalent (e.g., `role="tablist"`, `role="tabpanel"`, `role="tab"`).

**Example — search form landmark:**
```html
<!-- Pre-<search> element approach -->
<form role="search">
  <input type="search" aria-label="Search through site content" />
  <button type="submit">Go!</button>
</form>

<!-- Modern preferred approach -->
<search>
  <form>
    <input type="search" name="q" placeholder="Search query"
           aria-label="Search through site content" />
    <input type="submit" value="Go!" />
  </form>
</search>
```

**`aria-label` on inputs without a visible `<label>`:**
```html
<!-- When a visual label would spoil the design (e.g., search bars) -->
<input type="search" aria-label="Search through site content" />
```
This provides an accessible name to the SR without rendering visible text.

---

### 6. Dynamic Content Updates — Live Regions

**The problem:** Screen readers take a snapshot at page load. Content inserted or updated by JavaScript after load (e.g., a quote that changes every 5 seconds) is invisible to screen readers by default.

**The solution: `aria-live`**

Applied to a container element. When content inside that container changes, the SR announces the new content automatically.

```html
<!-- Without ARIA: SR never announces quote changes -->
<blockquote>
  <p></p>
</blockquote>

<!-- With ARIA: SR announces quote changes per the urgency value -->
<blockquote aria-live="assertive">
  <p></p>
</blockquote>
```

**`aria-live` values:**

| Value | Behaviour |
|---|---|
| `off` | **Default.** No announcements — updates are silent. |
| `polite` | SR announces the update **when the user is idle** (finishes reading other content). Use for non-urgent updates (news tickers, search suggestions). |
| `assertive` | SR **immediately interrupts** what it is reading to announce the update. Use only for important, time-critical information (error messages, alerts). |

**Companion live region attributes:**

| Attribute | Purpose |
|---|---|
| `aria-atomic="true"` | When set, SR reads the **entire element** as one unit, not just the changed portion — useful when a heading + content should be read together on each update. |
| `aria-relevant` | Controls *what kinds* of changes trigger announcements. Values: `additions`, `removals`, `text`, `all`. Default is `additions text`. |

**`role="alert"` as a live region shortcut:**
```html
<div class="errors" role="alert" aria-relevant="all">
  <ul></ul>
</div>
```
- `role="alert"` automatically makes the element a live region with `aria-live="assertive"` semantics.
- It also semantically marks the content as an alert (important, time-sensitive information).
- `aria-relevant="all"` ensures the SR announces both additions *and* removals from the list.
- Preferred over `window.alert()` (modal dialogs have numerous accessibility problems).

---

### 7. Enhancing Keyboard Accessibility

**Native elements with built-in keyboard accessibility:** `<button>`, `<a>`, `<input>`, `<select>`, `<textarea>`.

**When non-focusable elements must be interactive**, WAI-ARIA extends `tabindex`:

| Value | Effect |
|---|---|
| `tabindex="0"` | Inserts element into the **natural tab order** (source order). Makes non-focusable elements keyboard-reachable. |
| `tabindex="-1"` | Element can receive focus **programmatically** (via JS `.focus()` or as an anchor target) but is **not** in the tab order. |

---

### 8. Accessibility of Non-Semantic Controls

#### 8a. ARIA Roles for Fake Buttons

A `<div>` used as a button announces itself as `"Click me!, group"` (or similar) — confusing.

```html
<!-- ❌ No semantic role — SR says "Click me!, group" -->
<div data-message="First button" tabindex="0">
  Click me!
</div>

<!-- ✅ role="button" — SR says "Click me!, button" -->
<div data-message="First button" tabindex="0" role="button">
  Click me!
</div>
```

Adding `role="button"` fixes the SR announcement, but you **still must manually add:**
- `Enter`/`Space` key event handlers (to activate on keyboard press).
- Disabled state handling (`aria-disabled`).
- Any other expected button behaviours.

> **Reminder:** If you can use `<button>`, always use `<button>`. ARIA is the fallback.

#### 8b. ARIA for Complex Widgets

Roles for fully custom widgets that have no HTML counterpart:

| ARIA Role | Widget it represents |
|---|---|
| `role="tablist"` | Container for a set of tabs |
| `role="tab"` | Individual clickable tab |
| `role="tabpanel"` | Content panel associated with a tab |
| `role="combobox"` | Combo input (text field + dropdown) |
| `role="slider"` | A range slider input |
| `role="tree"` | Collapsible tree structure |
| `role="listbox"` | A custom select-like list |

---

### 9. ARIA for Form Accessibility

#### 9a. `aria-required`

Visual asterisks (*) are meaningless to screen readers. `aria-required="true"` explicitly communicates required status:

```html
<!-- Visual hint only — SR ignores the asterisk -->
<label for="name">Name *</label>
<input type="text" id="name" name="name" />

<!-- With ARIA: SR reads "Name, required, edit text" -->
<label for="name">Name *</label>
<input type="text" id="name" name="name" aria-required="true" />
```

#### 9b. `placeholder` for value hints

```html
<label for="age">Your age:</label>
<input type="number"
       id="age"
       name="age"
       placeholder="Enter 1 to 150"
       required
       aria-required="true" />
```

`placeholder` provides a visible (and sometimes SR-readable) hint about expected values. However, `placeholder` is not a replacement for `<label>` — always include a `<label for>`.

#### 9c. `aria-disabled`

```html
<input type="text" id="instrument" aria-disabled="true" disabled />
```

- Some browsers skip past `disabled` elements causing them to be skipped by screen readers entirely.
- `aria-disabled="true"` ensures the SR still announces the field and its disabled status.
- Unlike `disabled`, `aria-disabled` does not prevent form submission — use together with the native `disabled` attribute.

#### 9d. Dynamic state changes with a hidden live region

When an element's disabled state changes, announce the change:

```html
<p class="hidden-alert" aria-live="assertive"></p>
```

```js
function toggleMusician(isMusician) {
  const instrument = formItems[formItems.length - 1];
  if (isMusician) {
    instrument.input.disabled = false;
    instrument.input.setAttribute("aria-disabled", "false");
    hiddenAlert.textContent = "Instruments played field now enabled; use it to tell us what you play.";
  } else {
    instrument.input.disabled = true;
    instrument.input.setAttribute("aria-disabled", "true");
    hiddenAlert.textContent = "Instruments played field now disabled.";
  }
}
```

#### 9e. Advanced form labelling methods

| Technique | When to use |
|---|---|
| `<label for="id">` | **Preferred always** — provides click target + accessible name |
| `aria-label="text"` | When a visible label would disrupt the design (e.g., search bars) |
| `aria-labelledby="id"` | When you want a non-`<label>` element (or multiple elements) to serve as the label |
| `aria-describedby="id"` | When you want to associate supplementary information (e.g., format hints) with a form field — read *in addition to* the label |

---

## Technical Deep-Dive

### Logic Walkthrough: The ARIA Attributes → Accessibility API → Screen Reader Pipeline

```
Developer writes HTML attribute: aria-live="polite"
            ↓
Browser parses the attribute and updates its internal Accessibility Tree
(a parallel tree to the DOM, used exclusively for AT communication)
            ↓
Browser exposes the updated Accessibility Tree via the OS Accessibility API:
  - macOS: NSAccessibility
  - Windows: UI Automation (UIA) or IAccessible2
  - Linux: ATK/AT-SPI
            ↓
Screen reader (VoiceOver, NVDA, JAWS, etc.) queries the Accessibility API
at its polling interval (or on change events)
            ↓
Screen reader synthesises speech or Braille output for the user
```

**Key fact:** WAI-ARIA attributes never affect:
- The DOM structure.
- CSS rendering.
- JavaScript execution.
- The page's visual output.

They communicate *exclusively* through the Accessibility API layer. This is why adding `role="button"` to a `<div>` makes a SR say "button" but does NOT make `Enter` or `Space` keys work — keyboard handlers are wired to the DOM/JS layer separately.

---

### Logic Walkthrough: Live Region Urgency Decision

```
Does the content update require immediate user attention?
  └─ NO (background information, non-critical updates):
      aria-live="polite"
      SR waits until the user is idle, then announces.
      Examples: search suggestions, news tickers, auto-save status, progress updates.
  └─ YES (errors, alerts, time-critical state changes):
      aria-live="assertive"  OR  role="alert"
      SR immediately interrupts current speech to announce.
      Examples: form validation errors, session timeout warnings, payment status.
```

**Additional nuances:**
- **`aria-atomic="true"`** — If a live region contains a heading + content block, and only the content changes, the SR might only read the new content snippet. `aria-atomic="true"` forces it to re-read the entire element — ensuring the heading ("Quote of the day:") is always re-read alongside the new quote.
- **`aria-relevant="all"`** — By default, only *additions* to a live region are announced. `aria-relevant="all"` also announces *removals* (e.g., when an error is cleared from an error list).

---

### Logic Walkthrough: Building an Accessible Tab Interface

A tabbed interface is a classic example where ARIA roles are required (no HTML-native equivalent):

```html
<div role="tablist" aria-label="Content sections">
  <button role="tab"
          id="tab-1"
          aria-controls="panel-1"
          aria-selected="true">
    Section 1
  </button>
  <button role="tab"
          id="tab-2"
          aria-controls="panel-2"
          aria-selected="false"
          tabindex="-1">
    Section 2
  </button>
</div>

<div role="tabpanel"
     id="panel-1"
     aria-labelledby="tab-1">
  <p>Content for section 1.</p>
</div>

<div role="tabpanel"
     id="panel-2"
     aria-labelledby="tab-2"
     hidden>
  <p>Content for section 2.</p>
</div>
```

**What each attribute does:**

| Attribute | Element | Purpose |
|---|---|---|
| `role="tablist"` | Container `<div>` | Declares the container as a tab bar — SR announces "Content sections, tab list" |
| `role="tab"` | Each `<button>` | Declares each button as a tab — SR says "Section 1, tab, 1 of 2, selected" |
| `aria-controls="panel-id"` | Tab `<button>` | Associates each tab with its panel — programmatic relationship |
| `aria-selected="true/false"` | Tab `<button>` | Communicates which tab is currently active — SR announces "selected" / "not selected" |
| `role="tabpanel"` | Content `<div>` | Declares the content area as a tab panel |
| `aria-labelledby="tab-id"` | Panel `<div>` | Associates the panel with its tab's text as its accessible name |
| `tabindex="-1"` | Inactive tabs | Removes inactive tabs from tab order; arrow keys manage focus within `tablist` |

**JavaScript responsibility:** The ARIA attributes describe relationships and states, but JS must:
1. Update `aria-selected` on tab click.
2. Move focus between tabs using arrow keys (standard tab widget keyboard pattern).
3. Show/hide panels (`hidden` attribute).

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **WAI-ARIA** | Web Accessibility Initiative – Accessible Rich Internet Applications; a W3C specification defining extra HTML attributes that expose additional semantics to the browser's accessibility API. |
| **Accessibility API** | An OS-level interface (e.g., UIAutomation on Windows, NSAccessibility on macOS) that browsers use to expose the accessibility tree to assistive technologies such as screen readers. |
| **Accessibility Tree** | A parallel tree structure maintained by the browser (derived from the DOM) that represents the semantic meaning of the page's elements as exposed to the accessibility API. |
| **ARIA Role** | A `role` attribute value that defines what an element *is* or *does* (e.g., `role="button"`, `role="tablist"`); communicates element type to screen readers. |
| **ARIA Property** | A fixed characteristic of an element that provides extra meaning (e.g., `aria-required="true"`, `aria-labelledby="id"`); does not change during the app lifecycle. |
| **ARIA State** | A current, potentially changing condition of an element (e.g., `aria-disabled`, `aria-checked`, `aria-expanded`); updated dynamically via JavaScript. |
| **Landmark role** | An ARIA role that designates a major page region navigable via AT (e.g., `banner`, `navigation`, `main`, `complementary`, `search`). |
| **`role="alert"`** | An ARIA role that designates an element as a live region with `assertive` urgency and marks its content as important/time-sensitive; SR announces changes immediately. |
| **`aria-live`** | An ARIA property on a container element that enables live region behaviour; values are `off`, `polite`, and `assertive`. |
| **`aria-live="polite"`** | Live region value that causes the SR to announce content changes only when the user is idle — appropriate for non-urgent updates. |
| **`aria-live="assertive"`** | Live region value that causes the SR to immediately interrupt its current speech to announce content changes — appropriate for errors or critical alerts. |
| **`aria-atomic`** | Live region property; when `true`, instructs the SR to read the entire element as one unit on any change, not just the changed portion. |
| **`aria-relevant`** | Live region property controlling which types of content changes trigger announcements: `additions`, `removals`, `text`, or `all`. |
| **`aria-label`** | Provides an accessible name directly as a string value — for elements without a visible text label (e.g., icon buttons, search inputs). |
| **`aria-labelledby`** | Points to the `id` of another element whose text content serves as this element's accessible name — allows labelling from any visible text on the page; supports multiple labels. |
| **`aria-describedby`** | Points to the `id` of an element containing supplementary description text — read *in addition to* the accessible name, after a brief pause. |
| **`aria-required`** | Communicates to screen readers that a form input must be filled before submission — AT-targeted complement to visual asterisk markers. |
| **`aria-disabled`** | State that communicates to screen readers that a form element is disabled even when the native `disabled` attribute might cause the element to be skipped. |
| **`aria-controls`** | Property that establishes a relationship between a controlling element (e.g., a tab) and the content region it controls (e.g., a tab panel). |
| **`aria-selected`** | State on tab and option elements; communicates which item in a `tablist` or `listbox` is currently selected — updated programmatically. |
| **`role="tablist"`** | ARIA landmark for the container of a set of tab buttons — the SR announces it as a group at browsing focus. |
| **`role="tab"`** | ARIA role for each individual tab button within a `tablist`. |
| **`role="tabpanel"`** | ARIA role for the content panel associated with a tab. |
| **`role="button"`** | ARIA role applied to a non-`<button>` element to declare it as a button to screen readers — does not add keyboard behaviour. |

---

## Watch Out For…

1. **Using ARIA instead of semantic HTML when the HTML equivalent exists** — `role="navigation"` on a `<div>` is a workaround; `<nav>` is the correct solution. Semantic HTML provides keyboard, styling, and AT benefits that ARIA alone cannot match.

2. **Adding ARIA roles that conflict with or override an element's native semantics** — `<button role="heading">` is destructive — it tells screen readers the button is a heading, stripping its interactive button semantics. ARIA overrides native roles completely.

3. **Thinking `role="button"` is sufficient to make a `<div>` fully button-accessible** — `role="button"` fixes the AT announcement but does NOT:
   - Add `Tab` focusability (need `tabindex="0"`).
   - Handle `Enter` / `Space` key activation (need a `keydown` event handler).
   - Handle disabled states, focus management, etc.

4. **Using `aria-live="assertive"` for non-critical updates** — Assertive regions interrupt the SR mid-sentence. Overusing `assertive` is disruptive and degrades the experience for SR users. Use `polite` for everything except genuine alerts and errors.

5. **Forgetting to update ARIA states with JavaScript** — Adding `aria-expanded="false"` to a disclosure button but never flipping it to `true` when the disclosure opens means the SR always reports false information. States *must be kept current* via JS.

6. **Relying on `placeholder` as a label replacement** — `placeholder` disappears on input and is inconsistently announced by screen readers. Always provide a `<label for>`, `aria-label`, or `aria-labelledby` for form controls.

7. **Omitting `aria-required` because the field visually shows an asterisk** — Asterisks are visual conventions. Screen readers do not infer required status from asterisks unless the `aria-required="true"` attribute is also present.

8. **Applying `aria-live` to the wrong element** — The live region must be in the DOM *before* content changes are made to it. Adding `aria-live` dynamically at the same time as inserting content may not trigger announcements in all SR/browser combinations.

9. **Not testing with real screen readers** — The article explicitly warns that computed AT support varies across OS/browser/SR combinations. Browser support for ARIA is near-universal, but SR support is uneven. Always test with at least VoiceOver (macOS/iOS) and NVDA or JAWS (Windows).

10. **Forgetting `aria-label` or `aria-labelledby` on inputs that lack a visible `<label>`** — A search input that visually has no label needs either a visible `<label for>` (preferred) or `aria-label` — `placeholder` alone is insufficient as an accessible name.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the three fundamental building blocks of WAI-ARIA, and what is the key difference between the last two?

**Q2.** A developer adds `aria-live="polite"` to a live region. Explain in precise terms what happens when JavaScript updates the text inside that region, and how it would differ if `aria-live="assertive"` were used instead.

**Q3.** A `<div tabindex="0" role="button">` has been created to act as a button. List everything that `role="button"` provides, everything it does NOT provide, and what additional steps are needed to make the element truly accessible.

**Q4.** A form has a checkbox that, when ticked, enables a previously disabled text input. Describe the complete, accessible pattern for communicating this state change to screen reader users.

**Q5.** Describe the full ARIA attribute pattern needed to implement an accessible two-tab interface, naming every attribute, where it goes, and what it communicates.

---

## Answer Key

---

**A1.** The three building blocks are:

1. **Roles** — Define what an element *is* or *does*. Applied via the `role` attribute. Example: `role="button"` tells the AT this element functions as a button.

2. **Properties** — Extra meaning or characteristics of an element. Example: `aria-required="true"` or `aria-labelledby="id"`. The key characteristic of properties is that they **do not change** during the application's lifecycle — they describe fixed aspects of the element.

3. **States** — The element's current condition. Example: `aria-disabled="true"`, `aria-expanded="false"`. States **differ from properties** in that they are expected to change dynamically — typically updated by JavaScript in response to user interaction or application logic.

---

**A2.**
- **`aria-live="polite"`:** When JS updates the text inside the element, the browser notes the change in the accessibility tree. The screen reader queues the new content to announce, but waits until the user is idle (finishes reading whatever current content they were hearing). If the user is actively navigating or listening, the announcement is deferred. This is appropriate for non-urgent updates (search suggestions, status messages, quote rotators).

- **`aria-live="assertive"`:** When JS updates the text, the screen reader **immediately interrupts** whatever it is currently reading to announce the new content. There is no deferral. This may cause the SR to cut off mid-sentence if the user was listening to something else. Assertive is only appropriate for urgent, time-critical information like form validation errors, security alerts, or session timeout warnings.

---

**A3.**

**What `role="button"` provides:**
- Communicates to screen readers that this element is a button — SR announces `"Click me!, button"` instead of `"Click me!, group"`.
- Updates the element's semantic role in the accessibility tree.

**What `role="button"` does NOT provide:**
- `Tab` focusability — the `<div>` is not focusable without `tabindex="0"`.
- `Enter` key activation — pressing `Enter` on a focused button does not fire `onclick` for non-native-button elements without a `keydown` handler.
- `Space` key activation — same issue.
- Disabled state management (`aria-disabled`).
- Default browser button styling and focus ring.
- Form submission behaviour (`type="submit"`).

**Additional steps required for a fully accessible fake button:**
```html
<div tabindex="0"
     role="button"
     onclick="handleAction()"
     onkeydown="if(event.key==='Enter'||event.key===' ') handleAction()">
  Click me!
</div>
```

1. Add `tabindex="0"` to insert it into the tab order.
2. Add an `onkeydown` handler that activates the button on `Enter` AND `Space` key presses.
3. Add an explicit `:focus` style (the default focus ring may be absent on `<div>` elements).
4. Manage `aria-disabled` state if the button can be disabled.

**Best advice:** Use `<button>` instead.

---

**A4.** The complete accessible pattern:

**HTML:**
```html
<!-- Checkbox that controls the input -->
<input type="checkbox" id="musician-check" name="musician" />
<label for="musician-check">Are you a musician?</label>

<!-- Label and initially disabled input -->
<label for="instrument" style="color: #999999">Instruments played:</label>
<input type="text"
       id="instrument"
       name="instrument"
       disabled
       aria-disabled="true" />

<!-- Hidden live region — positioned off-screen with position:absolute to stay AT-accessible -->
<p class="hidden-alert" aria-live="assertive"></p>
```

**CSS (visually hides the alert but keeps it accessible):**
```css
.hidden-alert {
  position: absolute;
  left: -9999px;
  width: 1px;
  overflow: hidden;
}
```

**JavaScript:**
```js
const checkbox = document.getElementById("musician-check");
const instrument = document.getElementById("instrument");
const label = instrument.previousElementSibling;
const hiddenAlert = document.querySelector(".hidden-alert");

checkbox.addEventListener("change", () => {
  if (checkbox.checked) {
    instrument.disabled = false;
    instrument.setAttribute("aria-disabled", "false");
    label.style.color = "black";
    hiddenAlert.textContent = "Instruments played field now enabled; use it to tell us what you play.";
  } else {
    instrument.disabled = true;
    instrument.setAttribute("aria-disabled", "true");
    label.style.color = "#999999";
    hiddenAlert.textContent = "Instruments played field now disabled.";
  }
});
```

**What each part does:**
- `aria-disabled="true"` — SR announces the field is disabled even if the native `disabled` attribute causes it to be skipped in focus order.
- Updating `aria-disabled` dynamically — keeps the AT state in sync with the visual state.
- `aria-live="assertive"` hidden paragraph — immediately announces the state change to the SR (the user is explicitly interacting, making immediate feedback appropriate).
- Absolute positioning (not `display:none`) — keeps the live region in the accessibility tree so announcements fire reliably.

---

**A5.** Full ARIA pattern for a two-tab accessible interface:

```html
<!-- tablist contains all tabs — aria-label names the group for SRs -->
<div role="tablist" aria-label="Content sections">

  <!-- First tab: active (aria-selected="true"), in tab order (no tabindex=-1) -->
  <button role="tab"
          id="tab-1"
          aria-controls="panel-1"
          aria-selected="true">
    Section 1
  </button>

  <!-- Second tab: inactive (aria-selected="false"), removed from tab order -->
  <button role="tab"
          id="tab-2"
          aria-controls="panel-2"
          aria-selected="false"
          tabindex="-1">
    Section 2
  </button>

</div>

<!-- Panel 1: visible, labelled by its matching tab's text via aria-labelledby -->
<div role="tabpanel"
     id="panel-1"
     aria-labelledby="tab-1">
  <p>Content for section 1.</p>
</div>

<!-- Panel 2: hidden, labelled by tab-2's text -->
<div role="tabpanel"
     id="panel-2"
     aria-labelledby="tab-2"
     hidden>
  <p>Content for section 2.</p>
</div>
```

**Attribute-by-attribute explanation:**

| Attribute | Element | Communication to SR |
|---|---|---|
| `role="tablist"` | Container | "Content sections, tab list — 2 items" |
| `aria-label="Content sections"` | `tablist` | Provides the group's accessible name |
| `role="tab"` | Each `<button>` | "Section 1, tab, 1 of 2, selected" / "Section 2, tab, 2 of 2" |
| `aria-controls="panel-id"` | Tab | Programmatic tab→panel relationship (not always announced, but enables AT navigation) |
| `aria-selected="true/false"` | Tab | Communicates active/inactive status to the SR |
| `tabindex="-1"` | Inactive tabs | Removes from default tab order; arrow keys handle focus within the `tablist` |
| `role="tabpanel"` | Content `<div>` | "Section 1 tab panel" |
| `aria-labelledby="tab-id"` | Panel | Associates panel with its tab's label ("Section 1") |
| `hidden` | Inactive panel | Hides from both visual rendering AND accessibility tree |

**JavaScript must also:**
- Toggle `aria-selected` when tabs are clicked.
- Move focus between tabs using `ArrowLeft`/`ArrowRight` keys (the standard tab widget keyboard interaction pattern).
- Toggle `hidden` on panels to show/hide them.
- Toggle `tabindex="-1"` / `tabindex="0"` across tabs to follow currently selected tab.
