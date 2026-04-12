# 📚 Sending Form Data — Exam Study Guide
**Source:** [MDN Web Docs — Sending and retrieving form data](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data)

---

## Executive Summary

This article explains what happens after a user submits a form: how an HTML `<form>` element maps directly onto an HTTP request, how the client-side attributes `action`, `method`, and `enctype` control where and how data is sent, and how a server-side language receives and processes that data. The central mechanism is the **client/server architecture** — the browser packages form field values into a structured HTTP request (GET or POST) and dispatches it to the URL specified in `action`. The most critical exam takeaway is that **GET appends data visibly in the URL query string while POST hides it in the request body**, making method choice a foundational security and usability decision.

---

## Core Pillars

### 1. The Client/Server Architecture

- The web runs on a **client/server model**: the browser (client) sends HTTP requests; a web server (Apache, Nginx, IIS, Tomcat, etc.) receives and processes them via the **HTTP protocol**.
- An HTML form is nothing more than **a user-friendly way to configure and send an HTTP request**. Every field value the user enters becomes part of that request.
- A form submission always results in an HTTP request being sent to a server, which then responds — usually by loading a new page or refreshing the current one.

---

### 2. The `action` Attribute — Where Data Goes

```html
<!-- Absolute URL -->
<form action="https://www.example.com">…</form>

<!-- Relative URL (same origin, different path) -->
<form action="/somewhere_else">…</form>

<!-- No action — data sent to the current page's URL -->
<form>…</form>
```

- **`action`** defines the URL that receives the submitted data.
- Its value must be a valid **relative or absolute URL**.
- **Default (no `action`):** Data is sent to the URL of the page containing the form — the current page.
- If the `action` URL uses **HTTPS** but the page itself is HTTP, data is still encrypted in transit. The reverse — HTTPS page, HTTP `action` — causes all browsers to display a **security warning**.
- The server at the `action` URL must contain logic to read and process the incoming `name=value` pairs.

---

### 3. The `method` Attribute — How Data Is Sent

The `method` attribute determines which **HTTP method** is used for the request. The two used by forms are `GET` and `POST`.

#### The GET Method

```html
<form action="https://www.example.com/greet" method="GET">
  <input name="say" value="Hi" />
  <input name="to" value="Mom" />
  <button>Send</button>
</form>
```

**Result URL after submit:**
```
https://www.example.com/greet?say=Hi&to=Mom
```

**HTTP request structure:**
```
GET /?say=Hi&to=Mom HTTP/2.0
Host: example.com
```

- Data is **appended to the URL** as a **query string**.
- Format: `?key=value&key2=value2` — pairs separated by `&`, prefixed by `?`.
- The HTTP request body is **empty**.
- The submitted data is **visible in the browser's address bar**, in server logs, and in browser history.

**Use GET when:**
- Fetching/retrieving data (search queries, filters).
- Idempotence is expected — same request can safely be repeated.
- The data is not sensitive.

#### The POST Method

```html
<form action="https://www.example.com/greet" method="POST">
  <input name="say" value="Hi" />
  <input name="to" value="Mom" />
  <button>Send</button>
</form>
```

**HTTP request structure:**
```
POST / HTTP/2.0
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```

- Data is placed in the **request body**, not the URL.
- The URL bar does **not** show the submitted data.
- `Content-Type` tells the server what format the body is in (`application/x-www-form-urlencoded` by default).
- `Content-Length` tells the server how many bytes the body contains.

**Use POST when:**
- Modifying data on the server (creating, updating, deleting).
- Sending sensitive data (passwords, payment info).
- Sending large amounts of data (URL length is browser/server limited).

---

### 4. GET vs. POST — Side-by-Side Comparison

