# 📚 Accessible Multimedia — Exam Study Guide

**Source:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/Multimedia

---

## Executive Summary

Multimedia content — images, audio, video, and `<canvas>` — presents accessibility challenges that go beyond simple text: screen readers cannot interpret visual or audio content without explicit text alternatives, and native browser media controls are not reliably keyboard-accessible across browsers. The exam-critical pattern is **three-layer coverage**: (1) descriptive `alt` text for images, (2) **custom keyboard-accessible controls** with a JavaScript fallback strategy for native controls, and (3) **text tracks (WebVTT + `<track>`)** and **transcripts** to make time-based media accessible to deaf, hard of hearing, visually impaired, and situationally limited users. The guiding principle from the article's closing is: *"Accessibility is about doing as much as you can, rather than striving for 100% all of the time."*

---

## Core Pillars

### 1. Simple Images

Text alternatives for images are covered fully in the HTML accessibility guide. The core rule applied here:

```html
<img
  src="dinosaur.png"
  alt="A red Tyrannosaurus Rex: A two legged dinosaur standing upright
       like a human, with small arms, and a large head with lots of
       sharp teeth."
/>
```

**Requirements:**
- Every meaningful image must have a descriptive `alt` attribute.
- Decorative images should use `alt=""` (empty) so screen readers skip them.
- Complex images (charts, diagrams) should have a longer description either in adjacent text or via `aria-describedby`.

---

### 2. The Problem With Native HTML Media Controls

HTML `<audio controls>` and `<video controls>` provide a built-in control bar (play/pause, seek bar, volume, etc.) out of the box. However, these have two critical accessibility problems:

| Problem | Detail |
|---|---|
| **Not keyboard-accessible** | In most browsers, you cannot `Tab` between individual controls inside the native player. Opera and Chrome partially support it, but it's inconsistent and unreliable. |
| **Not stylable** | Native controls differ in styling and functionality between browsers; they cannot be made to match a site's design system. |

**The solution:** Remove the native controls via JavaScript and replace them with **custom controls built from semantic `<button>` elements** — which are natively keyboard-accessible, focusable, and fully stylable.

**Critical resilience pattern — remove controls via JavaScript, not HTML:**

```js
// Remove controls in JS, not by omitting the controls attribute in HTML
player.removeAttribute("controls");
```

Why: If JavaScript fails to load (network error, parse error, JS disabled), the user still has the native controls available as a fallback. Removing them via JS means the fallback always exists. Omitting `controls` from the HTML entirely leaves users with zero controls if JS fails.

---

### 3. Building Custom Accessible Media Controls

The custom player pattern uses the **HTMLMediaElement API** — a set of properties and methods available on any `<audio>` or `<video>` element.

#### HTML Structure

```html
<section class="player">
  <!-- Video element: starts with controls for no-JS fallback -->
  <video controls>
    <source src="rabbit320.mp4" type="video/mp4" />
    <source src="rabbit320.webm" type="video/webm" />
    <!-- Fallback link if browser doesn't support HTML video -->
    <p>Your browser doesn't support HTML video.
       Here is a <a href="rabbit320.mp4">link to the video</a> instead.
    </p>
  </video>

  <!-- Custom controls — semantic <button> elements for keyboard access -->
  <div class="controls">
    <button class="play-pause">Play</button>
    <button class="stop">Stop</button>
    <button class="rwd">Rwd</button>
    <button class="fwd">Fwd</button>
    <div class="time">00:00</div>
  </div>
</section>
```

**Why `<button>` for every control:** Native `<button>` elements are keyboard-focusable, activated by `Enter` and `Space`, announced properly by screen readers ("Play, button"), and styled via CSS. Custom `<div>` controls would require `tabindex`, `role="button"`, and extra keyboard handlers — all unnecessary overhead.

#### JavaScript — Core Player Logic

