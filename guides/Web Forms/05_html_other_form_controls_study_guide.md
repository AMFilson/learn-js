# 📚 Other Form Controls — Exam Study Guide
**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Other_form_controls

---

## Executive Summary

HTML provides several form control elements beyond basic `<input>` types to handle specialized data collection needs. These elements include `<textarea>` for multi-line text, `<select>` for drop-down lists, `<datalist>` for autocomplete suggestions, and `<meter>`/`<progress>` for visual representations of numeric values. Understanding these non-input form elements is essential for building complete, accessible, and user-friendly web forms.

---

## Core Pillars

### 1. Textarea for Multi-line Text Input
The `<textarea>` element provides a multi-line text input field, allowing users to enter text with line breaks.

- Created with `<textarea></textarea>` (requires closing tag, unlike `<input>`)
- Default text is placed between opening and closing tags (not in a `value` attribute)
- Users can press Enter to create hard line breaks that are submitted with the form
- Best used for longer text like messages, comments, or descriptions
- Different from `<input type="text">` which enforces single-line input

**Attributes:**
- **`cols`** — Specifies visible width in average character widths (default: 20); can be overridden by CSS or user resizing
- **`rows`** — Specifies visible height in text rows (default: 2); can be overridden by CSS or user resizing
- **`wrap`** — Controls text wrapping behavior:
  - `soft` (default) — Text wraps visually but submitted text is not wrapped
  - `hard` — Both rendered and submitted text are wrapped; **requires `cols` attribute**
  - `off` — No wrapping applied

**CSS Resizing:**
The `resize` CSS property controls textarea resizeability:
- `both` (default) — Allows resizing horizontally and vertically
- `horizontal` — Resize width only
- `vertical` — Resize height only
- `none` — Disables resizing
- `block`/`inline` — Experimental; resize in block or inline direction based on text direction

**Code Example:**
```html
<textarea cols="30" rows="8"></textarea>

<!-- With default text -->
<textarea cols="30" rows="8">This is default text content.</textarea>

<!-- Wrapped submission -->
<textarea cols="40" rows="5" wrap="hard"></textarea>

<!-- Disable resizing -->
<textarea style="resize: none;"></textarea>
```

### 2. Select Dropdown Lists
The `<select>` element creates a dropdown list allowing users to choose one or more values from predefined options.

- Created with `<select>` containing one or more `<option>` children
- By default allows only a single selection
- Each `<option>` represents one selectable choice
- The `selected` attribute on an `<option>` preselects it when the page loads

**Code Example:**
```html
<select id="simple" name="simple">
  <option>Banana</option>
  <option selected>Cherry</option>
  <option>Lemon</option>
</select>
```

### 3. Option Groups (Optgroup)
The `<optgroup>` element groups related options visually within a select dropdown.

- `<option>` elements nested inside `<optgroup>` are grouped together
- The `label` attribute on `<optgroup>` displays the group header
- Group labels are typically bolded and visually separate from options
- Group labels are **not selectable** — only options within groups are selectable

**Code Example:**
```html
<select id="groups" name="groups">
  <optgroup label="fruits">
    <option>Banana</option>
    <option selected>Cherry</option>
    <option>Lemon</option>
  </optgroup>
  <optgroup label="vegetables">
    <option>Carrot</option>
    <option>Eggplant</option>
    <option>Potato</option>
  </optgroup>
</select>
```

### 4. Option Value Attributes
The `value` attribute on `<option>` elements allows sending different data to the server than what displays to users.

- If `value` attribute is **omitted**, the option's text content becomes the submitted value
- If `value` attribute is **present**, that value is submitted instead of the text content
- Useful for sending abbreviated or coded values while displaying human-readable labels
- Without explicit values, displayed text and submitted data are identical

**Code Example:**
```html
<select id="simple" name="simple">
  <option value="banana">Big, beautiful yellow banana</option>
  <option value="cherry">Succulent, juicy cherry</option>
  <option value="lemon">Sharp, powerful lemon</option>
</select>
```

### 5. Multiple-Selection Dropdowns
Adding the `multiple` attribute to `<select>` allows users to select multiple values simultaneously.

