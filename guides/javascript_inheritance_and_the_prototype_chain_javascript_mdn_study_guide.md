# 📚 Inheritance and the prototype chain - JavaScript | MDN — Exam Study Guide
Source: [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain)

## Executive Summary

This guide covers **Inheritance and the prototype chain - JavaScript | MDN** and distills the source page into exam-ready notes anchored to the page structure and wording.
It organizes the material into major themes, the mechanism behind them, and the terminology that is most likely to matter under time pressure.
Use it to review the structure first, then test yourself with the recall questions before trying to explain the topic from memory.

## Core Pillars

### 1. Inheritance and the prototype chain
- **Inheritance and the prototype chain** appears in the source and deserves deliberate review.
- **In this article** appears in the source and deserves deliberate review.
```js
const o = {
  a: 1,
  b: 2,
  // __proto__ sets the [[Prototype]]. It's specified here
  // as another object literal.
  __proto__: {
    b: 3,
    c: 4,
  },
};

// o.[[Prototype]] has properties b and c.
// o.[[Prototype]].[[Prototype]] is Object.prototype (we will explain
// what that means later).
// Finally, o.[[Prototype]].[[Prototype]].[[Prototype]] is null.
// This is the end of the prototype chain, as null,
// by definition, has no [[Prototype]].
// Thus, the full prototype chain looks like:
// { a: 1, b: 2 } ---> { b: 3, c: 4 } ---> Object.prototype ---> null

console.log(o.a); // 1
// Is there an 'a' own property on o? Yes, and its value is 1.

console.log(o.b); // 2
// Is there a 'b' own property on o? Yes, and its value is 2.
// The prototype also has a 'b' property, but it's not visited.
// This is called Property Shadowing

console.log(o.c); // 4
// Is there a 'c' own property on o? No, check its prototype.
// Is there a 'c' own property on o.[[Prototype]]? Yes, its valu
```

### 2. In this article
- **Inheritance with the prototype chain** appears in the source and deserves deliberate review.
- **Inheriting properties** appears in the source and deserves deliberate review.
```js
const o = {
  a: 1,
  b: 2,
  // __proto__ sets the [[Prototype]]. It's specified here
  // as another object literal.
  __proto__: {
    b: 3,
    c: 4,
    __proto__: {
      d: 5,
    },
  },
};

// { a: 1, b: 2 } ---> { b: 3, c: 4 } ---> { d: 5 } ---> Object.prototype ---> null

console.log(o.d); // 5
```

### 3. Inheritance with the prototype chain
- **Inheriting "methods"** appears in the source and deserves deliberate review.
- **Constructors** appears in the source and deserves deliberate review.

### 4. Inheriting properties
- **Implicit constructors of literals** appears in the source and deserves deliberate review.
- **Building longer inheritance chains** appears in the source and deserves deliberate review.

### 5. Inheriting "methods"
- **Inspecting prototypes: a deeper dive** appears in the source and deserves deliberate review.
- **Different ways of creating and mutating prototype chains** appears in the source and deserves deliberate review.

### 6. Constructors
- **Objects created with syntax constructs** appears in the source and deserves deliberate review.
- **With constructor functions** appears in the source and deserves deliberate review.

### 7. Implicit constructors of literals
- **With Object.create()** appears in the source and deserves deliberate review.
- **With classes** appears in the source and deserves deliberate review.

### 8. Building longer inheritance chains
- **With Object.setPrototypeOf()** appears in the source and deserves deliberate review.
- **With the __proto__ accessor** appears in the source and deserves deliberate review.

## Technical Deep-Dive

### Step-by-Step Logic Walkthrough: Inheritance and the prototype chain

1. **Input** — Identify the problem statement, page rule, or example pattern the source is trying to explain.
2. **Process** — Map the visible structure, the key attributes, or the sequence of operations that the page emphasizes.
3. **Output** — Confirm the final behavior, rendered result, or response that should appear when the mechanism is used correctly.

```js
function Graph() {
  this.vertices = [];
  this.edges = [];
}

Graph.prototype.addVertex = function (v) {
  this.vertices.push(v);
};

const g = new Graph();
// g ---> Graph.prototype ---> Object.prototype ---> null

g.hasOwnProperty("vertices"); // true
Object.hasOwn(g, "vertices"); // true

g.hasOwnProperty("nope"); // false
Object.hasOwn(g, "nope"); // false

g.hasOwnProperty("addVertex"); // false
Object.hasOwn(g, "addVertex"); // false

Object.getPrototypeOf(g).hasOwnProperty("addVertex"); // true
```

## Key Terminology Bank

| Term | Meaning |
|---|---|
| **`Inheritance and the prototype chain`** | Important source concept to remember during recall. |
| **`In this article`** | Important source concept to remember during recall. |
| **`Inheritance with the prototype chain`** | Important source concept to remember during recall. |
| **`Inheriting properties`** | Important source concept to remember during recall. |
| **`Inheriting "methods"`** | Important source concept to remember during recall. |
| **`Constructors`** | Important source concept to remember during recall. |
| **`Implicit constructors of literals`** | Important source concept to remember during recall. |
| **`Building longer inheritance chains`** | Important source concept to remember during recall. |
| **`Inspecting prototypes: a deeper dive`** | Important source concept to remember during recall. |
| **`Different ways of creating and mutating prototype chains`** | Important source concept to remember during recall. |
| **`Objects created with syntax constructs`** | Important source concept to remember during recall. |
| **`With constructor functions`** | Important source concept to remember during recall. |
| **`With Object.create()`** | Important source concept to remember during recall. |
| **`With classes`** | Important source concept to remember during recall. |
| **`With Object.setPrototypeOf()`** | Important source concept to remember during recall. |

## Watch Out For...

- **Surface reading** — Assuming the first visible heading is the whole topic — Read the page structure, code, and supporting text together.
- **Context loss** — Treating a rule as universal when it only applies in one example — Check whether the source limits the rule to a specific case.
- **Ignoring examples** — Skipping code blocks because the prose seems sufficient — Code blocks usually carry the operational detail.
- **Overgeneralizing** — Using one section to explain the entire page — Separate the main pattern from the edge cases and exceptions.
- **Missing constraints** — Thinking an implementation works even if a required attribute or step is omitted — Constraints are part of the answer, not an optional detail.
- **Wrong priority** — Putting memorization ahead of mechanism — Learn the mechanism first so the details make sense.
- **Terminology drift** — Using similar words as if they mean the same thing — Use the page's exact language when possible.
- **No review pass** — Assuming the first draft is enough for exam prep — Use the recall questions and tighten weak spots before saving.

## Active Recall

1. **Conceptual** — What is the core purpose of **Inheritance and the prototype chain - JavaScript | MDN** in the source material?
2. **Code** — Which example code or structure from the page best demonstrates the main mechanism?
3. **Contrast** — What changes when you compare the simplest path with the more complete or safer path?
4. **Prediction** — If one key rule is removed, what outcome should you expect and why?
5. **Integration** — How would you explain the topic to someone else using the page's vocabulary and examples?

## Answer Key

### 1. Conceptual
Full marks answer: The source frames **Inheritance and the prototype chain - JavaScript | MDN** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.

### 2. Code
Full marks answer: The source frames **Inheritance and the prototype chain - JavaScript | MDN** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.

### 3. Contrast
Full marks answer: The source frames **Inheritance and the prototype chain - JavaScript | MDN** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.

### 4. Prediction
Full marks answer: The source frames **Inheritance and the prototype chain - JavaScript | MDN** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.

### 5. Integration
Full marks answer: The source frames **Inheritance and the prototype chain - JavaScript | MDN** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.
