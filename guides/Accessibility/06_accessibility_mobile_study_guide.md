# 📚 Mobile Accessibility — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/Mobile

---

## Executive Summary

Mobile accessibility sits at the intersection of three disciplines: **screen reader operation** (gesture-based rather than keyboard-based), **device-independent event handling** (touch ≠ mouse), and **responsive design** (layout, image sizing, and zoom). The central message of this article is that mobile accessibility requires no entirely new principles — it applies the same general best practices (semantic HTML, accessible controls, good responsiveness) — but with three specific mobile considerations: (1) controls must work equally well on touch *and* mouse/keyboard, (2) user input must minimize typing via smart form design, and (3) layouts must be responsive and must **never disable user zoom**. The two major mobile screen readers — **TalkBack** (Android) and **VoiceOver** (iOS) — operate via gestures and expose the same semantic page structure (headings, landmarks, links, form controls) as their desktop equivalents.

---

## Core Pillars

### 1. The State of Mobile Accessibility

Modern mobile platforms have dramatically improved:
- Full-featured browsers with strong WAI-ARIA support.
- Built-in screen readers on both major platforms (TalkBack on Android, VoiceOver on iOS).
- No longer any need for separate mobile-only sites or browser sniffing.

**The three main mobile-specific areas needing special attention:**

| Area | The Problem | Solution |
|---|---|---|
| **Control mechanisms** | Touch-only gestures (no keyboard) can't trigger mouse-specific events | Use device-independent events (`click`) or provide touch + mouse equivalents |
| **User input** | Virtual keyboards are slow and error-prone | Minimize typing; use `<select>`, specialized `<input>` types |
| **Responsive design** | Small screens, slow connections, high-DPI displays | Media queries, viewport meta, responsive images, SVG |

---

### 2. TalkBack (Android Screen Reader)

**TalkBack** is the built-in Android screen reader, operated entirely via touch gestures.

#### Enabling TalkBack

- Navigate to Settings → Accessibility → TalkBack (exact location varies by device/Android version; some manufacturers such as Samsung ship their own screen reader instead).
- Toggle the slider switch to on.
- Follow on-screen prompts.

**Note:** Some Samsung phones replace TalkBack with their own screen reader (Samsung Voice Assistant / TalkBack is still available but may need to be installed).

#### Core TalkBack Gestures

| Gesture | Action |
|---|---|
| **Single tap** | Select an item — TalkBack reads it aloud |
| **Double tap** | Activate the selected item (open app, press button, follow link) |
| **Swipe left / right** | Move to previous / next item on screen |
| **Explore by touch** (hold + drag) | Read items as you drag — like moving a cursor across the screen |
| **Two-finger swipe up from bottom** | Unlock screen when TalkBack is on |
| **Swipe up + left (smooth)** | Go to home screen |
| **Two-finger swipe left / right** | Switch between home screens |
| **Quick swipe down → right** | Open global context menu |
| **Quick swipe up → right** | Open local context menu |

#### TalkBack Context Menus

- **Global menu** (`swipe down → right`): Device-level options (volume, etc.)
- **Local menu** (`swipe up → right`): App/screen-specific navigation options

**Web browsing navigation modes (accessed via local menu):**
- Headings and ARIA Landmarks
- Form controls
- Links
- Line-by-line
- Default (sequential element navigation)

**Turning TalkBack off:**
- Navigate to the TalkBack settings screen using TalkBack gestures, then toggle the slider off.

---

### 3. VoiceOver (iOS Screen Reader)

**VoiceOver** is the built-in iOS screen reader.

#### Enabling VoiceOver

- Settings → Accessibility → VoiceOver → toggle slider on.
- (Older iOS: Settings → General → Accessibility → VoiceOver)

#### Core VoiceOver Gestures

