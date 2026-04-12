# 📚 Classes in JavaScript — Exam Study Guide
**Source:** [MDN Web Docs — Classes in JavaScript](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Classes_in_JavaScript)

---

## Executive Summary

This article translates the OOP concepts from the previous article (classes, instances, inheritance, encapsulation) into **real JavaScript syntax** using the `class` keyword. The critical insight is that **`class` syntax is syntactic sugar** — under the hood it still uses the prototype system described in article 01. Classes don't change *how* JavaScript works; they provide a **cleaner, more readable way** to write OOP code that resembles classical OOP languages like Java or C++. The three key practical skills are: declaring a class with a constructor, using `extends` and `super()` for inheritance, and using the `#` prefix for genuine private fields and methods.

---

## Core Pillars

### 1. Declaring a Class

Use the `class` keyword followed by the class name. The body contains:
- **Field declarations** (optional but recommended for clarity)
- A **`constructor()`** method
- **Methods** (no `function` keyword needed)

```js
class Person {
  name;                          // field declaration (optional)

  constructor(name) {
    this.name = name;            // initialise via constructor
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}`);
  }
}
```

**Notes on field declarations:**
- `name;` on its own declares the field with value `undefined`.
- `name = '';` declares with a **default value**.
- The field declaration is **optional** — omitting it and just writing `this.name = name` in the constructor also works. But explicit declarations make the class's shape immediately visible to readers.

---

### 2. Creating Instances with `new`

Call the class name like a function, preceded by `new`:

```js
const giles = new Person("Giles");
giles.introduceSelf(); // "Hi! I'm Giles"
```

The `constructor()` is called automatically by `new`. Note that the constructor is invoked using the **class name** (`Person`), not the word `constructor`.

---

### 3. Omitting the Constructor

If a class requires **no special initialisation**, the `constructor` can be omitted. JavaScript generates a default empty constructor automatically.

```js
class Animal {
  sleep() {
    console.log("zzzzzzz");
  }
}

const spot = new Animal();
spot.sleep(); // 'zzzzzzz'
```

---

### 4. Inheritance with `extends` and `super()`

Use the `extends` keyword to inherit from another class. In the subclass constructor, **`super()` must be called first** before accessing `this`.

```js
class Professor extends Person {
  teaches;                                    // new property

  constructor(name, teaches) {
    super(name);                              // call Person's constructor
    this.teaches = teaches;                   // then set own property
  }

  introduceSelf() {                           // override parent method
    console.log(
      `My name is ${this.name}, and I will be your ${this.teaches} professor.`
    );
  }

  grade(paper) {
    const grade = Math.floor(Math.random() * (5 - 1) + 1);
    console.log(grade);
  }
}
```

```js
const walsh = new Professor("Walsh", "Psychology");
walsh.introduceSelf(); // 'My name is Walsh, and I will be your Psychology professor'
walsh.grade("my paper"); // a random integer 1–4
```

**What `super(name)` does:**
- Calls the **parent class's constructor** (`Person`'s constructor).
- The parent constructor handles initialising `this.name`.
- Only *after* `super()` returns can you safely use `this` in the subclass constructor.

---

### 5. Encapsulation — Private Fields with `#`

Prefix a field name with `#` to make it a **private field**. Private fields:
- **Must be declared** in the class body before they can be used.
- Can only be accessed or modified by the **class's own methods**.
- Attempting access from outside the class throws a **`SyntaxError`**.

```js
class Student extends Person {
  #year;                                      // private field declaration

  constructor(name, year) {
    super(name);
    this.#year = year;                        // set private field
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}, and I'm in year ${this.#year}.`);
  }

  canStudyArchery() {
    return this.#year > 1;                    // access private field internally
  }
}
```

```js
const summers = new Student("Summers", 2);
summers.introduceSelf();      // "Hi! I'm Summers, and I'm in year 2."
summers.canStudyArchery();    // true
summers.#year;                // SyntaxError ← private field, cannot access externally
```

> **Note:** Chrome DevTools console can access private fields outside the class — this is a deliberate DevTools relaxation and does **not** reflect normal runtime behaviour.

---

### 6. Private Methods with `#`

