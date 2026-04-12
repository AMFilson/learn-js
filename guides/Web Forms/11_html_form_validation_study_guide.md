# Form Validation Study Guide

## Executive Summary

Form validation ensures user data meets application requirements before submission. HTML constraint attributes (`required`, `minlength`, `pattern`, `type`, etc.) provide declarative validation. The Constraint Validation API gives JavaScript control via `validity`, `checkValidity()`, `setCustomValidity()`. CSS pseudo-classes (`:valid`, `:invalid`, `:in-range`) provide visual feedback. **Critical:** Client-side validation is UX only—never security. Server validation is mandatory. Complete validation combines HTML (semantic rules) + CSS (visual feedback) + JavaScript (custom logic) + Server (security).

---

## Core Pillars

### 1. Understanding Form Validation: Three Core Reasons

(1) **Data correctness** — Apps need specific data formats; invalid data breaks logic. (2) **User security** — Password complexity and email validation protect accounts. (3) **Application security** — Unvalidated inputs enable SQL/XSS injection.

**Critical caveat:** Client-side validation only addresses #1 and #2. Malicious users bypass it via DevTools, network interception, or direct HTTP requests. **Server validation is mandatory for security.**

### 2. HTML Constraint Validation: Built-In Validation Attributes

HTML5 attributes provide declarative validation requiring zero JavaScript.

**Common attributes:**

- `required` — Field must have value
- `minlength` / `maxlength` — String length constraints
- `min` / `max` — Numeric range constraints for number, date inputs
- `type` — Preset validation (email, url, number, date)
- `pattern` — Custom regex pattern for value matching

**Example:**

```html
<input type="email" name="email" required />
<input type="number" name="age" min="18" max="120" required />
<input type="text" name="username" minlength="3" maxlength="20" />
```

**Browser behavior:**

- Form won't submit if required field is empty or invalid
- Browser displays default error message
- Input receives `:invalid` pseudo-class if constraints fail

### 3. Validation States and CSS Pseudo-Classes

**Core pseudo-classes:**

- `:valid` — Control's value satisfies constraints
- `:invalid` — Control's value violates constraints
- `:required` / `:optional` — Has/lacks required attribute
- `:in-range` / `:out-of-range` — Numeric value within/outside min/max

**Example:**

```css
input:invalid {
  border: 2px solid red;
  background-color: #ffe6e6;
}
input:valid {
  border: 2px solid green;
  background-color: #e6ffe6;
}
input:out-of-range {
  border: 3px solid orange;
}
```

### 4. The Constraint Validation API: JavaScript Inspection and Control

**Key properties:**

- `element.validity` — ValidityState object with error properties
- `element.validationMessage` — Browser's error message string
- `element.willValidate` — Boolean if element validates on submission

**ValidityState properties (read-only):**

- `valueMissing` — Required field is empty
- `typeMismatch` — Type validation failed (e.g., invalid email)
- `patternMismatch` — Pattern attribute validation failed
- `tooShort` / `tooLong` — String length violations
- `rangeUnderflow` / `rangeOverflow` — Numeric range violations
- `valid` — All constraints satisfied

**Example:**

```javascript
const input = document.getElementById("email");
if (input.validity.valid) {
  console.log("Email is valid!");
} else if (input.validity.typeMismatch) {
  console.log("Invalid email format");
}
```

### 5. Custom Validation Messages: setCustomValidity() Method

Use `setCustomValidity(message)` to replace browser error messages with custom text.

**Example:**

```javascript
const input = document.getElementById("email");

input.addEventListener("input", () => {
  input.setCustomValidity(""); // Clear previous error

  if (!input.validity.valid) return; // Let built-in handle it

  // Custom domain validation
  if (!input.value.endsWith("@example.com")) {
    input.setCustomValidity("Only @example.com emails allowed");
  }
});
```

**Key behavior:**

- Non-empty message makes element invalid
- Empty string clears custom error
- Custom message replaces browser message in form submission UI

### 6. Preventing Default Form Submission and Form Validation Methods

**Key methods:**

- `form.checkValidity()` — Returns true if all controls valid; returns false and fires `invalid` event if any invalid
- `form.reportValidity()` — Like checkValidity but ALSO displays browser validation UI and focuses first invalid field
- `element.checkValidity()` / `element.reportValidity()` — Check single element

