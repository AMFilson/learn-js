# 📚 What is Accessibility? — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/What_is_accessibility

---

## Executive Summary

This article introduces web accessibility as the practice of making websites usable by as many people as possible, including those with physical, cognitive, visual, and hearing disabilities. It centers on the interplay between disability types, assistive technologies (ATs), legal obligations, and the OS-level accessibility APIs that enable ATs to consume web content. The most exam-critical takeaway is that **accessibility must be built in from the project start**, not retrofitted — and that WCAG conformance is the internationally recognised standard for meeting both ethical and legal obligations.

---

## Core Pillars

### 1. Defining Accessibility

- **Accessibility** = making websites usable by *as many people as possible*, not just people with disabilities.
- Also benefits: mobile users, users on slow/limited connections, aging populations.
- Framed as a **human-rights issue**: excluding someone from a website due to a disability is analogous to excluding a wheelchair user from a physical building.
- Key business and technical incentives:
  - **Semantic HTML** → improves both accessibility *and* SEO.
  - Accessible sites reach wider audiences and comply with legal requirements.
  - Good accessibility practices (e.g., clear layouts, readable text) improve UX for *all* users.
  - Accessibility is the **law** in several jurisdictions.

---

### 2. Disability Categories & Assistive Technologies

> WHO statistic: ~15% of the world's population (~1 billion people) live with some form of disability.

#### Visual Impairments

| Condition | Common AT |
|---|---|
| Blindness | Screen readers (software that reads digital text aloud) |
| Low vision | Screen magnifiers (physical or software zoom) |
| Colour blindness | Colour contrast tools, custom stylesheets |

**Screen reader examples:**

| Category | Examples |
|---|---|
| Commercial (Windows) | JAWS, Dolphin Screen Reader |
| Free (Windows) | NVDA |
| Built into OS | VoiceOver (macOS/iOS), Narrator (Windows), ChromeVox (ChromeOS), TalkBack (Android) |
| Free (Linux) | Orca |

- ~285 million people are visually impaired globally (39M blind, 246M low vision — WHO).

#### Hearing Impairments (Deaf/Hard-of-Hearing — DHH)

- DHH users rarely use specialised hardware ATs; the AT gap is filled by **content-based solutions**.
- Required accommodations:
  - **Manual captions** on all videos.
  - **Transcripts** for all audio content.
  - **Text simplification** — DHH populations can experience language deprivation, reducing reading fluency.
- ~466 million people worldwide have disabling hearing loss (WHO).

#### Mobility Impairments

- Range: loss of limb, paralysis, neurological/genetic conditions, old age, no mouse available.
- Primary web impact: controls **must be keyboard-accessible**.
  - Users navigate with `Tab` key, directional keys, head pointers, switch devices.
- ~16.1% of non-institutionalised US adults have physical functioning difficulty (CDC).

#### Cognitive Impairments

- Broadest category: intellectual disabilities, mental illness (depression, schizophrenia), learning disabilities (dyslexia, ADHD), age-related cognitive decline.
- Shared functional problems: difficulty understanding content, remembering tasks, confusion from inconsistent layouts.
- Design best practices for cognitive accessibility:
  - Deliver content via **multiple modalities** (text, video, TTS).
  - Use **plain language** standards.
  - Focus attention on important content; **minimise distractions**.
  - **Consistent layout and navigation** across pages.
  - Use **familiar conventions** (unvisited links = blue, visited = purple).
  - Break multi-step processes into **logical steps with progress indicators**.
  - **Simplify authentication** without compromising security.
  - Provide **clear error messages** and easy error recovery in forms.
- CDC (2018): 1 in 4 US citizens have a disability; cognitive impairment is the most common type in young people.
- W3C's **Cognitive and Learning Disabilities Accessibility Task Force (COGA)** produces relevant guidelines.

---

### 3. Implementing Accessibility in a Project

**The retrofit myth:** Accessibility is expensive only when bolted on late. When integrated from the start, incremental cost is minimal.

