# Customizable Select Listboxes Study Guide

## Executive Summary

Customizable select listboxes extend the customizable select specification to controls that display multiple options simultaneously (rather than as dropdown pickers), enabled by `<select multiple>` or `<select size="N">` where N > 1. Unlike dropdown selects, listboxes eliminate complexity around picker positioning, button styling, and picker animations, providing a simpler styling model with full CSS control over the visible list container, individual options, scrollbars, height animations, and layout directions (vertical or horizontal). By combining `appearance: base-select`, `:checked` pseudo-class, `::checkmark` pseudo-element, JavaScript for filtering/selection management, and modern CSS features like `:has()` and `interpolate-size`, developers can build flexible multi-select widgets with progressive enhancement fallback to native listboxes in non-supporting browsers.

---

## Core Pillars

### 1. Listbox vs Dropdown Select: Fundamental Architectural Differences

Listboxes and dropdown selects are two distinct `<select>` modes, each with different use cases and styling requirements. Understanding the differences is critical for choosing the right approach and avoiding unnecessary complexity.

**Listbox mode** is triggered by:
- `<select multiple>` — allows selecting zero, one, or multiple options simultaneously
- `<select size="N">` where N > 1 — displays N options at once (single or multiple selection per spec)

**Dropdown mode** is the default when using `<select>` without attributes — displays button when closed, picker when open.

**Code Example:**
```html
<!-- Dropdown select: button + picker approach -->
<select id="single">
  <option>Choose...</option>
</select>

<!-- Listbox select: always-visible list -->
<select id="multiple" multiple>
  <option>Option 1</option>
  <option>Option 2</option>
</select>

<!-- Listbox select: size attribute -->
<select id="size-three" size="3">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

**Key differences:**

| Aspect | Dropdown | Listbox |
|--------|----------|---------|
| Default rendering | Button + hidden picker | Visible box showing N options |
| Picker positioning needed? | Yes (CSS anchor positioning) | No (always visible) |
| `::picker(select)` pseudo-element | Yes | No (not applicable) |
| `::selectedcontent` element | Yes | No (not applicable) |
| `::picker-icon` styling | Yes | No (not applicable) |
| Selection method | Click to open, select option | Direct click/keyboard on option |
| Scrolling | Picker scrolls if overflow | Container scrolls with `overflow-y` |
| Use case | Single selection + space-constrained | Multiple selection + list comparison |

Listboxes are simpler to style because there's no dropdown picker state, no position-try fallbacks needed, and no button/selectedcontent management.

### 2. Basic Listbox Styling: `appearance: base-select`, Size, Overflow

The foundation of a customizable listbox is setting `appearance: base-select` (same as dropdown) and defining the visible area with `width`, `height`, and `overflow` properties. The listbox displays all options within this bounded area.

**Code Example:**
```html
<select id="pets" multiple>
  <option value="cat">Cat</option>
  <option value="dog">Dog</option>
  <option value="bird">Bird</option>
  <option value="fish">Fish</option>
</select>
```

**CSS:**
```css
select {
  appearance: base-select;
  
  /* Container dimensions */
  width: 200px;
  height: 150px;
  
  /* Handle overflow with scrollbars */
  overflow-y: scroll;
  overflow-x: hidden;
  
  /* Styling */
  border: 2px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  padding: 0; /* Options add padding internally */
}

/* Individual option styling */
option {
  padding: 10px;
  background: white;
  height: 40px; /* Fixed height for consistent spacing */
}

/* Zebra-striping for readability */
option:nth-of-type(odd) {
  background: #f5f5f5;
}

/* Selection and keyboard focus states */
option:checked {
  background: #e3f2fd;
  font-weight: bold;
}

option:hover,
option:focus {
  background: #bbdefb;
  outline: none;
}
```

**Behavior:**
- `height: 150px` with 40px options = 3.75 options visible; scrollbar appears for remaining options
- `overflow-y: scroll` allows vertical scrolling through options
- Each option is a direct child of the select; no wrapper elements needed
- The scrollbar is the native browser scrollbar (unstyled in most browsers)

### 3. Checkmark Positioning and Customization with `::checkmark`

By default, checkmarks appear on the left side of selected options in listboxes. The `::checkmark` pseudo-element allows customizing the checkmark icon, position, color, and size.

**Code Example:**
```css
/* Default checkmark on left */
option:checked {
  font-weight: bold;
}

/* Move checkmark to right and customize it */
option::checkmark {
  order: 1; /* Requires flexbox; options are flex by default */
  margin-left: auto; /* Push to right in flex container */
  content: "☑️"; /* Replace default ✓ with custom emoji */
  font-size: 1.2em;
  color: #4caf50;
}

/* Hide checkmark entirely if preferred */
option::checkmark {
  display: none;
}
```

**Key points:**
- `order: 1` moves the checkmark within the flexbox row (options use `display: flex` by default)
- `margin-left: auto` aligns it to the right edge
- `content` property replaces the default checkmark symbol
- Content is NOT in the accessibility tree; screen readers won't announce emoji changes
- Without custom styling, the browser renders a default checkmark (usually "✓")

### 4. Expanding Listbox: Smooth Height Animations with `interpolate-size`

An expanding listbox starts at a compact size (single row or few rows) and expands on hover/focus to show the full list. This requires animating from a `height` value to `fit-content` using CSS `transition` and the `interpolate-size` property.

**Code Example:**
```html
<select id="expandable" multiple>
  <option>Option 1</option>
  <option>Option 2</option>
  <option>Option 3</option>
  <option>Option 4</option>
</select>
```

**CSS:**
```css
select {
  appearance: base-select;
  
  /* Start collapsed: show only one option */
  height: 44px;
  overflow: hidden;
  
  /* Smooth height transition */
  transition: height 0.4s ease;
  interpolate-size: allow-keywords;
  
  border: 2px solid #ddd;
  border-radius: 8px;
}

option {
  padding: 10px;
  height: 44px;
}

/* Expand on hover */
select:hover {
  height: fit-content;
}