| Feature | GET | POST |
|---|---|---|
| Data location | URL query string | HTTP request body |
| Visible to user | Yes (address bar, history, logs) | No |
| Body | Empty | Contains form data |
| Sensitive data | ❌ Never | ✅ Appropriate (with HTTPS) |
| Large payloads | ❌ URL length limits apply | ✅ No practical limit |
| Idempotent | Yes (safe to repeat) | No (may cause side-effects) |
| Cacheable | Yes | No |
| Browser "Back" button | Safe to revisit | Shows "resubmit?" dialog |

---

### 5. Viewing HTTP Requests in DevTools

HTTP requests are not shown to the user by default. To inspect them:
1. Open **Developer Tools** (F12).
2. Go to the **Network** tab.
3. Select **All**.
4. Submit the form.
5. Click the request for the current domain in the Name panel.
6. View the **Request** tab (Firefox) or **Payload** tab (Chrome/Edge).

- With **GET**: Form data is visible in the URL bar and the request headers.
- With **POST**: Form data is in the Payload/Body section only — not the URL bar.

---

### 6. On the Server Side — Retrieving the Data

Regardless of method used, the server receives the data as a **string of `name=value` pairs** which it parses into key/value pairs. How you access them depends on the server-side language or framework.

#### PHP Example

```php
<?php
// $_POST to access POST data; $_GET to access GET data
$say = htmlspecialchars($_POST["say"]);
$to  = htmlspecialchars($_POST["to"]);
echo $say, " ", $to;  // outputs: Hi Mom
?>
```

- `$_POST` / `$_GET` are **superglobal arrays** — PHP automatically populates them from the request.
- `htmlspecialchars()` escapes dangerous HTML characters — a basic XSS defence.

#### Python (Flask) Example

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('greeting.html',
                           say=request.form['say'],
                           to=request.form['to'])
```

- `request.form` is a dict-like object Flask populates from the POST body.
- Flask routes define which URL paths trigger which functions.

#### Key Point: Framework Usage

Writing raw server-side code to handle forms is possible but uncommon. Most production applications use frameworks that abstract HTTP parsing:

| Language | Common Frameworks |
|---|---|
| Python | Django, Flask, web2py, py4web |
| Node.js | Express, Next.js, Nuxt, Remix |
| PHP | Laravel, Symfony, Laminas |
| Ruby | Ruby on Rails |
| Java | Spring Boot |

---

### 7. A Special Case: Sending Files

Files are **binary data**; standard form encoding treats all data as text. Three specific requirements apply:

```html
<form method="post" action="https://example.com/upload" enctype="multipart/form-data">
  <label for="file">Choose a file</label>
  <input type="file" id="file" name="myFile" />
  <button>Send the file</button>
</form>
```

**The three mandatory requirements for file upload:**

1. **`method="post"`** — Files cannot be embedded in a URL query string.
2. **`enctype="multipart/form-data"`** — Tells the browser to split the request body into multiple parts: one per file, one for each text field.
3. **`<input type="file">`** — Provides the file picker UI.

Without all three, file content is **not actually uploaded** — only the filename may be sent.

---

### 8. The `enctype` Attribute

`enctype` sets the value of the `Content-Type` HTTP header sent with the request body.

| `enctype` Value | When to Use | Effect |
|---|---|---|
| `application/x-www-form-urlencoded` | **Default** — all non-file forms | Values URL-encoded as `key=value&key2=value2` |
| `multipart/form-data` | **Required for file uploads** | Body split into sections; binary data preserved |
| `text/plain` | Debugging only; not for production | Data sent as plain text; no encoding |

---

### 9. Security Issues — "Be Paranoid: Never Trust Your Users"

The article's golden rule: **all data reaching your server must be checked and sanitised. Always. No exceptions.**

HTML forms are by far the most common **server attack vector**. The vulnerability is never in the HTML itself — it's in how the server handles the incoming data.

**Three core defensive rules:**

1. **Escape potentially dangerous characters** — Convert characters that could be interpreted as executable code (JavaScript, SQL commands, HTML tags). Every server-side language provides functions for this (PHP: `htmlspecialchars()`, `mysqli_real_escape_string()`; Python: template auto-escaping).

2. **Limit incoming data** — Constrain lengths and types. Only accept what you actually need; reject the rest.

3. **Sandbox uploaded files** — Store uploaded files on a separate server or subdomain. Never serve them from the same origin. Grant access only through a distinct domain, preventing execution in your app's context.

**Common attack types (referenced):**
- **XSS (Cross-Site Scripting):** Injecting malicious JavaScript into displayed form data.
- **SQL Injection:** Inserting SQL commands into form fields to manipulate the database.
- **File upload abuse:** Uploading executable files disguised as images.

> A front-end developer is **not** responsible for the security model — but understanding it is essential for building correct forms.

---

## Technical Deep-Dive

### Logic Walkthrough: GET Form Submission

**Setup:**
```html
<form action="https://www.example.com/greet" method="GET">
  <input name="say" value="Hi" />
  <input name="to" value="Mom" />
  <button>Send my greetings</button>