#### When retrofitting is expensive — triggered by:
- Existing site with significant legacy accessibility issues.
- Accessibility only considered in the late stages of a project.

#### Recommended workflow:
1. **Factor accessibility testing into the testing regime from day one** — treat it like any other quality target (e.g., browser compatibility).
2. **Test early and often:**
   - Automated tools: detect missing `alt` text, poor link text, missing form labels.
   - Manual testing with disabled user groups for complex interactions.
3. **Key questions to validate:**
   - Is a date picker widget usable by screen reader users?
   - Are dynamically updated regions announced to screen reader users?
   - Are UI buttons accessible via both keyboard and touch?
4. **Budget realism:** "100% accessibility" is an unobtainable ideal. Provide accessible *alternatives* where full accessibility of a feature is impractical (e.g., a data table alongside a 3D chart).
5. **Publish an accessibility statement** describing your policy and the steps taken — demonstrates good faith and provides a contact point for issues.

#### Core principle:
> An accessibility bug is like any other bug: the later it's found, the more expensive it is to fix.

---

### 4. Accessibility Guidelines (WCAG)

**WCAG (Web Content Accessibility Guidelines)** — published by the W3C.

- Large, technology-agnostic document defining precise conformance criteria.
- Criteria are grouped into **four principles (POUR)**:

| Principle | Meaning |
|---|---|
| **Perceivable** | Information must be presentable in ways users can perceive (e.g., text alternatives for images) |
| **Operable** | UI components must be operable by all users (e.g., keyboard navigability) |
| **Understandable** | Information and UI operation must be understandable |
| **Robust** | Content must be robust enough to be interpreted by a wide variety of ATs |

- Recommended entry point: **WCAG at a Glance** — not necessary to memorise all criteria, but key areas must be understood.

---

### 5. Legal Requirements by Jurisdiction

| Region | Legislation |
|---|---|
| European Union | EN 301 549 |
| United States | Section 508 of the Rehabilitation Act |
| Germany | Federal Ordinance on Barrier-Free Information Technology |
| United Kingdom | Accessibility Regulations 2018 |
| Italy | Accessibilità |
| Australia | Disability Discrimination Act |

- The W3C maintains a list of **Web Accessibility Laws & Policies** by country.
- Non-compliance can create **legal liability** — failure to make content accessible is not merely an ethical failing.

---

### 6. Accessibility APIs

**Mechanism:** Browsers expose content to ATs via **accessibility APIs** built into each OS.

- ATs consume **semantic information** from the **accessibility tree** — not styling or JavaScript runtime state.
- The accessibility tree is a structured representation of the DOM's semantics.

**OS-specific accessibility APIs:**

| OS | API |
|---|---|
| Windows | MSAA/IAccessible, UIAExpress, IAccessible2 |
| macOS | NSAccessibility |
| Linux | AT-SPI |
| Android | Accessibility framework |
| iOS | UIAccessibility |

#### WAI-ARIA

- When native HTML semantics are insufficient, **WAI-ARIA (Accessible Rich Internet Applications)** provides additional semantic attributes to supplement the accessibility tree.
- WAI-ARIA attributes are read by ATs via the OS accessibility API — they do not affect visual rendering.
- Use native HTML semantics first; WAI-ARIA is a supplement, not a replacement.

---

## Technical Deep-Dive

### Logic Walkthrough: How the Accessibility Tree Bridges HTML → AT

**Setup (HTML):**
```html
<!-- Button with meaningful label -->
<button id="submit-order">Place Order</button>

<!-- Image with alt text -->
<img src="product.jpg" alt="Blue denim jacket, size M" />

<!-- Input with associated label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" />
```

**Step-by-step flow:**

1. **Browser parses HTML** → builds the DOM tree.
2. **Browser derives semantics** from element types (`<button>`, `<img>`, `<input>`) and attributes (`alt`, `for`/`id` pairing).
3. **Browser constructs the accessibility tree** — a parallel structure containing: role, name, state, value for each node.
   - `<button>` → role: `button`, name: `"Place Order"`, state: `enabled`
   - `<img>` → role: `img`, name: `"Blue denim jacket, size M"`
   - `<input type="email">` → role: `textbox`, name: `"Email address"`, state: `focused / unfocused`