/* Expand on focus — note: focus moves to first option, not select itself */
select:has(option:focus) {
  height: fit-content;
}
```

**Critical detail:** When you tab into a customizable listbox, focus moves to the first `<option>`, NOT the `<select>` element itself. Therefore, use `select:has(option:focus)` instead of `select:focus` to detect keyboard focus on options.

**How `interpolate-size` works:**
- By default, CSS can't smoothly transition between length values (44px) and keyword values (fit-content)
- `interpolate-size: allow-keywords` tells the browser to compute fit-content as a length and animate between 44px ↔ computed fit-content value
- Without this property, the height would jump instantly instead of animating smoothly

### 5. Horizontal Listbox Layout: Flexbox and Overflow-X Scrolling

A horizontal listbox displays options left-to-right instead of top-to-bottom, useful for scenarios like image galleries with selection or horizontal comparison lists. This requires flexbox layout, fixed widths, and horizontal scrolling.

**Code Example:**
```html
<div class="container">
  <select id="horizontal" multiple>
    <div class="wrapper">
      <option>Cat</option>
      <option>Dog</option>
      <option>Bird</option>
      <option>Fish</option>
      <option>Hamster</option>
    </div>
  </select>
</div>
```

**CSS:**
```css
.container {
  width: 90%;
  margin: 0 auto;
}

select {
  appearance: base-select;
  width: 100%; /* Full width of container */
  height: fit-content;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow-x: auto; /* Horizontal scrolling */
  overflow-y: hidden; /* No vertical scrolling */
}

.wrapper {
  display: flex; /* Layout options horizontally */
  width: fit-content; /* Ensure wrapper is wide enough for all options */
  gap: 0; /* Options touch without gap */
}

option {
  padding: 15px 30px;
  background: white;
  border: 1px solid #eee;
  position: relative; /* For absolute-positioned checkmark */
  white-space: nowrap; /* Prevent text wrapping */
  flex-shrink: 0; /* Prevent options from shrinking */
}

option:nth-of-type(odd) {
  background: #f5f5f5;
}

/* Position checkmark absolutely for compact appearance */
option::checkmark {
  position: absolute;
  top: 4px;
  left: 8px;
  font-size: 1.2rem;
  color: #4caf50;
  content: "✓";
}
```

**Key techniques:**
- `.wrapper` div inside select must use `display: flex` and `width: fit-content` to force horizontal layout
- `overflow-x: auto` enables horizontal scrolling when wrapper exceeds select width
- `flex-shrink: 0` prevents options from compressing; they maintain their minimum width
- `white-space: nowrap` prevents long text from wrapping to multiple lines
- `position: relative` on options enables `position: absolute` on the checkmark

### 6. Multiple Selection and `select.selectedOptions` Collection

Listboxes allow selecting multiple options by clicking with Ctrl/Cmd held or by using Shift+click for range selection. Accessing selected options requires JavaScript and the `select.selectedOptions` collection (or `select.options` with `.selected` property checking).

**Code Example:**
```html
<select id="multi" multiple>
  <option value="a">Option A</option>
  <option value="b">Option B</option>
  <option value="c">Option C</option>
</select>

<button id="submit">Get Selections</button>
<div id="result"></div>
```

**JavaScript:**
```javascript
const selectEl = document.querySelector('#multi');
const submitBtn = document.querySelector('#submit');
const resultDiv = document.querySelector('#result');

submitBtn.addEventListener('click', () => {
  // Get selected options using selectedOptions collection
  const selectedOptions = Array.from(selectEl.selectedOptions);
  const selectedValues = selectedOptions.map(opt => opt.value);
  
  // Alternative: iterate all options and check .selected property
  // const selectedValues = Array.from(selectEl.options)
  //   .filter(opt => opt.selected)
  //   .map(opt => opt.value);
  
  resultDiv.textContent = `Selected: ${selectedValues.join(', ')}`;
});

// Sync selection state automatically
selectEl.addEventListener('change', (event) => {
  console.log('Selection changed:', event.target.selectedOptions);
});
```

**Key APIs:**
- `select.selectedOptions` — HTMLCollection of currently-selected `<option>` elements (read-only)
- `option.selected` — Boolean property; can be set programmatically to select/deselect options
- `select.options` — HTMLCollection of all `<option>` elements
- Form submission automatically includes all selected option values

### 7. Filtering Listbox Options with JavaScript and Dynamic Population

A common pattern combines a text input filter field with a listbox that dynamically updates to show only matching options. This requires filtering the data array, clearing the listbox, and repopulating it with filtered options.

**Code Example:**
```html
<input type="text" id="filter" placeholder="Filter options..." />
<select id="filtered" multiple>
  <!-- Options populated by JavaScript -->
</select>
```

**JavaScript:**
```javascript
const filterInput = document.querySelector('#filter');
const select = document.querySelector('#filtered');

// Data source
const allContacts = [
  { name: "Alice", selected: false },
  { name: "Bob", selected: false },
  { name: "Charlie", selected: false },
  { name: "Diana", selected: false },
];

// Populate select with options from array
function populateOptions(dataArray) {
  select.innerHTML = ''; // Clear existing options
  
  dataArray.forEach(item => {
    const option = document.createElement('option');
    option.textContent = item.name;
    option.value = item.name;
    option.selected = item.selected;
    select.appendChild(option);
  });
}

// Filter data and repopulate
function filterOptions(searchString) {
  if (searchString.trim() === '') {
    populateOptions(allContacts);
  } else {
    const filtered = allContacts.filter(item =>
      item.name.toLowerCase().startsWith(searchString.toLowerCase())
    );
    populateOptions(filtered);
  }
}

// Listen to input changes
filterInput.addEventListener('input', (e) => {
  filterOptions(e.target.value);
});

// Sync selection state when user toggles options
select.addEventListener('change', () => {
  const currentValues = Array.from(select.selectedOptions).map(opt => opt.value);
  
  allContacts.forEach(item => {
    item.selected = currentValues.includes(item.name);
  });
  
  console.log('Updated selections:', allContacts);
});

// Initial population
populateOptions(allContacts);
```

**Key pattern:**
- Clear and repopulate the entire listbox when filter changes (simpler than removing individual options)
- Maintain a data array that stores selection state
- Sync the data array selection state when user changes options
- This prevents losing selections when the filter updates

### 8. Preventing Focus Loss with `select:has()` Pseudo-Class

The `:has()` pseudo-class allows selecting elements based on their descendants' state. For listboxes, `select:has(option:focus)` detects when any option inside the select has focus, enabling focus-based styling without JavaScript.

**Code Example:**
```css
select {
  appearance: base-select;
  height: 100px;
  border: 2px solid #ccc;
  transition: all 0.3s;
}

/* Select styling changes based on descendant option focus */
select:has(option:focus) {
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
  background: #f0f5ff;
}