**Example:**

```javascript
const form = document.getElementById("form");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (form.checkValidity()) {
    console.log("Valid, submitting...");
    form.submit();
  } else {
    console.log("Invalid form");
  }
});
```

### 7. Using the novalidate Attribute for Custom Validation UI

Add `novalidate` to `<form>` to disable browser validation UI, enabling custom error styling.

**Example:**

```html
<form novalidate>
  <input id="username" type="text" required minlength="3" />
  <span id="error" aria-live="polite"></span>
</form>
```

```javascript
const input = document.getElementById("username");
const errorSpan = document.getElementById("error");

input.addEventListener("input", () => {
  if (input.validity.valid) {
    errorSpan.textContent = "";
  } else if (input.validity.valueMissing) {
    errorSpan.textContent = "Username required";
  } else if (input.validity.tooShort) {
    errorSpan.textContent = `Minimum ${input.minLength} characters`;
  }
});
```

**Benefits:** Localized messages, custom styling, matches app design system.

### 8. Validating Without the Constraint Validation API

For custom controls or legacy systems, implement validation with JavaScript regex and conditional logic.

**Example:**

```javascript
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const email = "user@example.com";

if (!emailRegex.test(email)) {
  console.log("Invalid email");
}
```

**Disadvantages:** Code duplication, error-prone, non-standard, harder to maintain.

**Best practice:** Use Constraint Validation API first; implement manual validation only when API insufficient.

### 9. Async Validation: Server-Side Checks with JavaScript

Some validation requires server round-trips: checking username availability, verifying coupon codes. Can't be done with HTML attributes alone.

**Example with debouncing:**

```javascript
const usernameInput = document.getElementById("username");
let checkTimeout;

usernameInput.addEventListener("input", () => {
  clearTimeout(checkTimeout);

  checkTimeout = setTimeout(async () => {
    try {
      const response = await fetch(
        `/api/check-username?u=${usernameInput.value}`,
      );
      const data = await response.json();

      if (!data.available) {
        usernameInput.setCustomValidity("Username taken");
      } else {
        usernameInput.setCustomValidity("");
      }
    } catch (error) {
      console.error("Check failed:", error);
    }
  }, 500); // Debounce 500ms
});
```

**Best practices:** Add debouncing, show "checking..." message, handle network errors, duplicate validation on server.

### 10. Combining HTML Validation, CSS Styling, and JavaScript for Complete UX

Production forms layer all three: HTML provides semantic rules; CSS provides visual feedback; JavaScript provides custom messages and async checks.

**Pattern:**

```html
<form novalidate>
  <input type="email" required placeholder="Email" />
  <span class="error" aria-live="polite"></span>
  <button type="submit">Submit</button>
</form>
```

```css
input:invalid {
  border: 2px solid red;
}
input:valid {
  border: 2px solid green;
}
```

```javascript
const input = document.querySelector("input");
const error = document.querySelector(".error");

input.addEventListener("input", () => {
  if (!input.validity.valid) {
    error.textContent = getErrorMessage(input);
  } else {
    error.textContent = "";
  }
});
```

**This provides:**

- HTML: semantic meaning + basic validation
- CSS: immediate visual feedback without JavaScript
- JavaScript: custom messages + complex validation
- Fallback: works partially if JavaScript fails

---

## Technical Deep-Dive

### Deep-Dive 1: Regular Expressions for Pattern Validation

**Scenario:** Phone number input requiring format (123) 456-7890.

**Pattern breakdown:**

- `\d{3}` — Exactly 3 digits
- `-` — Literal hyphen
- `\d{4}` — Exactly 4 digits

**HTML:**

```html
<input
  type="tel"
  pattern="\(\d{3}\) \d{3}-\d{4}"
  placeholder="(123) 456-7890"
/>
```

**Multiple formats (pipe `|` means OR):**

```html
<input pattern="\d{3}-\d{3}-\d{4}|(\d{3}) \d{3}-\d{4}" />
```

**JavaScript error message:**

