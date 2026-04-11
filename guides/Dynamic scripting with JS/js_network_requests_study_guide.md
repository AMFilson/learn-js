# 🌐 JavaScript Network Requests (Fetch API) — Exam Study Guide
**Source:** [MDN Web Docs — Making network requests with JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Network_requests)

---

## Executive Summary

Modern websites avoid full page reloads by using the **Fetch API** to make **asynchronous HTTP requests** that retrieve only the data needed to update a specific section of the page — a technique historically called **AJAX**. The `fetch()` function is the modern standard: it returns a **Promise** that resolves to a `Response` object, which you then convert to usable data using methods like `response.text()` (for plain text), `response.json()` (for JSON data), or `response.blob()` (for binary files like images). Always chain a `.catch()` handler to the end of every Fetch chain to handle network errors, and always check `response.ok` before processing the response body to catch server-side HTTP errors like 404.

---

## Core Pillars

### 1. The Problem — Why We Need Network Requests

- The **traditional web model**: the browser makes a request → the server returns an **entire new HTML page** → the browser re-renders everything.
- This is **wasteful** when only one section of a page needs to update (e.g., search results, a product listing).
- **Modern approach**: JavaScript makes a targeted HTTP request and updates only the relevant part of the DOM — **no full page reload**.

**Benefits of the modern approach:**
- **Faster** — only the changed data travels the network, not a full HTML document.
- **More responsive** — no white-flash page reload; the user stays in context.
- **Less bandwidth** — critical on mobile devices and slow connections.

> **AJAX** (Asynchronous JavaScript and XML) is the historical name for this technique. Modern code requests JSON rather than XML, but the term is still widely used.

---

### 2. The Fetch API — Overview

- The entry point is the **global `fetch()` function**, available in all modern browsers.
- Takes a **URL string** as its first argument (and an optional options object for custom settings).
- Returns a **Promise** — fetch is **asynchronous**; it does not block the rest of your code while waiting for a response.
- The Promise resolves to a **`Response` object** — this holds the HTTP response metadata and methods to access the body.

```js
fetch(url)
  .then((response) => { /* handle the Response object */ })
  .catch((error)   => { /* handle network failure */ });
```

---

### 3. The Promise Chain — `.then()` and `.catch()`

Because `fetch()` returns a Promise, you handle its result with `.then()`:

```js
fetch("verse1.txt")
  .then((response) => {
    // First .then() — receives the Response object
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.text();   // returns ANOTHER Promise
  })
  .then((text) => {
    // Second .then() — receives the resolved text string
    poemDisplay.textContent = text;
  })
  .catch((error) => {
    // .catch() — handles ANY error thrown in the chain
    poemDisplay.textContent = `Could not fetch verse: ${error}`;
  });
```

**Why two `.then()` calls?**
- `fetch()` returns a Promise for the `Response` — but the response *body* is also streamed asynchronously.
- Methods like `response.text()` and `response.json()` **also return Promises**.
- You `return` the inner Promise from the first `.then()`, then chain a second `.then()` to handle the fully-resolved body data.

---

### 4. Checking `response.ok` — Handling HTTP Errors

- A `fetch()` Promise **only rejects** on a **network failure** (no connection, DNS error, CORS block).
- It does **NOT** reject on HTTP error status codes like 404 or 500 — the Promise still resolves!
- You must **manually check `response.ok`** (or `response.status`) inside the first `.then()`.
- `response.ok` is `true` for status codes 200–299, `false` for anything else.

```js
fetch("products.json")
  .then((response) => {
    if (!response.ok) {
      // Server returned 404, 500, etc. — manually throw to jump to .catch()
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();  // Only parse if the request succeeded
  })
  .then((json) => initialize(json))
  .catch((err) => console.error(`Fetch problem: ${err.message}`));
```

---

### 5. Response Body Methods — Parsing the Data

After confirming `response.ok`, call the appropriate method on the response to get the data:

| Method | Returns | Use for |
|---|---|---|
| **`response.text()`** | Promise → `string` | Plain text, HTML, CSV |
| **`response.json()`** | Promise → JS object/array | JSON data from APIs |
| **`response.blob()`** | Promise → `Blob` | Binary data: images, audio, video |

All three methods **return Promises** — always `return` them inside `.then()` and chain another `.then()` to access the result.

```js
// Fetching JSON (API data)
fetch("products.json")
  .then((r) => r.json())         // returns Promise<object>
  .then((data) => render(data)); // data is now a JS object/array

// Fetching plain text
fetch("verse1.txt")
  .then((r) => r.text())         // returns Promise<string>
  .then((text) => display(text));

// Fetching a binary image (Blob)
fetch("img/cat.jpg")
  .then((r) => r.blob())         // returns Promise<Blob>
  .then((blob) => showImage(blob));
```

---

### 6. Blobs — Displaying Fetched Images

- A **Blob** (Binary Large Object) represents raw binary data (images, audio, video files).
- To display a fetched image Blob, use **`URL.createObjectURL(blob)`** to create a temporary URL that an `<img>` `src` can point to.

```js
fetch(imageUrl)
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    return response.blob();
  })
  .then((blob) => {
    const objectURL = URL.createObjectURL(blob);
    const image = document.createElement("img");
    image.src = objectURL;
    document.body.appendChild(image);
  })
  .catch((err) => console.error(`Fetch problem: ${err.message}`));
```

---

### 7. XMLHttpRequest (XHR) — The Legacy API

- **XHR** predated Fetch and was the original AJAX mechanism.
- MDN recommends **Fetch** — it is simpler, more modern, and Promise-based.
- You will encounter XHR in older codebases, so you must recognise it.

**XHR has 5 steps:** create → open → attach load listener → attach error listener → send.

```js
const request = new XMLHttpRequest();
try {
  request.open("GET", "products.json");  // method + URL
  request.responseType = "json";          // tell XHR what format to expect
  request.addEventListener("load", () => initialize(request.response));
  request.addEventListener("error", () => console.error("XHR error"));
  request.send();
} catch (error) {
  console.error(`XHR error ${request.status}`);
}
```

**XHR vs Fetch comparison:**

| Feature | `fetch()` | `XMLHttpRequest` |
|---|---|---|
| API style | Promise-based | Event/callback-based |
| Error handling | Single `.catch()` | Errors in two places |
| Readability | Cleaner chain | More boilerplate |
| **Recommendation** | Use this | Legacy — avoid in new code |

---

### 8. Security — Fetch Only Works from a Server