4. **Browser exposes accessibility tree** to the OS accessibility API (e.g., UIAExpress on Windows).
5. **AT (e.g., NVDA)** queries the OS API → announces: *"Place Order, button"*, *"Email address, edit text"*.
6. **WAI-ARIA gap filling:** if a custom `<div>` is used instead of `<button>`:
   ```html
   <!-- Without ARIA — AT sees no role, no interaction hint -->
   <div onclick="submitOrder()">Place Order</div>

   <!-- With ARIA — AT correctly announces as a button -->
   <div role="button" tabindex="0" onclick="submitOrder()" onkeydown="handleKey(event)">
     Place Order
   </div>
   ```
   - `role="button"` → tells AT the element behaves as a button.
   - `tabindex="0"` → makes it keyboard-focusable.
   - Keyboard event handler is still required manually — native `<button>` handles this automatically.

**Output / AT experience:** Without proper semantics, a screen reader user hears nothing useful. With correct semantics, they hear role + name + state for every interactive element.

---

### Logic Walkthrough: Cognitive Accessibility — Multi-Step Form

**Setup (Design Pattern):**
```html
<!-- Step 1 of 3 — with progress indicator -->
<fieldset>
  <legend>Step 1 of 3: Personal Details</legend>
  <label for="fname">First name</label>
  <input id="fname" type="text" autocomplete="given-name" />

  <label for="lname">Last name</label>
  <input id="lname" type="text" autocomplete="family-name" />

  <!-- Clear, inline error — not just colour -->
  <p id="fname-error" role="alert" style="color: red;">
    ⚠ First name is required. Please enter your first name.
  </p>
</fieldset>
```

**Cognitive accessibility principles applied:**
1. `<fieldset>` + `<legend>` → groups related fields and indicates position in process.
2. `autocomplete` attributes → reduce cognitive load by allowing browser to prefill.
3. `role="alert"` on error → announced immediately by screen readers without user re-focusing.
4. Error message is descriptive (*what* is wrong + *how* to fix it) — not just "Invalid input".

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Accessibility** | The practice of designing and building websites so they are usable by as many people as possible, including those with disabilities. |
| **Assistive Technology (AT)** | Hardware or software used by people with disabilities to interact with digital content (e.g., screen readers, refreshable Braille displays). |
| **Screen reader** | Software that converts digital text and UI element information into synthesised speech or Braille output for users with visual impairments. |
| **WCAG** | Web Content Accessibility Guidelines — the W3C's primary technology-agnostic standard for web accessibility conformance, structured around the POUR principles. |
| **POUR** | The four WCAG principles: **P**erceivable, **O**perable, **U**nderstandable, **R**obust. |
| **Accessibility tree** | A browser-maintained parallel structure of the DOM that contains semantic role, name, state, and value information exposed to OS accessibility APIs. |
| **Accessibility API** | OS-level interface through which browsers expose the accessibility tree to assistive technologies (e.g., MSAA/IAccessible2 on Windows, NSAccessibility on macOS). |
| **WAI-ARIA** | Web Accessibility Initiative — Accessible Rich Internet Applications; a W3C specification providing attributes (roles, states, properties) to supplement native HTML semantics for AT consumers. |
| **`role` attribute** | A WAI-ARIA attribute that explicitly declares the semantic role of an element to the accessibility tree (e.g., `role="button"`, `role="alert"`). |
| **`tabindex`** | HTML attribute controlling keyboard focusability; `tabindex="0"` inserts an element into the natural tab order; `tabindex="-1"` makes it programmatically focusable but not tab-reachable. |
| **`alt` attribute** | Text alternative for `<img>` elements; exposed as the accessible name of the image in the accessibility tree; critical for screen reader users. |
| **DHH** | Deaf and Hard-of-Hearing — a collective term for users with hearing loss ranging from mild to profound. |
| **Language deprivation** | A condition common in DHH populations where limited exposure to early language development reduces reading fluency, warranting simplified text on the web. |
| **Section 508** | US federal law (amendment to the Rehabilitation Act) requiring federal agencies and those receiving federal funding to make ICT accessible. |
| **EN 301 549** | EU standard mandating accessibility requirements for public sector ICT products and services. |
| **Cognitive accessibility** | Design practices addressing the needs of users with cognitive impairments — including consistency, plain language, minimal distractions, and error recovery. |
| **NVDA** | NonVisual Desktop Access — a free, open-source screen reader for Windows widely used for accessibility testing. |
| **VoiceOver** | Built-in screen reader on Apple devices (macOS, iOS, iPadOS); commonly used as the primary AT testing tool for Apple platforms. |
| **Accessibility statement** | A public-facing webpage a site publishes to document its accessibility policy, conformance level, and contact process for reporting issues. |
| **`role="alert"`** | WAI-ARIA live region role that causes screen readers to announce content immediately when it is inserted into the DOM, without requiring user focus change. |