```js
// Step 1: Store references to all controls and the player
const playPauseBtn = document.querySelector(".play-pause");
const stopBtn      = document.querySelector(".stop");
const rwdBtn       = document.querySelector(".rwd");
const fwdBtn       = document.querySelector(".fwd");
const timeLabel    = document.querySelector(".time");
const player       = document.querySelector("video"); // HTMLMediaElement

// Step 2: Remove native controls (JS loaded successfully)
player.removeAttribute("controls");

// Step 3: Play/Pause toggle
playPauseBtn.onclick = () => {
  if (player.paused) {
    player.play();
    playPauseBtn.textContent = "Pause";
  } else {
    player.pause();
    playPauseBtn.textContent = "Play";
  }
};

// Step 4: Stop (no native stop() — pause + reset currentTime)
stopBtn.onclick = () => {
  player.pause();
  player.currentTime = 0;
  playPauseBtn.textContent = "Play";
};

// Step 5: Rewind and Fast Forward (adjust currentTime directly)
rwdBtn.onclick = () => {
  player.currentTime -= 3;
};

fwdBtn.onclick = () => {
  player.currentTime += 3;
  // Guard: stop if at/past end, or if video was paused
  if (player.currentTime >= player.duration || player.paused) {
    player.pause();
    player.currentTime = 0;
    playPauseBtn.textContent = "Play";
  }
};

// Step 6: Time display (fires once per second via ontimeupdate)
player.ontimeupdate = () => {
  const minutes = Math.floor(player.currentTime / 60);
  const seconds = Math.floor(player.currentTime - minutes * 60);
  // Pad single-digit numbers with a leading zero
  const minuteValue = minutes < 10 ? `0${minutes}` : minutes;
  const secondValue = seconds < 10 ? `0${seconds}` : seconds;
  timeLabel.textContent = `${minuteValue}:${secondValue}`;
};
```

#### Key HTMLMediaElement API Members Used

| API Member | Type | What it does |
|---|---|---|
| `player.paused` | Property (boolean) | `true` if the media is currently paused or hasn't started |
| `player.play()` | Method | Starts or resumes playback |
| `player.pause()` | Method | Pauses playback (playhead stays at current position) |
| `player.currentTime` | Property (number) | Gets or sets the current playback position in **seconds** |
| `player.duration` | Property (number) | Total duration of the media in **seconds** (read-only) |
| `player.ontimeupdate` | Event handler | Fires approximately once per second during playback |
| `player.removeAttribute("controls")` | Method call | Removes the native control bar |

**Why there is no `stop()` method:** `HTMLMediaElement` intentionally has no `stop()`. "Stop" is semantically equivalent to `pause()` + resetting `currentTime` to `0` — the pattern used here.

---

### 4. Audio Transcripts

A **transcript** is a full text version of the spoken content in an audio (or audio-only) recording. It provides access to users who are:
- Deaf or hard of hearing.
- In noisy environments (pub, commute) where they can't hear audio.
- On low-bandwidth connections where downloading audio is inconvenient.
- Wanting to quickly scan, search, or reference specific content.

#### Transcript Production Options

| Method | Quality | Speed | Cost |
|---|---|---|---|
| **Commercial transcription services** (e.g., Rev, Scribie, Casting Words) | High | Fast | Paid |
| **Self / community transcription** | Variable | Slow | Free |
| **AI automated services** (e.g., Trint, YouTube auto-captions) | Variable (depends on audio clarity) | Fast | Free or low cost |

**Important rule:** Do not publish audio and promise to publish the transcript "later" — such promises are frequently broken and erode user trust. The transcript must be published simultaneously with the audio.

#### Transcript Presentation Patterns

- **Same page:** Include the transcript on the same page as the audio player, ideally in a show/hide panel to avoid cluttering the page.
- **Separate page:** Link to a dedicated transcript page from the audio player area.
- **YouTube / platform UI:** YouTube generates transcripts automatically — users access them via the three-dot menu → "Show Transcript."

#### Audio Descriptions (for audio accompanying visuals)

When audio references visual content (e.g., a recording of a meeting that references a chart), you must:
1. Provide the referenced resources (charts, spreadsheets) as linked files.
2. Specifically link to them in the transcript at the exact point where they are referenced.

This helps all users, not just those with disabilities.

---

### 5. Video Text Tracks (WebVTT + `<track>`)