Methods can also be private using the `#` prefix. They follow the same rules as private fields — only callable from within the class.

```js
class Example {
  somePublicMethod() {
    this.#somePrivateMethod();            // called internally ✓
  }

  #somePrivateMethod() {
    console.log("You called me?");
  }
}

const myExample = new Example();
myExample.somePublicMethod();     // 'You called me?'
myExample.#somePrivateMethod();   // SyntaxError ← cannot call externally
```

---

### 7. `class` Is Syntactic Sugar Over Prototypes

> **Critical reminder from the article:** The `class` features are not a new way of combining objects. Under the hood, they still use prototypes. `class` is just a cleaner way to set up a prototype chain.

What the `class` keyword actually does behind the scenes:

| `class` feature | Prototype equivalent |
|---|---|
| `class Person { ... }` | Defining a constructor function `Person` |
| Methods in the class body | Methods added to `Person.prototype` |
| `extends Person` | Setting up the `[[Prototype]]` chain |
| `super(name)` | Calling the parent constructor function |
| `#year` private field | No direct prototype equivalent (new language feature) |

Private fields (`#`) are the **one genuine addition** that has no equivalent in the old prototype syntax — they are enforced by the JavaScript engine, not merely a convention.

---

## Technical Deep-Dive

### Logic Walkthrough: Building the Full School Hierarchy in Real JS

**Start with the base class:**

```js
class Person {
  name;

  constructor(name) {
    this.name = name;
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}`);
  }
}
```

**Extend to `Professor`:**

```js
class Professor extends Person {
  teaches;

  constructor(name, teaches) {
    super(name);           // ← must come FIRST; initialises this.name via Person
    this.teaches = teaches;
  }

  introduceSelf() {
    console.log(`My name is ${this.name}, and I will be your ${this.teaches} professor.`);
  }

  grade(paper) {
    const grade = Math.floor(Math.random() * (5 - 1) + 1);
    console.log(grade);
  }
}
```

**Extend to `Student` with private field:**

```js
class Student extends Person {
  #year;                 // ← private: declared here, accessible only internally

  constructor(name, year) {
    super(name);
    this.#year = year;
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}, and I'm in year ${this.#year}.`);
  }

  canStudyArchery() {
    return this.#year > 1;
  }
}
```

**Instantiate and test:**

```js
const pratt   = new Person("Pratt");
const walsh   = new Professor("Walsh", "Psychology");
const summers = new Student("Summers", 2);

pratt.introduceSelf();
// "Hi! I'm Pratt"

walsh.introduceSelf();
// "My name is Walsh, and I will be your Psychology professor."

walsh.grade("essay");
// random number 1–4

summers.introduceSelf();
// "Hi! I'm Summers, and I'm in year 2."

summers.canStudyArchery();
// true (2 > 1)

summers.#year;
// SyntaxError — private field
```

**Prototype chain for `walsh`:**
```
walsh → Professor.prototype → Person.prototype → Object.prototype → null
```
- `walsh.name` and `walsh.teaches` are **own properties** (set in constructors).
- `walsh.grade` and `walsh.introduceSelf` are found on **`Professor.prototype`**.
- `Person.prototype.introduceSelf` is **shadowed** by `Professor.prototype.introduceSelf`.

---

### Logic Walkthrough: The `super()` Requirement in Subclass Constructors

**Why is `super()` mandatory before `this`?**

When `new Professor("Walsh", "Psychology")` is called:
1. A new empty object is created with `Professor.prototype` as its `[[Prototype]]`.
2. Because `Professor extends Person`, the new object must also be initialised by `Person`'s constructor.
3. Until `super()` is called, `this` is **uninitialised** in the subclass constructor — accessing it throws a `ReferenceError`.
4. `super(name)` calls `Person`'s constructor, which sets `this.name = name`. Now `this` is ready.
5. The subclass constructor continues: `this.teaches = teaches`.

**Sequence diagram:**
```
new Professor("Walsh", "Psychology")
  → creates new object
  → enters Professor constructor
  → super("Walsh")
      → enters Person constructor
      → this.name = "Walsh"       ← completed
  → this.teaches = "Psychology"   ← now safe to use `this`
  → returns the completed object