option:focus {
  outline: none;
  background: #e3f2fd;
}
```

**Why this matters:**
- Keyboard users tab into the listbox and focus the first option
- Without `select:has(option:focus)`, the `<select>` element wouldn't know it has focus
- `select:focus` doesn't work because focus is on the option, not the select
- `select:has(option:focus)` provides keyboard focus indication without JavaScript

### 9. Native Scrollbar Styling Limitations and Workarounds

Customizable listboxes use the native browser scrollbar for vertical/horizontal overflow. In most browsers, scrollbar styling is limited or impossible via CSS (except in Firefox with `::-webkit-scrollbar` pseudo-elements, which have limited support).

**Current limitations:**
```css
/* These don't work reliably across browsers */
select {
  overflow-y: scroll;
  
  /* No standard CSS properties for scrollbar styling */
  /* Firefox supports ::-webkit-scrollbar but Chrome/Safari/Edge support varies */
  
  /* Some properties work on <input> and <textarea> but not <select> in all browsers */
}

/* Partial support in some browsers */
select::-webkit-scrollbar {
  width: 12px;
}

select::-webkit-scrollbar-track {
  background: #f1f1f1;
}

select::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 6px;
}
```

**Workaround:** If consistent scrollbar styling is critical, wrap options in a scrollable `<div>` instead of relying on select overflow:
```html
<select id="custom">
  <div class="scrollable-wrapper">
    <option>Option 1</option>
    <option>Option 2</option>
    <!-- Many more options -->
  </div>
</select>
```

### 10. Keyboard Navigation and Accessibility in Listboxes

Customizable listboxes inherit native keyboard navigation from the select element: arrow keys move focus between options, Enter toggles selection in multiple mode, and standard select accessibility features work (ARIA labels, etc.).

**Code Example:**
```html
<label for="colors">Available colors (select all you like):</label>
<select id="colors" multiple aria-label="Color choices">
  <option value="red">Red</option>
  <option value="green">Green</option>
  <option value="blue">Blue</option>
  <option value="yellow">Yellow</option>
</select>
```

**Keyboard behavior (automatic):**
- **Tab** — moves focus into the listbox (first option gets focus)
- **Arrow Up/Down** — navigate between options in multiple mode
- **Space/Enter** — toggle option selection in multiple mode
- **Ctrl+A** — select all options (in multiple mode, varies by browser)
- **Shift+Arrow** — range selection (varies by browser/OS)

**Accessibility considerations:**
- Always provide associated `<label>` or `aria-label`
- Focus styling is critical; don't remove `option:focus` styles
- Maintain visual indication of `:checked` state (bold, background color, checkmark)
- Test with keyboard navigation and screen readers (NVDA, JAWS, VoiceOver)

---

## Technical Deep-Dive

### Deep-Dive 1: Height Animation from Fixed Value to `fit-content` with `interpolate-size`

**Scenario:** An expanding listbox starts at 44px (showing one option) and must smoothly animate to `fit-content` (showing all options) when hovered or focused.

**Problem:** CSS transitions don't work between length values (44px) and keywords (fit-content) by default.

**Step 1: Without `interpolate-size` (broken)**
```css
select {
  height: 44px;
  transition: height 0.4s ease;
}

select:hover {
  height: fit-content; /* Browser can't animate: 44px → fit-content */
}
```

**Result:** Height jumps instantly from 44px to fit-content with no animation. The transition property is ignored because the values are incompatible.

**Step 2: Browser's computation of `fit-content`**
The `fit-content` keyword doesn't have a fixed pixel value; it depends on the content size. For this select with options measuring 44px each:
- 1 option: 44px fit-content
- 4 options: 176px fit-content
- Browser must compute this at runtime

**Step 3: With `interpolate-size: allow-keywords` (fixed)**
```css
select {
  height: 44px;
  transition: height 0.4s ease;
  interpolate-size: allow-keywords;
}

select:hover {
  height: fit-content;
}
```

**Timeline of animation:**
1. User hovers; browser triggers the hover state
2. Browser receives `height: fit-content` in new state
3. `interpolate-size: allow-keywords` tells the browser: "I'm about to animate between a keyword and a length; go ahead and compute the keyword as a pixel value"
4. Browser computes `fit-content` as 176px (for example, 4 options × 44px)
5. Browser animates from 44px → 176px over 0.4s using the `ease` timing function
6. Result: Smooth expansion animation ✅

**Step 4: For expanding animation on focus (with `:has()`)**
```css
select:has(option:focus) {
  height: fit-content;
}
```

**Browser detection:** When user tabs into the select, the first option receives focus. The `:has(option:focus)` selector matches the select element, triggering the animated height change.

**Key insight:** `interpolate-size` is necessary for any animation between fixed lengths and keywords like `fit-content`, `min-content`, or `max-content`.

---

### Deep-Dive 2: Filtering Listbox Options and Maintaining Selection State Across Filter Changes

**Scenario:** User has selected "Alice" and "Charlie" from a 10-person contact list. User types "ali" in the filter field. The listbox updates to show only "Alice". User deselects "Alice" (clearing the filter). The entire list reappears, and "Alice" should remain deselected while "Charlie" stays selected.

**Step 1: Initial state**
```
Data array:
{ name: "Alice", selected: true }
{ name: "Bob", selected: false }
{ name: "Charlie", selected: true }
{ name: "Diana", selected: false }
...
```

**Step 2: User types "ali" in filter**
```javascript
filterOptions("ali");
```

- Filter the data array: Only "Alice" matches
- Clear the listbox
- Populate with filtered items: `<option selected>Alice</option>`
- Listbox displays: Alice (with checkmark)

**Step 3: User deselects Alice in the filtered view**
- Dispatch 'change' event
- Read `select.selectedOptions`: Now empty (Alice is deselected)
- Update data array: Set Alice.selected = false
- Data array now: Alice.selected = false, Charlie.selected = true (still true from before)

**Step 4: User clears filter (types "")**
```javascript
filterOptions("");
```

- Filter the data array: Returns all items (full list)
- Clear the listbox
- Populate with all items:
  ```html
  <option>Alice</option> <!-- not selected -->
  <option>Bob</option>
  <option selected>Charlie</option> <!-- selected: true from data -->
  <option>Diana</option>
  ```
- Listbox displays: All 10 items with only Charlie checked ✅

**Critical implementation detail:**
```javascript
select.addEventListener('change', () => {
  // Get currently displayed option values
  const allCurrentValues = Array.from(select.options).map(opt => opt.value);
  
  // Get currently selected option values
  const currentSelectedValues = Array.from(select.selectedOptions).map(
    opt => opt.value
  );
  
  // Update data array: Only edit selection state for displayed items
  allContacts.forEach(contact => {
    // Skip items not currently displayed (filtered out)
    if (!allCurrentValues.includes(contact.name)) {
      return; // Don't toggle their selected state
    }
    
    // Update selection state for displayed items
    contact.selected = currentSelectedValues.includes(contact.name);
  });
});
```

**Why check `allCurrentValues`?**
Without this check: If "Alice" is filtered out and the listbox is repopulated, Alice isn't in `select.options` anymore. If you unconditionally set `contact.selected = false` for missing items, you'd lose their previous selection state.

With this check: Only items currently displayed in the listbox have their selection state updated. Filtered-out items maintain their previous state.

**Result:** Selection state persists correctly across filter changes, providing seamless UX.

---

### Deep-Dive 3: Horizontal Listbox Layout with Flex Wrapper and Scrollbar Behavior

**Scenario:** A gallery-like multi-select showing 5 pet types horizontally. User can scroll left/right to see more pets and select multiple via clicking with Ctrl held.

**Step 1: Basic structure with wrapper div**
```html
<select id="gallery" multiple>
  <div class="gallery-wrapper">
    <option value="cat">🐱 Cat</option>
    <option value="dog">🐶 Dog</option>
    <option value="bird">🐦 Bird</option>
    <option value="fish">🐟 Fish</option>
    <option value="hamster">🐹 Hamster</option>
    <option value="rabbit">🐰 Rabbit</option> <!-- Hidden unless scrolled -->
  </div>
