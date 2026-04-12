# UI Pseudo-Classes Study Guide

## Executive Summary

UI pseudo-classes are CSS selectors that target form controls based on their interactive state, validation state, and requirement status, enabling visual feedback without JavaScript. These include `:required/:optional` (requirement status), `:valid/:invalid/:in-range/:out-of-range` (validation), `:enabled/:disabled/:read-only/:read-write` (interactivity), `:checked/:indeterminate/:default` (checkbox/radio states), and advanced classes like `:focus-visible`, `:placeholder-shown`, and (future) `:user-invalid`. Combined with pseudo-elements (`::before`, `::after`) and CSS generated content, UI pseudo-classes allow developers to provide clear visual indicators of form control state, replacing the need for JavaScript state tracking in many cases while maintaining comprehensive accessibility and semantic meaning.

---

## Core Pillars

### 1. Fundamental UI Pseudo-Classes: :hover, :focus, :active

Before exploring form-specific pseudo-classes, understand the foundational interactive pseudo-classes that work on all elements, including form controls.

**Code Example:**
```css
/* Basic interactive pseudo-classes */
input {
  border: 2px solid #ccc;
  padding: 8px;
  transition: all 0.3s ease;
}

/* Hover: when mouse hovers over the input */
input:hover {
  border-color: #999;
  background-color: #f9f9f9;
}

/* Focus: when keyboard tab or click gives focus */
input:focus {
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
  border-color: #4a90e2;
  background-color: white;
}

/* Active: while being clicked or Enter pressed */
input:active {
  background-color: #e0e0e0;
}
```

**Behavior:**
- `:hover` matches when the mouse pointer is over the element
- `:focus` matches when keyboard focus or click focus is on the element
- `:active` matches while the element is being activated (clicked or Enter pressed)
- These work on all form elements: input, textarea, select, button, etc.
- Use `:focus` for keyboard accessibility indicators; `:hover` provides mouse feedback

### 2. Required vs Optional: `:required` and `:optional` Pseudo-Classes

The `:required` and `:optional` pseudo-classes target form inputs based on whether they have the `required` attribute, providing visual distinction between required and optional fields without JavaScript.

**Code Example:**
```html
<form>
  <div>
    <label for="name">Name:</label>
    <input id="name" name="name" type="text" required />
  </div>
  <div>
    <label for="email">Email (optional):</label>
    <input id="email" name="email" type="email" />
  </div>
  <button>Submit</button>
</form>
```

**CSS:**
```css
input:required {
  border: 2px solid #000;
  border-left: 4px solid red;
}

input:optional {
  border: 2px solid #ccc;
  border-left: 4px solid green;
}

/* Better: use generated content for visual indicator */
input:required {
  background-image: url('required-icon.svg');
  background-position: right 8px center;
  background-repeat: no-repeat;
  padding-right: 32px;
}
```

**Key Points:**
- Only applies to form controls that support the `required` attribute: `<input>`, `<select>`, `<textarea>`
- Elements without `required` attribute default to `:optional` (optional by default)
- If a radio button in a group has `required`, ALL radios in that group require selection, but only the one with `required` attribute matches `:required` pseudo-class
- Use non-color indicators (icons, borders, symbols) to avoid accessibility issues with colorblind users

### 3. Generated Content with Pseudo-Elements for Accessibility

The `::before` and `::after` pseudo-elements combined with the `content` property allow adding visual indicators to form controls without adding extra DOM elements, improving accessibility.

**Code Example:**
```html
<div>
  <label for="fname">First name:</label>
  <input id="fname" name="fname" type="text" required />
  <span></span> <!-- Anchor for ::after pseudo-element -->
</div>
```

**CSS:**
```css
/* Style the anchor element */
input + span {
  position: relative;
}

/* Generate "required" indicator after optional span element */
input:required + span::after {
  font-size: 0.75rem;
  position: absolute;
  content: "required";
  color: white;
  background-color: black;
  padding: 4px 8px;
  border-radius: 3px;
  top: -26px;
  left: -70px;
  white-space: nowrap;
}

/* Custom checkmark for valid inputs */
input:valid + span::before {
  content: "✓";
  color: green;
  position: absolute;
  right: -24px;
  top: 8px;
  font-size: 1.2rem;
  font-weight: bold;
}

input:invalid + span::before {
  content: "✗";
  color: red;
  position: absolute;
  right: -24px;
  top: 8px;
  font-size: 1.2rem;
  font-weight: bold;
}
```

**Critical Notes:**
- Generated content is NOT in the accessibility tree; screen readers don't announce it
- Only specific input types support pseudo-elements: text inputs DON'T display generated content
- Radio buttons, checkboxes, range, color DO support generated content
- Keep text-based inputs for their default rendering; use generated content on non-text inputs
- Generated content acts as a child of the pseudo-element's element for positioning purposes

### 4. Validation State: `:valid` and `:invalid` Pseudo-Classes

The `:valid` and `:invalid` pseudo-classes target form controls based on constraint validation, allowing real-time visual feedback on data validity.

**Code Example:**
```html
<form>
  <div>
    <label for="email">Email:</label>
    <input id="email" name="email" type="email" required />
  </div>
  <div>
    <label for="age">Age (18-100):</label>
    <input id="age" name="age" type="number" min="18" max="100" required />
  </div>
</form>
```

**CSS:**
```css
/* All inputs are invalid when empty (if required) */
input:required:invalid {
  border: 2px solid red;
  background-color: #ffe6e6;
}

/* Becomes valid when filled correctly */
input:required:valid {
  border: 2px solid green;
  background-color: #e6ffe6;
}

/* Non-required empty inputs are valid */
input:optional:invalid {
  border: 2px solid orange; /* Invalid but not required, so less urgent */
}

/* Email type validation */
input[type="email"]:valid {
  border-color: green;
}

input[type="email"]:invalid {
  border-color: red;
}

/* URL type validation */
input[type="url"]:valid {
  border-left: 4px solid green;
}

input[type="url"]:invalid {
  border-left: 4px solid red;
}
```

**Rules for `:valid`/`:invalid` matching:**
- Controls with NO constraint validation always match `:valid` (no restrictions = valid)
- `:required` inputs with empty values match `:invalid`
- Email/URL types match `:invalid` when data doesn't match expected pattern
- Email inputs with empty value (and not required) still match `:valid`
- Inputs are validated continuously as user types; `:invalid` may appear temporarily

### 5. Range Validation: `:in-range` and `:out-of-range`