```

> **Rule:** In any subclass constructor, `super()` must be called **before any reference to `this`**. Forgetting this is a common bug.

---

### Logic Walkthrough: Private Fields vs. Convention (`_property`)

**Old convention (pre-private fields):**
```js
// Nothing stops external access — purely a naming signal
function Student(name, year) {
  this.name = name;
  this._year = year;   // underscore means "please treat as private"
}

const s = new Student("Alice", 1);
console.log(s._year); // 1 — accessible! Convention is not enforcement.
```

**Modern private fields (`#`):**
```js
class Student extends Person {
  #year;

  constructor(name, year) {
    super(name);
    this.#year = year;
  }

  canStudyArchery() { return this.#year > 1; }
}

const s = new Student("Alice", 1);
console.log(s.#year); // SyntaxError — enforced by the engine, not a convention
```

| Feature | `_year` Convention | `#year` Private Field |
|---|---|---|
| Can be accessed externally | Yes (no enforcement) | No (SyntaxError) |
| Must be declared in class body | No | Yes |
| Works in old `function` constructors | Yes | No — class syntax only |
| Supported in | Always | ES2022+ |

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`class` keyword** | ES6+ syntax for declaring a class in JavaScript; syntactic sugar over the prototype-based constructor function pattern. |
| **Class body** | The block `{ }` after the class name containing field declarations, the constructor, and methods. |
| **Field declaration** | Listing a property name (e.g., `name;` or `name = ''`) at the top of a class body to document the class's shape; optional but recommended. |
| **`constructor()` method** | A special method inside a class that runs when `new` is called; initialises the new instance's own properties via `this`. |
| **`new` keyword** | Operator that creates a new instance by calling the class constructor; syntax: `new ClassName(args)`. |
| **`extends` keyword** | Used in a class declaration to inherit from a parent class; sets up the prototype chain automatically. |
| **`super()`** | Called inside a subclass constructor to invoke the parent class's constructor; must be called before `this` is used. |
| **`super.method()`** | Calls a method from the parent class, allowing a subclass to extend (rather than fully replace) parent behaviour. |
| **Method override** | Defining a method in a subclass with the same name as one in the parent class; the subclass version takes precedence for instances of the subclass. |
| **Private field (`#`)** | A class field prefixed with `#`; can only be accessed or modified by the class's own methods; enforced by the JS engine, not just convention. |
| **Private method (`#`)** | A method prefixed with `#`; only callable from within the class body. |
| **`SyntaxError`** | The error thrown when attempting to access a private field or method from outside the class. |
| **Syntactic sugar** | New syntax that makes code easier to write/read, but compiles to the same underlying mechanism (here: `class` syntax over prototypes). |
| **Subclass / Child class** | A class that `extends` another class and inherits its properties and methods, potentially adding or overriding them. |
| **Superclass / Parent class** | The class being extended; its constructor and methods are available to subclasses via `super` and the prototype chain. |
| **Own property** | A property set directly on an instance (e.g. in the constructor via `this.name = name`), as opposed to one inherited from the prototype. |
| **Default constructor** | An implicit, empty constructor generated by JavaScript when a class has no explicit `constructor()`. |
| **`Math.floor(Math.random() * (max - min) + min)`** | Common idiom for generating a random integer between `min` (inclusive) and `max` (exclusive); used in the `grade()` example. |

---

## Watch Out For...

1. **`super()` must be called before `this` in subclass constructors.** If you reference `this` before calling `super()` in a subclass, you get a `ReferenceError: Must call super constructor in derived class before accessing 'this'`. This is the single most common `class` / `extends` pitfall for beginners.