| Gesture | Action |
|---|---|
| **Single tap** | Select the tapped item — VoiceOver reads it aloud |
| **Swipe left / right** | Move to previous / next focusable item |
| **Slide finger around screen** | Move between items as you drag; release to select |
| **Double tap anywhere** | Activate currently selected item |
| **Three-finger swipe** | Scroll through a page |
| **Two-finger tap** | Context-relevant action (e.g., take photo in camera app) |

**Turning VoiceOver off:** Settings → General → Accessibility → VoiceOver → toggle slider off.

#### The Rotor

The **Rotor** is VoiceOver's navigation mode selector — accessed by **twisting two fingers on screen like a dial**.

**How to use:**
1. Twist two fingers on screen — VoiceOver announces each option as you rotate.
2. Release to select the option.
3. Use **swipe up / down** to iterate through values or items in the selected mode.

**Rotor options available when browsing web pages:**

| Rotor Option | What it navigates |
|---|---|
| Speaking Rate | Adjust TTS speed (swipe up = faster, down = slower) |
| Containers | Semantic containers on the page (landmarks) |
| Headings | Move between heading elements |
| Links | Move between hyperlinks |
| Form Controls | Move between form inputs, buttons |
| Language | Switch between available translations |

The Rotor options available are **context-sensitive** — they change depending on the current app or view.

#### VoiceOver Web Browser Navigation

1. Open browser → activate URL bar (swipe left/right to find it, double-tap to focus).
2. Type URL: hold finger on virtual keyboard until you find the character, release to select it, then double-tap to type.
3. Navigate page: swipe left/right between items; double-tap to activate.
4. Use Rotor → **Headings** to jump between headings (swipe up/down to navigate headings).

---

### 4. Control Mechanisms: Touch + Mouse Event Parity

The article directly references the CSS/JavaScript accessibility guide's mouse-specific events section. The core principle: **`click` is device-independent; `mousedown`/`mouseup` are not.**

#### The Problem — Mouse-Specific Events

```js
// ❌ BAD: mousedown/mouseup only fire from a mouse pointer.
// Touch users and keyboard users cannot activate this.
div.onmousedown = () => {
  initialBoxX = div.offsetLeft;
  initialBoxY = div.offsetTop;
  movePanel();
};
document.onmouseup = stopMove;
```

**What fails:**
- Touch users: `mousedown` does not fire from touch events.
- Keyboard users: No mechanism to trigger mousedown via keyboard.

#### The Solution — Parallel Touch Events

```js
// ✅ GOOD: Touch events fire from finger interactions on touchscreens.
div.ontouchstart = (e) => {
  initialBoxX = div.offsetLeft;
  initialBoxY = div.offsetTop;
  positionHandler(e);
  movePanel();
};
panel.ontouchend = stopMove;
```

Implement both sets of handlers in parallel:

```js
// Device-independent approach: handle mouse AND touch together
div.onmousedown = startDrag;
div.ontouchstart = startDrag; // same handler, or adapted version

document.onmouseup = stopMove;
panel.ontouchend = stopMove;
```

#### Touch Event vs. Mouse Event Equivalents

| Mouse Event | Touch Equivalent | Notes |
|---|---|---|
| `mousedown` | `touchstart` | Fires when finger first contacts screen |
| `mousemove` | `touchmove` | Fires as finger moves across screen |
| `mouseup` | `touchend` | Fires when finger lifts from screen |
| `click` | `click` (also fires on touch) | **Device-independent — the safest choice** |

**Key rule:** For simple interactions (buttons, links, form elements), always prefer `click` — it fires on mouse click, keyboard Enter/Space, and touch tap. Only implement separate touch events when you need complex touch-specific behaviors (multi-touch, swipe gestures, drag-and-drop).

---

### 5. Responsive Design for Mobile Accessibility

Responsive design is required for mobile accessibility, not just aesthetics. Three specific problem areas:

#### 5a. Layout Suitability

Multi-column desktop layouts break on narrow screens. Text may become unreadably small.