</select>
```

**Step 2: CSS for horizontal layout**
```css
select {
  appearance: base-select;
  width: 500px; /* Container visible width */
  height: auto;
  overflow-x: auto; /* Horizontal scrollbar */
  overflow-y: hidden;
  border: 2px solid #ddd;
}

.gallery-wrapper {
  display: flex;
  width: fit-content; /* Expands to fit all options */
  gap: 0;
}

option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
  min-width: 100px; /* Ensure minimum width per option */
  height: auto;
  padding: 20px 15px;
  background: white;
  border: 1px solid #eee;
  border-right: none; /* Remove right border; adjacent option provides it */
  cursor: pointer;
  flex-shrink: 0; /* Don't compress options */
}

option:last-child {
  border-right: 1px solid #eee; /* Last option gets right border */
}

option:hover,
option:focus {
  background: #f0f0f0;
}

option:checked {
  background: #e3f2fd;
  border: 2px solid #4a90e2;
}
```

**Step 3: Scrollbar appearance and behavior**
- `.gallery-wrapper` width is `fit-content`, expanding to accommodate all 6 options (6 × 100px = 600px)
- `select` width is 500px, creating 100px overflow
- `overflow-x: auto` triggers horizontal scrollbar
- User scrolls horizontally; scrollbar indicates position and allows direct scrollbar dragging
- Options remain in flexbox row; no wrapping

**Step 4: Keyboard and mouse interaction**
- Keyboard: Arrow Up/Down (or Left/Right in some browsers) navigates through options
- Mouse scrolling: Horizontal wheel scroll (or trackpad two-finger scroll) scrolls the view
- Shift+Click: Range selection works across the entire option list (not just visible ones)
- Ctrl/Cmd+Click: Toggle individual options

**Step 5: Selection state across scrolling**
```javascript
const gallery = document.querySelector('#gallery');