- Users hold Cmd (Mac) or Ctrl (Windows/Linux) while clicking to select multiple options
- Without `multiple`, only one option can be selected at a time
- With `multiple`, the dropdown displays as a list instead of a dropdown box
- The `size` attribute controls how many options are visible (default: 1 for single select, multiple visible options for multi-select)
- Multiple selections are submitted as an array of selected values

**Code Example:**
```html
<select id="multi" name="multi" multiple size="2">
  <optgroup label="fruits">
    <option>Banana</option>
    <option selected>Cherry</option>
    <option>Lemon</option>
  </optgroup>
  <optgroup label="vegetables">
    <option>Carrot</option>
    <option>Eggplant</option>
    <option>Potato</option>
  </optgroup>
</select>
```

### 6. Datalist for Autocomplete Suggestions
The `<datalist>` element provides suggested autocomplete values for a text-based input field.

- Created with `<datalist>` containing `<option>` child elements
- Must have a unique `id` attribute
- Linked to an `<input>` via the input's `list` attribute (value = datalist id)
- As users type, the browser filters suggestions matching their input
- Suggestions appear in a dropdown; users can select or ignore them
- User is **not limited** to suggested values — any input is accepted

**Code Example:**
```html
<label for="myFruit">What's your favorite fruit?</label>
<input type="text" name="myFruit" id="myFruit" list="mySuggestion" />
<datalist id="mySuggestion">
  <option>Apple</option>
  <option>Banana</option>
  <option>Blackberry</option>
  <option>Blueberry</option>
  <option>Lemon</option>
  <option>Lychee</option>
  <option>Peach</option>
  <option>Pear</option>
</datalist>
```

**Progressive Enhancement:**
Datalist can be used with other input types:
- **`range` inputs** — Tick marks display above the slider for each option value
- **`color` inputs** — Custom color palette displays as default options
- Browser behavior varies; treat as progressive enhancement

### 7. Meter Element
The `<meter>` element displays a scalar value (like disk usage or temperature) as a visual gauge bar.

- Not a form control (not submitted with forms)
- Represents a **fixed value** within a defined range
- Displays as a colored bar: **green** (preferred), **yellow** (average), or **red** (worst)

**Key Attributes:**
- **`min`** — Minimum value of range (default: 0)
- **`max`** — Maximum value of range (default: 1)
- **`value`** — Current value being metered
- **`low`** — Threshold for "low" portion of range (inclusive with min)
- **`high`** — Threshold for "high" portion of range (exclusive with low)
- **`optimum`** — Optimal value that determines color interpretation

**Range Breakdown:**
The `low` and `high` attributes divide the range into three parts:
1. Lower part: `min` to `low` (inclusive)
2. Medium part: `low` to `high` (exclusive)
3. Higher part: `high` to `max` (inclusive)

**Color Logic (based on `optimum` placement):**
- If `optimum` is in **low portion**: low=green, medium=yellow, high=red
- If `optimum` is in **medium portion**: low=yellow, medium=green, high=yellow
- If `optimum` is in **high portion**: low=red, medium=yellow, high=green

**Code Example:**
```html
<meter min="0" max="100" value="75" low="33" high="66" optimum="0">75</meter>
```

### 8. Progress Element
The `<progress>` element displays a progress bar showing how much of a task is complete.

- Not a form control (not submitted with forms)
- Represents a **changing value** progressing toward a maximum
- Used for download progress, quiz completion, file uploads, etc.
- **No color coding** like meter; simply shows completion percentage

**Key Attributes:**
- **`max`** — Maximum value (default: 1); represents 100% completion
- **`value`** — Current progress value (0 to max)
- Content between tags is fallback text for unsupported browsers

**Calculation:**
Progress percentage = (value / max) × 100

**Code Example:**
```html
<progress max="100" value="75">75/100</progress>

<!-- Almost complete -->
<progress max="100" value="95"></progress>

<!-- Just started -->
<progress max="100" value="10"></progress>
```

---

## Technical Deep-Dive

### Logic Walkthrough: Select Box Value Submission

**Scenario:** User selects an option from a select dropdown and submits the form.