Text tracks are timed text files synchronized with video playback. They serve multiple user groups beyond those with disabilities:
- Deaf users (captions).
- Users who don't speak the language (subtitles).
- Visually impaired users (descriptions).
- Users in noisy or quiet environments.
- Search engines (SEO benefit — text tracks allow engines to link to specific points mid-video).

#### Text Track Types

| Track `kind` | Audience | What it contains |
|---|---|---|
| `captions` | Deaf / hard of hearing | All audio: speech, speaker IDs, sound effects, music mood |
| `subtitles` | Non-speakers of the audio language | Translation of the spoken dialogue only |
| `descriptions` | Visually impaired | Description of the visual scene for those who cannot see |
| `chapters` | All users | Chapter title markers for navigating long media |

**Captions vs. Subtitles distinction:** Captions include non-speech audio context (e.g., `[dramatic music]`, `[door slams]`) — subtitles only translate speech. This distinction matters for WCAG compliance.

#### WebVTT File Format

Text tracks must be written in **WebVTT** (Web Video Text Tracks) format — a plain text file with the `.vtt` extension.

```
WEBVTT

1
00:00:22.230 --> 00:00:24.606
This is the first subtitle.

2
00:00:30.739 --> 00:00:34.074
This is the second.
```

**Structure of a WebVTT cue:**
- Cue number (optional, for reference)
- Timestamp range: `HH:MM:SS.mmm --> HH:MM:SS.mmm`
- Text content (the caption/subtitle text)

WebVTT also supports limited styling and positioning — cues can be positioned anywhere on screen and styled with pseudo-elements in CSS.

#### Linking a `.vtt` File with `<track>`

```html
<video controls>
  <source src="example.mp4" type="video/mp4" />
  <source src="example.webm" type="video/webm" />
  <!-- Track element: must come after all <source> elements -->
  <track kind="subtitles"
         src="subtitles_en.vtt"
         srclang="en"
         label="English" />
  <track kind="subtitles"
         src="subtitles_de.vtt"
         srclang="de"
         label="Deutsch" />
</video>
```

**`<track>` attribute reference:**

| Attribute | Required? | Purpose |
|---|---|---|
| `kind` | ✅ Required | Type of text track: `subtitles`, `captions`, `descriptions`, `chapters`, `metadata` |
| `src` | ✅ Required | URL to the `.vtt` file |
| `srclang` | ✅ (for subtitles/captions) | BCP 47 language tag (e.g., `en`, `de`, `fr`, `es`) |
| `label` | Recommended | Human-readable label displayed in the player's text track menu (e.g., "English", "Deutsch") |
| `default` | Optional | If present, this track is enabled by default |

**Placement rules:** `<track>` elements must appear *inside* `<audio>` or `<video>`, and *after* all `<source>` elements.

---

## Technical Deep-Dive

### Logic Walkthrough: Custom Player Stop Function

**Why there's no `stop()` on `HTMLMediaElement`:**

The HTML spec defines only `play()` and `pause()`. "Stop" is a compositional operation:

```js
stopBtn.onclick = () => {
  player.pause();        // 1. Halt playback at current position
  player.currentTime = 0; // 2. Move playhead to beginning
  playPauseBtn.textContent = "Play"; // 3. Update button label state
};
```

Setting `currentTime = 0` is synchronous — it immediately repositions the media's internal playback pointer to the start. The next `play()` call will begin from frame zero.

---

### Logic Walkthrough: Fast Forward Guard Condition

```js
fwdBtn.onclick = () => {
  player.currentTime += 3;
  if (player.currentTime >= player.duration || player.paused) {
    player.pause();
    player.currentTime = 0;
    playPauseBtn.textContent = "Play";
  }
};
```

**Why the guard exists — two cases handled:**

1. **Past end of video (`currentTime >= duration`):** Adding 3s to a time near the end would push `currentTime` beyond `duration`. Without the guard, the player would sit in a broken state showing the final frame with no UI feedback.

2. **Forward while paused (`player.paused`):** If the user repeatedly taps Fwd while the video is paused, the playhead jumps but the video never starts. The guard resets everything to a clean stopped state, preventing UI confusion.

---

### Logic Walkthrough: Time Display Formatting