gallery.addEventListener('change', () => {
  const selected = Array.from(gallery.selectedOptions).map(opt => opt.value);
  console.log('Selected pets:', selected); // Works regardless of which options are visible
});
```

Selected options remain selected even if they're scrolled off-screen. The selection state is independent of visibility.

**Result:** Professional gallery-style multi-select with smooth horizontal scrolling and persistent selection state.

---

## Key Terminology Bank

1. **`<select multiple>` attribute** — Enables listbox mode for a select element, allowing users to select zero, one, or multiple options simultaneously. The select displays as a list rather than a dropdown button.

2. **`<select size="N">` attribute** — Alternative method to trigger listbox mode by specifying how many options should be visible. `size="3"` displays 3 options at once; any additional options require scrolling.

3. **`appearance: base-select`** — CSS property value that opts a listbox select into customizable rendering mode, removing OS-level styling. Required for both dropdown and listbox customizable selects.

4. **Listbox vs dropdown mode** — Two distinct `<select>` rendering modes: Listbbox shows multiple options in a box (triggered by `multiple` or `size > 1`); dropdown shows a button and picker (default).

5. **`::checkmark` pseudo-element** — Targets the checkmark indicator displayed next to selected options in listboxes. Can customize content, position, color, or hide entirely using `display: none`.

6. **`option::checkmark` with `order: 1`** — Flexbox property that repositions the checkmark from left to right by giving it a higher sort order than text content (which has default `order: 0`).

7. **`overflow-y: scroll`** — CSS property that enables vertical scrollbars for content exceeding the container's height. Listboxes use this to handle option lists longer than the display area.

8. **`overflow-x: auto`** — CSS property that enables horizontal scrollbars only when content exceeds the container's width. Used for horizontal listbox layouts with many options.

9. **`height: fit-content`** — CSS keyword that sizes the element to match its content's natural height. Combined with `interpolate-size: allow-keywords`, enables smooth animations between fixed heights and fit-content.

10. **`interpolate-size: allow-keywords`** — CSS property that enables transitions between length values (e.g., 44px) and size keywords (e.g., fit-content). Required for expanding listbox animations.

11. **`select:has(option:focus)` selector** — CSS functional pseudo-class that matches a select element if any of its descendant options has focus. Enables focus styling without JavaScript since focus is on the option, not the select.

12. **`select.selectedOptions` collection** — JavaScript HTMLCollection of currently-selected `<option>` elements in a listbox. Read-only; access via `Array.from(select.selectedOptions)` to iterate.

13. **`select.options` collection** — JavaScript HTMLCollection of all `<option>` elements in a select. Used to iterate all available options regardless of selection state.

14. **`option.selected` property** — JavaScript boolean property on `<option>` elements. Can be read to check if selected or written to programmatically select/deselect options: `option.selected = true`.

15. **Multiple selection via Ctrl+Click** — Native keyboard-mouse interaction in listboxes: Holding Ctrl (Windows/Linux) or Cmd (Mac) while clicking an option toggles its selection without affecting others.

16. **Range selection via Shift+Click** — Native interaction that selects a contiguous range of options. Shift+Click on option A then option B selects all options between them (varies by browser/OS implementation).

17. **`flex-shrink: 0`** — Flexbox property that prevents items from compressing when space is limited. Used on options in horizontal listboxes to maintain fixed widths and force scrollbars.

18. **`white-space: nowrap`** — CSS property that prevents text from wrapping to multiple lines. Used on horizontal listbox options to keep labels on a single line, preventing height expansion.

19. **Dynamic option population with `innerHTML = ""`** — JavaScript pattern that clears all options then repopulates a select by setting `innerHTML` to empty string and appending new `<option>` elements. Used for filtering workflows.

20. **`Array.from(select.selectedOptions).map(opt => opt.value)`** — JavaScript idiom converting the selectedOptions HTMLCollection to an array of option values for easier manipulation and storage.

21. **Filtering persistence pattern** — Design pattern that maintains a data array separate from the DOM, allowing filtered views to be repopulated without losing selection state of hidden items.

22. **Focus indicator with `:has()` pseudo-class** — CSS technique using `select:has(option:focus) { border-color: blue; }` to style the select container based on whether any contained option has keyboard focus.

---

## Watch Out For

### 1. ⚠️ Focus moves to first `<option>`, NOT the `<select>` element

**Misconception:** "I'll use `select:focus` to detect when the listbox receives keyboard focus."

**Reality:** In customizable listboxes, when you tab into the select, focus jumps directly to the first `<option>` element, not the `<select>` itself. The `select:focus` pseudo-class never matches.

**Why it matters:** Your `select:focus { border: 3px solid blue; }` styling won't work; the user won't see focus indication on the select container.

**What to do:** Use `select:has(option:focus)` instead to detect when any option inside the select has focus, or style the `option:focus` state directly.

---

### 2. ⚠️ `option.selected` property doesn't update when filtering without data array sync

**Misconception:** "If I filter the select options dynamically, the browser will remember which ones were previously selected."

**Reality:** Every time you repopulate the select (clear innerHTML and append new options), the DOM `<option>` elements are recreated. They don't retain their previous selected state unless you explicitly set `option.selected = true/false` during creation.

**Why it matters:** User loses their selections when the filter changes, frustrating UX.

**What to do:** Maintain a separate data array that stores selection state. When repopulating the select, consult the data array to set `option.selected` correctly:

```javascript
array.forEach(item => {
  const option = document.createElement('option');
  option.textContent = item.name;
  option.selected = item.selected; // Read from data array
  select.appendChild(option);
});
```

---

### 3. ⚠️ `interpolate-size: allow-keywords` is required for keyword-to-length animations

**Misconception:** "`transition: height 0.4s` will smoothly animate my select from `height: 44px` to `height: fit-content`."

**Reality:** Without `interpolate-size: allow-keywords`, the height changes instantly. CSS can't animate between length and keyword values without explicit permission.

**Why it matters:** Your expanding listbox animation appears broken, jumping instantly instead of smoothly expanding.

**What to do:** Always add `interpolate-size: allow-keywords` when animating between keywords like `fit-content`, `min-content`, `max-content` and length values.

---

### 4. ⚠️ Horizontal listbox requires wrapper `<div>` with `display: flex` inside `<select>`

**Misconception:** "I'll set `select { display: flex; flex-direction: row; }` to make options display horizontally."

**Reality:** You can't style the `<select>` element itself with flex in the way you're imagining. The HTML5 spec allows container `<div>` elements inside `<select>` for grouping options, which you can set to `display: flex`.

**Why it matters:** Without the wrapper div, options won't display horizontally; they remain vertical.

**What to do:** Use a wrapper div inside the select:

```html
<select multiple>
  <div class="horizontal">
    <option>A</option>
    <option>B</option>
  </div>
</select>
```

```css
.horizontal { display: flex; width: fit-content; }
```

---

### 5. ⚠️ `flex-shrink: 0` is essential for horizontal layouts

**Misconception:** "Options will maintain their width in a horizontal listbox without any flex properties."

**Reality:** By default, flex items (options) shrink when space is limited. If the select width is 500px but all options total 600px, options compress to 83% of their intended size without `flex-shrink: 0`.

**Why it matters:** Your horizontal options become cramped and text crushes together instead of triggering scrollbars.

**What to do:** Add `flex-shrink: 0` to option styles to maintain minimum widths and force scrollbars.

---

### 6. ⚠️ Scrollbar styling has severe browser support issues

**Misconception:** "I'll use `::-webkit-scrollbar` pseudo-elements to style the listbox scrollbars consistently."

**Reality:** Scrollbar styling is not standardized. `::-webkit-scrollbar` works in Chrome/Edge/Safari but not Firefox. Firefox uses different non-standard pseudo-elements. Consistent cross-browser scrollbar styling is currently impossible.

**Why it matters:** Your scrollbar styling looks perfect in Chrome but completely ignored in Firefox.

**What to do:** Accept native browser scrollbars as-is, or wrap options in a custom scrollable container (div) that you can style with custom scrollbars using JavaScript libraries.

---

### 7. ⚠️ `::checkmark` content is NOT in the accessibility tree

**Misconception:** "I'll replace the default ✓ with an emoji ⭐ using `content` on `::checkmark`, and screen reader users will know what it means."

**Reality:** CSS-generated content via pseudo-elements is not exposed to assistive technologies. Screen readers announce "option selected" but they don't know about the emoji.

**Why it matters:** Users relying on screen readers might miss the visual distinction your emoji provides.

**What to do:** Ensure semantic selection is announced by the browser (it is, via "selected" state). The checkmark is purely visual; don't rely on it conveying critical information to assistive tech users.

---

### 8. ⚠️ Filtering doesn't preserve selection state without explicit data array synchronization

**Misconception:** "I'll filter the options list and re-render it; selections will persist automatically."

**Reality:** Repopulating the select with new HTML `<option>` elements doesn't preserve previous selection state. Each new option has `selected: false` by default unless you explicitly set it during creation.

**Why it matters:** User selects "Alice" and "Charlie", filters to "Ali" to find "Alice", then clears the filter. Now only "Charlie" is still selected; "Alice" was lost because the new `<option>` element created during re-render had `selected: false`.

**What to do:** Maintain a parallel JavaScript data structure (array of objects) that tracks selection state independently of the DOM. Consult this array when creating options during repopulation.

---

### 9. ⚠️ `overflow-y: scroll` shows both vertical AND horizontal scrollbars in some contexts

**Misconception:** "`overflow-y: scroll` will only show vertical scrollbars."

**Reality:** If the listbox content is wider than the container (e.g., long option text), the browser may show both vertical and horizontal scrollbars even if you only specified `overflow-y`.

**Why it matters:** Unexpected horizontal scrollbars appear, crowding your layout.

**What to do:** Set `overflow-x: hidden` explicitly to prevent horizontal scrollbars, or use `white-space: nowrap` on options to prevent text wrapping.

---

### 10. ⚠️ `size` attribute doesn't prevent scrollbars if content exceeds visible area

**Misconception:** "`<select size="3">` will show exactly 3 options without scrollbars."

**Reality:** `size="3"` allocates vertical space for 3 options, but if you add 10 options, scrollbars appear automatically. The `size` attribute sets the initial visible height; it's not a maximum.

**Why it matters:** Listings overflow, contradicting the assumption that `size` limits visible options permanently.

**What to do:** Use CSS `height` property instead of relying on `size` attribute. Set `height` to a fixed pixel value to match your intended number of visible options exactly.

---

## Active Recall: Exam-Ready Questions

### Question 1: Recall - What attributes/modes trigger listbox rendering?
**Difficulty: Recall**

Name the two HTML attributes that trigger listbox mode for a `<select>` element and explain the difference between them.

<details>
<summary>Answer</summary>

The two attributes are:

1. **`<select multiple>`** — Triggers listbox mode and allows selecting zero, one, or multiple options. The select displays all options in a visible box (scrollable if overflow).

2. **`<select size="N">`** where N > 1 — Triggers listbox mode by specifying how many options should be visible at once. For example, `<select size="5">` shows 5 options; additional options are scrollable.

**Difference:**
- `multiple` allows multiple selections; default is single selection
- `size` controls the visible height (in number of option rows); if N=1 or missing, renders as dropdown

**Example:**
```html
<!-- Single selection, 3 options visible -->
<select size="3">
  <option>Option 1</option>
  <option>Option 2</option>
  <option>Option 3</option>
