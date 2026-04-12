# 📚 Object Building Practice — Bouncing Balls — Exam Study Guide
**Source:** [MDN Web Docs — Object building practice](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object_building_practice)

---

## Executive Summary

This article is a **practical application** of all the OOP concepts from the prior three guides — constructors, classes, methods, and real-world object design — through a "bouncing balls" Canvas demo. The exam value here is not the specific demo, but the **patterns and techniques** it demonstrates: using a class to bundle related state and behaviour, the **animation loop** pattern with `requestAnimationFrame`, **wall-bounce physics** via velocity reversal, and **circle collision detection** using the Pythagorean theorem. These are foundational patterns that recur in games, simulations, and data visualisations.

> **APIs used:** Canvas API (drawing) and `requestAnimationFrame` (animation timing). No prior knowledge of these is required — the guide explains exactly what each call does.

---

## Core Pillars

### 1. The Project Structure

The demo uses three starter files — `index.html`, `style.css`, `main.js` — with a `<canvas>` element as the drawing surface. The JS sets up the canvas and two helper functions, then defines the `Ball` class and animation loop.

**Canvas setup:**
```js
const canvas = document.querySelector("canvas");
const ctx    = canvas.getContext("2d");                    // 2D drawing context
const width  = (canvas.width  = window.innerWidth);       // fit to viewport
const height = (canvas.height = window.innerHeight);
```

- `canvas.getContext("2d")` returns a `CanvasRenderingContext2D` object (`ctx`) — the object through which all drawing commands are issued.
- Setting `canvas.width` and `canvas.height` to `window.innerWidth`/`window.innerHeight` makes the canvas fill the entire browser viewport.
- The **chained assignment** `const width = (canvas.width = window.innerWidth)` sets both `canvas.width` and the local `width` constant in one line.

**Helper functions:**
```js
function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomRGB() {
  return `rgb(${random(0, 255)} ${random(0, 255)} ${random(0, 255)})`;
}
```

- `random(min, max)` — returns a **random integer** inclusive of both `min` and `max`.
- `randomRGB()` — returns a random CSS colour string like `"rgb(123 45 200)"`.

---

### 2. The `Ball` Class — Properties

The `Ball` class models a single bouncing ball with six properties set in the constructor:

```js
class Ball {
  constructor(x, y, velX, velY, color, size) {
    this.x     = x;      // horizontal position (centre of ball)
    this.y     = y;      // vertical position   (centre of ball)
    this.velX  = velX;   // horizontal velocity (pixels per frame)
    this.velY  = velY;   // vertical velocity   (pixels per frame)
    this.color = color;  // fill colour (CSS string)
    this.size  = size;   // radius in pixels
  }
}
```

| Property | Type | Purpose |
|---|---|---|
| `x` | Number | Horizontal position of ball centre |
| `y` | Number | Vertical position of ball centre |
| `velX` | Number | Pixels moved horizontally per frame |
| `velY` | Number | Pixels moved vertically per frame |
| `color` | String | CSS colour value (e.g. `"rgb(255 0 128)"`) |
| `size` | Number | Radius in pixels |

**Key insight:** Position (`x`, `y`) is always the **centre** of the ball, not its top-left corner. The radius (`size`) must be accounted for in all boundary and collision calculations.

---

### 3. The `draw()` Method — Rendering to Canvas

```js
draw() {
  ctx.beginPath();
  ctx.fillStyle = this.color;
  ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
  ctx.fill();
}
```

**Step-by-step Canvas drawing sequence:**

| Step | API call | What it does |
|---|---|---|
| 1 | `ctx.beginPath()` | Starts a new drawing path (resets the current shape) |
| 2 | `ctx.fillStyle = this.color` | Sets the fill colour for the next shape |
| 3 | `ctx.arc(x, y, r, start, end)` | Traces a circular arc path |
| 4 | `ctx.fill()` | Fills the enclosed path with `fillStyle` |