**Solutions:**
- **Media queries** — reflow layout at breakpoints:
  ```css
  @media (max-width: 600px) {
    .columns { flex-direction: column; }
  }
  ```
- **Viewport meta tag** — tell the browser to use the device's actual width (see section 6 on not disabling zoom).
- **Flexbox / CSS Grid** — flexible layout systems that naturally adapt to available space.

#### 5b. Image Size (Bandwidth)

Mobile users often have slower network connections. Sending a 2000px-wide desktop image to a 375px phone wastes bandwidth and slows page load.

**Solution: Responsive images**

```html
<!-- srcset + sizes: browser picks the most appropriate image -->
<img
  src="image-small.jpg"
  srcset="image-small.jpg 480w, image-medium.jpg 800w, image-large.jpg 1200w"
  sizes="(max-width: 600px) 480px, (max-width: 1000px) 800px, 1200px"
  alt="Description of image"
/>
```

Or use the `<picture>` element for art-direction (different crop/composition per breakpoint).

#### 5c. High-Resolution Screens (Retina/HiDPI)

Many mobile devices have pixel-dense screens (2x, 3x device pixel ratio). A 100px CSS image rendered on a 2x screen uses 200 physical pixels — a standard-resolution image will appear blurry.

**Solutions:**
- Provide higher-resolution image versions in `srcset` with `2x` / `3x` descriptors.
- Use **SVG** for icons, logos, and illustrations — SVG is vector-based, scales to any size without quality loss, and typically has a much smaller file size than raster equivalents.

```html
<!-- SVG: sharp at any resolution, single file, small size -->
<img src="logo.svg" alt="Company logo" />
```

---

### 6. Specific Mobile Considerations

#### 6a. Never Disable Zoom (`user-scalable=no`)

The viewport meta tag controls how mobile browsers render and scale a page.

**CORRECT pattern — always use this:**

```html
<meta name="viewport" content="width=device-width; user-scalable=yes" />
```

**NEVER use this:**

```html
<!-- ❌ WRONG: disables pinch-to-zoom — a critical accessibility feature -->
<meta name="viewport" content="width=device-width; user-scalable=no" />
<!-- Also forbidden: -->
<meta name="viewport" content="width=device-width; maximum-scale=1" />
```

**Why `user-scalable=no` is harmful:**
- Many users with low vision rely on pinch-to-zoom to read text that is too small.
- Text that appears readable at 16px may be illegible at 10px for users with vision impairments.
- Disabling zoom is a WCAG 2.1 Level AA failure (Success Criterion 1.4.4 — Resize text).
- There is almost no valid reason to disable zoom; if your UI breaks when zoomed, the UI has a design problem that needs fixing.

**If you genuinely cannot allow zoom** (e.g., a map interface), provide an alternative — such as a control that increases the font size within the component — that doesn't disable the system-level zoom capability.

#### 6b. Accessible Hamburger Menus

Mobile navigation is commonly collapsed into a hamburger menu (☰ icon) to conserve screen space.

**Requirements for an accessible hamburger menu:**
1. **The toggle button must be accessible by touch** — use a real `<button>` element (not a `<div>` or `<span>`).
2. **Correct ARIA state** — use `aria-expanded="false"` / `aria-expanded="true"` on the button to communicate open/closed state to screen readers.
3. **Page content must be hidden or unreachable** while the menu is open — prevent screen reader users from accidentally navigating into the page behind the open menu.

```html
<!-- Example accessible hamburger button -->
<button
  class="hamburger"
  aria-expanded="false"
  aria-controls="nav-menu"
  aria-label="Open navigation menu"
>☰</button>

<nav id="nav-menu" hidden>
  <!-- Navigation links -->
</nav>
```

```js
hamburgerBtn.addEventListener("click", () => {
  const isExpanded = hamburgerBtn.getAttribute("aria-expanded") === "true";
  hamburgerBtn.setAttribute("aria-expanded", String(!isExpanded));
  navMenu.hidden = isExpanded;
});
```