2. **`class` is still prototype-based under the hood.** The class syntax does not copy properties to instances — it sets up prototype chains. Methods are on the prototype, not copied to each instance. All the rules from guide 01 (Object Prototypes) still apply.

3. **Private fields (`#`) must be declared in the class body.** Unlike regular properties, you cannot create a private field by doing `this.#newField = value` without first declaring `#newField;` at the top of the class. Attempting this throws a `SyntaxError`.

4. **The `#` is part of the field name.** `this.#year` and `this.year` are **two completely different properties**. You could technically have both in the same class — they do not conflict.

5. **Private fields are not inherited by subclasses.** A subclass cannot access a parent's private field directly (even with `this.#field`). If access is needed, the parent must provide a public or protected method.

6. **Chrome DevTools can access private fields — this is exceptional.** The browser console relaxes the private field restriction for debugging convenience. Never rely on this as evidence that `#` fields are accessible in production code.

7. **Methods in a class body are on the prototype, not the instance.** Writing `myMethod() { ... }` inside a `class` body adds `myMethod` to `ClassName.prototype` — it is NOT copied to each instance. This is memory-efficient but means you can't use arrow functions in the class body for methods if you need the prototype placement (though class field arrow functions are an option for bound methods).

8. **Field declarations with a default value create an own property on EVERY instance.** `name = '';` in the class body means every new instance gets its own `name` property initialised to `''`, even before the constructor runs. This is fine for primitives but can cause the "shared reference type" problem if you write `tags = []` — every instance would start with its own separate `[]`, which is actually correct here (unlike the prototype mutation trap in guide 01).

9. **Omitting the constructor in a subclass delegates to the parent.** If a subclass omits `constructor`, the default generated constructor is `constructor(...args) { super(...args); }` — it correctly passes all arguments up to the parent. However, if you write *any* constructor in the subclass, you must call `super()` explicitly.

10. **`extends` can only create a single parent.** JavaScript classes support **single inheritance** only — you cannot `extends` two classes simultaneously. Multiple inheritance patterns must be solved with mixins (composition).

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Write the complete `Person` class with a `name` field, a constructor, and an `introduceSelf()` method. Then create an instance and call the method. What does the `name;` declaration at the top of the class body actually do?

**Q2.** Write a `Professor` class that extends `Person`, adds a `teaches` property, overrides `introduceSelf()`, and adds a `grade()` method that logs a random integer. Explain why `super(name)` must come before `this.teaches = teaches` in the constructor.

**Q3.** Write the `Student` class that extends `Person` with a **private** `#year` field. Show what happens when external code tries to access `#year` directly. How does this differ from the old `_year` naming convention?

**Q4.** A new developer joins your team and tells you that JavaScript's `class` keyword is "just like Java classes" — properties are copied into each instance. How do you correct them? What is actually happening under the hood?

**Q5.** Write a `AdminStudent` class that extends `Student`. It should add an `adminLevel` property. What challenge do you face, and how do you solve it given that `Student` has a private `#year` field?

---

## Answer Key

---

**A1.**

```js
class Person {
  name;                          // field declaration

  constructor(name) {
    this.name = name;
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}`);
  }
}

const giles = new Person("Giles");
giles.introduceSelf(); // "Hi! I'm Giles"
```

**What `name;` does:** The `name;` declaration at the top of the class body documents that instances of `Person` will have a property called `name`. At the point of declaration, `name` is set to `undefined` on each newly created instance. The constructor then immediately overwrites it with the actual value. The declaration is **optional** — if omitted, `this.name = name` in the constructor still creates the property — but explicit field declarations serve as documentation, making the class's intended shape immediately clear to human readers.

---

**A2.**

```js
class Professor extends Person {
  teaches;

  constructor(name, teaches) {
    super(name);               // ← MUST come first
    this.teaches = teaches;
  }

  introduceSelf() {
    console.log(
      `My name is ${this.name}, and I will be your ${this.teaches} professor.`
    );
  }