The `:in-range` and `:out-of-range` pseudo-classes specifically target numeric inputs with `min` and `max` attributes, providing more specific feedback than generic `:valid`/`:invalid`.

**Code Example:**
```html
<input id="age" name="age" type="number" min="18" max="100" required />
```

**CSS:**
```css
input[type="number"] {
  transition: all 0.3s ease;
}

/* When value is within min-max range */
input:in-range {
  border: 2px solid green;
  background-color: #e6ffe6;
}

/* When value is outside min-max range */
input:out-of-range {
  border: 2px solid red;
  background-color: #ffe6e6;
}

/* Combined with generated content for messaging */
input + span::after {
  display: none;
  position: absolute;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 3px;
  white-space: nowrap;
}

input:out-of-range + span::after {
  display: block;
  content: "Value outside allowable range (18-100)";
  background-color: red;
  color: white;
  top: -26px;
  left: -200px;
}

input:in-range + span::after {
  display: none;
}
```

**Key Points:**
- Applies only to numeric input types: `date`, `month`, `week`, `time`, `datetime-local`, `number`, `range`
- Out-of-range inputs also match `:invalid` (but `:out-of-range` is more semantically specific)
- Useful for providing specific messaging: "Value too high" vs generic "Invalid"
- In-range values also match `:valid`; out-of-range also match `:invalid`
- Numeric spinners on number inputs prevent exceeding min/max, but keyboard entry can violate limits

### 6. Enabled vs Disabled: `:enabled` and `:disabled`

The `:enabled` and `:disabled` pseudo-classes target form controls based on their disabled state, allowing styling of inactive form elements.

**Code Example:**
```html
<form>
  <div>
    <label for="name">Name:</label>
    <input id="name" name="name" type="text" />
  </div>
  <div>
    <label for="billing-same" class="billing-label">Same as shipping:</label>
    <input type="checkbox" id="billing-same" checked />
  </div>
  <div>
    <label for="billing-address" class="billing-label">Billing address:</label>
    <input id="billing-address" name="billing-address" type="text" disabled />
  </div>
  <button>Submit</button>
</form>
```

**CSS:**
```css
/* Enabled inputs - default interactive state */
input:enabled {
  border: 2px solid #ccc;
  background-color: white;
  cursor: text;
}

input:enabled:hover {
  border-color: #999;
}

/* Disabled inputs - not interactive */
input:disabled {
  border: 2px solid #ddd;
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Gray out labels associated with disabled inputs */
label:has(+ :disabled) {
  color: #999;
  font-weight: normal;
}

/* Disabled inputs don't respond to hover */
input:disabled:hover {
  border-color: #ddd;
  background-color: #f5f5f5;
}
```

**Key Behavior:**
- Disabled inputs cannot be focused, clicked, or edited
- Disabled input values are NOT submitted with form data
- `:enabled` is DEFAULT behavior; rarely needed explicitly unlike `:disabled`
- Form submission is blocked if validation constraints fail, regardless of `:disabled` styling
- Use `:has()` selector to target labels of disabled inputs: `label:has(+ :disabled)`

### 7. Read-Only vs Read-Write: `:read-only` and `:read-write`

The `:read-only` and `:read-write` pseudo-classes target form controls based on the `readonly` attribute, distinguishing between uneditable but submittable controls and fully editable ones.

**Code Example:**
```html
<!-- Confirmation page: user reviews and confirms previous data -->
<form>
  <div>
    <label for="name">Name:</label>
    <input id="name" name="name" type="text" value="John Doe" readonly />
  </div>
  <div>
    <label for="email">Email:</label>
    <input id="email" name="email" type="email" value="john@example.com" readonly />
  </div>
  <div>
    <label for="comments">Additional comments:</label>
    <textarea id="comments" name="comments" rows="5"></textarea>
  </div>
  <button>Submit Order</button>
</form>
```

**CSS:**
```css
/* Read-only inputs: can't edit, but values submit */
input:read-only,
textarea:read-only {
  background-color: #f9f9f9;
  border: none;
  border-bottom: 1px solid #ccc;
  color: #333;
  cursor: default;
  box-shadow: none;
}

input:read-only:focus,
textarea:read-only:focus {
  outline: none; /* Don't show focus style for read-only */
  background-color: #f9f9f9;
}

/* Read-write inputs: fully editable (default) */
textarea:read-write {
  background-color: white;
  border: 2px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

textarea:read-write:focus {
  border-color: #4a90e2;
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
}
```