```js
player.ontimeupdate = () => {
  // currentTime is in fractional seconds — floor to whole seconds
  const minutes = Math.floor(player.currentTime / 60);
  const seconds = Math.floor(player.currentTime - minutes * 60);

  // Pad single-digit values with a leading zero for "MM:SS" format
  const minuteValue = minutes < 10 ? `0${minutes}` : minutes;
  const secondValue = seconds < 10 ? `0${seconds}` : seconds;

  timeLabel.textContent = `${minuteValue}:${secondValue}`;
};
```

**`ontimeupdate` frequency:** Fires approximately once per second during playback (the exact rate is browser-dependent but typically 4Hz). It does not fire faster by design — frequent DOM updates would cause layout thrashing.

**Why subtract `minutes * 60` for seconds:**
`currentTime` is a flat seconds value. `Math.floor(currentTime / 60)` gives whole minutes. The remaining seconds are `currentTime - (minutes * 60)`. Without this subtraction, `seconds` would be the total elapsed seconds, not the seconds within the current minute.

---

### Logic Walkthrough: WebVTT → Browser → Video Player Pipeline

```
Developer saves: subtitles_en.vtt
         ↓
HTML: <track kind="captions" src="subtitles_en.vtt" srclang="en" />
         ↓
Browser parses the .vtt file at load time:
  - Validates WEBVTT header
  - Parses each cue: timestamp range + text
  - Stores cues in memory indexed by start/end time
         ↓
During video playback, the browser's media engine compares
currentTime against each cue's start/end timestamps
         ↓
When currentTime enters a cue's range:
  - Browser displays the cue text as a caption overlay
  - Screen readers (for descriptions tracks) may read the text aloud
  - JavaScript can access cues via the TextTrack API for custom UIs
         ↓
When currentTime exits the cue's range:
  - Caption overlay is removed or replaced with the next cue
```

**SEO bonus:** The browser also exposes cue text to search engine crawlers, allowing them to index video content and deep-link to specific timestamps within the video.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`HTMLMediaElement`** | The Web API interface shared by both `<audio>` and `<video>` elements; provides properties (`currentTime`, `duration`, `paused`) and methods (`play()`, `pause()`) for programmatic media control. |
| **`controls` attribute** | An HTML boolean attribute on `<audio>` and `<video>` that shows the browser's native media control bar; removed via JS (`removeAttribute("controls")`) when implementing custom controls. |
| **`player.paused`** | An `HTMLMediaElement` boolean property that is `true` when the media is not currently playing (paused or not yet started). |
| **`player.currentTime`** | A readable/writable `HTMLMediaElement` property representing the current playback position in seconds; setting it programmatically seeks to that position. |
| **`player.duration`** | A read-only `HTMLMediaElement` property giving the total length of the media in seconds. |
| **`player.ontimeupdate`** | An `HTMLMediaElement` event handler called approximately once per second during playback; used for updating time displays. |
| **`play()` / `pause()`** | `HTMLMediaElement` methods that start and stop playback respectively; there is no native `stop()` method. |
| **Audio transcript** | A complete text version of spoken audio content; enables access for deaf users, low-bandwidth users, and users in noisy environments. |
| **WebVTT** | Web Video Text Tracks; a plain text file format (`.vtt`) for defining timed text cues synchronized with a video or audio element. |
| **Cue** | An individual timed text entry in a WebVTT file, consisting of a timestamp range (`start --> end`) and associated text content. |
| **`<track>` element** | An HTML element placed inside `<audio>` or `<video>` (after all `<source>` elements) that links a `.vtt` file to the media element as a text track. |
| **`kind` attribute** | The `<track>` attribute specifying what type of text track it is: `subtitles`, `captions`, `descriptions`, `chapters`, or `metadata`. |
| **`srclang` attribute** | The `<track>` attribute specifying the BCP 47 language code of the text track's content (e.g., `en`, `fr`, `de`). |
| **`label` attribute** | The `<track>` attribute providing a human-readable name for the track shown in the player's subtitle/caption selection menu. |
| **Captions** | A text track (`kind="captions"`) that includes all audio content: speech, speaker identification, sound effects, and music mood — for deaf or hard of hearing users. |
| **Subtitles** | A text track (`kind="subtitles"`) that provides a translation of spoken dialogue for users who don't understand the audio language. |
| **Descriptions** | A text track (`kind="descriptions"`) containing descriptions of visual scene content for visually impaired users who cannot see the video. |
| **Chapters** | A text track (`kind="chapters"`) providing named navigation markers for jumping to specific segments of long media. |
| **No-JS fallback for media** | The pattern of keeping the native `controls` attribute in HTML and removing it via JS; ensures users always have some player controls even if JavaScript fails. |
| **`ontimeupdate` event** | A media event that fires approximately once per second during playback; used to update elapsed time displays in custom player UIs. |