**Step 1 — HTML setup**
```html
<form method="POST">
  <select id="fruit" name="fruit">
    <option value="banana">Big yellow banana</option>
    <option value="cherry">Red cherry</option>
    <option value="lemon">Yellow lemon</option>
  </select>
  <button type="submit">Submit</button>
</form>
```

**Step 2 — User selects option**
- User clicks dropdown and selects "Red cherry" option
- Display text: "Red cherry"
- Internal value: "cherry"

**Step 3 — Form submission**
- User clicks submit button
- Browser packages form data: `fruit=cherry`
- Note: Display text "Red cherry" is **not** sent

**Step 4 — Server receives**
Server receives: `{"fruit": "cherry"}`
- The abbreviated value is transmitted, not the full text
- This allows cleaner server-side code and smaller payloads

**Comparison without value attribute:**
```html
<select id="fruit" name="fruit">
  <option>Big yellow banana</option>
  <option>Red cherry</option>
  <option>Yellow lemon</option>
</select>
```
If user selects "Red cherry", server receives: `{"fruit": "Red cherry"}` (full text)

### Logic Walkthrough: Meter Coloring with Optimum

**Scenario:** Website displays disk usage meter with different optimal ranges.

**Setup 1 — Optimum in low range (prefer low usage)**
```html
<!-- Prefer empty disk (low usage) -->
<meter min="0" max="100" value="75" low="33" high="66" optimum="10">75%</meter>
```

Range breakdown:
- Low: 0–33 (green when optimum=10)
- Medium: 33–66 (yellow)
- High: 66–100 (red)

Current value 75 is in "high" range = **RED** (worst state)

**Setup 2 — Optimum in high range (prefer high scores)**
```html
<!-- Test score: prefer high results -->
<meter min="0" max="100" value="75" low="33" high="66" optimum="90">75%</meter>
```

Range breakdown:
- Low: 0–33 (red when optimum=90)
- Medium: 33–66 (yellow)
- High: 66–100 (green when optimum=90)

Current value 75 is in "high" range = **GREEN** (preferred state)

### Logic Walkthrough: Datalist Filtering and Suggestion

**Scenario:** User types in a fruit autocomplete field.

**Step 1 — Initial page load**
```html
<input type="text" id="myFruit" list="fruits" />
<datalist id="fruits">
  <option>Apple</option>
  <option>Apricot</option>
  <option>Banana</option>
  <option>Blueberry</option>
  <option>Cherry</option>
</datalist>
```

Field is empty, no suggestions shown.

**Step 2 — User types "a"**
- Suggestions appear: "Apple", "Apricot"
- Only options starting with "a" (case-insensitive) display
- Browser filters automatically

**Step 3 — User continues typing "ap"**
- Filtered suggestions: "Apple", "Apricot"
- Closer match displayed first

**Step 4 — User continues typing "app"**
- Only suggestion: "Apple"
- Single match highly filtered

**Step 5 — User types "xyz"**
- No matching options
- **No error shown** — field accepts any value
- User can submit "xyz" even though it's not in the datalist