```javascript
input.addEventListener("input", () => {
  if (input.validity.patternMismatch) {
    input.setCustomValidity("Format: (123) 456-7890 or 123-456-7890");
  } else {
    input.setCustomValidity("");
  }
});
```

**Key insights:**

- Escape special characters: `\.` instead of `.` (period is any character without escape)
- Test patterns at regex101.com before implementing
- User-friendly error messages must explain acceptable formats

---

### Deep-Dive 2: ValidityState Properties and Validation Cascading

**Scenario:** Date input with constraints: required, min="2025-01-01", max="2030-12-31".

**Testing different inputs:**

| Input      | valueMissing | rangeUnderflow | rangeOverflow | valid | Error                  |
| ---------- | ------------ | -------------- | ------------- | ----- | ---------------------- |
| (empty)    | true         | false          | false         | false | Required               |
| 2024-12-25 | false        | true           | false         | false | Date before 2025-01-01 |
| 2031-06-15 | false        | false          | true          | false | Date after 2030-12-31  |
| 2027-07-04 | false        | false          | false         | true  | (none)                 |

**Cascading error messages:**

```javascript
function getError(input) {
  if (input.validity.valueMissing) return "Date required";
  if (input.validity.rangeUnderflow) return `Cannot be before ${input.min}`;
  if (input.validity.rangeOverflow) return `Cannot be after ${input.max}`;
  return "";
}
```

**Key insight:** ValidityState is read-only. Use `setCustomValidity()` to modify state, not direct property assignment.

---

### Deep-Dive 3: Progressive Enhancement with Fallback Validation

**Scenario:** Login form working with AND without Constraint Validation API.

```javascript
const hasConstraintAPI = typeof input.checkValidity === "function";

if (hasConstraintAPI) {
  // Modern approach: use Constraint Validation API
  input.addEventListener("input", () => {
    if (input.checkValidity()) {
      error.textContent = "";
    } else {
      error.textContent = input.validationMessage;
    }
  });
} else {
  // Fallback: manual regex validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  input.addEventListener("input", () => {
    if (!emailRegex.test(input.value)) {
      error.textContent = "Invalid email";
    } else {
      error.textContent = "";
    }
  });
}
```

**Both approaches validate with identical rules, ensuring consistent behavior whether using modern API or fallback.**

---

## Key Terminology Bank

1. **Form validation** — Process of checking that user-entered data meets application requirements before processing on the server.

2. **Client-side validation** — Validation performed in the browser before form submission, used for UX but not security.

3. **Server-side validation** — Validation performed on the web server after form submission; essential for security and data integrity.

4. **Constraint Validation API** — JavaScript API providing `validity`, `validationMessage`, `checkValidity()`, `setCustomValidity()`, etc. for custom validation control.

5. **Constraint validation attributes** — HTML attributes that define validation rules: `required`, `minlength`, `maxlength`, `min`, `max`, `pattern`, `type`, `step`.

6. **ValidityState object** — Read-only object with properties like `valueMissing`, `typeMismatch`, `patternMismatch`, `tooShort`, `tooLong`, `rangeUnderflow`, `rangeOverflow`, `valid`.

7. **`:valid` pseudo-class** — CSS pseudo-class matching form controls that satisfy all validation constraints.

8. **`:invalid` pseudo-class** — CSS pseudo-class matching form controls that violate at least one constraint.

9. **`required` attribute** — HTML attribute marking a form field as mandatory; empty values fail validation.

10. **`pattern` attribute** — HTML attribute containing a regular expression that the input value must match to be valid.

11. **`minlength` / `maxlength` attributes** — HTML attributes constraining the minimum and maximum character length of string inputs.

12. **`min` / `max` attributes** — HTML attributes constraining the minimum and maximum values of numeric, date, and time inputs.

13. **Type validation** — Built-in validation that checks if value matches the input's type (e.g., email type checks email pattern).

14. **Regular expression (regex)** — Pattern matching syntax used in `pattern` attribute and JavaScript validation; e.g., `/^[a-z0-9]+@[a-z]+\.[a-z]+$/i`.

15. **`setCustomValidity(message)` method** — JavaScript method that sets a custom validation error message; non-empty string makes element invalid.

