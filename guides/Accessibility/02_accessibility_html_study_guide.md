# 📚 HTML: A Good Basis for Accessibility — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML

---

## Executive Summary

This article demonstrates how using correct, semantic HTML elements is the single most impactful step toward making web content accessible. The central mechanism is **POSH (Plain Old Semantic HTML)**: browsers provide keyboard accessibility, screen reader semantics, and focus management *for free* when native elements are used correctly, but all of this must be manually reconstructed when non-semantic alternatives like `<div>` are used instead. The critical exam takeaway is that semantic HTML, proper `alt` text, accessible table headers, meaningful link text, and programmatic label associations are the non-negotiable foundations of accessible HTML — and that getting them wrong makes content inaccessible even to users who rely entirely on built-in assistive technology.

---

## Core Pillars

### 1. The Case for Semantic HTML (POSH)

**POSH = Plain Old Semantic HTML** — using native HTML elements for their intended purpose.

**Why it matters for accessibility:**
- Browsers have built-in accessibility hooks wired to native elements.
- A `<button>` is automatically keyboard-focusable via `Tab`, activatable via `Space`/`Enter`/`Return`, and announced as "button" by screen readers.
- A `<div>` mimicking a button loses all of this — and requires keyboard event handlers, `tabindex`, and `role="button"` to partially reconstruct it.

**Secondary benefits of semantic HTML:**
1. **Easier development** — built-in behaviour reduces custom code.
2. **Better mobile** — lighter file size, easier to make responsive.
3. **Better SEO** — search engines weight keywords in headings and links more heavily than in `<div>` content.

**The rule:** Always use the right element for the right job. Replace bad markup wherever possible in both static and dynamically-generated HTML.

---

### 2. Well-Structured Text Content

A screen reader user's primary navigation tool is the **document's heading structure**.

**Good semantic example:**
```html
<h1>My heading</h1>
<p>This is the first section of my document.</p>
<ol>
  <li>Here is</li>
  <li>a list for</li>
  <li>you to read</li>
</ol>
<h2>My subheading</h2>
<p>This is the first subsection of my document.</p>
```

**What screen readers can do with proper heading structure:**
- Announce each element type as it is encountered (heading, paragraph, list item, etc.).
- Allow the user to jump to the next/previous heading.
- Generate a **table of contents** from all headings on the page.

**Bad pattern to avoid:**
```html
<!-- Visually looks like a heading, but has no semantic value -->
<span style="font-size: 3em">My heading</span><br /><br />
This is the first section of my document.
```

With the bad version, a screen reader has no structural signposts — the entire page is read as one giant block.

**Side effect:** Non-semantic markup is also harder to style with CSS and manipulate with JavaScript (no meaningful selectors).

---

### 3. Clear Language

Language choices directly affect accessibility for screen readers and cognitive accessibility alike.

| Problem | Solution |
|---|---|
| Dashes in ranges: `5–7` | Write out: `5 to 7` |
| Abbreviations: `Jan` | Expand: `January` |
| Acronyms: `WHO` | Expand at first use, then use `<abbr>` |

```html
<!-- Correct use of <abbr> -->
<abbr title="World Health Organization">WHO</abbr>
```

Clear language benefits: users with cognitive disabilities, non-native speakers, younger readers, and AI/SR parsing systems.

---

### 4. Logical Page Section Structure

Use HTML5 **sectioning elements** to give screen readers and AT users structural landmarks:

```html
<header>
  <h1>Header</h1>
</header>
<nav>
  <!-- main navigation -->
</nav>
<main>
  <article>
    <h2>Article heading</h2>
    <!-- article content -->
  </article>
  <aside>
    <h2>Related</h2>
    <!-- sidebar content -->
  </aside>
</main>
<footer>
  <!-- footer content -->
</footer>
```

**Key principle:** Content must make logical sense in **source order**, independent of CSS layout. Screen readers consume source order, not visual order.

**Landmark elements and their roles:**

| Element | Landmark Role |
|---|---|
| `<header>` | `banner` |
| `<nav>` | `navigation` |
| `<main>` | `main` |
| `<aside>` | `complementary` |
| `<footer>` | `contentinfo` |
| `<article>` | `article` |

---

### 5. Semantic UI Controls

Native UI controls (`<button>`, `<a>`, `<input>`, `<select>`) provide **keyboard accessibility for free**:

| Key | Native behaviour |
|---|---|
| `Tab` | Moves focus between interactive elements |
| `Enter` / `Return` | Follows a focused link; activates a focused button |
| `Space` | Activates a focused button |
| `↑` / `↓` arrows | Cycles `<select>` options |

**Anti-pattern — fake buttons using `<div>`:**
```html
<!-- ❌ No keyboard access, no AT role -->
<div data-message="First button">Click me!</div>
```

**Correct pattern:**
```html
<!-- ✅ Full keyboard and AT support out of the box -->
<button data-message="First button">Click me!</button>
```

**If a non-button element must be used** (rare), the full minimum reconstruction is:
```html
<div
  data-message="First button"
  tabindex="0"
  role="button"
  onclick="handleAction()"
  onkeydown="if(event.key==='Enter'||event.key===' ') handleAction()">
  Click me!
</div>
```

Plus JavaScript to handle `Enter`/`Return` key activation:
```js
document.onkeydown = (e) => {
  if (e.key === "Enter") {
    document.activeElement.click(); // activates the focused element
  }
};
```

---

### 6. `tabindex` Behaviour

| Value | Behaviour |
|---|---|
| `tabindex="0"` | Inserts element into the **natural tab order** (source order). Most useful for making non-focusable elements focusable. |
| `tabindex="-1"` | Element can receive focus **programmatically** (via JS or as a link target) but is **not in the tab order**. |
| `tabindex="1+"` | Creates a **custom tab order** — almost always a bad idea. Causes confusion and should be avoided. |

---

### 7. Meaningful Text Labels

Screen reader users commonly pull up a **list of all buttons and links** on a page — labels must make sense **out of context**.

**Bad link text:**
```html
<p>To find out more about whales, <a href="whales.html">click here</a>.</p>
```

**Good link text:**
```html
<p>Whales are really awesome creatures. <a href="whales.html">Find out more about whales</a>.</p>
```

**Form labels — bad (unlabelled input):**
```html
Fill in your name: <input type="text" id="name" name="name" />
<!-- Screen reader: "edit text" — no clue what to fill in -->
```

**Form labels — good (programmatically associated):**
```html
<div>
  <label for="name">Fill in your name:</label>
  <input type="text" id="name" name="name" />
</div>
<!-- Screen reader: "Fill in your name: edit text" -->
```

The `for` attribute on `<label>` must match the `id` of the input. This also gives the input a larger hit area — clicking the label activates the input.

---

### 8. Accessible Data Tables

A bare table with only `<td>` cells is inaccessible — screen readers cannot associate data cells with their row/column groupings.

**Inaccessible table:**
```html
<table>
  <tr><td>Name</td><td>Age</td><td>Pronouns</td></tr>
  <tr><td>Gabriel</td><td>13</td><td>he/him</td></tr>
</table>
```

**Accessible table pattern:**
```html
<table>
  <caption>Class roster</caption>
  <tr>
    <th scope="col">Name</th>
    <th scope="col">Age</th>
    <th scope="col">Pronouns</th>
  </tr>
  <tr>
    <td>Gabriel</td>
    <td>13</td>
    <td>he/him</td>
  </tr>
</table>
```

**Key elements and attributes:**

