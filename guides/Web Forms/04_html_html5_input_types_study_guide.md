# 📚 HTML5 Input Types — Exam Study Guide
**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/HTML5_input_types

---

## Executive Summary

HTML5 introduced specialized input types that provide built-in browser validation and improved user experience across devices. These input types (`email`, `tel`, `url`, `number`, `range`, `date`, `time`, `color`) extend the basic text input with semantic meaning and platform-optimized controls. Mastering these types is critical for creating modern, accessible forms that work seamlessly on both desktop and mobile devices.

---

## Core Pillars

### 1. Email Input Type
The `email` input type enforces that values must be valid email addresses and provides built-in client-side validation.

- Created with `<input type="email" />`
- Browser validates format before form submission
- Invalid entries trigger the `:invalid` pseudo-class and set `validityState.typeMismatch` to `true`
- By default allows intranet addresses (e.g., `a@b` is valid)
- The `multiple` attribute allows comma-separated email addresses in a single field
- On touch devices, browsers typically display an `@` key on the virtual keyboard
- Client-side validation is helpful but **not a security measure** — server-side validation is always required

**Code Example:**
```html
<input type="email" id="email" name="email" />

<!-- Allow multiple emails -->
<input type="email" id="emails" name="emails" multiple />
```

### 2. Search Input Type
The `search` input type creates a specialized text field optimized for search functionality.

- Created with `<input type="search" />`
- Visually styled differently in browsers (rounded corners in some, clear icon in others)
- Many browsers display an "Ⓧ" clear button when the field has focus and contains a value
- The clear button appears only when the field has a value and is focused (except Safari, where it may appear differently)
- On devices with dynamic keyboards, the enter key often displays "search" or a magnifying glass icon
- Browsers automatically save and reuse search values for autocomplete across pages of the same site
- Primary difference from `text` type is styling and browser-level autocomplete behavior

**Code Example:**
```html
<input type="search" id="search" name="search" />
```

### 3. Phone Number Input Type
The `tel` input type is designed specifically for telephone number entry.

- Created with `<input type="tel" />`
- **Does not enforce format validation** — accepts letters, numbers, and special characters (wide variety of international formats exist)
- On touch devices with dynamic keyboards, displays a numeric keypad
- Useful anywhere a numeric keypad is beneficial, not just for phone numbers
- The `pattern` attribute can be used to enforce specific format constraints
- No built-in validation, so validation must be implemented via `pattern` attribute or JavaScript if needed

**Code Example:**
```html
<input type="tel" id="tel" name="tel" />

<!-- With pattern validation -->
<input type="tel" id="phone" name="phone" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" />
```

### 4. URL Input Type
The `url` input type is specialized for entering web addresses with built-in format validation.

- Created with `<input type="url" />`
- Requires a valid protocol (e.g., `http:`, `https:`, `ftp:`) and proper URL structure
- Browser validates that the value is a well-formed URL before submission
- A well-formed URL doesn't guarantee the location actually exists — validation only checks syntax
- On touch devices, virtual keyboards typically display colon, period, and forward slash as default keys
- Triggers `:invalid` pseudo-class if the URL is malformed or missing a protocol

**Code Example:**
```html
<input type="url" id="url" name="url" />
```

### 5. Number Input Type
The `number` input type creates a control for entering floating-point numbers with spinner buttons.

- Created with `<input type="number" />`
- Appears as a text field but only accepts numeric input
- Includes spinner buttons (up/down arrows) to increment/decrement values
- On touch devices displays a numeric keyboard
- Supports `min` and `max` attributes to constrain the range of valid values
- Supports `step` attribute to control increment amounts (defaults to `1`, allowing only integers)
- Use `step="any"` to allow any float value, or `step="0.01"` for specific decimal precision
- If `step` is omitted, only whole numbers are valid (step defaults to `1`)

**Code Example:**
```html
<!-- Odd numbers 1-10, incrementing by 2 -->
<input type="number" name="age" id="age" min="1" max="10" step="2" />

<!-- Decimal values 0-1, incrementing by 0.01 -->
<input type="number" name="change" id="pennies" min="0" max="1" step="0.01" />
```

### 6. Range Slider Input Type
The `range` input type creates a slider control for picking a number within a specified range.