**Step 6 — User clicks on suggestion**
- If user clicks "Apple", the field is populated: `<input value="Apple" />`
- Form submission sends: `myFruit=Apple`

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`<textarea>` element** | A multi-line text input control that accepts hard line breaks (Enter key) from users and renders them when submitted. |
| **`cols` attribute** | Specifies the visible width of a textarea in average character widths; can be overridden by CSS or user resizing. |
| **`rows` attribute** | Specifies the visible height of a textarea in text lines; can be overridden by CSS or user resizing. |
| **`wrap` attribute** | Controls how text wrapping is applied in a textarea; values are `soft` (visual wrap only), `hard` (wrap submitted text), or `off` (no wrap). |
| **`<select>` element** | A dropdown list control allowing users to select one or more predefined values from a set of options. |
| **`<option>` element** | Represents a single selectable choice within a select dropdown or datalist. |
| **`selected` attribute** | Boolean attribute that preselects an option when the form page loads. |
| **`<optgroup>` element** | Groups related option elements visually within a select dropdown; displays a non-selectable label header. |
| **`value` attribute on `<option>`** | Explicit value sent to server when an option is selected; if omitted, the option's text content is sent instead. |
| **`multiple` attribute** | Boolean attribute that allows multiple selections in a select dropdown; selected values are submitted as an array. |
| **`size` attribute on `<select>`** | Controls how many options are visible in the dropdown; defaults to 1 for single-select, displays multiple for multi-select. |
| **`<datalist>` element** | Provides a list of suggested autocomplete values for a text-based input; links to input via the `list` attribute. |
| **`list` attribute on `<input>`** | References a datalist by its ID to provide autocomplete suggestions from the datalist's options. |
| **`<meter>` element** | Displays a fixed scalar value as a colored gauge bar (green/yellow/red) representing status within a defined range. |
| **`<progress>` element** | Displays a progress bar showing how much of a task is complete, changing from 0 to a maximum value. |
| **`min` / `max` attributes** | Define the lower and upper bounds of the range for meter and progress elements. |
| **`value` attribute** | Specifies the current value being measured in meter or progress elements. |
| **`low` / `high` attributes on `<meter>`** | Define thresholds that divide the meter's range into lower (preferred), medium (average), and higher (worst) portions. |
| **`optimum` attribute on `<meter>`** | Defines the optimal value; determines which range portion is "preferred" (green), affecting the meter's color coding. |
| **Void element** | An HTML element with no closing tag (e.g., `<input>`); content cannot be placed inside it. |
| **Hard line break** | A line break created by pressing Enter that is preserved and submitted with form data (supported by textarea). |
| **Progressive enhancement** | Technique of using HTML features (like datalist with range inputs) that work in modern browsers but gracefully degrade in unsupported ones. |

---

## Watch Out For...

1. **`<textarea>` is not a void element** — Unlike `<input>`, the textarea requires a closing tag: `<textarea></textarea>`. Default content goes **between the tags**, not in a `value` attribute. Attempting to use `<textarea value="...">` will not work; the attribute is ignored and content must be placed between opening and closing tags.

2. **`cols` and `rows` are starting dimensions, not constraints** — The `cols` and `rows` attributes set the **initial** display size, but users can resize the textarea (if `resize` CSS property allows), and CSS can override these dimensions. These attributes don't constrain the amount of text that can be entered.

3. **`wrap="hard"` requires `cols` attribute** — When using `wrap="hard"` to apply hard wrapping to submitted text, the `cols` attribute **must be specified**. Without it, some browsers may ignore the `hard` wrap mode or behave unexpectedly.

4. **Select boxes don't enforce options in multiple mode** — With `<select multiple>`, the form validates the selected options exist in the list, but if you manipulate the DOM via JavaScript, you can submit values not in the original list. The browser doesn't prevent invalid selections if the options are removed or modified.

5. **`selected` attribute only marks one default option** — Include the `selected` attribute on multiple options, and most browsers will select **only the last one**. Only one option should have `selected` in a standard select box; use `multiple` attribute and multiple `selected` attributes if you truly want multiple defaults.

6. **Optgroup labels are never selectable** — Even though `<optgroup>` appears in the dropdown, clicking the group label does nothing — only options within the group are selectable. This confuses some developers who expect group labels to act as containers that can be selected.

7. **Datalist suggestions don't validate input** — Datalist provides suggestions but **does not restrict** user input to those values. If a user types something not in the datalist, the field accepts it and the form submits. If you need strict validation, use `<select>` instead or add JavaScript validation. Datalist is for *suggestions*, not *constraints*.

8. **Datalist is not a form control itself** — The `<datalist>` element is a container for suggestions; it cannot be submitted and doesn't appear by itself in the form. It must be linked to an `<input>` via the `list` attribute to function. Stray `<datalist>` elements without associated inputs are invisible.

9. **Meter and progress are not form controls** — Neither `<meter>` nor `<progress>` are reported in form submissions. They are **visual display elements only**, like `<img>` or `<video>`. If you need to submit a value, use a hidden `<input>` in addition.