| Element/Attribute | Purpose |
|---|---|
| `<th>` | Marks a cell as a header (row or column) |
| `scope="col"` | Declares the `<th>` is a column header |
| `scope="row"` | Declares the `<th>` is a row header |
| `<caption>` | Provides an accessible summary of the table — preferred over `summary` attribute |
| `summary` attribute | Deprecated alternative to `<caption>`; screen-reader only (sighted users can't see it) |

Screen readers use `<th scope>` to announce data cells in context: *"Gabriel, Name column, Age column: 13"*.

---

### 9. Text Alternatives for Images

**Four methods for providing image descriptions:**

```html
<!-- 1. No alt — BAD: screen reader reads the filename -->
<img src="dinosaur.png" />

<!-- 2. Descriptive alt — GOOD: full description in alt attribute -->
<img src="dinosaur.png"
     alt="A red Tyrannosaurus Rex: A two legged dinosaur standing upright like a human,
          with small arms, and a large head with lots of sharp teeth." />

<!-- 3. alt + title — title shown as tooltip on hover; read by some SRs -->
<img src="dinosaur.png"
     alt="A red Tyrannosaurus Rex…"
     title="The Mozilla red dinosaur" />

<!-- 4. aria-labelledby — reuses visible text as the image label (useful for multiple images sharing a description) -->
<img src="dinosaur.png" aria-labelledby="dino-label" />
<p id="dino-label">The Mozilla red Tyrannosaurus Rex: A two legged dinosaur…</p>
```

**Rules for writing `alt` text:**
- Must convey all information the image conveys visually that is **relevant in context**.
- Must not duplicate surrounding text.
- Must be **brief and concise** — include only what matters in context.
- For decorative images: use `alt=""` (empty string) — do NOT omit the attribute.

**Why `alt=""` and not omitting `alt`:** Omitting `alt` entirely causes some screen readers to announce the full image filename, which is disruptive.

**Alternative for decorative images:**
```html
<img src="decorative-icon.png" alt="" />
<!-- or -->
<img src="decorative-icon.png" role="presentation" />
<!-- Best: use CSS background-image for purely decorative images -->
```

---

### 10. `<figure>` and `<figcaption>`

Associate a visual element with a visible caption:

```html
<figure>
  <img src="dinosaur.png"
       alt="The Mozilla Tyrannosaurus"
       aria-describedby="dinodescr" />
  <figcaption id="dinodescr">
    A red Tyrannosaurus Rex: A two legged dinosaur standing upright like a human,
    with small arms, and a large head with lots of sharp teeth.
  </figcaption>
</figure>
```

- `<figure>` groups the image and its caption semantically.
- `aria-describedby` links the image to its description element via `id`.
- The caption is visible to sighted users — unlike `alt` text, which is invisible.
- Mixed SR support for implicit `<figure>`/`<figcaption>` association; explicit `aria-describedby` is more reliable.

---

### 11. Link Accessibility

**Default accessible link styling (do not remove):**
- Unvisited: blue + underlined
- Visited: purple + underlined
- Keyboard focused: focus ring visible

**Colour contrast requirements:**
- Link text vs background: **4.5:1 minimum**
- Link text vs surrounding non-link text: **3:1 minimum** (across default, visited, and focused states)

**The `onclick` anti-pattern:**
```html
<!-- ❌ Using anchor as a pseudo-button -->
<a href="#" onclick="doSomething()">Click me</a>
<a href="javascript:void(0)" onclick="doSomething()">Click me</a>
```

These break: copy/drag, new tab opening, bookmarking, and JS-disabled operation. Use `<button>` for actions; use `<a href>` only for navigation.

**External links and file downloads — disclose the behaviour:**
```html
<!-- Warn users of new tab/window -->
<a target="_blank" href="https://www.wikipedia.org/">
  Wikipedia (opens in a new window)
</a>

<!-- Warn users of non-HTML resource -->
<a href="2017-annual-report.ppt">
  2017 Annual Report (PowerPoint)
</a>
```

**Skip links (skipnav):**

```html
<!-- Placed as the very first child of <body> -->
<a href="#main-content">Skip to main content</a>
...
<main id="main-content">...</main>
```

- Allows keyboard/AT users to bypass repetitive navigation on every page.
- Critical for users with switch control, voice command, mouth sticks, or head wands.
- Required by WCAG 2.4.1 (Bypass Blocks).

**Proximity — interactive element spacing:**
- Dense clusters of links/buttons are problematic for users with fine motor impairments.
- Use CSS `margin` to ensure adequate spacing between interactive targets.

---

## Technical Deep-Dive

### Logic Walkthrough: Semantic vs Non-Semantic UI Controls

**The scenario:** Developer needs a clickable button that triggers an action.

---

**Option A — Semantic (correct):**
```html
<button onclick="submitForm()">Submit</button>
```

| Feature | Provided automatically |
|---|---|
| Keyboard focus via `Tab` | ✅ Yes |
| Activation via `Enter` | ✅ Yes |
| Activation via `Space` | ✅ Yes |
| AT role announcement | ✅ "Submit, button" |
| Default hover/focus styling | ✅ Yes |
| Works with `document.activeElement.click()` | ✅ Yes |

---

**Option B — Non-semantic (incorrect):**
```html
<div onclick="submitForm()">Submit</div>
```

| Feature | Available? |
|---|---|
| Keyboard focus via `Tab` | ❌ No — must add `tabindex="0"` |
| Activation via `Enter` | ❌ No — must add `onkeydown` handler |
| Activation via `Space` | ❌ No — must add `onkeydown` handler |
| AT role announcement | ❌ No — must add `role="button"` |
| Default styling | ❌ No |

**Reconstructed version (partial fix only):**
```html
<div
  tabindex="0"
  role="button"
  onclick="submitForm()"
  onkeydown="if(event.key==='Enter'||event.key===' ') submitForm()">
  Submit
</div>
```

Still missing: default accessible focus styling, proper disabled state handling, form submission integration, `<button type="submit">` semantics.

**Conclusion:** The native `<button>` does all this for free. The custom `<div>` requires extensive manual work and is prone to gaps.

---

### Logic Walkthrough: `alt` Text Decision Tree

**Scenario:** Developer must decide what `alt` text to write for various image contexts.

```
Is the image purely decorative?
  └─ YES → alt="" (or role="presentation", or CSS background-image)
  └─ NO →
      Does surrounding text already describe the image fully?
        └─ YES → alt="" (avoid duplication)
        └─ NO →
            Is the image shared across multiple pages/contexts?
              └─ YES → Use aria-labelledby pointing to a visible <p>
                        (one description reused by many images)
              └─ NO →
                  Write descriptive alt text that:
                  - Conveys all visually relevant information
                  - Reflects the context (avatar vs adoption page)
                  - Does not repeat surrounding text
                  - Is concise — not exhaustive
```

**Example — context-dependent alt:**
```html
<!-- Context: product thumbnail in a shop listing -->
<img src="jacket.jpg" alt="Blue denim jacket" />

<!-- Context: main image on the product detail page (colour, size, material all matter now) -->
<img src="jacket.jpg" alt="Blue denim jacket, slim fit, size M, 100% cotton, two front pockets" />
```

---

### Logic Walkthrough: Accessible Form Labels

**Step-by-step breakdown of how `<label for>` works:**

```html
<div>
  <label for="email">Email address</label>   <!-- Step 1: for="email" -->
  <input type="email" id="email"             <!-- Step 2: id="email" matches -->
         name="email" />
</div>
```

1. Browser finds `<label for="email">`.
2. Browser finds the element whose `id` matches — `<input id="email">`.
3. Browser **programmatically associates** them: the label becomes the input's accessible name.
4. Screen reader announces: *"Email address, edit text"* — not just *"edit text"*.
5. **Bonus:** Clicking the `<label>` text focuses the associated input (larger interactive hit area).

**What happens without `<label for>`:**
```html
Email address: <input type="text" id="email" name="email" />
<!-- Screen reader: "edit text" — no label context at all -->
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **POSH** | Plain Old Semantic HTML — the practice of using native HTML elements for their intended purpose to leverage built-in accessibility, SEO, and style benefits. |
| **`<button>`** | Native HTML interactive element that provides built-in keyboard focus (`Tab`), activation (`Enter`/`Space`), screen reader role (`button`), and click handling — all without additional scripting. |
| **`tabindex="0"`** | HTML attribute value that inserts a non-focusable element into the document's natural tab order, making it keyboard-accessible. |
| **`tabindex="-1"`** | HTML attribute value that allows an element to receive focus programmatically (via JS or anchor target) without being reachable via keyboard `Tab` navigation. |
| **`role="button"`** | WAI-ARIA attribute added to non-button elements to declare their semantic role as a button in the accessibility tree, enabling screen readers to announce them correctly. |
| **`<label for="id">`** | HTML element that creates a programmatic association between a text label and a form control via matching `for`/`id` values, providing an accessible name to the control. |
| **`alt` attribute** | Required attribute on `<img>` that provides a text alternative read by screen readers; must be set to `""` (empty) for decorative images, never omitted entirely. |
| **`aria-labelledby`** | WAI-ARIA attribute that sets an element's accessible name by referencing the `id` of another visible element — useful for sharing one description across multiple images. |
| **`aria-describedby`** | WAI-ARIA attribute that provides an extended description of an element by referencing the `id` of a description element (typically used alongside a shorter `alt` or label). |
| **`<th>`** | HTML table header cell element, semantically distinct from `<td>`; tells screen readers which cells are headers and allows them to announce data cells in their row/column context. |
| **`scope` attribute** | Attribute on `<th>` specifying whether the header applies to a `col` (column), `row`, `colgroup`, or `rowgroup` — required for accessible table navigation. |
| **`<caption>`** | HTML element that provides a visible title/summary for a `<table>`, read by screen readers as an accessible description of the table. Preferred over the deprecated `summary` attribute. |
| **`<figure>` / `<figcaption>`** | HTML elements that semantically associate a visual element (image, diagram, code) with a visible caption; `<figcaption>` provides the accessible description to sighted and AT users alike. |
| **Skip link (skipnav)** | An `<a>` element placed immediately after `<body>` that links to `#main-content`, enabling keyboard/AT users to bypass repetitive header navigation on every page load. |
| **Source order** | The sequential order of HTML elements as written in the document — the order in which screen readers consume and read content, independent of visual CSS positioning. |
| **`<abbr>` element** | HTML element used to mark up abbreviations and acronyms; the `title` attribute provides the full expansion, which screen readers can read aloud. |
| **`<nav>` / `<main>` / `<aside>`** | HTML5 sectioning elements that map to ARIA landmark roles (`navigation`, `main`, `complementary`), giving AT users structural jump points through the page. |
| **Focus ring** | The browser's default visual indicator (typically an outline) that shows which element currently has keyboard focus; removing it via CSS (`outline: none`) without a replacement harms keyboard accessibility. |
| **`target="_blank"`** | `<a>` attribute that opens a link in a new tab/window; must be disclosed in link text so AT users are not surprised by the context change. |
| **`role="presentation"`** | WAI-ARIA role that instructs screen readers to ignore an element's implicit semantics — used on decorative images as an alternative to `alt=""`. |

---

## Watch Out For...

1. **Omitting the `alt` attribute entirely** — MDN explicitly states that omitting `alt` causes many screen readers to announce the full image filename (e.g., `/dinosaur.png, image`), which is often meaningless or disruptive. Always include `alt` — use `alt=""` for decorative images, not no attribute at all.

2. **Using `<a href="#">` or `<a href="javascript:void(0)">` as buttons** — These break copy/drag, new-tab behaviour, bookmarking, and fail when JavaScript is unavailable. They also convey incorrect semantics to ATs. Use `<button>` for actions, `<a href="real-url">` for navigation.

3. **Setting positive `tabindex` values (e.g., `tabindex="2"`)** — Positive `tabindex` creates a custom tab order that overrides natural source order, almost always causing confusing and unpredictable navigation. Use `tabindex="0"` or `tabindex="-1"` only.

4. **Removing the focus ring with `outline: none` in CSS without a replacement** — The focus ring is the primary visual indicator for keyboard navigation. Removing it without adding a custom `:focus` style leaves keyboard users with no indication of where focus is.

5. **Writing generic link text like "click here" or "read more"** — Screen readers present a list of all links on a page; "click here" repeated 10 times is meaningless out of context. Link text must describe the destination or action when read in isolation.

6. **Forgetting that `<label for>` must match the input's `id`, not `name`** — The `for` attribute pairs with `id`, not `name`. Mismatching these breaks the programmatic association and destroys the accessible label.

7. **Assuming `<figcaption>` alone is sufficient to create the AT association** — Screen reader support for the implicit `<figure>`/`<figcaption>` association is inconsistent across AT/browser combinations. Always explicitly add `aria-labelledby` or `aria-describedby` to bridge the gap.

8. **Including text inside images** — MDN explicitly warns against this: "you should never include text content inside an image — screen readers can't access it." Also: it can't be selected, copied, or translated.

9. **Overriding link colours without checking contrast ratios** — Links must maintain **4.5:1** contrast against the background and **3:1** against surrounding non-link text across all states (default, visited, focus/active). Restyling links for aesthetic reasons without checking these ratios is a WCAG Perceivable violation.

10. **Using non-semantic tags for structure instead of heading hierarchy** — Using `<span style="font-size:3em">` instead of `<h1>` destroys screen reader navigation. The visual appearance is irrelevant; the semantic element is what exposes structure to ATs and enables heading-jump navigation.

11. **Not warning users when a link opens a new tab** — `target="_blank"` changes context unexpectedly for AT users, particularly those who cannot easily navigate back. The link text must disclose this: *(opens in a new window)*.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are three concrete advantages of using semantic HTML (`<button>`, `<h1>`, `<nav>`) over non-semantic equivalents (`<div>`, `<span>`) — beyond just accessibility?

**Q2.** A developer has written the following form input. Identify the accessibility problem and rewrite it correctly:
```html
Enter your email: <input type="email" id="user-email" name="email" />
```

**Q3.** What is the difference between `tabindex="0"` and `tabindex="-1"`? In what scenario would you use each?

**Q4.** A page has this image in a `<h3>` heading: `<img src="icon.png" />`. What accessibility problem does this cause and how should it be fixed?

**Q5.** A `<table>` displays quarterly sales data with both row and column headers. Describe the complete set of HTML elements and attributes required to make this table fully accessible to screen reader users.

---

## Answer Key

---

**A1.** Three advantages of semantic HTML beyond accessibility:
1. **SEO** — Search engines weight keywords inside semantic elements (`<h1>`, `<a>`, `<nav>`) more heavily than the same content inside generic `<div>` containers. Using correct heading hierarchy and link text directly improves search discoverability.
2. **Ease of development** — Native elements provide built-in functionality (keyboard events, form submission, focus management) that reduces custom JavaScript. The codebase is also more readable because element names reflect their purpose.
3. **Mobile performance** — Semantic HTML produces leaner markup than non-semantic "spaghetti" equivalents (fewer nested `<div>`s, less inline styling), resulting in smaller file sizes and easier responsive layout adaptation.

---

**A2.** The problem: the label text (`"Enter your email:"`) is placed as a bare text node adjacent to the input — it has no programmatic association with the input. A screen reader will only announce *"edit text"* with no clue about what to enter.

**Fixed version:**
```html
<div>
  <label for="user-email">Enter your email:</label>
  <input type="email" id="user-email" name="email" />
</div>
```

The `<label for="user-email">` matches the input's `id="user-email"`, creating a programmatic association. Screen readers now announce: *"Enter your email: edit text"*. As a bonus, clicking the label text focuses the input, increasing the interactive hit area.

---

**A3.**
- **`tabindex="0"`** — Inserts the element into the **natural tab order** (where it falls in source order). Used to make normally non-focusable elements (like `<div>`, `<span>`) keyboard-accessible by `Tab`. Most commonly used when building a custom interactive component from a non-interactive element.
- **`tabindex="-1"`** — The element does **not** appear in the tab order and cannot be reached via keyboard `Tab`. However, it can receive focus **programmatically** via JavaScript's `.focus()` method, or as the target of an anchor link (e.g., skip links where the `<main>` receives programmatic focus). Used for managing focus in modals, dialogs, or after user actions redirect attention to a specific element.

---

**A4.** The problem: no `alt` attribute is present on the image. When a screen reader encounters `<img>` without `alt`, it falls back to announcing the filename: `"icon.png, image"` — which is disruptive, meaningless, and pollutes the heading's content when read aloud.

Because the image is **decorative** (a visual icon that accompanies the heading text which already describes the content), the correct fix is an **empty `alt` attribute**:

```html
<h3>
  <img src="icon.png" alt="" />
  Tyrannosaurus Rex: the king of the dinosaurs
</h3>
```

`alt=""` tells screen readers to skip the image entirely. The heading text provides all the meaning; the icon is purely visual reinforcement. An alternative is `role="presentation"` on the `<img>`, or using a CSS background image instead.

---

**A5.** A fully accessible quarterly sales table requires:

```html
<table>
  <!-- caption provides an accessible summary of the whole table -->
  <caption>Quarterly sales figures by region, 2024</caption>
  <thead>
    <tr>
      <!-- scope="col" declares each <th> as a column header -->
      <th scope="col">Region</th>
      <th scope="col">Q1</th>
      <th scope="col">Q2</th>
      <th scope="col">Q3</th>
      <th scope="col">Q4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <!-- scope="row" declares this <th> as a row header -->
      <th scope="row">North</th>
      <td>$12,000</td>
      <td>$14,500</td>
      <td>$13,200</td>
      <td>$16,100</td>
    </tr>
    <tr>
      <th scope="row">South</th>
      <td>$9,800</td>
      <td>$11,300</td>
      <td>$10,500</td>
      <td>$12,700</td>
    </tr>
  </tbody>
</table>
```

**Required components and their roles:**
- `<caption>` — visible accessible summary; preferred over the deprecated `summary` attribute.
- `<th scope="col">` — marks each column header and scopes it to its column, allowing AT to announce: *"Q1, North: $12,000"*.
- `<th scope="row">` — marks each row's identifying header cell (the region name), scoping it to its row.
- `<thead>` / `<tbody>` — group rows semantically; while not strictly required for AT, they are best practice for both accessibility and CSS styling.
- All data cells use `<td>` — not `<th>`, since they are data, not headers.