**Critical Distinction:**
- **Read-only (`:read-only`):** User cannot edit; values ARE submitted; data goes to server
- **Disabled (`:disabled`):** User cannot edit; values are NOT submitted; data ignored
- Use read-only for review pages, confirmation flows where you need to preserve data
- Use disabled for conditional fields (e.g., "other" option fields when that option isn't selected)
- `:read-write` is rarely used because inputs default to read-write

### 8. Checkbox and Radio States: `:checked`, `:default`, `:indeterminate`

The `:checked` pseudo-class targets selected checkboxes and radio buttons. `:default` matches elements selected by default on page load. `:indeterminate` targets elements in an ambiguous state.

**Code Example:**
```html
<input type="checkbox" id="agree" name="agree" />
<label for="agree">I agree to terms</label>

<fieldset>
  <legend>Preferred color:</legend>
  <input type="radio" id="red" name="color" value="red" />
  <label for="red">Red</label>
  <input type="radio" id="blue" name="color" value="blue" checked />
  <label for="blue">Blue (default)</label>
  <input type="radio" id="green" name="color" value="green" />
  <label for="green">Green</label>
</fieldset>
```

**CSS:**
```css
/* Style checkbox appearance with custom box */
input[type="checkbox"] {
  appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  vertical-align: middle;
  transition: all 0.2s ease;
}

input[type="checkbox"]:checked {
  background-color: #4a90e2;
  border-color: #4a90e2;
}

/* Animated checkmark with ::before pseudo-element */
input[type="checkbox"]::before {
  content: "";
  display: block;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg) translate(2px, 2px) scale(0);
  transform-origin: center;
  transition: all 0.2s ease;
}

input[type="checkbox"]:checked::before {
  transform: rotate(45deg) translate(2px, 2px) scale(1);
}

/* Highlight default option label */
input:default ~ label {
  font-weight: bold;
  color: #333;
}

input:default ~ label::after {
  content: " (default)";
  font-size: 0.85rem;
  color: #999;
}

/* Indeterminate state (parent checkbox with mixed children selected) */
input[type="checkbox"]:indeterminate {
  background-color: #fff;
  border-color: #999;
}

input[type="checkbox"]:indeterminate::before {
  content: "";
  display: block;
  width: 10px;
  height: 2px;
  background-color: #999;
}
```

**States and Matching:**
- `:checked` — Matched when user selects a checkbox or radio button
- `:default` — Matches checkbox/radio with `checked` attribute on page load (even after user unchecks it)
- `:indeterminate` — Matches radios when NO radio in group is selected, or checkboxes when `indeterminate` property is `true` via JavaScript

### 9. Advanced Pseudo-Classes: `:focus-visible`, `:placeholder-shown`, `:user-invalid`

Additional UI pseudo-classes provide more nuanced control over form styling for specific use cases and user interactions.

**Code Example:**
```html
<input type="text" placeholder="Enter your name" />
<input type="email" />
```

**CSS:**
```css
/* :focus-visible - Show focus style only for keyboard focus, not mouse/touch */
input:focus-visible {
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
  border-color: #4a90e2;
}

/* Don't show outline for mouse focus (touch/mouse users don't need the visual) */
input:focus:not(:focus-visible) {
  outline: none;
}

/* :placeholder-shown - Style input while placeholder is visible (value is empty) */
input:placeholder-shown {
  background-image: linear-gradient(to right, #f9f9f9, white);
  border-color: #ddd;
}

input:placeholder-shown::placeholder {
  opacity: 0.5;
  color: #999;
}

/* Hide icon when placeholder shown, show when user starts typing */
input:placeholder-shown + .input-icon {
  opacity: 0;
}

input:not(:placeholder-shown) + .input-icon {
  opacity: 1;
}

/* :user-invalid (future pseudo-class, limited support) */
/* Matches :invalid only when user finishes editing (blur) and value is invalid */
/* More user-friendly than :invalid which shows errors while typing */
input:user-invalid {
  border: 3px solid red;
  background-color: #ffe6e6;
}
```

**Browser Support and Behavior:**
- `:focus-visible` — Well supported (Chrome 86+, Firefox 85+); keyboard focus receives outline, mouse/touch don't
- `:placeholder-shown` — Good support (95%+ of modern browsers); matches while placeholder text is visible
- `:user-invalid` — Limited/experimental support; future feature for better UX (don't show errors while typing)

### 10. Combining Pseudo-Classes for Complex State Logic

Multiple pseudo-classes can be chained together to target very specific form control states, creating sophisticated styling logic without JavaScript.

**Code Example:**
```html
<input id="age" name="age" type="number" min="18" max="100" required />
```

**CSS:**
```css
/* Complex selector: required number input that is valid and in-range */
input[type="number"]:required:valid:in-range {
  border: 3px solid green;
  background-color: #e6ffe6;
  background-image: url('checkmark.svg');
  background-position: right 8px center;
  background-repeat: no-repeat;
  padding-right: 32px;
}

/* Required input, invalid (empty) */
input[type="number"]:required:invalid:not(:focus) {
  border: 2px solid red;
  background-color: #ffe6e6;
}

/* Required input, invalid, and out of range (more specific) */
input[type="number"]:required:out-of-range {
  border: 2px solid red;
  background-color: #ffe6e6;
  box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
}

/* Disabled state takes precedence over validation states */
input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

input:disabled + label {
  color: #ccc;
  cursor: not-allowed;
}

/* Focus state for accessibility (highest precedence) */
input:focus {
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
}

/* Cascade ordering matters: later rules override earlier */
/* Ensure :disabilities styles override earlier rules */
fieldset:has(input:disabled) {
  background-color: #f5f5f5;
  border: 1px dashed #ccc;
}
```

**Specificity and Cascade Rules:**
- Each additional pseudo-class increases specificity equally
- Order matters: `:required:valid:in-range` is different from `:in-range:valid:required`
- Later rules override earlier ones (cascade)
- More specific selectors (more pseudo-classes) override less specific ones
- State changes (e.g., user action) update pseudo-class matches in real-time

---

## Technical Deep-Dive

### Deep-Dive 1: How `:valid` and `:invalid` Constraint Validation Works

**Scenario:** A form with email and age inputs. Email is optional; age is required with range limits. We need to style based on validation state and understand when each pseudo-class matches.

**Step 1: Page load (initial state)**
```html
<input type="email" id="email" name="email" />
<input type="number" id="age" name="age" min="18" max="100" required />
```

**Analysis:**
- Email input: No `required` attribute, value is empty
  - `:valid` matches (no constraints = valid when empty)
  - `:invalid` does NOT match
- Age input: `required` attribute, value is empty
  - `:invalid` matches (required + empty = invalid)
  - `:valid` does NOT match

**Step 2: User types "abc" in email field**
- Email validation checks if "abc" matches email pattern (no @ symbol)
- Result: `:invalid` matches (pattern mismatch)
- `:valid` does NOT match

**Step 3: User types "abc@example.com" in email**
- Email validation passes
- Result: `:valid` matches
- `:invalid` does NOT match

**Step 4: User types "10" in age field (out of range: min is 18)**
- Age validation checks constraints:
  - Is value required? Yes → has a value ✓
  - Is value in range [18-100]? No (10 < 18) ✗
- Result: `:invalid` matches AND `:out-of-range` matches (but `:out-of-range` is more specific)
- Browser shows both pseudo-classes match

**Step 5: User changes age to "25" (valid and in-range)**
- Age validation:
  - Is required? Yes → has a value ✓
  - Is in range [18-100]? Yes (25 is between 18-100) ✓
- Result: `:valid` matches AND `:in-range` matches
- `:invalid` does NOT match

**Step 6: User clears age field (return to empty)**
- Age validation:
  - Is required? Yes → value is empty ✗
- Result: `:invalid` matches again (required + empty)
- `:valid` does NOT match

**Key Insight:** Validation is continuous; pseudo-class matches update in real-time as the user types. The `:invalid` state appears temporarily while typing (e.g., "1" during typing of "25"), allowing you to show error messages incrementally.

---

### Deep-Dive 2: Generated Content Visibility and Layout Positioning

**Scenario:** Adding "required" indicators to form inputs using `::after` pseudo-element and generated content, positioned absolute relative to a relative-positioned span anchor.

**Step 1: HTML structure**
```html
<div>
  <label for="fname">First name:</label>
  <input id="fname" name="fname" type="text" required />
  <span></span> <!-- Anchor for generated content; width: 0 so doesn't affect layout -->
</div>
```

**Step 2: Making the layout predictable with flexbox**
```css
fieldset > div {
  display: flex;
  flex-flow: row wrap;
  margin-bottom: 20px;
}

label {
  width: 100%;
}

input {
  width: 100%;
}

input + span {
  width: 0; /* Collapse span to zero width; doesn't take up space */
  position: relative; /* Positioning context for generated content */
}
```

**Result:** Label takes full width on one line, input takes full width on another line, span has 0 width and doesn't create a line.

**Step 3: Positioning generated content**
```css
input:required + span::after {
  content: "required";
  position: absolute;
  top: -26px; /* Position above input */
  left: -70px; /* Position to left of span anchor (input's right edge) */
  background-color: black;
  color: white;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 0.75rem;
  white-space: nowrap; /* Prevent text wrap */
}
```

**Layout Calculation:**
- `input` element ends at x-coordinate (let's say 200px from left)
- `span` anchor is immediately after input, positioned at x: 200px to 200px (width: 0)
- `span` has `position: relative`, creating positioning context
- `::after` pseudo-element `left: -70px` = 200px - 70px = 130px from window left
- `top: -26px` = 26px above the span's baseline
- Result: "required" badge appears above and to the left of the input

**Step 4: When layout is responsive (mobile, narrower viewport)**
- Label width: 100% at 320px = displays normally
- Input width: 100% at 320px = displays normally
- Span: 0 width, positioned relative to input end
- Generated content positioning remains calculated from CSS values
- Text may overflow viewport if left: -70px puts it beyond left edge on narrow screens

**Solution:** Use media queries to adjust positioning on narrow viewports:
```css
@media (max-width: 480px) {
  input:required + span::after {
    top: 42px; /* Position below instead of above */
    left: 0; /* Align with input left edge */
  }
}
```

**Key Insight:** Generated content positioning is context-dependent; always consider the layout (flex, grid, absolute positioning context) when calculating absolute positioning values.

---

### Deep-Dive 3: Disabling Form Groups and Styles with `:has()` Pseudo-Class

**Scenario:** A billing address form section is disabled conditionally based on a "same as shipping" checkbox. When disabled, all inputs in the section are disabled, and their labels should gray out. Use `:has()` to style labels based on their associated inputs' state.

**Step 1: HTML structure**
```html
<fieldset id="billing">
  <legend>Billing address</legend>
  
  <div>
    <input type="checkbox" id="billing-same" checked />
    <label for="billing-same">Same as shipping address</label>
  </div>
  
  <div>
    <label for="billing-name" class="billing-label">Name:</label>
    <input 
      id="billing-name" 
      name="billing-name" 
      type="text" 
      disabled 
      required 
    />
  </div>
  
  <div>
    <label for="billing-address" class="billing-label">Address:</label>
    <input 
      id="billing-address" 
      name="billing-address" 
      type="text" 
      disabled 
      required 
    />
  </div>
</fieldset>
```

**Step 2: JavaScript toggle function**
```javascript
const checkbox = document.getElementById('billing-same');
const billingInputs = document.querySelectorAll('#billing input[type="text"]');

function toggleBillingFields() {
  billingInputs.forEach(input => {
    input.disabled = !input.disabled;
  });
}

checkbox.addEventListener('change', toggleBillingFields);
```

When checkbox is checked (initially): all billing inputs get `disabled` attribute.
When user unchecks: `disabled` attribute removed.

**Step 3: Styling disabled inputs and associated labels with `:has()`**
```css
/* Style disabled inputs */
input[type="text"]:disabled {
  background-color: #eeeeee;
  border: 1px solid #cccccc;
  color: #999;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Style labels that precede disabled inputs using :has() pseudo-class */
label:has(+ :disabled) {
  color: #aaaaaa;
  font-weight: normal;
  cursor: not-allowed;
}
```

**How `:has(+ :disabled)` works:**
1. `:has()` is a "parent selector" that matches elements containing specific descendants
2. `+ :disabled` is "the immediate next sibling is a disabled element"
3. `label:has(+ :disabled)` matches: "Label element that has an immediately-following disabled sibling"
4. In HTML: `<label>Name:</label><input disabled />` → label matches `:has(+ :disabled)`

**Step 4: Real-time update when toggling**
When checkbox is clicked:
1. JavaScript removes/adds `disabled` attribute on inputs
2. `:disabled` pseudo-class match updates in real-time
3. `label:has(+ :disabled)` pseudo-class match updates because the `:disabled` match changed
4. CSS styles automatically apply/remove without JavaScript intervention

**Result:**
- Initial: All billing labels gray out (`:has(+ :disabled)` matches)
- User unchecks: JavaScript removes `disabled` attributes
- Immediately after: Labels un-gray (`:has()` match updates automatically)

**Browser Support:** `:has()` was experimental but now has good support (Chrome 105+, Firefox 121+, Safari 15.4+).

---

## Key Terminology Bank

1. **`:required` pseudo-class** — Matches form controls that have the `required` HTML attribute, indicating the field must be filled before form submission.

2. **`:optional` pseudo-class** — Matches form controls that don't have the `required` attribute (default state for most form inputs).

3. **`:valid` pseudo-class** — Matches form controls whose current value satisfies all constraint validation rules (min/max, pattern, type-specific validation, etc.).

4. **`:invalid` pseudo-class** — Matches form controls whose current value violates constraint validation (required + empty, pattern mismatch, out of range, etc.).

5. **`:in-range` pseudo-class** — Matches numeric form controls (number, date, range, etc.) whose value is within the min and max attribute limits.

6. **`:out-of-range` pseudo-class** — Matches numeric form controls whose value falls outside the min/max range limits.

7. **`:enabled` pseudo-class** — Matches form controls that are not disabled (default interactive state; rarely used explicitly).

8. **`:disabled` pseudo-class** — Matches form controls that have the `disabled` HTML attribute, making them uneditable and preventing value submission.

9. **`:read-only` pseudo-class** — Matches form controls with the `readonly` HTML attribute (values cannot be edited but ARE submitted with the form).

10. **`:read-write` pseudo-class** — Matches form controls that are editable (default state; `readonly` attribute not set).

11. **`:checked` pseudo-class** — Matches radio buttons and checkboxes that are currently selected/checked by the user.

12. **`:default` pseudo-class** — Matches radio buttons and checkboxes that have the `checked` attribute on page load (matches even if user later unchecks them).

13. **`:indeterminate` pseudo-class** — Matches radio button groups when no button is selected, checkboxes with `indeterminate` property set to `true` via JavaScript, or progress elements with no value.

14. **Constraint validation** — HTML5 mechanism that validates form control values clientside using attributes like `required`, `min`, `max`, `pattern`, `type` (email, url, number).

15. **`:focus-visible` pseudo-class** — Matches focused elements that received focus via keyboard interaction (not mouse or touch), enabling keyboard-specific focus indicators.

16. **`:focus` pseudo-class** — Matches elements that have keyboard or click focus, regardless of interaction method.

17. **`:placeholder-shown` pseudo-class** — Matches form inputs whose placeholder text is visible (value is empty) because the user hasn't entered data.

18. **Generated content** — CSS `content` property on `::before` and `::after` pseudo-elements that creates visual elements without adding DOM nodes.

19. **`position: relative` context** — Positioning property that makes an element a positioning context for `position: absolute` descendants (including pseudo-elements).

20. **`:has()` pseudo-class** — Functional selector that matches elements containing specific descendants/selectors (e.g., `label:has(+ :disabled)` matches labels before disabled inputs).

21. **Cascade rules** — CSS specificity and declaration order rules that determine which styles apply when multiple rules target the same element.

22. **Accessibility tree** — Browser data structure exposing semantic information to assistive technologies; pseudo-element-generated content is NOT in the accessibility tree.

---

## Watch Out For

### 1. ⚠️ Generated content is NOT announced by screen readers

**Misconception:** "I'll use `::after { content: "required"; }` to add a 'required' indicator, and screen reader users will hear it."

**Reality:** CSS-generated content via `content` property is NOT in the accessibility tree. Screen readers don't announce it. A user with a screen reader might miss critical information you intended to convey.

**Why it matters:** Accessibility violations; some users don't receive important form information.

**What to do:** Use generated content only for redundant visual indicators. Combine with alternate semantic methods (e.g., semantic HTML, `aria-required="true"`). Keep generated content purely visual.

---

### 2. ⚠️ Text input types don't support pseudo-elements

**Misconception:** "I'll style checkmarks inside text inputs using `input[type="text"]::before { content: "✓"; }`."

**Reality:** Text input types (`text`, `password`, `email`, `url`, `tel`, `search`) don't display pseudo-element content. Only non-text inputs (radio, checkbox, range, color, etc.) support pseudo-elements.

**Why it matters:** Your generated checkmark won't appear; code silently fails with no error message.

**What to do:** For text inputs, use adjacent elements as anchors: `<input /><span></span>` then style `input + span::after`.

---

### 3. ⚠️ `:invalid` matches DURING typing, causing jarring error messages

**Misconception:** "`:invalid` will show error messages only when the user finishes editing."

**Reality:** `:invalid` matches immediately when validation fails, even while the user is mid-typing. An email input shows `:invalid` while typing "j" before "john@example.com" is complete.

**Why it matters:** Error messages appear prematurely, annoying users and creating poor UX.

**What to do:** Style `:invalid` more subtly for in-progress work (e.g., light red border). Use `:user-invalid` (future pseudo-class with better support soon) or JavaScript change/blur events for error message triggering. Show errors on blur event, not real-time.

---

### 4. ⚠️ Required attribute on one radio in a group affects ALL radios

**Misconception:** "I'll put `required` on one radio button in a group so at least one must be selected."

**Reality:** Setting `required` on one radio button makes ALL radios in the group (same `name` attribute) invalid until ANY one is selected. However, only the radio with `required` attribute matches `:required` pseudo-class.

**Why it matters:** CSS selector `:required` may not match all affected radios; logic doesn't match user perception that all radios are required.

**What to do:** Set `required` on the parent fieldset conceptually, not individual radios. Use JavaScript or form validation to provide clear messaging about group-level requirements.

---

### 5. ⚠️ `:read-only` inputs submit values; `:disabled` inputs don't

**Misconception:** "`:disabled` and `:read-only` are the same; both prevent editing."

**Reality:** Both prevent editing, but `:disabled` values don't submit with the form (discarded). `:read-only` values ARE submitted (preserved).

**Why it matters:** Accidentally using wrong pseudo-class causes data loss or unwanted submissions.

**What to do:** Use `:disabled` for fields that don't apply to the current user. Use `:read-only` for review/confirmation pages where you need to preserve pre-filled data. Clear distinction: `:disabled` = no data, `:read-only` = unchangeable data.

---

### 6. ⚠️ Empty inputs without `required` are `:valid`, not `:invalid`

**Misconception:** "Empty inputs with validation constraints (like min/max) are `:invalid`."

**Reality:** Optional inputs (no `required` attribute) are `:valid` when empty, even if they have type="email" or min/max constraints. Validation only applies when the field has a value.

**Why it matters:** Error styling doesn't appear on optional empty fields (correct behavior), but it can seem like validation is broken when it's not.

**What to do:** Understand that validation is constraint-based, not presence-based. Empty optional fields are always valid. Validation errors only appear when: (1) required + empty, or (2) required/optional + value does exist and violates constraints.

---

### 7. ⚠️ `:focus` matches any focus, but `:focus-visible` only keyboard focus

**Misconception:** "`:focus-visible` matches both keyboard and mouse focus for better visibility."

**Reality:** `:focus` matches ANY focus (keyboard, mouse, touch, API). `:focus-visible` only matches keyboard focus (or browser deems it needed for accessibility).

**Why it matters:** Mouse users see no outline with `:focus-visible` (intentional), but if you remove `:focus` styling entirely, users have no focus indicator.

**What to do:** Keep `:focus` styling for accessibility, but use `:focus-visible` for keyboard-specific styles. Best practice: `input:focus-visible { outline: ... }` and `input:focus:not(:focus-visible) { outline: none; }`.

---

### 8. ⚠️ Cascade order determines which pseudo-class style wins when multiple match

**Misconception:** "`:invalid` styles will always override `:required` styles."

**Reality:** CSS cascade applies; whichever CSS rule appears LATER in the stylesheet wins, regardless of pseudo-class names.

**Why it matters:** Earlier rules get overridden silently; expected styling doesn't appear.

**What to do:** Understand the cascade. Place more specific/important styles later in the CSS. For complex state interactions (`:required:invalid:out-of-range`), order selectors intentionally and verify with DevTools that correct rule applies.

---

### 9. ⚠️ Color-only styling violates accessibility for required/invalid states

**Misconception:** "I'll use `input:required { border-color: red; } input:optional { border-color: green; }` to distinguish required from optional."

**Reality:** Colorblind users can't distinguish red from green. WCAG standards require non-color indicators (icons, borders, symbols) for critical information.

**Why it matters:** Accessibility violations; some users can't determine which fields are required.

**What to do:** Use multiple indicators: color + icon + symbol + text. Examples: `border: 4px solid red` (thick border) + `::after { content: " *"; color: red; }` (asterisk) + `aria-required="true"` (semantic).

---

### 10. ⚠️ `:has()` browser support is recent; older browsers don't recognize it

**Misconception:** "I'll use `label:has(+ :disabled)` to style labels of disabled inputs in all browsers."

**Reality:** `:has()` pseudo-class only recently gained browser support (Chrome 105+, Firefox 121+, Safari 15.4+). Older browsers don't recognize it; the selector is ignored.

**Why it matters:** Styling fails silently in unsupported browsers; labels don't gray out as intended.

**What to do:** Use feature detection with `@supports` or provide JavaScript fallback for older browsers. For robust support, use adjacent sibling combinator with adjusted HTML structure or JavaScript-based classes.

---

## Active Recall: Exam-Ready Questions

### Question 1: Recall - Name the main UI pseudo-classes for form validation states

**Difficulty: Recall**

List the six primary UI pseudo-classes that target form validation and constraint states, and explain what each matches.

<details>
<summary>Answer</summary>

The six primary UI pseudo-classes for validation are:

1. **`:required`** — Matches form controls with the `required` HTML attribute; indicates the field must be filled.

2. **`:optional`** — Matches form controls without the `required` attribute (default state); field is not required to be filled.

3. **`:valid`** — Matches form controls whose current value satisfies all constraint validation rules (type validation, pattern, min/max, etc.).

4. **`:invalid`** — Matches form controls whose current value violates constraint validation (required + empty, pattern mismatch, out-of-range values).

5. **`:in-range`** — Matches numeric form controls (number, date, range, etc.) whose value is within the min and max attribute limits.

6. **`:out-of-range`** — Matches numeric form controls whose value exceeds the min/max range limits.

**Additional related pseudo-classes:**
- `:enabled` — Interactive form controls (default state); not disabled
- `:disabled` — Form controls with `disabled` attribute; not interactive
- `:read-only` — Form controls with `readonly` attribute; can't be edited but values submit
- `:read-write` — Editable form controls (default state); `readonly` attribute not set
- `:checked` — Selected checkboxes and radio buttons
- `:default` — Radio buttons and checkboxes with `checked` attribute on page load
- `:indeterminate` — Radio groups with no selection, checkboxes with `indeterminate` property true

</details>

---

### Question 2: Application - Build form validation styling with generated content indicators

**Difficulty: Application**

Write HTML and CSS to create a form with visual validation indicators. Include: (1) "required" label using generated content, (2) valid checkmark, (3) invalid X mark. Show both input and adjacent span structure.

<details>
<summary>Answer</summary>

**HTML:**
```html
<form>
  <div class="form-group">
    <label for="email">Email:</label>
    <input id="email" name="email" type="email" required />
    <span class="indicator"></span>
  </div>
  
  <div class="form-group">
    <label for="age">Age (18-100):</label>
    <input id="age" name="age" type="number" min="18" max="100" required />
    <span class="indicator"></span>
  </div>
  
  <button type="submit">Submit</button>
</form>
```

**CSS:**
```css
.form-group {
  display: flex;
  flex-flow: row wrap;
  margin-bottom: 20px;
  position: relative;
}

label {
  width: 100%;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.indicator {
  width: 0;
  position: relative;
}

/* "required" label using generated content */
input:required + .indicator::after {
  content: "required";
  position: absolute;
  top: -26px;
  left: -70px;
  background-color: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 0.75rem;
  white-space: nowrap;
  pointer-events: none;
}

/* Valid input styling */
input:valid {
  border-color: green;
  background-color: #f0fff0;
}

input:valid + .indicator::before {
  content: "✓";
  position: absolute;
  right: -24px;
  top: 10px;
  color: green;
  font-size: 1.2rem;
  font-weight: bold;
}

/* Invalid input styling */
input:invalid {
  border-color: red;
  background-color: #fff0f0;
}

input:invalid + .indicator::before {
  content: "✗";
  position: absolute;
  right: -24px;
  top: 10px;
  color: red;
  font-size: 1.2rem;
  font-weight: bold;
}

/* Required + empty = invalid; show urgent styling */
input:required:invalid:not(:focus) {
  border-width: 3px;
  box-shadow: 0 0 0 3px rgba(255, 0, 0, 0.1);
}

/* Focus state overrides invalid state for better UX */
input:focus {
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
}

/* Optional email inputs are valid when empty */
input:optional:invalid::placeholder {
  opacity: 0.3;
}

/* Out-of-range styling supersedes general invalid */
input:out-of-range {
  border-color: #ff8c00;
  background-color: #fff8f0;
}

button {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #2e5c8a;
}
```

**Result:**
- "required" label appears above required fields
- Green checkmark appears when input is valid
- Red X mark appears when input is invalid
- Out-of-range numbers show orange border
- Focus state provides keyboard accessibility indicator

</details>

---

### Question 3: Analysis - Explain why `:invalid` styling appears mid-typing and how to improve UX

**Difficulty: Analysis**

A form shows red error styling on email input while the user is typing "j" (incomplete email). Explain why this happens, why it's poor UX, and how to fix it using pseudo-classes and/or events.

<details>
<summary>Answer</summary>

**Why it happens:**

`:invalid` pseudo-class matches immediately when validation fails. As the user types "j" into an email field:
1. Browser validates: "j" against email pattern (must contain `@` symbol)
2. Pattern doesn't match → `:invalid` pseudo-class matches
3. CSS rule applies: `input:invalid { border: 2px solid red; background-color: #fff0f0; }`
4. Red styling appears mid-typing

This occurs for every keystroke until a valid email is entered.

---

**Why it's poor UX:**

1. **Premature error messages** — Users see "invalid" error while they're still composing the address (not finished)
2. **Cognitive overload** — Users focus on fixing the error instead of completing their thought
3. **Discourages form completion** — Negative feedback while in progress feels punishing
4. **Mobile issues** — Triggers keyboards to show error states prematurely on touch devices

---

**Solutions:**

**Solution 1: Softer styling during input (blur-based errors)**

```css
/* Subtle styling during input; data is just incomplete, not necessarily wrong */
input:invalid {
  border: 1px solid #ffcc00; /* Light warning, not error */
  background-color: white; /* No background change */
}

/* Show prominent error only after user leaves the field (blur) */
input:invalid:not(:focus) {
  border: 2px solid red;
  background-color: #fff0f0;
}

/* No error styling on optional empty inputs */
input:optional:invalid {
  border: 1px solid #ccc;
  background-color: white;
}
```

**Solution 2: Use `:user-invalid` pseudo-class (future, limited support)**

```css
/* Only show prominent error after user finishes editing */
input:user-invalid {
  border: 2px solid red;
  background-color: #fff0f0;
}

/* While typing (focus), no error styling */
input:user-invalid:focus {
  border: 1px solid #ffcc00;
  background-color: white;
}
```

**Solution 3: JavaScript blur event (robust, works now)**

```javascript
const emailInput = document.querySelector('input[type="email"]');

// Only show errors after user leaves the field
emailInput.addEventListener('blur', function() {
  if (!this.validity.valid) {
    this.classList.add('show-error');
  }
});

// Clear error class when user starts typing again
emailInput.addEventListener('input', function() {
  this.classList.remove('show-error');
});
```

```css
input:invalid.show-error {
  border: 2px solid red;
  background-color: #fff0f0;
}

input:invalid:not(.show-error) {
  border: 1px solid #ccc;
}
```

**Solution 4: Combine soft `:invalid` with positive `:valid` feedback**

```css
/* Optional inputs: only show styling if user has typed something */
input:optional {
  border: 1px solid #ccc;
}

input:optional:valid {
  border: 1px solid green;
  background-color: #f0fff0;
}

input:optional:invalid:not(:focus) {
  border: 2px solid red;
  background-color: #fff0f0;
}

/* Required inputs: be strict but forgiving during focus */
input:required:invalid:focus {
  border: 1px solid #ffcc00;
  background-color: white;
}

input:required:invalid:not(:focus) {
  border: 2px solid red;
  background-color: #fff0f0;
}
```

**Best Practice Hybrid:**
1. Use `:invalid:focus` for soft warning (yellow border) while typing
2. Use `:invalid:not(:focus)` for error state (red border) after blur
3. Use `:valid` to show green checkmark when field is correct
4. Always provide live error message only on blur, not during typing
5. Combine CSS with JavaScript for best UX and browser support

</details>

---

### Question 4: Synthesis - Design disabled form fields with labels that gray out automatically using `:has()`

**Difficulty: Synthesis**

Create a shipping/billing address form where a checkbox toggles whether billing fields are disabled. Use CSS `:has()` to automatically gray out labels of disabled inputs without JavaScript selection. Include HTML, CSS, and JavaScript toggle.

<details>
<summary>Answer</summary>

**HTML:**
```html
<form>
  <fieldset id="shipping">
    <legend>Shipping Address</legend>
    <div class="form-group">
      <label for="ship-name">Name:</label>
      <input id="ship-name" name="ship-name" type="text" required />
    </div>
    <div class="form-group">
      <label for="ship-address">Address:</label>
      <input id="ship-address" name="ship-address" type="text" required />
    </div>
  </fieldset>

  <fieldset id="billing">
    <legend>Billing Address</legend>
    <div class="form-group">
      <label for="billing-same">
        <input type="checkbox" id="billing-same" checked />
        Same as shipping address
      </label>
    </div>

    <div class="form-group">
      <label for="bill-name">Name:</label>
      <input 
        id="bill-name" 
        name="bill-name" 
        type="text" 
        disabled 
        required 
      />
    </div>
    <div class="form-group">
      <label for="bill-address">Address:</label>
      <input 
        id="bill-address" 
        name="bill-address" 
        type="text" 
        disabled 
        required 
      />
    </div>
  </fieldset>

  <button type="submit">Submit Order</button>
</form>
```

**CSS:**
```css
form {
  max-width: 500px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

fieldset {
  border: 2px solid #ddd;
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 20px;
}

legend {
  font-size: 1.1rem;
  font-weight: bold;
  padding: 0 10px;
  margin-left: -10px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
  transition: color 0.3s ease;
}

/* Key: Gray out label when it precedes a disabled input */
label:has(+ :disabled) {
  color: #999;
  font-weight: 400;
  cursor: not-allowed;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input[type="text"]:enabled {
  background-color: white;
}

input[type="text"]:enabled:focus {
  border-color: #4a90e2;
  outline: 3px solid rgba(74, 144, 226, 0.1);
}

/* Disabled inputs: grayed out, not interactive */
input[type="text"]:disabled {
  background-color: #f5f5f5;
  border-color: #ddd;
  color: #999;
  cursor: not-allowed;
  opacity: 0.7;
}

input[type="text"]:disabled:focus {
  outline: none;
}

/* Checkbox styling */
input[type="checkbox"] {
  margin-right: 8px;
  cursor: pointer;
  vertical-align: middle;
}

/* Label for checkbox is directly around the checkbox, not using :has() */
label:has(input[type="checkbox"]) {
  display: flex;
  align-items: center;
  color: #333;
  font-weight: 500;
  cursor: pointer;
}

/* Fieldset styling when billing fields are disabled */
#billing:has(input[type="text"]:disabled) {
  background-color: #f9f9f9;
  border-color: #ddd;
  opacity: 0.8;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover:not(:disabled) {
  background-color: #2e5c8a;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
```

**JavaScript:**
```javascript
const billingCheckbox = document.getElementById('billing-same');
const billingInputs = document.querySelectorAll('#billing input[type="text"]');

function toggleBillingFields() {
  billingInputs.forEach(input => {
    input.disabled = !input.disabled;
  });
}

billingCheckbox.addEventListener('change', toggleBillingFields);
```

**How it works:**

1. **Initial state:** Checkbox is checked; all billing text inputs have `disabled` attribute
2. **CSS selectors activate:**
   - `label:has(+ :disabled)` matches labels before disabled inputs
   - Labels gray out automatically with `color: #999`
3. **User unchecks checkbox:**
   - JavaScript removes `disabled` attribute from all billing inputs
4. **CSS updates automatically:**
   - `:disabled` pseudo-class no longer matches
   - `label:has(+ :disabled)` no longer matches
   - Labels color changes from `#999` back to `#333` instantly
   - Input styling changes from grayed-out to interactive

**Result:**
- Zero DOM manipulation for styling (purely CSS)
- `:has()` makes selectors update automatically when pseudo-class matches change
- No need to add/remove classes manually
- Clean separation of concerns: JavaScript handles state, CSS handles presentation

**Browser support:** `:has()` supported in Chrome 105+, Firefox 121+, Safari 15.4+. For older browsers, add JavaScript fallback or use adjacent sibling combinator with different HTML structure.

</details>

---

### Question 5: Evaluation - Identify issues in this form validation styling implementation

**Difficulty: Evaluation**

Review this form code and identify all CSS and HTML issues, accessibility problems, and UX concerns:

```html
<input type="email" id="email" required />
<input type="password" id="password" required />
```

```css
input:invalid {
  border: 2px solid red;
  background-color: #ffcccc;
}

input:required::after {
  content: "*";
  color: red;
  margin-left: 5px;
}

input:disabled {
  opacity: 0.5;
}
```

<details>
<summary>Answer</summary>

**Issue 1: Text inputs don't display pseudo-element content**
- **Problem:** `input:required::after { content: "*"; }` won't work on text inputs
- **Why:** Input type="email" and type="password" don't support pseudo-elements; generated content doesn't display
- **Symptom:** Red asterisk never appears on required fields
- **Fix:** Use adjacent element: `<input /><span class="required">*</span>`

---

**Issue 2: Validation errors show mid-typing, poor UX**
- **Problem:** `:invalid { border: red; background: #ffcccc; }` styling appears immediately
- **Why:** Email input shows invalid while user types "j" (incomplete email not yet valid)
- **Symptom:** User sees error message while still composing; red styling during normal input
- **Fix:** Soften `:invalid:focus` styling, show errors only on `:invalid:not(:focus)` (after blur)

---

**Issue 3: Color-only accessibility violation**
- **Problem:** Using only red border and red background as distinguishing indicators
- **Why:** Colorblind users can't distinguish red from other colors
- **Accessibility:** WCAG violation; fails color contrast and color-only requirements
- **Fix:** Add non-color indicators: `border: 3px solid red; border-left: 5px solid red;` (thick borders) or icon/symbol

---

**Issue 4: No label associations**
- **Problem:** No `<label>` elements; no `id` linking to inputs
- **Why:** Screen readers can't match labels to inputs; form not semantically correct
- **Accessibility:** WCAG failure; users relying on screen readers don't know what each input is for
- **Fix:** Add labels: `<label for="email">Email:</label><input id="email" />`

---

**Issue 5: No focus indicator**
- **Problem:** No `:focus` styling on inputs; keyboard users can't see which input has focus
- **Why:** Accessibility requirement; keyboard navigation requires visible focus
- **Accessibility:** WCAG failure; keyboard-only users can't navigate form effectively
- **Fix:** Add `input:focus { outline: 3px solid #4a90e2; outline-offset: 2px; }`

---

**Issue 6: Opacity alone for disabled state accessibility**
- **Problem:** `input:disabled { opacity: 0.5; }` makes inputs harder to see but doesn't clearly indicate disabled
- **Why:** Opacity alone doesn't convey that field is disabled; users might click/tab to disabled field
- **Accessibility:** Disabled state not clearly communicated
- **Fix:** Add multiple indicators: `background-color: #f5f5f5; border: 1px solid #ddd; color: #999; cursor: not-allowed;`

---

**Issue 7: Required styling missing**
- **Problem:** No way to tell visually that fields are required (pseudo-element workaround fails)
- **Why:** No visual indicator of required status besides HTML attribute
- **Solution:** Add legend text: `<p>Fields marked with * are required.</p>` + adjacent span with asterisk

---

**Issue 8: No form structure**
- **Problem:** Inputs exist without `<form>`, `<fieldset>`, or semantic wrapper
- **Why:** Not semantic HTML; form purpose unclear
- **Accessibility:** Screen readers get no context; not semantically valid
- **Fix:** Wrap in `<form><fieldset><legend>Form Title</legend>...</fieldset></form>`

---

**Issue 9: Missing submit button**
- **Problem:** No way to submit the form (no button)
- **Why:** Form is incomplete; can't be used
- **Fix:** Add `<button type="submit">Submit</button>`

---

**Corrected version:**

```html
<form id="login">
  <fieldset>
    <legend>Login Form</legend>
    <p>Fields marked with <span class="required-indicator">*</span> are required.</p>
    
    <div class="form-group">
      <label for="email">Email <span class="required-indicator">*</span></label>
      <input 
        id="email" 
        name="email" 
        type="email" 
        required 
        aria-required="true"
      />
    </div>
    
    <div class="form-group">
      <label for="password">Password <span class="required-indicator">*</span></label>
      <input 
        id="password" 
        name="password" 
        type="password" 
        required 
        aria-required="true"
      />
    </div>
    
    <button type="submit">Sign In</button>
  </fieldset>
</form>
```

```css
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.required-indicator {
  color: red;
  font-weight: bold;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus {
  border-color: #4a90e2;
  outline: 3px solid rgba(74, 144, 226, 0.2);
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* Soft styling while focus (user still typing) */
input:required:invalid:focus {
  border-color: #ffcc00;
  background-color: white;
}

/* Prominent error after blur (user left field) */
input:required:invalid:not(:focus) {
  border: 3px solid red;
  border-left: 5px solid red;
  background-color: #fff5f5;
}

input:required:valid {
  border-color: green;
  background-color: #f5fff5;
}

input:disabled {
  background-color: #f5f5f5;
  border-color: #ddd;
  color: #999;
  cursor: not-allowed;
}

button {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background-color: #2e5c8a;
}

button:focus-visible {
  outline: 3px solid #4a90e2;
  outline-offset: 2px;
}
```

**Summary of fixes:**
✅ Removed failing pseudo-element on text inputs
✅ Soft `:invalid:focus` + prominent `:invalid:not(:focus)` for UX
✅ Added non-color indicators (thick borders, multiple visual cues)
✅ Added associated labels and semantic structure
✅ Added focus indicators for accessibility
✅ Clear disabled state with multiple properties
✅ Added form, fieldset, legend for semantic HTML
✅ Added submit button
✅ Added `aria-required` for screen readers
✅ Added comprehensive focus and accessibility styling

</details>

---

## Summary

UI pseudo-classes provide powerful, declarative ways to style form controls based on their state without JavaScript. `:required/:optional` distinguish field requirements. `:valid/:invalid/:in-range/:out-of-range` communicate validation status. `:enabled/:disabled/:read-only/:read-write` control interactivity. `:checked/:default/:indeterminate` manage checkbox/radio states. Combined with pseudo-elements (`::before`, `::after`) for generated content, `:has()` for dependent styling, and proper understanding of the CSS cascade, UI pseudo-classes enable comprehensive form styling while maintaining accessibility and progressive enhancement principles.

---

**Next Steps for Mastery:**
- Build a complex multi-step form with conditional field validation using UI pseudo-classes
- Create accessible form validation feedback without JavaScript state management
- Implement `:user-invalid` pattern with JavaScript fallbacks for browsers without support
- Design form styling systems that work across multiple form patterns (login, checkout, survey)
- Test form accessibility with screen readers and keyboard-only navigation