10. **Meter color depends on `optimum`, not just the value** — The same meter value (e.g., 75) can display as green, yellow, or red depending on where `optimum` is placed. Many developers assume high values are always "green" or low values always "red"; the actual meaning depends on context set by `optimum`.

11. **Progress doesn't have `low` and `high`** — Unlike `<meter>`, the `<progress>` element doesn't have `low`, `high`, or `optimum` attributes. It simply shows a percentage bar. Attempting to use these attributes on progress does nothing; progress is always a single-color bar.

12. **`<progress value>` can exceed `max` without error** — Setting `<progress value="150" max="100">` is technically invalid but the browser won't error; the bar will appear overfilled. Always ensure value ≤ max through validation.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the key difference between `<input type="text">` with the `value` attribute and `<textarea>` for setting default content?

**Q2.** Write HTML code for a select dropdown that displays "United States" to users but sends the code "US" to the server.

**Q3.** Explain the relationship between `<option>` elements, `value` attributes, and what gets submitted when a form is sent.

**Q4.** How does the `optimum` attribute on a `<meter>` element change the color interpretation of the meter?

**Q5.** Compare `<datalist>` and `<select>` in terms of user input validation and flexibility.

---

## Answer Key

---

**A1.** The `<input type="text">` element uses the `value` attribute to set default content: `<input value="default text">`. The `<textarea>` element **does not use a `value` attribute** — default text is placed **between the opening and closing tags**: `<textarea>default text</textarea>`. This is because textarea is a container element (not void), while input is a void element. Both display default content on page load, but the syntax is fundamentally different.

**A2.**
```html
<select id="country" name="country">
  <option value="US">United States</option>
  <option value="CA">Canada</option>
  <option value="MX">Mexico</option>
</select>
```

When a user selects "United States," the browser displays that text, but the form sends `country=US` to the server. The `value` attribute allows the displayed label to differ from the submitted value. Without `value` attributes, the full "United States" text would be sent.

**A3.** When a form is submitted:

1. **If `<option>` has a `value` attribute** → The `value` is sent to the server
2. **If `<option>` has NO `value` attribute** → The option's text content is sent to the server

Example comparison:
```html
<!-- This option sends "cherry" to the server -->
<option value="cherry">Sweet cherry fruit</option>

<!-- This option sends "apple" to the server (the text content) -->
<option>apple</option>
```

The `value` attribute is optional but recommended because it allows readable display text while sending compact data to the server.

**A4.** The `optimum` attribute defines which part of the meter's range is "preferred." The `low` and `high` attributes divide the range into three zones, and the meter's color depends on which zone the current `value` falls into:

- If `optimum` is in the **low zone**: low=green (preferred), medium=yellow, high=red
- If `optimum` is in the **medium zone**: low=yellow, medium=green (preferred), high=yellow
- If `optimum` is in the **high zone**: low=red, medium=yellow, high=green (preferred)

**Example:**
- Disk usage: `<meter min="0" max="100" value="80" low="33" high="66" optimum="10">` → value 80 is in high zone, optimum is in low zone, so high zone is red (bad) = **RED meter**
- Test score: `<meter min="0" max="100" value="80" low="33" high="66" optimum="90">` → value 80 is in high zone, optimum is in high zone, so high zone is green (good) = **GREEN meter**

The same value (80) produces different colors based on where `optimum` is placed!

**A5.** 

| Aspect | `<datalist>` | `<select>` |
|---|---|---|
| **Input restriction** | User input is NOT restricted; suggestions are for autocomplete only | User input IS restricted to predefined options only |
| **User flexibility** | User can type anything, even if not in the list | User can only choose from provided options |
| **Form submission** | Can submit any value, not just suggested values | Can only submit values from the option list |
| **Best use** | Autocomplete scenarios where custom input is acceptable | Strict validation where only specific choices are valid |
| **Example** | Searching for a city (user might type a custom city name) | Selecting a country from a fixed list of countries |

**Key difference:** `<datalist>` provides **suggestions** with **no enforcement**, while `<select>` **enforces choice** from a **fixed set**. If you need strict validation, use `<select>`. If you want to be helpful but allow flexibility, use `<datalist>`.

---