**`ctx.arc()` parameters:**
- `x`, `y` — centre point of the circle
- `r` — radius
- `start` — start angle in **radians** (0 = 3 o'clock position)
- `end` — end angle in **radians** (`2 * Math.PI` = full circle = 360°)

> `2 * Math.PI` radians = 360°. `Math.PI` radians = 180° (semicircle).

---

### 4. The `update()` Method — Movement and Wall Bouncing

```js
update() {
  // Right wall
  if (this.x + this.size >= width)  { this.velX = -this.velX; }
  // Left wall
  if (this.x - this.size <= 0)      { this.velX = -this.velX; }
  // Bottom wall
  if (this.y + this.size >= height) { this.velY = -this.velY; }
  // Top wall
  if (this.y - this.size <= 0)      { this.velY = -this.velY; }

  this.x += this.velX;  // move horizontally
  this.y += this.velY;  // move vertically
}
```

**Wall-bounce logic:**

The ball bounces by **reversing the sign** of the relevant velocity component when the ball's edge reaches a wall:

| Condition | Meaning | Action |
|---|---|---|
| `this.x + this.size >= width` | Right edge of ball hit right wall | `velX = -velX` (reverse horizontal) |
| `this.x - this.size <= 0` | Left edge of ball hit left wall | `velX = -velX` (reverse horizontal) |
| `this.y + this.size >= height` | Bottom edge hit bottom | `velY = -velY` (reverse vertical) |
| `this.y - this.size <= 0` | Top edge hit top | `velY = -velY` (reverse vertical) |

**Why use `this.x ± this.size`?** Because `(x, y)` is the *centre* of the ball. The ball's actual edge is `size` pixels away from the centre, so boundary checks must account for the radius.

After the boundary checks, the ball's position is updated:
```js
this.x += this.velX;
this.y += this.velY;
```
Called every frame, this moves the ball by `velX` pixels horizontally and `velY` pixels vertically per frame.

---

### 5. Creating Multiple Balls

```js
const balls = [];

while (balls.length < 25) {
  const size = random(10, 20);
  const ball = new Ball(
    random(0 + size, width - size),   // x: at least 'size' px from edges
    random(0 + size, height - size),  // y: at least 'size' px from edges
    random(-7, 7),                    // velX: -7 to +7 px/frame
    random(-7, 7),                    // velY: -7 to +7 px/frame
    randomRGB(),                      // random colour
    size,                             // radius 10–20 px
  );
  balls.push(ball);
}
```

- A `while` loop runs until `balls.length < 25` is false (i.e., 25 balls created).
- Each ball's starting position is padded inward by `size` to prevent the ball from spawning partially off-screen.
- Velocity ranges from -7 to +7 — negative values move left/up, positive right/down.
- All 25 `Ball` instances are stored in the `balls` array for later iteration.

---

### 6. The Animation Loop — `requestAnimationFrame`

```js
function loop() {
  ctx.fillStyle = "rgb(0 0 0 / 25%)";        // semi-transparent black overlay
  ctx.fillRect(0, 0, width, height);          // cover the whole canvas

  for (const ball of balls) {
    ball.draw();              // render ball at current position
    ball.update();            // update position and check walls
    ball.collisionDetect();   // check for collisions with other balls
  }

  requestAnimationFrame(loop); // schedule next frame
}

loop(); // start the animation
```

**How the animation loop works:**

1. **Ghost trail effect:** Drawing a semi-transparent black rectangle (`25%` opacity) over the entire canvas each frame covers previous drawings without completely erasing them. This leaves a fading trail behind each ball. Use `100%` opacity for clean erasure; lower percentages make longer trails.

2. **`for...of` ball iteration:** Each frame, every ball calls `draw()`, `update()`, and `collisionDetect()` — rendering it, moving it, and checking for collisions.

3. **`requestAnimationFrame(loop)`:** Schedules `loop` to be called on the next display repaint (typically 60fps). By passing `loop` to itself each time, the function becomes **recursive** — creating a continuous animation cycle.

4. **`loop()`:** The initial call that starts the cycle.

> **Recursive animation pattern:** `loop()` → calls `requestAnimationFrame(loop)` → browser calls `loop()` on next frame → repeat. This is the standard pattern for all browser animation.

---

### 7. Collision Detection — Circle-Circle

```js
collisionDetect() {
  for (const ball of balls) {
    if (this !== ball) {                              // skip self-comparison
      const dx       = this.x - ball.x;
      const dy       = this.y - ball.y;
      const distance = Math.sqrt(dx * dx + dy * dy); // Pythagorean distance

      if (distance < this.size + ball.size) {         // circles overlap?
        ball.color = this.color = randomRGB();         // change both colours
      }
    }
  }
}
```

**Algorithm breakdown:**

1. **Iterate all other balls:** The outer `for...of` loop goes through every ball in `balls`.
2. **Skip self:** `if (this !== ball)` prevents comparing a ball with itself (distance would be 0, always triggering a "collision").
3. **Calculate distance between centres:** Using the **Pythagorean theorem**:
   ```
   distance = √((x₁ - x₂)² + (y₁ - y₂)²)
   ```
   - `dx = this.x - ball.x` — horizontal separation
   - `dy = this.y - ball.y` — vertical separation
   - `distance = Math.sqrt(dx * dx + dy * dy)` — straight-line distance between centres
4. **Collision test:** Two circles overlap if the distance between their centres is **less than the sum of their radii**: `distance < this.size + ball.size`
5. **Response:** On collision, both balls get a new random colour: `ball.color = this.color = randomRGB()` (chained assignment sets both simultaneously).

**Why not realistic physics bounce?** Calculating realistic elastic collision vectors is complex. For a learning demo, a colour change is the simplest visible response. Real physics would require reversing/exchanging velocity components along the collision normal — typically handled by a physics library.

---

## Technical Deep-Dive

### Logic Walkthrough: The Complete `Ball` Class

```js
class Ball {
  constructor(x, y, velX, velY, color, size) {
    this.x     = x;
    this.y     = y;
    this.velX  = velX;
    this.velY  = velY;
    this.color = color;
    this.size  = size;
  }

  draw() {
    ctx.beginPath();
    ctx.fillStyle = this.color;
    ctx.arc(this.x, this.y, this.size, 0, 2 * Math.PI);
    ctx.fill();
  }

  update() {
    if (this.x + this.size >= width)  { this.velX = -this.velX; }
    if (this.x - this.size <= 0)      { this.velX = -this.velX; }
    if (this.y + this.size >= height) { this.velY = -this.velY; }
    if (this.y - this.size <= 0)      { this.velY = -this.velY; }
    this.x += this.velX;
    this.y += this.velY;
  }

  collisionDetect() {
    for (const ball of balls) {
      if (this !== ball) {
        const dx       = this.x - ball.x;
        const dy       = this.y - ball.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < this.size + ball.size) {
          ball.color = this.color = randomRGB();
        }
      }
    }
  }
}
```

**OOP justification for using a class here:**
- Each ball has **shared structure** (same 6 properties) — the constructor defines this once.
- Each ball has **shared behaviour** (`draw`, `update`, `collisionDetect`) — defined once on the prototype, used by all 25 instances.
- All per-ball state (position, velocity, colour) is encapsulated on the instance — no global variables needed per ball.
- Adding a new ball is simply `new Ball(...)` — the class handles everything else.

---

### Logic Walkthrough: Frame-by-Frame Animation

**What happens each frame (at ~60fps):**

```
Frame N:
  1. Draw semi-transparent black rect → fade previous frame
  2. For each ball:
     a. ball.draw()           → paint circle at (x, y) with current color
     b. ball.update()         → check walls, then x += velX, y += velY
     c. ball.collisionDetect()→ check all other balls, change colour on overlap
  3. requestAnimationFrame(loop) → queue Frame N+1
```

**Trail effect mechanics:**
- `"rgb(0 0 0 / 25%)"` means the black overlay has **25% opacity**.
- At 25% opacity, each frame slightly darkens what was drawn before rather than erasing it completely.
- After ~4 frames, older ball positions have been darkened 4 times → nearly invisible.
- Result: each ball appears to leave a short fading tail.

---

### Logic Walkthrough: Pythagorean Collision Detection

**The maths behind circle-circle collision:**

Two circles collide (overlap) when the distance between their centres is less than the sum of their radii.

```
Circle A: centre (ax, ay), radius rA
Circle B: centre (bx, by), radius rB

dx = ax - bx
dy = ay - by
distance = √(dx² + dy²)   ← straight-line distance between centres

Collision if: distance < (rA + rB)
```

**Visual intuition:**
```
     [A]           [B]
  radius=10       radius=15
  centre=(50,50)  centre=(70,50)

  dx = 50 - 70 = -20
  dy = 50 - 50 = 0
  distance = √(400 + 0) = 20

  Sum of radii = 10 + 15 = 25
  20 < 25 → COLLISION  ✓
```

If the centres were 30px apart instead:
```
  distance = 30
  30 < 25 → false → No collision  ✗
```

**Why `Math.sqrt` isn't always used in production:** Computing `Math.sqrt()` is relatively expensive. Optimised collision detection often compares `dx*dx + dy*dy < (rA + rB)*(rA + rB)` to avoid the square root. For 25 balls this makes no difference, but matters at scale.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Canvas API** | A browser API for drawing 2D (and WebGL 3D) graphics dynamically using JavaScript; accessed via a `<canvas>` element. |
| **`getContext("2d")`** | Method on a `<canvas>` element that returns a `CanvasRenderingContext2D` object (`ctx`) used to issue all drawing commands. |
| **`ctx` (drawing context)** | The `CanvasRenderingContext2D` object representing the 2D drawing surface of the canvas; all draw calls go through it. |
| **`ctx.beginPath()`** | Starts a new path (clears any previous path vertices); must be called before tracing a new shape. |
| **`ctx.arc(x, y, r, start, end)`** | Traces an arc at centre `(x, y)` with radius `r`, from angle `start` to `end` (in radians). `0` to `2*Math.PI` traces a full circle. |
| **`ctx.fill()`** | Fills the current path with the colour specified in `ctx.fillStyle`. |
| **`ctx.fillStyle`** | Property that sets the fill colour for subsequent `fill()` calls; accepts CSS colour strings. |
| **`ctx.fillRect(x, y, w, h)`** | Draws and fills a rectangle at `(x, y)` with `width` w and `height` h; used here for the per-frame background wash. |
| **`requestAnimationFrame(fn)`** | Browser API that schedules `fn` to be called before the next screen repaint (≈60fps); used to create smooth animations. |
| **Animation loop** | A function that updates program state and renders a frame repeatedly, scheduling itself via `requestAnimationFrame` to run on each paint cycle. |
| **Recursive animation** | When an animation loop function calls `requestAnimationFrame` with itself as the callback, causing it to run continuously each frame. |
| **Velocity** | A number representing how many pixels an object moves in a given direction per animation frame (`velX`, `velY`). |
| **Wall bounce** | Reversing the sign of the velocity component perpendicular to a boundary wall when the ball's edge touches that wall (`velX = -velX`). |
| **`window.innerWidth` / `window.innerHeight`** | Browser properties returning the viewport width/height (the visible area of the page), used to size the canvas. |
| **Chained assignment** | Assigning a value to multiple variables in one statement, e.g. `const w = (canvas.width = window.innerWidth)`. |
| **`random(min, max)`** | Custom helper returning a random integer between `min` and `max` inclusive; wraps `Math.floor(Math.random() * ...)`. |
| **`randomRGB()`** | Custom helper returning a random CSS `rgb()` colour string. |
| **Circle collision detection** | A method for detecting overlap between two circular objects by comparing the Pythagorean distance between their centres with the sum of their radii. |
| **Pythagorean theorem (2D distance)** | `distance = √((x₁-x₂)² + (y₁-y₂)²)` — the straight-line distance between two points; foundation of circle collision detection. |
| **Trail effect** | The visual fading tail behind moving objects created by overlaying a semi-transparent background each frame instead of fully erasing it. |
| **Ghost / semi-transparent wash** | Drawing `"rgb(0 0 0 / 25%)"` black overlay each frame to slowly fade previous drawings rather than instantly clearing the canvas. |
| **`Math.sqrt(n)`** | Returns the square root of `n`; used to compute Euclidean distance in collision detection. |
| **`this !== ball` guard** | A check in `collisionDetect()` that prevents a ball from comparing itself against itself (which would always register as a collision). |

---

## Watch Out For...

1. **`(x, y)` is the ball's CENTRE, not its edge.** All boundary calculations must use `this.x ± this.size` to check where the ball's *edge* is, not where its centre is. Using raw `this.x >= width` would let half the ball disappear off-screen before bouncing.

2. **Angle must be in radians for `ctx.arc()`.** A full circle is `2 * Math.PI`, not `360`. Passing degrees directly gives the wrong arc shape. Conversion: `degrees × (Math.PI / 180) = radians`.

3. **`ctx.beginPath()` must come before each shape.** Without it, `ctx.arc()` adds to the *previous* path rather than starting fresh. This causes all previously traced shapes to be redrawn/refilled with every `fill()` call — a subtle and hard-to-debug rendering bug.

4. **Not calling `loop()` means no animation starts.** `requestAnimationFrame(loop)` inside `loop` only schedules the *next* call. The very first call `loop()` at the bottom of the script is what kicks the whole cycle off.

5. **`requestAnimationFrame` is not `setInterval`.** It synchronises with the display's refresh rate (typically 60fps) and pauses when the tab is hidden, making it more efficient and smoother than `setInterval(fn, 16)`.

6. **Background opacity controls trail length.** Lower opacity (e.g. `10%`) → longer trails (old frames fade more slowly). Higher opacity (e.g. `100%`) → no trail (canvas fully cleared each frame). This is a useful creative parameter, not a bug.

7. **`this !== ball` must use strict identity (`!==`), not deep equality.** It checks if the two variables point to the *same object in memory*, not if they happen to have the same position values. Two different balls could be at the same coordinates — that's a collision, not the same ball.

8. **The `while (balls.length < 25)` loop — zero velocity is possible.** `random(-7, 7)` can return `0`. A ball with `velX = 0` and `velY = 0` would never move. The article doesn't guard against this, but in robust code you'd retry if both velocities are zero.

9. **Collision detection is O(n²) — quadratic complexity.** Every ball checks every other ball → 25 balls = 25×24 = 600 checks per frame. At 10,000 balls this becomes extremely slow. Real games use spatial partitioning (quadtrees, spatial hashing) to optimise this.

10. **Colour change is not physically accurate.** The collision response (colour change) is a simplification for teaching purposes. Real elastic circle collision requires calculating the collision normal vector and exchanging velocity components along that normal — a topic for physics/game libraries like `matter.js` or `PhysicsJS`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** List the six properties of the `Ball` class. Why is `(x, y)` described as the ball's *centre*, and why does this matter for the `update()` boundary checks?

**Q2.** Explain the four-step Canvas 2D drawing sequence used in `draw()`. What does each API call do? What error occurs if you forget `ctx.beginPath()`?

**Q3.** Walk through the `update()` method. For each of the four boundary checks, state the condition tested, what it detects, and how the ball responds. Then explain what happens after all four checks.

**Q4.** Describe the animation loop pattern. What is `requestAnimationFrame`, why is the loop recursive, and what is the visual purpose of drawing a semi-transparent black rectangle at the start of each frame?

**Q5.** Explain the `collisionDetect()` method step by step. What mathematical formula is used to find the distance between two ball centres? What is the collision condition for two circles, and why is the `this !== ball` guard necessary?

---

## Answer Key

---

**A1.**

| Property | Role |
|---|---|
| `x` | Horizontal position of the ball's centre |
| `y` | Vertical position of the ball's centre |
| `velX` | Pixels moved horizontally per frame |
| `velY` | Pixels moved vertically per frame |
| `color` | CSS colour string for the ball's fill |
| `size` | Radius in pixels |

`(x, y)` is the **centre** because `ctx.arc(x, y, r, start, end)` draws a circle centred at `(x, y)`. The ball extends `size` pixels in every direction from that centre.

This matters for boundary checks because the ball's *edge* touches a wall at `x + size` (right), `x - size` (left), `y + size` (bottom), `y - size` (top). Checking raw `x >= width` would only trigger when the *centre* reaches the wall — the ball would be halfway through the wall before bouncing.

---

**A2.**

```js
draw() {
  ctx.beginPath();                                  // Step 1
  ctx.fillStyle = this.color;                       // Step 2
  ctx.arc(this.x, this.y, this.size, 0, 2*Math.PI);// Step 3
  ctx.fill();                                       // Step 4
}
```

1. **`ctx.beginPath()`** — Resets the current path. Tells the canvas "start a brand new shape."
2. **`ctx.fillStyle = this.color`** — Sets the fill colour that will be applied when `fill()` is called.
3. **`ctx.arc(x, y, r, 0, 2*Math.PI)`** — Traces a full circle (arc from `0` to `2π` radians = 360°) at `(x, y)` with radius `r`.
4. **`ctx.fill()`** — Fills the traced path with the colour set in `fillStyle`.

**If you forget `beginPath()`:** The new arc is appended to whatever path was already being traced. On `fill()`, the canvas fills the combined path of all shapes since the last `beginPath()`. Every frame all previously drawn circle paths get re-filled — producing visual artefacts and performance problems.

---

**A3.**

```js
update() {
  if (this.x + this.size >= width)  { this.velX = -this.velX; } // right wall
  if (this.x - this.size <= 0)      { this.velX = -this.velX; } // left wall
  if (this.y + this.size >= height) { this.velY = -this.velY; } // bottom
  if (this.y - this.size <= 0)      { this.velY = -this.velY; } // top

  this.x += this.velX;
  this.y += this.velY;
}
```

| Check | Condition | Detected situation | Response |
|---|---|---|---|
| Right wall | `x + size >= width` | Ball's right edge at/beyond canvas right | Reverse `velX` |
| Left wall | `x - size <= 0` | Ball's left edge at/beyond canvas left | Reverse `velX` |
| Bottom | `y + size >= height` | Ball's bottom edge at/beyond canvas bottom | Reverse `velY` |
| Top | `y - size <= 0` | Ball's top edge at/beyond canvas top | Reverse `velY` |

**After the four checks:** `this.x += this.velX` and `this.y += this.velY` move the ball by its velocity. If a velocity was reversed by a boundary check in this same call, the ball moves away from the wall starting on this very frame.

---

**A4.**

**`requestAnimationFrame(fn)`** is a browser API that schedules `fn` to be called just before the browser's next screen repaint — at the display's native refresh rate (typically 60fps). It is more efficient than `setInterval` because it pauses when the tab is not active.

**Why recursive:** Inside `loop()`, the last line is `requestAnimationFrame(loop)`. This tells the browser: "after you render this frame, call `loop` again." This creates an infinite cycle: `loop` → renders frame → schedules `loop` → browser paints → `loop` → etc. A single external call `loop()` kicks it off.

**Semi-transparent black rectangle:** `ctx.fillStyle = "rgb(0 0 0 / 25%)"` followed by `ctx.fillRect(0, 0, width, height)` paints a 25%-opaque black layer over the entire canvas each frame. Rather than erasing the previous frame's balls completely, it *slightly darkens* them. After 3–4 frames they have been overlaid multiple times and become nearly invisible. This gives each ball a **fading trail effect** that makes the motion feel fluid and dynamic.

---

**A5.**

```js
collisionDetect() {
  for (const ball of balls) {
    if (this !== ball) {
      const dx       = this.x - ball.x;
      const dy       = this.y - ball.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      if (distance < this.size + ball.size) {
        ball.color = this.color = randomRGB();
      }
    }
  }
}
```

**Steps:**
1. **Iterate all balls** — Loop through the global `balls` array to check every other ball.
2. **Skip self** — `if (this !== ball)` compares object references: if the loop is currently on the same ball that called `collisionDetect`, skip it. Without this, a ball always "collides" with itself (distance = 0).
3. **Compute centre-to-centre distance:**
   - `dx = this.x - ball.x` — horizontal separation between centres
   - `dy = this.y - ball.y` — vertical separation between centres
   - `distance = √(dx² + dy²)` — Pythagorean distance formula
4. **Collision condition:** `distance < this.size + ball.size` — two circles overlap when the distance between their centres is less than the **sum of their radii**. If centre-to-centre distance equals sum of radii, the circles are tangent (touching edges only); less than that means they overlap.
5. **Response:** `ball.color = this.color = randomRGB()` — chained assignment sets both balls to the same new random colour simultaneously.

**Why `this !== ball` must use strict identity:** It checks whether two variables point to the *exact same object* in memory — not whether they have equal properties. Two different balls might coincidentally have the same `x`, `y` and `size`, but they are not the same ball. Using `!==` correctly identifies the one instance to skip.