---

## Watch Out For...

1. **"Accessibility is only for blind users"** — Accessibility encompasses visual, auditory, motor, and cognitive disabilities, as well as situational impairments (e.g., a user holding a baby with one hand, bright sunlight on a screen). Designing only for screen readers leaves out the majority of users with disabilities.

2. **"Accessibility can be added at the end of a project"** — Retrofitting accessibility onto an existing site with significant issues is expensive and disruptive. The correct practice is to integrate accessibility from the planning phase, testing it continuously like any other quality target.

3. **"WAI-ARIA replaces semantic HTML"** — WAI-ARIA *supplements* the accessibility tree when native HTML semantics are insufficient; it does not replace them. A `<div role="button">` still requires manual keyboard event handling and `tabindex="0"`, while a native `<button>` provides all of these automatically.

4. **"Colour alone communicates information"** — Relying solely on colour (e.g., red = error, green = success) fails users with colour blindness. Always pair colour with text labels, icons, or patterns.

5. **"100% accessibility is achievable"** — MDN explicitly states "100% accessibility is an unobtainable ideal." Focus on maximising coverage and providing accessible alternatives rather than seeking perfection for every edge case.

6. **"Accessibility APIs expose styling/JavaScript information"** — Accessibility APIs expose only **semantic** information (role, name, state, value). CSS styles and JavaScript runtime state are generally not surfaced to ATs via the accessibility tree.

7. **"Captions and transcripts serve the same purpose"** — **Captions** are synchronised with video playback and typically replace audio for DHH users watching video. **Transcripts** are full text documents of audio content, suitable for audio-only media. Both are required for full DHH access.

8. **"Accessibility is optional if not legally required in my region"** — Beyond legal risk and liability, inaccessibility excludes a substantial user base (WHO estimates ~15% of the global population). The ethical and business case for accessibility exists independently of local statutory requirements.

9. **"Keyboard accessibility is only for power users"** — Keyboard accessibility is the primary interaction method for users with mobility impairments who cannot use a mouse. It is a core WCAG requirement under the **Operable** principle.

10. **"The `alt` attribute is optional for decorative images"** — Decorative images should use `alt=""` (empty string), *not* omit the attribute entirely. Omitting `alt` causes some screen readers to announce the image filename, which is disruptive.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the four WCAG POUR principles, and what does each require of a web implementation?

**Q2.** A developer creates a custom clickable element using a `<div>`. What ARIA attributes and event handlers are minimally required to make it keyboard and screen-reader accessible? Write the HTML.

**Q3.** What is the difference between a **transcript** and **captions** for multimedia content, and when is each required?

**Q4.** What happens when a browser processes a page — specifically, how does content reach an assistive technology like NVDA? Describe the full chain from HTML to AT output.