</select>

<!-- Multiple selection, auto-height to fit content -->
<select multiple>
  <option>Option A</option>
  <option>Option B</option>
</select>
```

Both require `appearance: base-select` in CSS to enable customizable rendering.

</details>

---

### Question 2: Application - Build an expanding listbox with smooth animation

**Difficulty: Application**

Write the HTML and CSS to create a listbox that starts showing only one option (44px height) and expands smoothly on hover to show all 5 options.

<details>
<summary>Answer</summary>

**HTML:**
```html
<label for="expand-list">Select items:</label>
<select id="expand-list" multiple>
  <option value="item1">Item 1</option>
  <option value="item2">Item 2</option>
  <option value="item3">Item 3</option>
  <option value="item4">Item 4</option>
  <option value="item5">Item 5</option>
</select>
```

**CSS:**
```css
select {
  appearance: base-select;
  
  /* Start collapsed */
  height: 44px;
  overflow: hidden;
  
  /* Enable smooth animation */
  transition: height 0.4s ease;
  interpolate-size: allow-keywords;
  
  /* Styling */
  width: 200px;
  border: 2px solid #ddd;
  border-radius: 6px;
  background: white;
}

option {
  padding: 10px;
  height: 44px;
  background: white;
  border-bottom: 1px solid #eee;
}

option:nth-of-type(odd) {
  background: #f5f5f5;
}

/* Expand on hover */
select:hover {
  height: fit-content;
}

/* Expand on keyboard focus (focus moves to first option) */
select:has(option:focus) {
  height: fit-content;
}

/* Hover/focus state for individual options */
option:hover,
option:focus {
  background: #c3e1ff;
  outline: none;
}

option:checked {
  background: #e3f2fd;
  font-weight: bold;
}
```

**How it works:**
1. Initial height is 44px (showing one 44px option)
2. Overflow is hidden; additional options don't show
3. On hover, height changes to `fit-content` (all 5 options × 44px = 220px)
4. `interpolate-size: allow-keywords` enables smooth animation from 44px → 220px
5. `select:has(option:focus)` detects keyboard focus and also triggers expand
6. Mouse-out returns height to 44px, collapsing smoothly

**Result:** Professional expanding list widget with zero JavaScript.

</details>

---

### Question 3: Analysis - Explain why selection state is lost when filtering without a data array

**Difficulty: Analysis**

A developer creates a contact filter listbox. User selects "Alice" and "Bob", filters to show only names starting with "A" (only Alice shows), then clears the filter. Only "Alice" remains selected; "Bob" was lost. Explain why and how to fix it.

<details>
<summary>Answer</summary>

**Why selection is lost:**

When the filter is applied:
1. Developer clears the select: `select.innerHTML = ""`
2. All previous `<option>` elements are deleted from the DOM
3. Developer repopulates with filtered options: only "Alice" `<option>` is created
4. During repopulation, `option.selected` is not explicitly set

When the filter is cleared:
1. Developer clears the select again: `select.innerHTML = ""`
2. All new `<option>` elements (including the old Alice and Bob) are deleted from the DOM
3. Developer repopulates with all unfiltered options
4. New "Alice" and "Bob" `<option>` elements are created
5. **Critical:** The new "Alice" option has `selected: false` by default because the code didn't explicitly set it during creation
6. Result: Both "Alice" and "Bob" lose their selected state

**The problem in code:**
```javascript
function repopulate(array) {
  select.innerHTML = ""; // Destroys DOM selection state
  
  array.forEach(item => {
    const option = document.createElement('option');
    option.textContent = item.name;
    // BUG: Never set option.selected, so it defaults to false
    select.appendChild(option);
  });
}
```

**The fix: Maintain a parallel data array**

```javascript
// Master data array (separate from DOM)
const allContacts = [
  { name: "Alice", selected: false },
  { name: "Bob", selected: false },
  { name: "Charlie", selected: false },
];

// When repopulating, read selection state from data array
function repopulate(array) {
  select.innerHTML = "";
  
  array.forEach(item => {
    const option = document.createElement('option');
    option.textContent = item.name;
    option.value = item.name;
    option.selected = item.selected; // ✓ READ from data array
    select.appendChild(option);
  });
}

// When user changes selection, sync back to data array
select.addEventListener('change', () => {
  const selectedValues = Array.from(select.selectedOptions).map(opt => opt.value);
  
  allContacts.forEach(contact => {
    contact.selected = selectedValues.includes(contact.name);
  });
  
  console.log('Synced:', allContacts);
});