16. **`checkValidity()` method** — JavaScript method that returns true if form/element is valid, false otherwise; fires `invalid` event if validation fails.

17. **`reportValidity()` method** — JavaScript method like `checkValidity()` but also displays browser's validation UI (error messages, focus).

18. **`novalidate` attribute** — HTML form attribute that disables browser's automatic validation UI, allowing custom JavaScript validation.

19. **`validationMessage` property** — JavaScript property returning the browser's localized error message for an invalid input.

20. **Accessibility tree** — Data structure exposed to assistive technologies; error messages must be explicitly placed in document (e.g., aria-live regions).

21. **`aria-live="polite"` attribute** — ARIA attribute making region announce updates to screen readers; essential for dynamic error message display.

22. **Debouncing** — Technique delaying action (e.g., async server validation) until user stops performing action (e.g., typing) to reduce unnecessary requests.

---

## Watch Out For

### 1. ⚠️ Client-side validation is NOT security; server validation is mandatory

**Misconception:** "If I validate all inputs on the client with JavaScript, my form is secure."

**Reality:** Client-side validation is trivially bypassable. A malicious user can disable JavaScript, modify network requests, or craft HTTP POST requests directly without touching your form. Security breaches happen when only client-side validation exists.

**Why it matters:** Data corruption, malicious data injection, potential SQL injection or script injection vulnerabilities, compliance failure (GDPR, etc.).

**What to do:** Always validate all form data on the server using identical rules. Client validation improves UX only.

---

### 2. ⚠️ Browser default validation messages are not localized to your app's language

**Misconception:** "I'll use the browser's default validation messages for users worldwide."

**Reality:** Browser error messages are localized to the browser's language setting, not your app's language. User sees Firefox's French error message on an English website, creating confusion.

**Why it matters:** Poor internationalization; user experience suffers when error messages don't match site language.

**What to do:** Use `novalidate` on the form and implement custom error messages via `setCustomValidity()` or custom error containers, ensuring they match your app's language.

---

### 3. ⚠️ `maxlength` attribute doesn't guarantee maxlength enforcement in all scenarios

**Misconception:** "Setting `maxlength="10"` prevents users from entering more than 10 characters."

**Reality:** Most browsers prevent typing beyond maxlength, but JavaScript can programmatically set values longer than maxlength. Pasting text longer than maxlength may or may not be prevented (browser-dependent).

**Why it matters:** Data exceeding length constraints could reach the server, breaking database fields with length limits.

**What to do:** Use validation logic (not just maxlength attribute) to enforce string length. Server-side validation must also check length.

---

### 4. ⚠️ Empty optional inputs are `:valid`, not `:invalid`, even with type constraints

**Misconception:** "An optional email input with empty value is `:invalid` because it doesn't match email pattern."

**Reality:** Empty optional inputs (no `required` attribute) match `:valid` pseudo-class. Validation constraints only apply when the field HAS a value.

**Why it matters:** Styling `:optional:invalid` won't trigger; you may think validation is broken when it's actually correct behavior.

**What to do:** Understand the validation model: optional + empty = valid. Optional + (non-empty AND invalid) = invalid.

---

### 5. ⚠️ Setting `setCustomValidity()` with message during `input` event causes form submission to block on `submit`

**Misconception:** "I'll set custom validity on input event, and form submission will be blocked immediately."

**Reality:** `setCustomValidity()` sets error state immediately, but form submission block only occurs when the form is actually submitted. User can still click Submit button; form will be blocked on submission.

**Why it matters:** User confusion: they don't know form won't submit until they attempt submission.

**What to do:** Call `checkValidity()` or `reportValidity()` immediately after `setCustomValidity()` if you want immediate feedback, or rely on form submission for blocking.

---

### 6. ⚠️ Radio button group `required` attribute on one button requires selection but doesn't match all buttons with `:required`

**Misconception:** "I'll put `required` on one radio button in a group, and all buttons will match `:required` pseudo-class."

**Reality:** Putting `required` on one radio in a group (same `name`) makes the GROUP required (one must be checked), but only the radio WITH `required` attribute matches `:required` pseudo-class.

**Why it matters:** CSS selectors won't target all radios in group; logic doesn't match user perception.