</form>
```

**Step-by-step:**

1. User clicks "Send my greetings".
2. Browser reads all named form controls with values.
3. Encodes them as URL parameters: `say=Hi` and `to=Mom`.
4. Appends the query string to the `action` URL: `https://www.example.com/greet?say=Hi&to=Mom`.
5. Sends an HTTP GET request with an **empty body** to that URL.
6. URL becomes visible in the browser address bar.
7. Server parses the query string, extracts `say` = `Hi` and `to` = `Mom`.
8. Server returns a response; browser loads the new page.

**Raw HTTP request:**
```
GET /greet?say=Hi&to=Mom HTTP/2.0
Host: www.example.com
```

---

### Logic Walkthrough: POST Form Submission

**Same form, `method="POST"`:**

**Step-by-step:**

1. User clicks submit.
2. Browser encodes form data identically: `say=Hi&to=Mom`.
3. Places the encoded data in the **body** of the HTTP request.
4. Sets `Content-Type: application/x-www-form-urlencoded`.
5. Sets `Content-Length: 13` (byte length of the body).
6. **URL does not change** — address bar shows the original page or `action` path only.
7. Server reads the body, parses the key/value pairs.
8. Returns a response.

**Raw HTTP request:**
```
POST /greet HTTP/2.0
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```

---

### Logic Walkthrough: File Upload Request

```html
<form method="post" action="/upload" enctype="multipart/form-data">
  <input type="file" name="myFile" />
  <input type="text" name="description" value="My photo" />
  <button>Upload</button>
</form>
```