// Filter and repopulate
function filterContacts(searchString) {
  if (searchString.trim() === '') {
    repopulate(allContacts); // Use full array
  } else {
    const filtered = allContacts.filter(item =>
      item.name.toLowerCase().startsWith(searchString.toLowerCase())
    );
    repopulate(filtered); // Use filtered array
  }
}
```

**How it works:**
1. `allContacts` array is the single source of truth for selection state
2. When filtering, the DOM options are repopulated but selection state comes from `allContacts`
3. When user toggles options, `allContacts` is updated
4. Filtering then repopulating consults `allContacts` again, preserving selections

**Result:** Selection persists across filter changes because selection state lives in JavaScript, not in the DOM.

</details>

---

### Question 4: Synthesis - Design a horizontal gallery-style multi-select listbox

**Difficulty: Synthesis**

Create a horizontal multi-select listbox for choosing pet images. Options include emoji + labels, displayed left-to-right with scrolling. Include custom checkmark styling and focus indicators. Show HTML, CSS, and explain the layout approach.

<details>
<summary>Answer</summary>

**HTML:**
```html
<form>
  <label for="pet-gallery">Choose your favorite pets:</label>
  <select id="pet-gallery" multiple>
    <div class="Gallery">
      <option value="cat">
        <span class="emoji">🐱</span>
        <span class="label">Cat</span>
      </option>
      <option value="dog">
        <span class="emoji">🐶</span>
        <span class="label">Dog</span>
      </option>
      <option value="bird">
        <span class="emoji">🐦</span>
        <span class="label">Bird</span>
      </option>
      <option value="fish">
        <span class="emoji">🐟</span>
        <span class="label">Fish</span>
      </option>
      <option value="hamster">
        <span class="emoji">🐹</span>
        <span class="label">Hamster</span>
      </option>
      <option value="rabbit">
        <span class="emoji">🐰</span>
        <span class="label">Rabbit</span>
      </option>
    </div>
  </select>
  <div id="selected">Selected: <span>None</span></div>
</form>
```

**CSS:**
```css
select#pet-gallery {
  appearance: base-select;
  width: 100%;
  max-width: 600px;
  height: 140px;
  overflow-x: auto; /* Horizontal scrolling */
  overflow-y: hidden;
  border: 2px solid #ddd;
  border-radius: 8px;
  background: white;
  padding: 0;
}

.Gallery {
  display: flex; /* Horizontal layout */
  width: fit-content; /* Expand to fit all options */
  gap: 0;
  height: 100%;
}

option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
  min-width: 100px; /* Minimum width per option */
  padding: 15px;
  border: 1px solid #eee;
  border-right: none;
  background: white;
  cursor: pointer;
  flex-shrink: 0; /* Don't compress */
  position: relative;
  transition: all 0.2s ease;
}

option:last-child {
  border-right: 1px solid #eee;
}

option .emoji {
  font-size: 2.5rem;
  line-height: 1;
  margin-bottom: 8px;
  text-box: trim-both cap alphabetic; /* Align emoji vertically */
}

option .label {
  font-size: 0.85rem;
  text-align: center;
  color: #333;
  white-space: nowrap;
}

/* Focus state for keyboard navigation */
option:focus {
  outline: none;
  background: #f5f5f5;
  box-shadow: inset 0 0 0 2px #4a90e2;
}

/* Hover state for visual feedback */
option:hover {
  background: #f9f9f9;
}

/* Checked/selected state */
option:checked {
  background: #e3f2fd;
  border: 2px solid #4a90e2;
  border-right: 2px solid #4a90e2;
}

option:checked .emoji {
  transform: scale(1.3);
  filter: drop-shadow(0 0 4px rgba(74, 144, 226, 0.5));
}

/* Checkmark styling */
option::checkmark {
  position: absolute;
  bottom: 6px;
  right: 6px;
  font-size: 1.3rem;
  color: #4a90e2;
  content: "✓";
  background: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #4a90e2;
}
```

**JavaScript (optional enhancement):**
```javascript
const form = document.querySelector('form');
const select = document.querySelector('#pet-gallery');
const selectedSpan = document.querySelector('#selected span');

select.addEventListener('change', () => {
  const selected = Array.from(select.selectedOptions).map(opt => {
    const emoji = opt.querySelector('.emoji').textContent;
    const label = opt.querySelector('.label').textContent;
    return `${emoji} ${label}`;
  });
  
  selectedSpan.textContent = selected.length > 0 ? selected.join(', ') : 'None';
});

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const values = Array.from(select.selectedOptions).map(opt => opt.value);
  console.log('Submitted pets:', values);
});
```

**Key design elements:**

1. **Horizontal layout:** `.Gallery` wrapper with `display: flex` and `width: fit-content`
2. **Scrolling:** `overflow-x: auto` enables horizontal scrollbar; `flex-shrink: 0` forces scrollbars
3. **Rich content:** Options contain nested emoji and label for visual gallery feel
4. **Focus indicator:** `box-shadow: inset` for keyboard navigation visibility
5. **Selection feedback:** Checked options get colored background, emoji scale-up, and decorative checkmark
6. **Checkmark:** Positioned absolutely in corner with custom styling
7. **Accessibility:** Native keyboard/mouse support; label provided; focus visible

**Responsive enhancement:**
```css
@media (max-width: 480px) {
  select#pet-gallery {
    max-width: 100%;
    height: 180px; /* More vertical space on small screens */
  }
  
  .Gallery {
    flex-wrap: wrap; /* Allow wrapping on very small screens */
  }
}
```

**Result:** Beautiful, interactive gallery-style multi-select with zero JavaScript required for core functionality (JavaScript enhancement adds live updating display).

</details>

---

### Question 5: Evaluation - Identify issues in this listbox filtering implementation

**Difficulty: Evaluation**

Review this contact filter listbox code and identify all bugs and accessibility issues:

```html
<input id="filter" type="text" placeholder="Filter" />
<select id="contacts" multiple>
  <!-- Options populated by JavaScript -->
</select>
<button id="export">Export Selected</button>
```

```javascript
const contacts = [
  { name: "Alice", selected: false },
  { name: "Bob", selected: false },
];

const filterInput = document.querySelector('#filter');
const select = document.querySelector('#contacts');

function getSelected() {
  return Array.from(select.selectedOptions).map(opt => opt.value);
}

function populate(array) {
  select.innerHTML = '';
  array.forEach(contact => {
    const option = document.createElement('option');
    option.textContent = contact.name;
    select.appendChild(option); // BUG 1
  });
}

filterInput.addEventListener('input', () => {
  const search = filterInput.value;
  const filtered = contacts.filter(c => 
    c.name.toLowerCase().includes(search.toLowerCase())
  );
  populate(filtered);
});