**What to do:** Recognize that radio groups are validated as a unit but only the specific radio with `required` matches `:required`. Use fieldset-level validation for clearer intent.

---

### 7. ⚠️ `type="email"` accepts intranet addresses like "user@intranet" by default

**Misconception:** "Email type validation requires a TLD (top-level domain) like .com; it won't accept user@intranet."

**Reality:** HTML5 email type validation allows intranet addresses without TLD by default. "user@intranet" and even "a@b" are valid email addresses per the spec.

**Why it matters:** If you need to enforce TLD requirement, email type alone isn't sufficient; you must add pattern attribute.

**What to do:** For strict email validation, use either `type="email"` with `pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}"` or custom validation.

---

### 8. ⚠️ ValidityState is read-only; you can't set properties directly

**Misconception:** "I can set `input.validity.valid = true` to make an input valid."

**Reality:** `validity` is a read-only object. Attempting to set properties has no effect. Use `setCustomValidity()` to modify validation state.

**Why it matters:** Code that tries to set validity properties silently fails; validation doesn't behave as expected.

**What to do:** Always use `setCustomValidity(message)` to set custom errors, never try to set ValidityState properties directly.

---

### 9. ⚠️ Pattern attribute anchors are implied; `pattern="123"` matches "0123abc" because pattern assumption is not `^123$`

**Misconception:** "`pattern='123'` will only match strings that are exactly '123'."

**Reality:** HTML pattern attribute implicitly allows any characters before/after the pattern. `pattern="123"` matches "0123abc" because pattern is internally treated as `.*123.*` (not `^123$`).

**Why it matters:** Pattern validation might unexpectedly match partial strings; users could enter "abc123def" thinking it wouldn't validate.

**What to do:** Use anchors in pattern explicitly if you need exact matching: `pattern="^123$"` (for full string match) or `pattern="^[0-9]{3}$"` for exactly 3 digits.

---

### 10. ⚠️ Error messages in async validation must clear when async check succeeds, or form blocking persists

**Misconception:** "After async validation succeeds, the form will automatically unblock."

**Reality:** If you called `setCustomValidity(message)` during async validation and didn't clear it on success, the input remains invalid.

**Why it matters:** Form stays blocked even after user corrects the issue (e.g., username becomes available).

**What to do:** Always call `setCustomValidity('')` (empty string) to clear custom error when async validation succeeds, making element valid again.

---

## Active Recall: Exam-Ready Questions

### Question 1: Recall - Name Three Reasons Form Validation Exists

List the three core reasons why form validation exists. Explain why client-side validation alone doesn't address one of them.

<details>
<summary>Answer</summary>

1. **Data Correctness** — Apps need specific formats; invalid data breaks logic.
2. **User Security** — Password complexity and email validation protect accounts.
3. **Application Security** — Unvalidated inputs enable SQL/XSS injection attacks.

**Why client-side validation doesn't address #3:** Users can bypass it via DevTools, network interception, or direct HTTP requests. Server validation is mandatory for security.

</details>

---

### Question 2: Application - Implement Required Field Validation

Build an HTML form with: (1) required fields with visual feedback, (2) custom error messages, (3) form submission blocking until valid. Include text and email inputs.

<details>
<summary>Answer</summary>

**HTML:**

```html
<form id="formex" novalidate>
  <input id="username" type="text" required minlength="3" />
  <span id="usernameError" aria-live="polite"></span>

  <input id="email" type="email" required />
  <span id="emailError" aria-live="polite"></span>

  <button type="submit">Submit</button>
</form>
```

**JavaScript:**

```javascript
const form = document.getElementById("formex");
const username = document.getElementById("username");
const usernameError = document.getElementById("usernameError");

username.addEventListener("input", () => {
  if (username.validity.valid) {
    usernameError.textContent = "";
  } else if (username.validity.valueMissing) {
    usernameError.textContent = "Username required";
  } else if (username.validity.tooShort) {
    usernameError.textContent = `Min ${username.minLength} chars`;
  }
});

form.addEventListener("submit", (e) => {
  if (!form.checkValidity()) {
    e.preventDefault();
  }
});
```

**CSS:**

```css
input:invalid {
  border: 2px solid red;
}
input:valid {
  border: 2px solid green;
}
```