- Created with `<input type="range" />`
- Movable via mouse, touch, or keyboard arrow keys
- Less accurate than text fields, used when precise values are not critical
- Supports `min`, `max`, and `step` attributes (highly recommended for proper configuration)
- Sliders provide no visual feedback of the current value; use `<output>` element to display value
- The `<output>` element can take a `for` attribute linking it to the range input
- Common to update `<output>` via JavaScript `input` event listener

**Code Example:**
```html
<label for="price">Choose a maximum house price:</label>
<input
  type="range"
  name="price"
  id="price"
  min="50000"
  max="500000"
  step="1000"
  value="250000" />
<output class="price-output" for="price"></output>

<script>
const price = document.querySelector("#price");
const output = document.querySelector(".price-output");

output.textContent = price.value;

price.addEventListener("input", () => {
  output.textContent = price.value;
});
</script>
```

### 7. Date and Time Picker Input Types
HTML5 provides multiple specialized input types for selecting dates and times with native browser pickers.

**`date`** — Selects year, month, and day (no time)
```html
<input type="date" name="date" id="date" />
```

**`datetime-local`** — Selects date and time without timezone information
```html
<input type="datetime-local" name="datetime" id="datetime" />
```

**`month`** — Selects month and year
```html
<input type="month" name="month" id="month" />
```

**`time`** — Selects time in 24-hour format (even if displayed in 12-hour format)
```html
<input type="time" name="time" id="time" />
```

**`week`** — Selects a specific week number and year
- Weeks start on Monday and run through Sunday
- Week 1 of each year contains the first Thursday of that year (may not include Jan 1)
```html
<input type="week" name="week" id="week" />
```

**Constraining Date/Time Values:**
All date and time inputs support `min` and `max` attributes to restrict selectable ranges, with optional `step` for further constraints.

```html
<label for="myDate">When are you available this summer?</label>
<input
  type="date"
  name="myDate"
  min="2025-06-01"
  max="2025-08-31"
  step="7"
  id="myDate" />
```

### 8. Color Picker Input Type
The `color` input type provides a native color selection interface.

- Created with `<input type="color" />`
- Clicking the control opens the operating system's default color picker
- Always returns color value as lowercase 6-digit hexadecimal (e.g., `#ff5733`)
- Underlying color formats can vary (RGB, HSL, keywords), but the returned value is always hex
- Provides a simple, native way to handle color selection

**Code Example:**
```html
<input type="color" name="color" id="color" />
```

---

## Technical Deep-Dive

### Logic Walkthrough: Email Validation Flow

**Scenario:** User submits a form with an email input containing an invalid value.

**Step 1 — User enters value**
```html
<!-- In browser: user types "notanemail" -->
<input type="email" id="email" name="email" />
```

**Step 2 — Form submission triggered**
User clicks submit button, `<form>` checks validity before sending data.

**Step 3 — Browser validates format**
- Browser checks if value matches email pattern
- `a@b` is considered valid (intranet address format)
- `notanemail` is considered invalid (no `@` symbol)

**Step 4 — Invalid state** (if validation fails)
- `:invalid` pseudo-class matches the input element
- `validityState.typeMismatch` property returns `true`
- Browser displays default error message: "Please enter an email address."
- Form submission is blocked

**Step 5 — Valid state** (if validation passes)
- `:valid` pseudo-class matches the input element
- Form submission proceeds
- Server receives email value and **must validate again server-side**

**Critical Point:** Client-side validation is easily bypassed. Always validate on the server regardless of client-side checks.

### Logic Walkthrough: Number Input with Step Behavior

**Scenario:** User interacts with a number input configured with `min="1"`, `max="10"`, `step="2"`.

**Step 1 — Initial state**
```html
<input type="number" name="age" id="age" min="1" max="10" step="2" />
```

**Step 2 — User clicks up arrow**
- Current value: `1` (starting at `min` since no default set)
- `step="2"` means increment by 2
- New value: `3`

**Step 3 — User clicks up arrow again**
- Current value: `3`
- Add step: `3 + 2 = 5`
- New value: `5`

**Step 4 — User types invalid value**
- User manually enters `6` (an even number, should only allow odd)
- Browser shows validation error
- Input shows as invalid

**Step 5 — Spinner buttons respect step**
- Spinner buttons always use the starting value (`min`) plus multiples of `step`
- Valid values: `1, 3, 5, 7, 9` (odd within 1-10 range)
- Manual entry of `2` or `4` is invalid despite being in range

### Logic Walkthrough: Range Slider with Output Display