**Q5.** A project manager argues: "We'll handle accessibility compliance at the end before launch — it's just a checklist." Identify *two* specific reasons this approach is problematic, using evidence from the MDN article.

---

## Answer Key

---

**A1.** The four WCAG principles (POUR) are:
- **Perceivable** — All information and UI components must be presentable to users in ways they can perceive. This means providing text alternatives for non-text content (images, video), captions for audio, and ensuring content can be presented in different ways without losing meaning.
- **Operable** — UI components and navigation must be operable. This includes making all functionality available from a keyboard, giving users enough time to read content, and not designing content that causes seizures.
- **Understandable** — Information and the operation of the UI must be understandable. This requires readable text, predictable page behaviour, and input assistance (e.g., error identification and suggestions).
- **Robust** — Content must be robust enough to be reliably interpreted by a wide variety of user agents, including current and future ATs. This is primarily achieved via valid, semantic HTML and correct ARIA usage.

---

**A2.** Minimum requirements for a keyboard- and AT-accessible custom clickable `<div>`:

```html
<div
  role="button"
  tabindex="0"
  onclick="handleAction()"
  onkeydown="if(event.key==='Enter'||event.key===' ') handleAction()"
>
  Click Me
</div>
```

- `role="button"` — declares the element's semantic role to the accessibility tree so screen readers announce it as a button.
- `tabindex="0"` — inserts the element into the natural keyboard tab order (without this, it cannot receive focus).
- `onkeydown` handler — replicates the native button's activation via `Enter` and `Space` keys; a native `<button>` handles this automatically.
- Note: native `<button>` is always preferred since it provides all of this behaviour for free without custom scripting.

---

**A3.**
- **Captions** are text equivalents of spoken audio (and sometimes sound effects/speaker identification) that are **time-synchronised** with video playback. They are displayed on-screen during video and are the primary accommodation for DHH users consuming video content.
- **Transcripts** are full-text documents of the audio content, delivered separately from the media file. They are appropriate for audio-only content (e.g., podcasts) and can also supplement video.
- **When each is required:** Captions are required for video-based content; transcripts are required for audio-only content. For video, providing both captions *and* a searchable transcript is best practice. The MDN article states both should be provided for hearing-impaired access.

---

**A4.** The complete chain from HTML to AT output:

1. **Browser parses HTML** and builds the **DOM tree**.
2. **Browser derives semantics** from native HTML elements (`<button>`, `<img alt="...">`, `<label for="...">`) and any WAI-ARIA attributes.
3. **Browser constructs the accessibility tree** — a parallel semantic structure containing each node's **role**, **accessible name**, **state**, and **value**.
4. **Browser exposes the accessibility tree** to the operating system's **accessibility API** (e.g., IAccessible2/UIAExpress on Windows, NSAccessibility on macOS).
5. The **AT (e.g., NVDA)** queries the OS accessibility API to retrieve information about the focused/changed element.
6. The AT converts the semantic information into **speech output** (e.g., "Place Order, button") or Braille.
7. If the HTML semantics are insufficient (e.g., a `<div>` used as a button), **WAI-ARIA attributes** (`role`, `aria-label`, `aria-expanded`, etc.) supplement the accessibility tree so the AT receives correct information.

---

**A5.** Two reasons the "bolt-on at the end" approach is problematic:

1. **Cost escalation:** The MDN article states directly: "an accessibility problem becomes more expensive to fix the later it is discovered" — mirroring the general engineering principle that bugs are cheaper to fix earlier. Retrofitting accessibility onto a site with "significant accessibility issues" is explicitly identified as the scenario where accessibility costs are genuinely high.

2. **Architectural incompatibility:** Many accessibility requirements are structural — they require semantic HTML at the skeleton level (e.g., correct heading hierarchy, form label associations, landmark regions). If non-semantic `<div>`-based markup is used throughout, retrofitting requires rewriting large portions of the HTML and potentially the component architecture. This cannot be addressed by a final pre-launch checklist pass — it requires revisiting fundamental design decisions.