---

### 7. User Input: Minimizing Mobile Typing

Typing on a virtual keyboard is significantly slower and more error-prone than on a physical keyboard. The article's core advice: **minimize typing requirements**.

#### Strategy 1: Replace Free-Text with `<select>` Menus

Instead of:
```html
<!-- ❌ Slow: forces user to type their job title character by character -->
<label for="job-title">Job title</label>
<input type="text" id="job-title" name="job-title" />
```

Use:
```html
<!-- ✅ Faster: user selects from common options with one tap -->
<label for="job-type">Job title</label>
<select id="job-type" name="job-type">
  <option>Software Engineer</option>
  <option>Product Manager</option>
  <option>Designer</option>
  <option>Other</option>
</select>
<!-- Show a text field only when "Other" is selected -->
```

**Additional benefits of `<select>`:** improves data consistency (no spelling variations, no case issues).

#### Strategy 2: Use Semantic HTML `<input>` Types

Mobile browsers display **context-appropriate virtual keyboards** for different input types — a massive usability win.

| `<input type="">` | Mobile benefit |
|---|---|
| `type="number"` | Shows numeric keypad |
| `type="tel"` | Shows telephone number keypad (includes `+`, `*`, `#`) |
| `type="email"` | Shows keyboard with `@` and `.com` keys visible |
| `type="url"` | Shows keyboard with `/`, `.`, and `.com` keys |
| `type="search"` | Shows keyboard with search/go button |
| `type="date"` | Shows native date picker widget (calendar UI) |
| `type="time"` | Shows native time picker widget |

These are not just usability improvements — they also communicate semantic meaning to AT and reduce validation errors.

#### Strategy 3: Feature Detection for Desktop Fallbacks

If a specialized input type doesn't fit the desktop UX, use feature detection to serve different markup conditionally:

```js
// Example: check if the browser supports a native date picker
const testInput = document.createElement("input");
testInput.setAttribute("type", "date");
if (testInput.type === "text") {
  // Browser doesn't support date input natively — load a JS date picker
}
```

---

## Technical Deep-Dive

### Deep-Dive 1: Why `click` Is Device-Independent (Event Model)

When a user **taps** on a mobile touchscreen:
1. `touchstart` fires.
2. `touchend` fires.
3. The browser synthesizes a **`click` event** (after ~300ms delay on older browsers, near-instantly on modern browsers with `touch-action: manipulation` or pointer events).

This is why `onclick` and `addEventListener("click", ...)` work on mobile without explicit touch event handlers. The browser itself bridges touch to click.