document.querySelector('#export').addEventListener('click', () => {
  const selected = getSelected();
  console.log(selected); // BUG 2
});
```

<details>
<summary>Answer</summary>

**Bug 1: Selection state lost during filtering**
- **Issue:** `populate()` doesn't read from `contact.selected` when creating options
- **Symptom:** User selects "Alice" and "Bob", filters to "Ali", then clears filter. Only the newly-created options have `selected: false`, so both lose selection
- **Fix:** Set `option.selected = contact.selected` during creation:
```javascript
function populate(array) {
  select.innerHTML = '';
  array.forEach(contact => {
    const option = document.createElement('option');
    option.textContent = contact.name;
    option.value = contact.name;
    option.selected = contact.selected; // ✓ Read from data array
    select.appendChild(option);
  });
}
```

---

**Bug 2: Selection state not synced back to data array**
- **Issue:** No event listener syncs selections from DOM to `contacts` array. When user checks "Alice" and exports, the data array wasn't updated with the selection
- **Symptom:** Export always returns empty array because `contact.selected` values are never updated
- **Fix:** Add change listener to sync selections:
```javascript
select.addEventListener('change', () => {
  const selectedValues = getSelected();
  contacts.forEach(contact => {
    contact.selected = selectedValues.includes(contact.name);
  });
});
```

---

**Bug 3: Missing label association**
- **Issue:** No `<label>` element associated with the input or select
- **Accessibility impact:** Screen reader users can't understand what the filter controls
- **Fix:** Add semantic labels:
```html
<label for="filter">Filter contacts:</label>
<input id="filter" type="text" placeholder="Filter" />
<label for="contacts">Select contacts (hold Ctrl/Cmd for multiple):</label>
<select id="contacts" multiple></select>
```

---

**Bug 4: No focus visible indication**
- **Issue:** No CSS for `option:focus` styling
- **Accessibility impact:** Keyboard users can't see which option has focus
- **Fix:** Add focus styling:
```css
option:focus {
  background: #c3e1ff;
  outline: none;
}
```

---

**Bug 5: Missing checked visual indicator**
- **Issue:** Selected options have no visual distinction (no bold, color, checkmark)
- **Accessibility impact:** Visual users can't easily see which options are selected
- **Fix:** Add checked styling:
```css
option:checked {
  background: #e3f2fd;
  font-weight: bold;
}
```

---

**Bug 6: Export button doesn't confirm successful submission**
- **Issue:** Clicking export just logs to console; no user feedback
- **Symptom:** User doesn't know if export succeeded or what was exported
- **Fix:** Update UI or server:
```javascript
document.querySelector('#export').addEventListener('click', () => {
  const selected = getSelected();
  if (selected.length === 0) {
    alert('Please select at least one contact');
    return;
  }
  console.log('Exporting:', selected);
  // Send to server or download file
});
```

---

**Corrected version:**

```html
<div>
  <label for="filter">Filter contacts:</label>
  <input id="filter" type="text" placeholder="Type to filter..." />
</div>

<div>
  <label for="contacts">Select contacts (Ctrl+Click for multiple):</label>
  <select id="contacts" multiple aria-label="Contact list"></select>
</div>

<button id="export">Export Selected</button>
<div id="feedback"></div>
```

```javascript
const contacts = [
  { name: "Alice", selected: false },
  { name: "Bob", selected: false },
  { name: "Charlie", selected: false },
];

const filterInput = document.querySelector('#filter');
const select = document.querySelector('#contacts');
const exportBtn = document.querySelector('#export');
const feedbackDiv = document.querySelector('#feedback');

function getSelected() {
  return Array.from(select.selectedOptions).map(opt => opt.value);
}

// ✓ Fixed: Reads selection state from data array
function populate(array) {
  select.innerHTML = '';
  array.forEach(contact => {
    const option = document.createElement('option');
    option.textContent = contact.name;
    option.value = contact.name;
    option.selected = contact.selected;
    select.appendChild(option);
  });
}

// ✓ Added: Sync selections to data array
select.addEventListener('change', () => {
  const selectedValues = getSelected();
  contacts.forEach(contact => {
    contact.selected = selectedValues.includes(contact.name);
  });
});

filterInput.addEventListener('input', () => {
  const filtered = contacts.filter(c =>
    c.name.toLowerCase().includes(filterInput.value.toLowerCase())
  );
  populate(filtered);
});

// ✓ Enhanced: Provide feedback
exportBtn.addEventListener('click', () => {
  const selected = getSelected();
  if (selected.length === 0) {
    feedbackDiv.textContent = '⚠️ Please select at least one contact';
    feedbackDiv.style.color = 'orange';
  } else {
    feedbackDiv.textContent = `✓ Exported: ${selected.join(', ')}`;
    feedbackDiv.style.color = 'green';
  }
});

// Initial population
populate(contacts);
```

```css
/* ✓ Added focus indicator */
option:focus {
  background: #c3e1ff;
  outline: none;
}

/* ✓ Added checked indicator */
option:checked {
  background: #e3f2fd;
  font-weight: bold;
}

select {
  appearance: base-select;
  width: 100%;
  height: 200px;
  border: 2px solid #ddd;
  border-radius: 6px;
  padding: 0;
  overflow-y: auto;
}

option {
  padding: 8px;
  background: white;
}

option:nth-of-type(odd) {
  background: #f9f9f9;
}
```

**Summary of fixes:**
✅ Selection state read from data array during populate
✅ Selection state synced to data array during select change
✅ Semantic labels for accessibility
✅ Focus and checked visual indicators
✅ User feedback for button actions
✅ Input validation before export

</details>

---

## Summary

Customizable select listboxes provide a simpler styling model than dropdown selects by eliminating popup picker complexity. By using `<select multiple>` or `<select size="N">`, `appearance: base-select`, CSS for sizing/scrolling/animations, and JavaScript for filtering and selection management, you can build powerful multi-select widgets. Key patterns include maintaining a separate data array for selection state, using `:has(option:focus)` for focus detection, `interpolate-size: allow-keywords` for smooth height animations, and flexbox layouts for horizontal galleries. Progressive enhancement ensures listboxes remain functional in non-supporting browsers while offering enhanced customization in capable browsers (Chrome 135+, Edge 135+, Safari TP).

---

**Next Steps for Mastery:**
- Build a contact picker with filter, multi-select, and persistence across sessions using localStorage
- Create responsive layouts that switch from horizontal gallery on desktop to vertical listbox on mobile
- Implement drag-and-drop reordering of selected options
- Combine listbox filtering with server-side search for large datasets
- Compare performance of customizable vs classic vs custom JavaScript select widgets