- Modern browsers block `fetch()` requests when running from a **local file** (`file://` protocol) due to security restrictions.
- To test Fetch locally, you must run a **local web server** (e.g., VS Code Live Server, Node.js `http-server`, Python's `http.server`).
- In production, your page and the fetched resources must comply with **CORS** (Cross-Origin Resource Sharing) rules if the data is on a different domain.

---

## Technical Deep-Dive

### Logic Walkthrough: The Full Fetch Chain — Step by Step

```js
fetch("verse1.txt")        // Step 1: Send HTTP GET to verse1.txt
                           //         Returns a Promise<Response>

  .then((response) => {   // Step 2: Promise resolves → response object arrives
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
      // Throwing here jumps directly to .catch()
    }
    return response.text();
    // Starts reading the body as text — returns Promise<string>
    // We RETURN this promise, so the next .then() waits for it
  })

  .then((text) => {        // Step 3: Body fully read → text is a string
    poemDisplay.textContent = text;
  })

  .catch((error) => {      // Step 4: Catches ANY error from steps 1, 2, or 3
    poemDisplay.textContent = `Could not fetch verse: ${error}`;
  });
```

**Key insight — every body method returns its own Promise:**
```
fetch()         → Promise<Response>      → .then((response) => ...)
response.text() → Promise<string>        → .then((text) => ...)
response.json() → Promise<object/array>  → .then((json) => ...)
response.blob() → Promise<Blob>          → .then((blob) => ...)
```
Always `return` the body-reading method call inside the first `.then()` so the chain waits for it.

---

### Logic Walkthrough: What `response.ok` Catches vs. `.catch()`

```
Network request made
       │
       ├─── Network failure (no internet, DNS, CORS block)
       │         → Promise REJECTS → .catch() ← AUTOMATIC
       │
       └─── Server responds (any status code)
                 → Promise RESOLVES → first .then()
                       │
                       ├─── response.ok = true  (200–299)
                       │         → continue safely
                       │
                       └─── response.ok = false (404, 500...)
                                 → MANUAL throw required
                                 → then .catch() handles it
```

> **The most-tested exam concept:** `fetch()` does NOT reject on 404 or 500. Those are "successful" HTTP transactions from fetch's perspective. You must check `response.ok` yourself.

---

### Logic Walkthrough: XHR vs Fetch Side-by-Side

```js
// XHR (legacy — 5 steps, event-based):
const request = new XMLHttpRequest();
try {
  request.open("GET", "products.json");
  request.responseType = "json";
  request.addEventListener("load",  () => initialize(request.response));
  request.addEventListener("error", () => console.error("XHR error"));
  request.send();
} catch (e) {
  console.error(`XHR error ${request.status}`);
}
// Error handling split across two places (try/catch + error event)

// Fetch (modern — Promise chain):
fetch("products.json")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    return response.json();
  })
  .then((json) => initialize(json))
  .catch((err) => console.error(`Fetch problem: ${err.message}`));
// All error handling in one .catch()
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **AJAX** | Asynchronous JavaScript and XML — the technique of making background HTTP requests to update page content without a full reload. Now typically uses JSON, but the term persists. |
| **Fetch API** | The modern browser API for making HTTP requests. Entry point is `fetch()`, which returns a Promise. Recommended over XHR. |
| **`fetch(url)`** | Global function that initiates an HTTP GET request to `url`. Returns `Promise<Response>`. |
| **Promise** | An object representing the eventual result of an asynchronous operation. Use `.then()` for success and `.catch()` for error. |
| **`.then(callback)`** | Chains onto a Promise. Runs when the Promise resolves, receives the resolved value, and returns a new Promise. |
| **`.catch(callback)`** | Runs if any Promise in the chain rejects or any handler throws. Used for centralised error handling. |
| **`Response` object** | Passed to the first `.then()`. Contains HTTP metadata (`ok`, `status`) and body-reading methods. |
| **`response.ok`** | `true` if status is 200–299, `false` otherwise. Must be checked manually — fetch does NOT auto-reject on 4xx/5xx. |
| **`response.status`** | Numeric HTTP status code of the response (200, 404, 500, etc.). |
| **`response.text()`** | Returns `Promise<string>` — reads the response body as plain text. |
| **`response.json()`** | Returns `Promise<object/array>` — parses the response body as JSON. |
| **`response.blob()`** | Returns `Promise<Blob>` — reads the response body as binary data, for images/audio/video. |
| **Blob** | Binary Large Object. Raw binary data. `URL.createObjectURL(blob)` converts it to a usable URL. |
| **`URL.createObjectURL(blob)`** | Creates a temporary URL from a Blob, usable as an image `src`. |
| **Asynchronous** | Does not block execution — runs in the background and notifies via callback/Promise when done. |
| **XMLHttpRequest (XHR)** | The legacy event-based API for HTTP requests, preceding Fetch. Still found in older code. |
| **CORS** | Cross-Origin Resource Sharing — browser security mechanism restricting requests to different domains. CORS violations cause the Fetch Promise to reject. |

---

## Watch Out For...

1. **`fetch()` does NOT reject on 404 or 500.** These status codes still resolve the Promise. You MUST check `response.ok` and manually `throw` to trigger `.catch()`. This is the #1 exam gotcha.

2. **Both `fetch()` AND `response.text()/.json()/.blob()` return Promises.** Always `return` the body-reading call inside the first `.then()`. Forgetting `return` means the second `.then()` gets `undefined` immediately, before the body is read.

3. **`fetch()` is blocked from local files.** Running from `file://` will fail. Always use a local web server (Live Server, `http-server`, etc.) when testing fetch code.

4. **Network failures auto-reject; HTTP errors do not.** Know exactly which errors are automatic vs. which require a manual `throw`: network failure = automatic; 404/500 = manual.

5. **`response.json()` throws if the body is not valid JSON.** If the server returns an HTML error page and you call `.json()`, it throws a parse error. That's why you check `response.ok` first.

6. **A single `.catch()` at the end covers everything** — network failures, manually thrown HTTP errors, and parse errors. You don't need separate catch blocks.

7. **XHR requires error handling in two separate places:** `try/catch` for `open()`/`send()`, plus an `error` event listener for async errors. Fetch consolidates both into one `.catch()`.

8. **"AJAX" still means this pattern, even though JSON replaced XML.** If an exam question mentions AJAX, it is asking about asynchronous HTTP requests — answered today with `fetch()`.

9. **`response.blob()` is for binary data only** — not JSON or text. Calling `blob()` on a JSON response gives you raw binary, not an object.

10. **`return` is mandatory inside `.then()`** — writing `response.text()` without `return` begins the read but gives the chain nothing to hold onto. The next `.then()` receives `undefined`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the problem with the traditional page-loading model that `fetch()` solves? Name two specific benefits of the modern approach.

**Q2.** Explain why a typical fetch chain has **two `.then()` calls**. What does each one receive?

**Q3.** Under what conditions does the `fetch()` Promise **reject automatically**? Under what conditions does it **NOT** reject even though something went wrong — and how do you handle that case?

**Q4.** Write a complete fetch chain that requests `api/products.json`, parses it as JSON, passes the result to a `render()` function, and handles errors properly.

**Q5.** What is `XMLHttpRequest`? Give two reasons why `fetch()` is preferred over it in modern code.

---

## Answer Key

---

**A1.**
**The problem:** The traditional model fetches and re-renders the **entire page** even when only a small section needs updating — slow, wasteful, and causes jarring full-page reloads.

**Two benefits of `fetch()`:**
1. **Faster and more responsive** — only changed data travels the network; no page white-flash.
2. **Less bandwidth** — critical on mobile and slow connections.

---

**A2.**
Two `.then()` calls are needed because fetch involves **two separate asynchronous steps**, each with its own Promise:

- **First `.then((response) => ...)`** — receives the `Response` object when HTTP headers arrive. The body is NOT yet read. Calling `response.json()` or `.text()` starts reading and returns *another Promise*, which you must `return`.

- **Second `.then((data) => ...)`** — receives the fully read and parsed body (string, object, Blob) once the body download is complete.

```
fetch(url)       → Promise<Response>   → .then((response) => { return response.json(); })
response.json()  → Promise<object>     → .then((json) => { render(json); })
```

---

**A3.**
- **Auto-rejects** (`.catch()` fires without any code from you): **Network-level failures** — no internet, DNS error, CORS policy block.

- **Does NOT auto-reject**: **HTTP error status codes** (404, 500, 403...). The server responded, so from `fetch()`'s perspective the transaction succeeded.

**How to handle HTTP errors manually:**
```js
.then((response) => {
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`); // forces .catch()
  }
  return response.json();
})
```

---

**A4.**
```js
fetch("api/products.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();   // returns Promise<object>
  })
  .then((data) => {
    render(data);             // data is the parsed JS object/array
  })
  .catch((err) => {
    console.error(`Fetch problem: ${err.message}`);
  });
```

---

**A5.**
**XMLHttpRequest (XHR)** is the legacy browser API for asynchronous HTTP requests, predating Fetch. It uses an event-driven model: create an `XMLHttpRequest` object, call `.open()`, attach event listeners for `load` and `error`, then call `.send()`.

**Two reasons Fetch is preferred:**
1. **Promise-based** — `.then()/.catch()` chains are cleaner and more readable than nested event callbacks.
2. **Centralised error handling** — one `.catch()` covers all error types; XHR requires handling errors in two separate places (`try/catch` + `error` event listener).