**Raw HTTP request structure:**
```
POST /upload HTTP/2.0
Host: example.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="description"

My photo
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="myFile"; filename="photo.jpg"
Content-Type: image/jpeg

[binary file data here]
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

- Each form field becomes a **separate "part"** in the multipart body.
- A `boundary` string separates parts — the browser generates this randomly.
- File content is transmitted raw (binary), preserving all bytes exactly.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`action`** | `<form>` attribute that specifies the URL to which form data is submitted; defaults to the current page's URL if omitted. |
| **`method`** | `<form>` attribute specifying the HTTP method (`GET` or `POST`) used to transmit form data to the server. |
| **`enctype`** | `<form>` attribute setting the `Content-Type` header of the request body; required to be `multipart/form-data` for file uploads. |
| **GET method** | HTTP method that appends form data as a query string to the URL; body is empty; data is visible in the address bar and logs. |
| **POST method** | HTTP method that places form data in the HTTP request body; URL remains unchanged; data is not visible in the address bar. |
| **Query string** | The `?key=value&key2=value2` portion appended to a URL when data is submitted via GET. |
| **`application/x-www-form-urlencoded`** | The default `enctype`; encodes form data as URL-encoded key/value pairs separated by `&`. |
| **`multipart/form-data`** | `enctype` value required for file uploads; splits the request body into separately encoded parts for each field and file. |
| **`Content-Type` header** | HTTP header that tells the server the format of the request body (set by `enctype` on forms). |
| **`Content-Length` header** | HTTP header indicating the byte size of the request body; set by the browser automatically on POST requests. |
| **Client/server architecture** | The web model where a client (browser) sends HTTP requests and a server (Apache, Nginx, etc.) responds using the same protocol. |
| **`$_POST` (PHP)** | PHP superglobal array automatically populated with key/value pairs from a POST request body. |
| **`$_GET` (PHP)** | PHP superglobal array automatically populated with key/value pairs from the URL query string. |
| **`request.form` (Flask)** | Flask's dict-like object containing POST body data, accessed by field name. |
| **`htmlspecialchars()` (PHP)** | PHP function that converts special HTML characters to their entity equivalents, preventing XSS injection. |
| **XSS (Cross-Site Scripting)** | A security attack where malicious JavaScript is injected into displayed content via unsanitised form inputs. |
| **SQL Injection** | A security attack where SQL commands are embedded in form field values to manipulate a database. |
| **Sanitisation** | The server-side process of cleaning and validating all incoming data before processing or storing it. |
| **Boundary string** | A randomly generated delimiter separating parts of a `multipart/form-data` request body. |
| **Idempotent** | A property of HTTP methods (like GET) where repeating the same request produces the same result without side-effects. |

---

## Watch Out For...

1. **Omitting `action` does not prevent submission.** A `<form>` with no `action` attribute submits data to the **current page's URL**. This is valid behaviour but is often unintentional.

2. **GET is NOT safe for sensitive data.** Passwords, tokens, and payment info submitted via `method="GET"` appear in the address bar, browser history, server logs, referrer headers, and proxy logs. Always use POST for sensitive data.

3. **URL length limits kill large GET submissions.** Browsers and servers have URL length limits (often 2,000–8,000 characters). Sending large datasets via GET either fails silently or is truncated. Use POST for large payloads.

4. **File uploads silently fail without all three requirements.** Omitting `method="post"`, `enctype="multipart/form-data"`, or `<input type="file">` will result in either no file being sent, only the filename being sent, or a browser error. All three are mandatory.

5. **`enctype` only applies to POST.** Setting `enctype` on a GET form has no effect — GET data goes into the URL regardless.

6. **Client-side validation is not security.** HTML5 validation, JavaScript validation, and even `type="email"` constraints can be bypassed by editing the DOM in DevTools. Server-side validation and sanitisation are mandatory for every submitted value.

7. **`action` URL using HTTP on an HTTPS page = security warning.** The browser will warn users that their data will be sent insecurely if the form's `action` points to an HTTP URL while the page itself is HTTPS. The reverse (HTTP page, HTTPS `action`) works correctly and encrypts data in transit.

8. **`$_POST` doesn't work for GET-submitted data (and vice versa in PHP).** If the form uses `method="GET"`, the server must read `$_GET`, not `$_POST`. Getting this backwards causes the server to see an empty array and silently produce wrong output.

9. **Uploaded files must be sandboxed.** Storing uploaded files in the same directory as your web application, or serving them from the same origin, risks allowing an attacker to upload a PHP/Python file and execute it on your server. Always store uploads separately and serve them via a distinct domain.

10. **A valid `action` URL doesn't mean the server is ready.** The browser sends to whatever URL `action` points to. If that URL doesn't have server-side code to parse the incoming data, the form data is simply ignored or causes a 404/500 error.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What are the two most important `<form>` attributes, and what exactly does each one control at the HTTP level?

**Q2.** Write the complete HTML for a form that collects a user's `username` and `password` and submits them securely to `/login`. Explain why each attribute choice is critical.

**Q3.** What is the difference between a GET and POST request at the HTTP level? Show the raw HTTP request structure for both, using the same form fields `say=Hi` and `to=Mom` being sent to `example.com/greet`.

**Q4.** What three specific things must be changed on a standard form to make file uploads work? What happens if you forget even one?

**Q5.** A developer builds a contact form. They sanitise data on the client side using HTML5 `required` and `type` attributes, then skip server-side sanitisation to "save time." Describe three specific attacks this application is now vulnerable to.

---

## Answer Key

---

**A1.**

- **`action`**: Specifies the **URL** (endpoint) to which the form data is sent as an HTTP request. Defaults to the current page's URL if omitted. Can be absolute (`https://example.com`) or relative (`/submit`).
- **`method`**: Specifies the **HTTP method** used to transmit the data. `GET` appends data as a URL query string (empty body); `POST` places data in the HTTP request body (URL unchanged). Determines visibility, security, data size limits, and server-side access patterns.