**Scenario:** Price filter with range slider that displays current value.

**Step 1 — HTML structure**
```html
<input type="range" name="price" id="price" min="50000" max="500000" step="1000" value="250000" />
<output class="price-output" for="price"></output>
```

**Step 2 — Initial JavaScript setup**
```javascript
const price = document.querySelector("#price");
const output = document.querySelector(".price-output");
output.textContent = price.value;  // Display initial value: "250000"
```

**Step 3 — User moves slider**
- Slider moves to position (user drags to represent $350,000)
- `input` event fires on the `<input>` element

**Step 4 — Event listener updates output**
```javascript
price.addEventListener("input", () => {
  output.textContent = price.value;  // Updates to "350000"
});
```

**Step 5 — Value displayed continuously**
- As slider moves, output updates in real-time
- Without this JavaScript, output would remain blank

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`type` attribute** | The HTML attribute that specifies the input control type, determining validation rules, keyboard display, and rendering. |
| **`email` type** | An input type that validates the value is a properly formatted email address before submission; by default accepts intranet addresses like `a@b`. |
| **`tel` type** | An input type for telephone numbers that does not enforce format validation but displays a numeric keyboard on touch devices. |
| **`url` type** | An input type that requires a valid protocol prefix (e.g., `http:`) and proper URL structure, validated before form submission. |
| **`number` type** | An input type for floating-point numbers that includes spinner buttons; by default only accepts integers unless `step="any"` or a decimal value is specified. |
| **`range` type** | An input type that creates a slider control for selecting a number; less accurate than text input but requires no visual feedback without additional elements. |
| **`date` type** | An input type that opens a native date picker calendar widget and stores values in YYYY-MM-DD format. |
| **`time` type** | An input type for selecting time; may display in 12-hour format but always returns values in 24-hour format. |
| **`search` type** | An input type optimized for search boxes; browsers provide auto-completion based on previous searches and a clear button. |
| **`color` type** | An input type that opens a native color picker and returns color values as lowercase hexadecimal (e.g., `#ff5733`). |
| **`min` attribute** | Specifies the minimum allowed value for number, range, and date/time input types. |
| **`max` attribute** | Specifies the maximum allowed value for number, range, and date/time input types. |
| **`step` attribute** | Specifies the increment amount for spinner buttons or valid values; defaults to `1` for number type (integers only). |
| **`step="any"`** | A special `step` value that allows any floating-point number with no specific increment constraint. |
| **`multiple` attribute** | Allows comma-separated values in email fields; e.g., `<input type="email" multiple />`. |
| **Client-side validation** | Browser-performed validation before form submission; helpful for UX but easily bypassed and must not be relied upon for security. |
| **`:invalid` pseudo-class** | CSS selector that matches form elements failing validation; allows styling of invalid inputs. |
| **`:valid` pseudo-class** | CSS selector that matches form elements passing validation; allows styling of valid inputs. |
| **`validityState.typeMismatch`** | A JavaScript property that returns `true` if a form control fails type validation (e.g., non-email value in email field). |
| **`<output>` element** | A semantic HTML element for displaying results of calculations or current values; can associate with inputs via `for` attribute. |
| **Virtual keyboard** | Platform-specific on-screen keyboard on touch devices; `type` attribute determines which keyboard layout displays. |
| **Intranet email address** | A valid email format on internal networks, like `a@b`, which passes default email validation; custom validation may be needed to restrict to standard email formats. |

---

## Watch Out For...

1. **Email validation allows intranet addresses by default** — The `email` input type considers `a@b` a valid email address because intranet email formats are valid. If you need to restrict to standard internet email formats, use the `pattern` attribute or custom validation. Many developers assume email validation is strict; it is not.

2. **Client-side validation is not security** — Browser validation can be disabled or bypassed by malicious users or network requests. Server-side validation is always required, regardless of how robust your client-side checks are. Treating client-side validation as a security measure is a critical error.

3. **Number type defaults to integer-only validation** — Without setting `step` to a decimal value or `"any"`, the `number` input type only accepts whole numbers. Setting `step="1"` (the default) invalidates entries like `3.14`. This surprises many developers expecting **any** number to be valid.

4. **Spinner buttons on number inputs follow step precisely** — Users cannot bypass the `step` constraint using the spinner buttons. Entering `4` in a field with `min="1"` `max="10"` `step="2"` (valid: 1, 3, 5, 7, 9) will show invalid, even though `4` is within the min/max range. **The step starting point matters.**