---

## Watch Out For…

1. **Omitting `controls` from the HTML and relying entirely on JavaScript** — If JS fails (network error, parse error, extension blocking), users are left with zero media controls. Always include `controls` in HTML and remove it via `player.removeAttribute("controls")` in JS — this way the native controls serve as a fallback.

2. **Using non-`<button>` elements for custom player controls** — A `<div class="play">Play</div>` requires `tabindex="0"`, `role="button"`, and `keydown` handlers for `Enter`/`Space` — and still may be announced inconsistently by screen readers. Use `<button>` — it is natively focusable, keyboard-activated, and correctly announced.

3. **Assuming native `<video controls>` is keyboard-accessible** — The article explicitly states controls are not keyboard-accessible in most browsers. Do not rely on the native player for keyboard users.

4. **Forgetting that `HTMLMediaElement` has no `stop()` method** — The correct stop pattern is `player.pause(); player.currentTime = 0;`. Trying to call `player.stop()` will throw a `TypeError`.

5. **Publishing audio without a simultaneous transcript** — Promising to add a transcript "later" is not an acceptable accessibility strategy. Transcripts must go live alongside the audio they describe.

6. **Using automated transcription without reviewing the output** — AI transcription quality varies significantly with audio clarity, accents, and technical vocabulary. Always review and correct automated transcripts before publishing.

7. **Confusing captions and subtitles** — Captions include all audio context (music, sound effects, speaker IDs); subtitles are language translations of speech only. WCAG requires captions for accessibility; subtitles alone are insufficient for deaf users.

8. **Placing `<track>` before `<source>` elements** — `<track>` must come *after* all `<source>` elements within the `<audio>` or `<video>` element. Incorrect placement may cause the track to be ignored.

9. **Omitting `srclang` from caption/subtitle tracks** — `srclang` is required for `kind="subtitles"` and `kind="captions"`. Without it, the browser and AT cannot identify the track's language for selection menus.

10. **Omitting the `label` attribute from `<track>` elements** — Without `label`, the player's text track selection menu may display empty or unreadable entries (e.g., just the ISO language code). Always provide a human-readable label like `"English"` or `"Español"`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Why should the native `controls` attribute be removed via JavaScript (`player.removeAttribute("controls")`) rather than simply being omitted from the HTML? What accessibility risk does omitting it from HTML create?

**Q2.** Write the complete JavaScript for a stop button that correctly stops a `<video>` element referenced as `player`, resets the time display, and updates the play/pause button label. Explain why there is no `player.stop()`.

**Q3.** A product team wants to add captions AND subtitles to a video that has English audio. Write the complete `<video>` HTML with two `<track>` elements — English captions and Spanish subtitles — explaining every attribute on each `<track>`.

**Q4.** Name the four main types of video text tracks, state their `kind` attribute value, and identify the primary user group each serves.

**Q5.** A developer creates a podcast page and publishes the audio player. They plan to publish the transcript "next week." Why is this approach unacceptable, and who benefits from transcripts beyond deaf users?

---

## Answer Key

---

**A1.** If the `controls` attribute is *included in HTML* and removed via JavaScript:
- When JS loads and executes correctly → `player.removeAttribute("controls")` removes the native controls and the custom JS controls take over. ✅
- When JS fails → the `controls` attribute is still present in the HTML; the browser renders the native control bar. Users can still play/pause/seek the video. ✅ **Fallback preserved.**