---

**A2.**

```html
<form action="/login" method="post">
  <label for="username">Username:</label>
  <input type="text" id="username" name="username" />

  <label for="password">Password:</label>
  <input type="password" id="password" name="password" />

  <button type="submit">Log In</button>
</form>
```

- **`method="post"`** — Critical. `method="GET"` would embed the password in the URL (`/login?username=andy&password=secret123`), making it visible in the browser address bar, browser history, server access logs, referrer headers, and any intermediate proxies. **This would be a catastrophic security vulnerability.**
- **`action="/login"`** — Points to the server endpoint that validates credentials. Without a correct action, data is sent to the wrong destination.
- **`type="password"`** — Masks the characters on screen, preventing shoulder surfing. (Note: this alone does not secure the data in transit — HTTPS is required for that.)
- The page itself must be served over **HTTPS** to actually encrypt the POST body during transmission.

---

**A3.**

**Setup:** A form with `name="say" value="Hi"` and `name="to" value="Mom"`, submitted to `https://example.com/greet`.

**GET request:**
```
GET /greet?say=Hi&to=Mom HTTP/2.0
Host: example.com
```
- Data is in the URL query string, visible in the address bar.
- Request body is empty.

**POST request:**
```
POST /greet HTTP/2.0
Host: example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```
- URL remains `/greet` — no query string.
- Data is in the request body.
- `Content-Type` declares the encoding format.
- `Content-Length` states the body's byte count.

---

**A4.**

The three mandatory requirements for a working file upload:

1. **`method="post"`** on the `<form>` — File content is binary and too large to fit in a URL. GET requests must have an empty body, so POST is mandatory.

2. **`enctype="multipart/form-data"`** on the `<form>` — The default encoding (`application/x-www-form-urlencoded`) URL-encodes all data as text. This destroys binary file content. `multipart/form-data` preserves binary data by splitting the body into separate, correctly typed parts.

3. **`<input type="file">`** inside the form — Provides the browser UI to select a file and attach it to the request.

**If any one is missing:**
- No `method="post"` → Browser uses GET; file data cannot be placed in a URL; at best, only the filename is sent.
- No `enctype="multipart/form-data"` → File content is URL-encoded and corrupted; server receives garbled binary data or just the filename.
- No `<input type="file">` → No file is attached to the request at all.

---

**A5.**

Without server-side sanitisation, the application is vulnerable to:

1. **XSS (Cross-Site Scripting):** An attacker submits a message of `<script>document.cookie</script>`. If the server stores and then displays this unsanitised, every user who views it has their session cookie stolen, allowing account takeover. Client-side `required` does not prevent this — the attacker bypasses the form entirely with a raw HTTP request.

2. **SQL Injection:** If the server stores the contact form message in a database using string concatenation (e.g., `"INSERT INTO messages VALUES ('" + message + "')"`) and an attacker submits `'; DROP TABLE messages; --` as the message, the database executes the injected SQL, potentially destroying all stored data. HTML5 attributes have zero effect on raw HTTP requests sent by an attacker.

3. **Stored malicious file content / payload injection:** Even in a text field, an attacker can bypass browser-side constraints and submit payloads of arbitrary length, encoding, or format. Without server-side length limits and character whitelisting, an attacker can submit multi-megabyte payloads causing denial-of-service, or inject template syntax (Server-Side Template Injection) if the data is processed by a templating engine.