  grade(paper) {
    const grade = Math.floor(Math.random() * (5 - 1) + 1);
    console.log(grade);
  }
}

const walsh = new Professor("Walsh", "Psychology");
walsh.introduceSelf(); // "My name is Walsh, and I will be your Psychology professor."
walsh.grade("essay");  // random integer 1–4
```

**Why `super()` first:** When `Professor extends Person`, the new object is considered "uninitialised" until `Person`'s constructor runs. JavaScript enforces this: accessing `this` before `super()` in a subclass constructor throws a `ReferenceError`. `super(name)` calls `Person`'s constructor, which sets `this.name = name` and makes the object ready. Only then can `this.teaches = teaches` safely run.

---

**A3.**

```js
class Student extends Person {
  #year;                        // private field — must be declared here

  constructor(name, year) {
    super(name);
    this.#year = year;
  }

  introduceSelf() {
    console.log(`Hi! I'm ${this.name}, and I'm in year ${this.#year}.`);
  }

  canStudyArchery() {
    return this.#year > 1;
  }
}

const summers = new Student("Summers", 2);
summers.introduceSelf();      // "Hi! I'm Summers, and I'm in year 2."
summers.canStudyArchery();    // true

summers.#year;                // SyntaxError: Private field '#year' must be declared in an enclosing class
```

**Difference from `_year` convention:**
- `_year` is just a naming hint — nothing in the language prevents `obj._year` from being read or written by external code. It's a gentleman's agreement.
- `#year` is **enforced by the JavaScript engine**. Any attempt to access it from outside the class body causes a hard `SyntaxError` at parse time, not just a runtime exception. The privacy is **real and guaranteed**, not just conventional.

---

**A4.**

JavaScript `class` syntax is syntactic sugar — it provides a cleaner way to write code that *under the hood* uses the same prototype system as before.

**What is NOT happening (Java model):**
- Properties and methods are NOT copied into each instance at creation time.
- There is no "flat object" with all inherited properties baked in.

**What IS happening (JavaScript prototype model):**
- `new Professor("Walsh", "Psychology")` creates an object with only its **own properties** (`name`, `teaches`).
- Methods like `introduceSelf()` and `grade()` live on **`Professor.prototype`** — a separate object.
- When `walsh.grade(...)` is called, JavaScript walks the prototype chain: checks `walsh` → checks `Professor.prototype` → finds `grade`. It is *delegated*, not copied.
- The prototype chain is: `walsh → Professor.prototype → Person.prototype → Object.prototype → null`.

The practical consequence: modifying `Professor.prototype.grade` after instances are created immediately affects all existing `Professor` instances — because they look up methods at call time, not at creation time.

---

**A5.**

The challenge is that `Student`'s `#year` is **private to `Student`** — `AdminStudent` cannot access `#year` at all, even though it inherits from `Student`. Private fields are *not* inherited.

**Solution:** `AdminStudent` cannot directly read or set `#year`. If it needs to interact with year-based logic, it must do so through `Student`'s public methods (like `canStudyArchery()`). `AdminStudent` simply adds its own `adminLevel` property and calls `super(name, year)` to let `Student` handle year initialisation:

```js
class AdminStudent extends Student {
  adminLevel;

  constructor(name, year, adminLevel) {
    super(name, year);           // Student handles #year internally
    this.adminLevel = adminLevel;
  }

  introduceSelf() {
    console.log(
      `Hi! I'm ${this.name}, a level-${this.adminLevel} admin student.`
    );
  }
}

const alex = new AdminStudent("Alex", 3, 2);
alex.introduceSelf();        // "Hi! I'm Alex, a level-2 admin student."
alex.canStudyArchery();      // true (3 > 1) — uses Student's method which accesses #year
// alex.#year                // SyntaxError — still private, even from a subclass
```

The encapsulation holds: `AdminStudent` benefits from `Student`'s year-based logic through the public API (`canStudyArchery()`), but cannot directly touch the private implementation detail (`#year`).