</details>

---

### Question 3: Analysis - When to Use HTML Validation vs JavaScript?

Compare HTML constraint attributes and Constraint Validation API. Give specific examples where each is appropriate.

<details>
<summary>Answer</summary>

**HTML attributes (best for):**

- Simple field-level validation (required, email, minlength)
- Type validation (date, number ranges)
- Progressive enhancement (works without JavaScript)
- Example: `<input type="email" required />`

**JavaScript API (best for):**

- Custom error messages in app language
- Cross-field validation (password confirmation)
- Async validation (username availability)
- Complex conditional logic
- Example: password matching, server availability checks

**Best practice:** Layer both. Start with HTML attributes for basic validation, add JavaScript for custom messages and complex logic.

</details>

---

### Question 4: Synthesis - Design Complete Validation Form

Create a "Create Account" form with HTML validation, CSS pseudo-classes, and JavaScript async username availability check (debounced).

<details>
<summary>Answer</summary>

**HTML:**

```html
<form novalidate>
  <input id="username" type="text" required minlength="3" />
  <span id="usernameError" aria-live="polite"></span>
  <button type="submit">Create</button>
</form>
```

**CSS:**

```css
input:valid {
  border: 2px solid green;
}
input:invalid {
  border: 2px solid red;
}
```

**JavaScript:**

```javascript
const input = document.getElementById("username");
const error = document.getElementById("usernameError");
let timeout;

input.addEventListener("input", () => {
  clearTimeout(timeout);
  error.textContent = "";

  if (!input.validity.valid) return;

  error.textContent = "Checking...";
  timeout = setTimeout(async () => {
    const res = await fetch(`/api/check-user?u=${input.value}`);
    const { available } = await res.json();

    if (!available) {
      input.setCustomValidity("Username taken");
      error.textContent = "Username taken";
    } else {
      input.setCustomValidity("");
      error.textContent = "✓ Available";
    }
  }, 500);
});
```

**Result:** Layered validation (HTML + CSS + JS + async) with debouncing, real-time feedback, and server round-trip.

</details>

---

### Question 5: Create - Build Custom Validation UI without novalidate

Implement validation using elements WITHOUT `novalidate` (instead use `reportValidity()`), showing default browser messages PLUS custom field-level error spans.

<details>
<summary>Answer</summary>

**HTML:**

```html
<form>
  <input id="password" type="password" required minlength="8" />
  <span id="pwdError" aria-live="polite"></span>
  <button>Submit</button>
</form>
```

**JavaScript:**

```javascript
const form = document.querySelector("form");
const pwd = document.getElementById("password");
const error = document.getElementById("pwdError");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  // Show browser's validation UI
  if (!form.reportValidity()) {
    // Also show custom error message
    if (pwd.validity.tooShort) {
      error.textContent = `Min 8 chars (you have ${pwd.value.length})`;
    }
  }
});
```

**Key difference:** `reportValidity()` shows browser's default messages PLUS allows custom supplementary messages in error spans.

</details>

### 10. ⚠️ Error messages in async validation must clear when async check succeeds, or form blocking persists

**Misconception:** "After async validation succeeds, the form will automatically unblock."

**Reality:** If you called `setCustomValidity(message)` during async validation and didn't clear it on success, the input remains invalid.

**Why it matters:** Form stays blocked even after user corrects the issue (e.g., username becomes available).

**What to do:** Always call `setCustomValidity('')` (empty string) to clear custom error when async validation succeeds, making element valid again.

---

## Active Recall: Exam-Ready Questions

### Question 1: Recall - Name Three Reasons Form Validation Exists

List the three core reasons why form validation exists. Explain why client-side validation alone doesn't address one of them.

<details>
<summary>Answer</summary>

1. **Data Correctness** — Apps need specific formats; invalid data breaks logic.
2. **User Security** — Password complexity and email validation protect accounts.
3. **Application Security** — Unvalidated inputs enable SQL/XSS injection attacks.

**Why client-side validation doesn't address #3:** Users can bypass it via DevTools, network interception, or direct HTTP requests. Server validation is mandatory for security.

</details>

---

### Question 2: Application - Implement Required Field Validation