If the `controls` attribute is *omitted from the HTML entirely* and custom controls are added only by JS:
- When JS loads → custom controls appear. ✅
- When JS fails → no `controls` attribute exists → **no controls of any kind are available**. The user cannot interact with the media at all. ❌ **Catastrophic failure.**

The accessibility risk of omitting `controls` from HTML is that any JavaScript failure (network timeout, parse error, ad blocker, Content Security Policy violation) leaves the user with a media element they cannot control — no play, no pause, no seek.

---

**A2.**

```js
const stopBtn       = document.querySelector(".stop");
const playPauseBtn  = document.querySelector(".play-pause");
const player        = document.querySelector("video");

stopBtn.onclick = () => {
  player.pause();          // 1. Halt playback
  player.currentTime = 0;  // 2. Reset playhead to beginning
  playPauseBtn.textContent = "Play"; // 3. Update button label
};
```

**Why there is no `player.stop()`:** The `HTMLMediaElement` API was designed without a `stop()` method because "stop" is a composite action — pause + seek to zero. The spec authors chose not to add a redundant named method for an operation that is trivially composable from two existing primitives (`pause()` and `currentTime = 0`). This keeps the API minimal and avoids ambiguity about what "stop" means for streams (where rewinding to zero may not be meaningful).

---

**A3.**

```html
<video controls>
  <!-- Primary video source — MP4 for broad browser support -->
  <source src="product-demo.mp4" type="video/mp4" />
  <!-- WebM as a fallback for browsers that prefer open formats -->
  <source src="product-demo.webm" type="video/webm" />

  <!-- Track 1: English captions — for deaf/hard of hearing users -->
  <!-- Captions include speech + sound effects + music mood -->
  <track kind="captions"
         src="captions_en.vtt"
         srclang="en"
         label="English"
         default />

  <!-- Track 2: Spanish subtitles — for Spanish-speaking users -->
  <!-- Subtitles contain only translated speech, no sound effect descriptions -->
  <track kind="subtitles"
         src="subtitles_es.vtt"
         srclang="es"
         label="Español" />
</video>
```

**Attribute explanations:**

| Attribute | Value | Meaning |
|---|---|---|
| `kind="captions"` | `captions` | Full audio description including non-speech sounds — for deaf users |
| `kind="subtitles"` | `subtitles` | Speech translation only — for language accessibility |
| `src` | `.vtt` file path | URL to the WebVTT file containing the cues |
| `srclang="en"` | `en` | BCP 47 language code identifying the track's language — required for subtitles/captions |
| `srclang="es"` | `es` | Spanish language code |
| `label="English"` / `label="Español"` | Human-readable | Shown in the player's subtitle selection menu |
| `default` | Boolean | Activates the English captions track by default without user action |

---

**A4.**

| Track type | `kind` value | Primary user group |
|---|---|---|
| **Captions** | `captions` | Deaf or hard of hearing users — includes all audio context (speech, sound effects, music mood) |
| **Subtitles** | `subtitles` | Users who don't understand the spoken language — translated speech only |
| **Descriptions** | `descriptions` | Visually impaired users — textual description of visual scene content |
| **Chapters** | `chapters` | All users — named navigation markers for long media |

---

**A5.** Publishing a "transcript later" commitment is unacceptable because:

1. **Such promises are frequently not kept** — the article explicitly states this. Once a publication deadline passes, the urgency to create a transcript diminishes and it often never appears.

2. **It creates unequal access** — deaf users have no access to the content during the gap period, while hearing users do. This is a WCAG violation.

3. **It erodes user trust** — broken promises damage the relationship between content publisher and audience, particularly users who already face barriers.

**Users who benefit from transcripts beyond deaf users:**

| User group | Why the transcript helps |
|---|---|
| **Low-bandwidth users** | Can read the transcript without downloading the audio file |
| **Users in noisy environments** | Can access the content where audio is not audible (commute, pub, open-plan office) |
| **Users in quiet environments** | Can read without disturbing others (library, sleeping partner) |
| **Non-native speakers** | Can read carefully at their own pace |
| **Users who want to scan / search** | Can `Ctrl+F` to find specific content in seconds rather than seeking through audio |
| **Search engines** | Index the transcript text, improving discoverability and enabling deep linking to specific content moments |