**The 300ms delay** was originally introduced to detect double-tap-to-zoom gestures. Modern mobile browsers eliminate this delay when:
- The viewport meta tag sets `width=device-width` (indicating a responsive site).
- CSS `touch-action: manipulation` is applied (tells browser this element won't use double-tap zoom).

**Implication for accessibility testing:** Always test interactive elements with both a mouse and your finger on a touch device. If an element only responds to mouse events, it will silently fail on mobile.

---

### Deep-Dive 2: TalkBack vs. VoiceOver — Comparison Table

| Feature | TalkBack (Android) | VoiceOver (iOS) |
|---|---|---|
| **Platform** | Android | iOS |
| **Enable location** | Settings → Accessibility → TalkBack | Settings → Accessibility → VoiceOver |
| **Navigate items** | Swipe left / right | Swipe left / right |
| **Activate item** | Double-tap anywhere | Double-tap anywhere |
| **Explore by touch** | Hold + drag | Slide finger around |
| **Page scroll** | Two-finger swipe | Three-finger swipe |
| **Navigation mode selector** | Local context menu (`swipe up → right`) | Rotor (twist two fingers) |
| **Navigate by heading** | Local menu → "Headings and Landmarks" | Rotor → Headings → swipe up/down |
| **Navigate by link** | Local menu → "Links" | Rotor → Links → swipe up/down |
| **Navigate by form control** | Local menu → "Form Controls" | Rotor → Form Controls → swipe up/down |
| **Semantic dependency** | Requires proper headings, ARIA landmarks, alt text | Same — semantic HTML equally critical |

**The shared lesson:** Both screen readers navigate web content using the same semantic cues as desktop screen readers — heading hierarchy, landmark regions, link text, form labels. A semantically correct page works correctly on both platforms without any mobile-specific AT code.

---

### Deep-Dive 3: Touch Event Object — Accessing Coordinates

When implementing custom touch interactions, the `TouchEvent` object has a different coordinate structure than `MouseEvent`:

```js
div.ontouchstart = (e) => {
  // TouchEvent has a "touches" list — not a single x/y like MouseEvent
  const touch = e.touches[0]; // First touch point

  const x = touch.clientX; // X coordinate relative to viewport
  const y = touch.clientY; // Y coordinate relative to viewport
  const pageX = touch.pageX; // X relative to full page (includes scroll)
  const pageY = touch.pageY;

  // Equivalent MouseEvent properties: e.clientX, e.clientY
  // This is why a generic positionHandler(e) needs to handle both types
};
```

This explains the `positionHandler(e)` call in the article's drag example — a function that abstracts the coordinate extraction from either a `TouchEvent` or `MouseEvent`.

```js
function getPosition(e) {
  // Handle both touch and mouse events
  if (e.touches) {
    return { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }
  return { x: e.clientX, y: e.clientY };
}
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **TalkBack** | The built-in screen reader on Android devices; operated via touch gestures (swipe, double-tap, explore by touch) rather than keyboard shortcuts. |
| **VoiceOver (mobile)** | The built-in screen reader on iOS devices; uses gestures including the Rotor for navigation mode selection. |
| **The Rotor** | A VoiceOver navigation control activated by twisting two fingers on screen; lets users switch between navigation modes (Headings, Links, Form Controls, etc.) |
| **TalkBack local context menu** | A gesture-accessible menu in TalkBack (swipe up + right) that provides page-level navigation modes such as Headings and Landmarks, Links, and Form Controls. |
| **Explore by touch** | A TalkBack interaction mode where users drag a finger across the screen and the device reads aloud every element the finger passes over. |
| **Global context menu (TalkBack)** | A TalkBack menu (swipe down + right) providing device-level options unrelated to the current app or page. |
| **`click` event** | A device-independent DOM event that fires for mouse clicks, keyboard Enter/Space activation, and touch screen taps — the preferred event for universal accessibility. |
| **`mousedown` / `mouseup`** | Mouse-specific events that are NOT triggered by touch or keyboard; cause accessibility failures if used as the sole interaction mechanism. |
| **`touchstart`** | A touch event that fires when a finger first contacts the screen; the touch equivalent of `mousedown`. |
| **`touchend`** | A touch event that fires when a finger is lifted from the screen; the touch equivalent of `mouseup`. |
| **`ontimeupdate`** | (Media context) An event firing ~once/second during playback — not mobile-specific. |
| **`user-scalable=no`** | A viewport meta parameter that disables pinch-to-zoom on mobile; a WCAG 2.1 Level AA failure (SC 1.4.4) that must not be used. |
| **`user-scalable=yes`** | The correct viewport meta value ensuring pinch-to-zoom remains available. |
| **`width=device-width`** | A viewport meta parameter that sets the layout viewport width to the device's screen width; required for responsive design and eliminates the 300ms click delay on modern browsers. |
| **Hamburger menu** | A navigation design pattern that collapses site navigation behind a button (typically ☰) on mobile; must use `<button>` with `aria-expanded` for accessibility. |
| **`aria-expanded`** | A WAI-ARIA state attribute (`true`/`false`) placed on a toggle control to inform AT whether the controlled region is currently expanded or collapsed. |
| **Responsive images** | HTML techniques (`srcset`, `sizes`, `<picture>`) that serve differently sized image files to different devices, reducing bandwidth waste on mobile. |
| **SVG (Scalable Vector Graphics)** | A vector image format that scales to any resolution without quality loss and typically has a small file size; the preferred format for icons and logos on high-DPI mobile screens. |
| **HiDPI / Retina screen** | A display with a device pixel ratio greater than 1 (typically 2x or 3x); requires higher-resolution images or SVG to appear sharp. |
| **Semantic `<input>` types** | HTML input type values (`number`, `tel`, `email`, `date`, `time`, etc.) that trigger context-appropriate virtual keyboards and native picker widgets on mobile. |
| **Feature detection** | A technique for checking whether the current browser supports a feature (e.g., a native date picker) and conditionally loading a polyfill or alternative — preferred over user-agent sniffing. |
| **300ms tap delay** | A historical mobile browser behavior that waited 300ms after a tap to determine if it was a double-tap-to-zoom; eliminated on modern browsers when `width=device-width` is set. |

---

## Watch Out For…

1. **Setting `user-scalable=no` or `maximum-scale=1` in the viewport meta tag** — This disables pinch-to-zoom and is a direct WCAG 2.1 AA violation. Many low-vision users (who do not use screen readers) depend on pinch-to-zoom as their primary accessibility workaround.

2. **Using `mousedown`/`mouseup` as the sole interaction handlers for custom controls** — These events don't fire on touch. Always pair mouse events with their touch equivalents, or use the device-independent `click` event wherever possible.

3. **Assuming `click` doesn't work on mobile** — It does. Modern mobile browsers synthesize a `click` event from a touch tap. Developers who reach for `touchstart` for simple button interactions are adding unnecessary complexity.

4. **Using a non-`<button>` element for the hamburger menu toggle** — A `<div>` or `<span>` is not focusable by default, won't be announced as a control by screen readers, and won't activate with touch AT double-tap. Use `<button>`.

5. **Omitting `aria-expanded` from the hamburger toggle button** — Without it, screen reader users have no way to know whether the navigation is open or closed. They cannot tell if their activation attempt had any effect.

6. **Not hiding the page content behind an open mobile menu** — If the hamburger menu overlays the page but doesn't move focus or hide underlying content, TalkBack and VoiceOver users will swipe into the page content behind the menu, creating a deeply confusing experience.

7. **Assuming `type="text"` is fine for phone and number fields on mobile** — It shows the full QWERTY keyboard. Using `type="tel"` or `type="number"` shows a numeric/phone keypad — a massive friction reduction. This is zero-cost accessibility AND usability.

8. **Serving full-resolution desktop images to mobile devices** — Large images on slow connections degrade performance (which is itself an accessibility concern for users on limited data plans or slow networks). Always implement responsive images.

9. **Not testing with actual mobile screen readers** — Emulators and DevTools' mobile simulation mode do not test TalkBack or VoiceOver gesture flows. Actual AT testing requires a real device with the screen reader enabled.

10. **Treating mobile accessibility as "extra"** — The article's opening establishes that mobile web access is now as common as desktop. Retrofitting mobile accessibility is far more expensive than building it in from the start.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** A developer has a draggable panel that uses `mousedown` and `mouseup` for dragging. It works on desktop but is completely non-functional on mobile touch. Explain the root cause and write the corrected JavaScript with both mouse and touch event handlers that make drag work on both platforms.

**Q2.** What is the VoiceOver Rotor? How is it activated, and name four navigation modes available when browsing a web page. What does this tell you about the importance of semantic HTML on mobile?

**Q3.** A product manager says: "Let's disable zoom on our mobile site so the layout doesn't break when users pinch." Write a full technical rebuttal explaining why `user-scalable=no` is unacceptable, citing the specific WCAG criterion it violates and who is harmed.

**Q4.** List the five `<input>` types that trigger specialized mobile virtual keyboards or picker widgets, state the keyboard/widget each displays, and explain why this is an accessibility consideration beyond just convenience.

**Q5.** Compare TalkBack and VoiceOver in three key areas: (a) navigation mode selector mechanism, (b) how users navigate by heading, and (c) how users activate an item on screen.

---

## Answer Key

---

**A1.**

**Root cause:** `mousedown` and `mouseup` are mouse-specific DOM events. They fire when a mouse pointer button is pressed and released respectively. On touchscreen devices, finger contact generates `touchstart` and `touchend` events — not `mousedown`/`mouseup`. Since no handler exists for the touch events, the drag functionality is completely inaccessible on mobile.

**Corrected JavaScript:**

```js
const div = document.querySelector(".draggable");

let initialBoxX, initialBoxY;

// Mouse events — for desktop users
div.onmousedown = (e) => {
  initialBoxX = div.offsetLeft;
  initialBoxY = div.offsetTop;
  positionHandler(e);
  movePanel();
};
document.onmouseup = stopMove;

// Touch events — for mobile touchscreen users
div.ontouchstart = (e) => {
  initialBoxX = div.offsetLeft;
  initialBoxY = div.offsetTop;
  positionHandler(e);
  movePanel();
};
// Note: touchend goes on the panel/document, not the div,
// so lifting the finger anywhere stops the drag
panel.ontouchend = stopMove;

// Coordinate abstraction — handles both MouseEvent and TouchEvent
function positionHandler(e) {
  const x = e.touches ? e.touches[0].clientX : e.clientX;
  const y = e.touches ? e.touches[0].clientY : e.clientY;
  // ... use x and y for positioning
}
```

**Why both sets of handlers:** Mouse and touch events are separate systems in the browser. A single unified handler requires the Pointer Events API (`pointerdown`, `pointermove`, `pointerup`) as a more modern alternative — but the parallel touch+mouse approach is widely supported and explicitly demonstrated in the MDN article.

---

**A2.**

**The Rotor** is VoiceOver's navigation mode selector — a virtual dial control that lets users choose how they want to move through content on the current screen.

**Activation:** Twist two fingers on the screen simultaneously, as if rotating a physical dial. VoiceOver announces each option as you rotate. Release when the desired mode is spoken.

**Four navigation modes when browsing web pages:**

1. **Headings** — After selecting: swipe up/down to jump between heading elements (`<h1>`–`<h6>`).
2. **Links** — After selecting: swipe up/down to jump between hyperlinks.
3. **Form Controls** — After selecting: swipe up/down to move between form inputs and buttons.
4. **Containers** — After selecting: swipe up/down to move between semantic containers (ARIA landmark regions, `<nav>`, `<main>`, `<section>`, etc.).

**What this tells us about semantic HTML on mobile:** The Rotor's navigation modes work by querying the accessibility tree for specific element types. If a page uses `<div class="heading">` instead of `<h2>`, heading navigation finds nothing. If a page uses `<div onclick>` instead of `<a>`, link navigation finds nothing. Semantic HTML is just as critical on mobile as on desktop — mobile screen readers have identical structural requirements; they just use gesture-based, not keyboard-based, navigation to traverse them.

---

**A3.**

**Technical rebuttal:**

Setting `user-scalable=no` (or equivalently `maximum-scale=1`) in the viewport meta tag disables the operating system's pinch-to-zoom feature in the browser. This violates **WCAG 2.1 Success Criterion 1.4.4 — Resize text (Level AA)**, which requires that:

> "Text can be resized without assistive technology up to 200 percent without loss of content or functionality."

Disabling zoom prevents users from resizing text to a comfortable reading size, which is a direct failure of this criterion.

**Who is harmed:**

1. **Users with low vision** — The largest group affected. Many users with mild-to-moderate vision impairment do not use a screen reader; they rely on pinch-to-zoom to make text large enough to read. Disabling this forces them to either abandon the site or struggle with unreadable text.

2. **Older users** — Age-related vision decline (presbyopia) is extremely common. Zoom is a primary coping mechanism.

3. **All users in situational challenges** — Reading in bright sunlight, on a small phone, or while fatigued. These are not disability scenarios but are real situations where users benefit from zoom.

**Why the layout breaking is not a valid reason:**

If your layout breaks when zoomed, this is a **responsive design defect**, not a reason to remove a fundamental accessibility feature. The correct solution is:
- Use relative units (`rem`, `%`, `vw`) instead of fixed pixel dimensions.
- Test your layout at 200% zoom and fix what breaks.
- If a specific interactive component genuinely cannot scale (e.g., a complex map widget), provide an in-component font-size control as an equivalent alternative — but do not disable system zoom globally.

**Correct viewport declaration:**

```html
<meta name="viewport" content="width=device-width; user-scalable=yes" />
```

---

**A4.**

| `type` value | Mobile keyboard / widget | Accessibility consideration |
|---|---|---|
| `type="number"` | Numeric keypad (digits 0–9, decimal, minus) | Reduces entry errors for numeric fields; communicates numeric expectation to AT |
| `type="tel"` | Telephone keypad (digits + `*`, `#`, `+`) | Optimized for phone number entry; less error-prone than QWERTY; semantically meaningful |
| `type="email"` | QWERTY with `@` and `.com` keys readily visible | Reduces errors in email entry; browser auto-validates format |
| `type="date"` | Native date picker / calendar widget | Eliminates date format ambiguity (MM/DD or DD/MM?); mobile calendar widget is clear and touch-friendly |
| `type="time"` | Native time picker widget | Eliminates AM/PM and format confusion; no manual text entry |

**Why this is an accessibility consideration beyond convenience:**

1. **Reduces cognitive load:** Showing a numeric keypad for a number field means users don't have to locate digits on a QWERTY layout — a significant benefit for users with cognitive or motor impairments.

2. **Reduces motor errors:** A larger, purpose-built keypad reduces tap accuracy requirements, helping users with tremors or limited fine motor control.

3. **Eliminates format errors:** Native date/time pickers prevent format mismatch errors (a common source of frustration that can lock out users who cannot understand error messages).

4. **Consistent semantic meaning:** `type="tel"` communicates "this is a phone number field" to AT, which can apply appropriate auto-fill strategies and contextual announcements.

5. **Form accessibility is WCAG-relevant (3.3.2 Labels or Instructions):** Ensuring input format is clear (by providing format-enforcing widgets) is part of WCAG's requirements for helping users avoid and correct input errors.

---

**A5.**

| Area | TalkBack (Android) | VoiceOver (iOS) |
|---|---|---|
| **(a) Navigation mode selector** | **Local context menu** — accessed by swiping up and to the right in a smooth motion; then swipe left/right between mode options; double-tap to activate. | **The Rotor** — accessed by twisting two fingers on the screen simultaneously as if turning a dial; each option is announced; release to select. |
| **(b) Navigate by heading** | Open local context menu → swipe to find "Headings and Landmarks" → double-tap to activate. Then swipe left/right to move between headings and ARIA landmarks. | Open Rotor → rotate to "Headings" → release. Then swipe up/down to move backward/forward through headings. |
| **(c) Activate an item** | **Double-tap anywhere on screen** while the desired item is selected (focus highlighted by TalkBack). | **Double-tap anywhere on screen** while the desired item is selected (announced by VoiceOver). |

**Common conclusion:** Both screen readers share the fundamental pattern of *select first, then activate* — a two-step model that differs from sighted mouse use (point and click simultaneously). This is why AT users may appear to interact more slowly; each action requires explicit selection confirmation.