Build an HTML form with: (1) required fields with visual feedback, (2) custom error messages, (3) form submission blocking until valid. Include text and email inputs.

<details>
<summary>Answer</summary>

**HTML:**

```html
<form id="formex" novalidate>
  <input id="username" type="text" required minlength="3" />
  <span id="usernameError" aria-live="polite"></span>

  <input id="email" type="email" required />
  <span id="emailError" aria-live="polite"></span>

  <button type="submit">Submit</button>
</form>
```

**JavaScript:**

```javascript
const form = document.getElementById("formex");
const username = document.getElementById("username");
const usernameError = document.getElementById("usernameError");

username.addEventListener("input", () => {
  if (username.validity.valid) {
    usernameError.textContent = "";
  } else if (username.validity.valueMissing) {
    usernameError.textContent = "Username required";
  } else if (username.validity.tooShort) {
    usernameError.textContent = `Min ${username.minLength} chars`;
  }
});

form.addEventListener("submit", (e) => {
  if (!form.checkValidity()) {
    e.preventDefault();
  }
});
```

**CSS:**

```css
input:invalid {
  border: 2px solid red;
}
input:valid {
  border: 2px solid green;
}
```

</details>

---

### Question 3: Analysis - When to Use HTML Validation vs JavaScript?

Compare HTML constraint attributes and Constraint Validation API. Give specific examples where each is appropriate.

<details>
<summary>Answer</summary>

**HTML attributes (best for):**

- Simple field-level validation (required, email, minlength)
- Type validation (date, number ranges)
- Progressive enhancement (works without JavaScript)
- Example: `<input type="email" required />`

**JavaScript API (best for):**

- Custom error messages in app language
- Cross-field validation (password confirmation)
- Async validation (username availability)
- Complex conditional logic
- Example: password matching, server availability checks

**Best practice:** Layer both. Start with HTML attributes for basic validation, add JavaScript for custom messages and complex logic.

</details>

---

### Question 4: Synthesis - Design Complete Validation Form

Create a "Create Account" form with HTML validation, CSS pseudo-classes, and JavaScript async username availability check (debounced).

<details>
<summary>Answer</summary>

**HTML:**

```html
<form novalidate>
  <input id="username" type="text" required minlength="3" />
  <span id="usernameError" aria-live="polite"></span>
  <button type="submit">Create</button>
</form>
```

**CSS:**

```css
input:valid {
  border: 2px solid green;
}
input:invalid {
  border: 2px solid red;
}
```

**JavaScript:**

```javascript
const input = document.getElementById("username");
const error = document.getElementById("usernameError");
let timeout;

input.addEventListener("input", () => {
  clearTimeout(timeout);
  error.textContent = "";

  if (!input.validity.valid) return;

  error.textContent = "Checking...";
  timeout = setTimeout(async () => {
    const res = await fetch(`/api/check-user?u=${input.value}`);
    const { available } = await res.json();

    if (!available) {
      input.setCustomValidity("Username taken");
      error.textContent = "Username taken";
    } else {
      input.setCustomValidity("");
      error.textContent = "✓ Available";
    }
  }, 500);
});
```

**Result:** Layered validation (HTML + CSS + JS + async) with debouncing, real-time feedback, and server round-trip.

</details>

---

### Question 5: Create - Build Custom Validation UI without novalidate

Implement validation using elements WITHOUT `novalidate` (instead use `reportValidity()`), showing default browser messages PLUS custom field-level error spans.

<details>
<summary>Answer</summary>

**HTML:**

```html
<form>
  <input id="password" type="password" required minlength="8" />
  <span id="pwdError" aria-live="polite"></span>
  <button>Submit</button>
</form>
```

**JavaScript:**

```javascript
const form = document.querySelector("form");
const pwd = document.getElementById("password");
const error = document.getElementById("pwdError");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  // Show browser's validation UI
  if (!form.reportValidity()) {
    // Also show custom error message
    if (pwd.validity.tooShort) {
      error.textContent = `Min 8 chars (you have ${pwd.value.length})`;
    }
  }
});
```

**Key difference:** `reportValidity()` shows browser's default messages PLUS allows custom supplementary messages in error spans.

</details>