5. **Range sliders offer no default visual feedback** — A `<input type="range">` displays no indication of its current value. Without an `<output>` element and JavaScript updating it, users cannot see what value they're selecting. This is a poor UX without the supporting display element.

6. **The `time` input displays in 12-hour format but returns 24-hour values** — Some browsers display the time picker in 12-hour format (with AM/PM), but the input's `value` attribute always contains 24-hour format. JavaScript will read and submit 24-hour format values even if the UI shows 12-hour time.

7. **Week input numbering is ISO-based, not calendar-based** — Week 1 is defined as the week containing the first Thursday of the year, not the week containing January 1. This means Week 1 may start in December and Week 52 or 53 might begin in early January. Developers unfamiliar with ISO 8601 often misunderstand which weeks are valid.

8. **Unchecked checkboxes do not submit in form data** — Unlike text inputs, unchecked checkboxes produce no form data submission. If a checkbox is unchecked, the field is absent from the submitted form data entirely (not submitted as `false` or empty string). Server logic must account for missing checkbox fields.

9. **Color picker always returns hexadecimal, never other formats** — Even if the user selects color in the OS picker using RGB or HSL, the `value` is always lowercase hex. Converting between formats must happen in JavaScript if other formats are needed; the input type does not support format conversion.

10. **Multiple email field submits as comma-separated string** — When `<input type="email" multiple />` is used, multiple emails are stored as a single comma-separated string value, not as an array. Server-side code must split the value if individual emails need processing.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the key difference between `<input type="email">` and `<input type="tel">` in terms of validation?

**Q2.** Write HTML code for a number input that accepts prices between $0 and $100 in increments of $0.25.

**Q3.** Explain why a range slider alone is considered poor UX, and what additional element is recommended to fix it.

**Q4.** Why is client-side form validation NOT sufficient for security, and what must developers always implement?

**Q5.** What is the correct behavior when a user clicks the "up" spinner button on `<input type="number" min="1" max="10" step="2" />`? What are the valid values this input accepts?

---

## Answer Key

---

**A1.** The `email` input type enforces email format validation before form submission and rejects non-email values (triggering the `:invalid` pseudo-class). The `tel` input type **does not validate format at all** — it accepts numbers, letters, and special characters because phone number formats vary internationally. The `tel` type's main feature is displaying a numeric keyboard on touch devices, not validating the input value.

**A2.** 
```html
<input type="number" name="price" id="price" min="0" max="100" step="0.25" />
```

The key points: `min="0"` sets the minimum, `max="100"` sets the maximum, and `step="0.25"` allows quarter-dollar increments (4 steps per dollar). Without the `step` attribute, the input would only accept whole numbers.

**A3.** Range sliders alone provide no visual feedback of the current selected value. Users cannot see what number the slider represents, making the UX poor and confusing. The solution is to pair the slider with an `<output>` element that displays the current value, and use JavaScript to update the `<output>` element's `textContent` whenever the `input` event fires on the range slider. This provides real-time feedback as the user moves the slider.

Example:
```html
<input type="range" id="price" min="50000" max="500000" step="1000" />
<output for="price"></output>

<script>
const price = document.querySelector("#price");
const output = document.querySelector("output");
output.textContent = price.value;
price.addEventListener("input", () => {
  output.textContent = price.value;
});
</script>
```

**A4.** Client-side validation runs in the browser and can be **easily disabled or bypassed** by malicious users — they can disable JavaScript, modify the DOM, or send requests directly to the server bypassing the browser entirely. Client-side validation is helpful for UX (immediate feedback), but it provides **zero security**. Developers must ALWAYS implement server-side validation to verify all submitted data before processing it. Server-side validation cannot be bypassed by the client and is the only reliable security layer.

**A5.** When the "up" spinner button is clicked on `<input type="number" min="1" max="10" step="2" />`:
- Current value before click: `1` (the starting minimum)
- Step value: `2`
- New value after click: `1 + 2 = 3`

The valid values this input accepts are: **`1, 3, 5, 7, 9`** (odd numbers from min to max, incrementing by step). Even though values like `2`, `4`, `6`, `8`, and `10` are within the min/max range, they are **invalid** because they don't align with the step increment starting from the `min` value. Users cannot use spinner buttons to select these values, and manually typing them would show a validation error.
