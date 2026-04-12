# 📚 Object Prototypes — Exam Study Guide
**Source:** [MDN Web Docs — Object prototypes](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object_prototypes)

---

## Executive Summary

This article explains prototypes — the fundamental mechanism by which JavaScript objects inherit features from one another. Every object in JavaScript has a built-in link to a **prototype object**, and when you access a property that doesn't exist on the object itself, JavaScript walks up the **prototype chain** until it finds the property or reaches `null`. The most critical exam takeaway is that **JavaScript inheritance is prototype-based, not class-based at its core** — `class` syntax (covered in later articles) is syntactic sugar over this prototype system.

---

## Core Pillars

### 1. What Is a Prototype?

- Every object in JavaScript has a built-in property that points to another object called its **prototype**.
- The prototype is itself an object, so it also has a prototype — forming a **prototype chain**.
- The chain terminates when a prototype's own prototype is `null`.

```js
const myObject = {
  city: "Madrid",
  greet() {
    console.log(`Greetings from ${this.city}`);
  },
};

myObject.greet(); // "Greetings from Madrid"
```

- Despite only defining `city` and `greet`, `myObject` has many more properties accessible (e.g., `toString`, `hasOwnProperty`, `valueOf`). These come from its prototype.

---

### 2. The Prototype Chain — How Property Lookup Works

When you access `obj.someProperty`, JavaScript follows this lookup sequence:

1. **Check the object itself** — does it have `someProperty` as an own property?
2. **Check the object's prototype** — does the prototype have `someProperty`?
3. **Keep walking up the chain** — check each successive prototype.
4. **Return `undefined`** if `null` is reached without finding the property.

```js
myObject.toString(); // "[object Object]"
```

`toString` is not defined on `myObject` — it's found on `Object.prototype`, which is `myObject`'s prototype.

---

### 3. `Object.prototype` — The Root of All Objects

```js
Object.getPrototypeOf(myObject); // Object { }
```

- For a plain object literal, the prototype is **`Object.prototype`**.
- `Object.prototype`'s own prototype is `null` — it is the **end of every prototype chain**.
- `Object.prototype` provides the methods all objects inherit: `toString()`, `valueOf()`, `hasOwnProperty()`, `isPrototypeOf()`, etc.

---

### 4. Accessing a Prototype

- **Standard method:** `Object.getPrototypeOf(obj)` — returns the prototype object.
- **Non-standard (legacy):** `obj.__proto__` — works in all browsers but not formally standardised; use `Object.getPrototypeOf()` instead.
- The `prototype` **property name** itself is not the pointer to the prototype (that causes confusion — see "Watch Out For").

---

### 5. Prototype Chains of Built-in Types

```js
const myDate = new Date();
let object = myDate;

do {
  object = Object.getPrototypeOf(object);
  console.log(object);
} while (object);

// Date.prototype
// Object { }   ← Object.prototype
// null
```

- `myDate`'s prototype chain: `myDate → Date.prototype → Object.prototype → null`
- When you call `myDate.getTime()`, JS finds `getTime` on `Date.prototype`.
- This applies to all built-in types: `Array`, `Function`, `RegExp`, etc., each has its own `.prototype` object that sits between instances and `Object.prototype`.

---

### 6. Shadowing Properties

**Shadowing** occurs when an object defines a property with the same name as one on its prototype chain:

```js
const myDate = new Date(1995, 11, 17);
console.log(myDate.getTime()); // 819129600000  ← from Date.prototype

myDate.getTime = function () {
  console.log("something else!");
};

myDate.getTime(); // "something else!" ← from myDate itself
```

- Lookup always starts at the **object itself**, so the own property takes precedence.
- The prototype's version is **not deleted** — it is merely hidden (shadowed).
- Removing the own property with `delete myDate.getTime` restores access to the prototype version.

---

### 7. Setting a Prototype — Method 1: `Object.create()`

```js
const personPrototype = {
  greet() {
    console.log("hello!");
  },
};

const carl = Object.create(personPrototype);
carl.greet(); // "hello!"
```

- `Object.create(proto)` creates a **new, empty object** whose prototype is set to `proto`.
- `carl` has no own properties — `greet` is inherited from `personPrototype`.
- Useful for manually setting up prototype chains without constructors.

---

### 8. Setting a Prototype — Method 2: Constructor Functions

All functions in JavaScript have a `prototype` property. When called with `new`, the newly created object's prototype is set to that function's `prototype`.

```js
const personPrototype = {
  greet() {
    console.log(`hello, my name is ${this.name}!`);
  },
};

function Person(name) {
  this.name = name;  // own property set in constructor
}

// Copy methods from personPrototype onto Person's prototype
Object.assign(Person.prototype, personPrototype);

const reuben = new Person("Reuben");
reuben.greet(); // "hello, my name is Reuben!"
```

**How `new Person("Reuben")` works:**
1. A new empty object is created.
2. Its `[[Prototype]]` is set to `Person.prototype`.
3. The constructor function runs with `this` pointing to the new object.
4. The object is returned.

This is why `myDate`'s prototype is called `Date.prototype` — it's the `prototype` property of the `Date` constructor.

---

### 9. Own Properties vs. Prototype Properties

| Concept | Definition | Example |
|---|---|---|
| **Own property** | Defined directly on the object (not inherited) | `name` set in the constructor |
| **Prototype property** | Inherited from the prototype chain | `greet` defined on `Person.prototype` |

```js
const irma = new Person("Irma");

Object.hasOwn(irma, "name");   // true  — set in constructor
Object.hasOwn(irma, "greet");  // false — on the prototype, not irma itself
```

**Common pattern** — define per-instance data as own properties, shared behaviour on the prototype:
```js
function Person(name) {
  this.name = name;         // ← own (different for each instance)
}
Person.prototype.greet = function() {  // ← shared (same for all instances)
  console.log(`hello, my name is ${this.name}!`);
};
```

---

### 10. Prototypes and Inheritance

- Prototype chains enable **inheritance**: one object type can inherit features from another.
- Example OOP model: `Student` and `Professor` both inherit shared properties from `Person`; each adds or overrides what's specific to them.
- In JavaScript, if `Student` and `Professor` objects have `Person.prototype` in their chain, they inherit all `Person` methods automatically.
- The next MDN article (Object-oriented programming) covers how to implement full OOP inheritance via prototypes and `class`.

---

## Technical Deep-Dive

### Logic Walkthrough: Tracing a Prototype Chain

**Goal:** Call `myDate.getTime()` and understand where JS finds it.

```js
const myDate = new Date(1995, 11, 17);
myDate.getTime(); // 819129600000
```

**Step-by-step property lookup:**

1. JS checks `myDate` — does it have an own property `getTime`? **No.**
2. JS gets `myDate`'s prototype: `Date.prototype`.
3. JS checks `Date.prototype` — does it have `getTime`? **Yes.**
4. JS calls `Date.prototype.getTime` with `this = myDate`.
5. Returns the timestamp.

**Walking the full prototype chain:**
```js
// myDate
//   → Date.prototype        (has: getTime, getFullYear, etc.)
//     → Object.prototype    (has: toString, valueOf, hasOwnProperty, etc.)
//       → null              (chain ends)
```

---

### Logic Walkthrough: Constructor + Prototype Setup Pattern

```js
// 1. Define shared methods on a plain object
const personPrototype = {
  greet() {
    console.log(`hello, my name is ${this.name}!`);
  },
};

// 2. Define a constructor for per-instance data
function Person(name) {
  this.name = name;
}

// 3. Merge methods onto the constructor's prototype
Object.assign(Person.prototype, personPrototype);

// 4. Create instances
const alice = new Person("Alice");
const bob   = new Person("Bob");

alice.greet(); // "hello, my name is Alice!"
bob.greet();   // "hello, my name is Bob!"

// 5. Verify the chain
Object.getPrototypeOf(alice) === Person.prototype;  // true
Object.getPrototypeOf(Person.prototype) === Object.prototype;  // true
```

- `alice.name` is an **own property** — each instance has its own copy.
- `alice.greet` is found on `Person.prototype` — **one shared function**, not copied to each instance. This is memory-efficient.

---

### Logic Walkthrough: `Object.create()` vs. Constructor Pattern

```js
// Object.create() approach
const proto = { greet() { console.log("hi"); } };
const obj1 = Object.create(proto);   // obj1's prototype IS proto

// Constructor approach
function Greeter() {}
Greeter.prototype.greet = function() { console.log("hi"); };
const obj2 = new Greeter();          // obj2's prototype IS Greeter.prototype
```

| | `Object.create()` | Constructor with `new` |
|---|---|---|
| Sets prototype to | The argument passed in | The function's `.prototype` property |
| Runs constructor logic | No | Yes |
| Own properties | Set manually after | Set inside constructor via `this` |
| Use case | Explicit prototype delegation | Creating multiple instances with shared state |

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Prototype** | The built-in object that every JavaScript object links to; the source of inherited properties and methods. |
| **Prototype chain** | The linked sequence of prototype objects traversed during property lookup; terminates when `null` is reached. |
| **`Object.prototype`** | The root prototype object at the top of every prototype chain; provides universal methods like `toString()`, `valueOf()`, and `hasOwnProperty()`. |
| **`Object.getPrototypeOf(obj)`** | The standard method to retrieve an object's prototype; preferred over `__proto__`. |
| **`__proto__`** | A non-standard, legacy accessor property that exposes an object's prototype; supported by all browsers but replaced by `Object.getPrototypeOf()`. |
| **`prototype` property** | A property on every JavaScript **function** that becomes the `[[Prototype]]` of objects created by calling that function with `new`. |
| **`[[Prototype]]`** | The internal slot in every object that stores its prototype reference; read via `Object.getPrototypeOf()`. |
| **Own property** | A property that exists directly on an object, not inherited from its prototype chain. |
| **Shadowing** | When an own property has the same name as a property on the prototype chain, hiding (but not deleting) the prototype version. |
| **`Object.create(proto)`** | Creates and returns a new object with `proto` set as its prototype. |
| **Constructor function** | A regular function invoked with `new` that initialises own properties of a new object via `this`. |
| **`new` keyword** | Operator that creates a new object, sets its prototype to the constructor's `prototype` property, runs the constructor with `this = newObject`, and returns the object. |
| **`Object.assign(target, source)`** | Copies all enumerable own properties from `source` to `target`; used to copy methods onto a constructor's `.prototype`. |
| **`Object.hasOwn(obj, key)`** | Static method returning `true` if `obj` has `key` as an own (non-inherited) property; preferred over `hasOwnProperty()`. |
| **Inheritance (prototype-based)** | The mechanism where objects inherit properties and methods through the prototype chain, not through copying. |
| **`Date.prototype`** | The prototype of all `Date` instances; contains `getTime()`, `getFullYear()`, etc. |
| **Property lookup** | The sequential search for a property starting at the object, then its prototype, then the prototype's prototype, until found or `null` is reached. |
| **`Object.hasOwnProperty(key)`** | Instance method checking if `key` is an own property; superseded by the static `Object.hasOwn()`. |

---

## Watch Out For...

1. **`prototype` ≠ the prototype of an object.** Every **function** has a `.prototype` property — this becomes the prototype of objects created with `new`. BUT `Object.getPrototypeOf(someObj)` does NOT return `someObj.prototype` — an ordinary object doesn't have a `.prototype` property at all. These are two different things that share a confusing name.

2. **`__proto__` is non-standard; use `Object.getPrototypeOf()`.** Although `__proto__` works in every browser, it's a legacy feature. Accessing or setting the prototype via `__proto__` in production code is bad practice.

3. **Shadowing does not modify the prototype.** If you set `myDate.getTime = function() {...}`, the original `Date.prototype.getTime` is completely untouched. Only the instance `myDate` is affected.

4. **Prototype properties are shared across ALL instances.** Methods on `Person.prototype` are shared — that's the point. But if you accidentally put a **reference type** (array or object) on the prototype, all instances share that exact same object and mutations on one affect all others.
   ```js
   Person.prototype.friends = [];  // ← SHARED across all Person instances!
   alice.friends.push("Bob");       // mutates the shared array
   console.log(bob.friends);        // ["Bob"] ← unintended!
   ```

5. **`Object.create(null)` creates an object with NO prototype.** The resulting object has no `toString`, no `hasOwnProperty`, nothing — not even `Object.prototype` methods. This is intentional in some cases (pure hash maps) but unexpected otherwise.

6. **Property lookup returns `undefined` — not an error — when reaching `null`.** Accessing `obj.nonExistentProp` returns `undefined` silently. This can mask bugs where you expect a method to exist but it doesn't.

7. **`Object.hasOwn()` vs. `in` operator.** `in` checks the whole prototype chain; `Object.hasOwn()` checks only own properties. Using `in` when you mean `hasOwn` can produce false positives (e.g., `"toString" in myObj` is always `true`).

8. **Adding methods to built-in prototypes (prototype pollution).** You can do `Array.prototype.sum = function() {...}` — but this is dangerous: it pollutes all arrays globally, breaks `for...in` loops, and creates conflicts with future JS standards. Never do this in production.

9. **The chain terminates at `null`, not `undefined`.** `Object.getPrototypeOf(Object.prototype)` returns `null` — not `undefined`. Code that checks `while (proto)` will stop at `null` because `null` is falsy.

10. **`Object.assign` copies own enumerable properties only — it does NOT set up a prototype link.** After `Object.assign(Person.prototype, personPrototype)`, the methods are copied **onto** `Person.prototype` as own properties — `Person.prototype` does NOT then inherit from `personPrototype`. Prototype delegation and property copying are fundamentally different.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Explain in plain terms what the prototype chain is and what happens when JavaScript cannot find a property on an object.

**Q2.** What is the difference between a function's `.prototype` property and what `Object.getPrototypeOf()` returns for an instance created with that function? Show a code example that makes the relationship clear.

**Q3.** What is property shadowing? Create a short code example demonstrating it, and explain what happens to the prototype's version of the property.

**Q4.** Compare `Object.create(proto)` and constructor functions with `new`. When would you choose each approach? Show equivalent code that achieves the same prototype relationship using both techniques.

**Q5.** You create a `Vehicle` constructor and want all instances to share a `describe()` method, while each instance has its own `make` and `model`. Write the complete implementation — constructor, prototype method assignment, and instance creation — then verify with `Object.hasOwn()` which properties are own vs. inherited.

---

## Answer Key

---

**A1.**

Every JavaScript object has an internal link to another object called its **prototype**. When you access a property on an object:
1. JS first checks if that property is an **own property** of the object.
2. If not found, it moves to the object's prototype and checks there.
3. It continues up the chain, checking each prototype.
4. If it reaches `null` (the end of the chain) without finding the property, it returns **`undefined`**.

This linked chain of prototype objects is called the **prototype chain**. It enables inheritance — objects can access methods and properties defined on other objects via this chain, without those properties being copied.

---

**A2.**

```js
function Person(name) {
  this.name = name;
}

const alice = new Person("Alice");

// The function's .prototype property:
console.log(Person.prototype);
// → { constructor: Person }  (plus anything we add to it)

// The prototype of the instance created with new:
console.log(Object.getPrototypeOf(alice));
// → { constructor: Person }  (same object!)

// They are the same object:
Object.getPrototypeOf(alice) === Person.prototype;  // true
```

**Key distinction:**
- `Person.prototype` is a property **on the function** — it's the object that will become the `[[Prototype]]` of instances.
- `Object.getPrototypeOf(alice)` is the **prototype of the instance** — the object JS searches when `alice.someProperty` isn't found on `alice`.
- They happen to be the **same object**, which is how `new` works: it sets the instance's `[[Prototype]]` to the constructor's `.prototype`.

---

**A3.**

**Shadowing** occurs when an object has an own property with the same name as a property on its prototype chain. The own property "shadows" (hides) the prototype version.

```js
const myDate = new Date(1995, 11, 17);

// Initially, getTime comes from Date.prototype
console.log(myDate.getTime()); // 819129600000

// Add own property with same name
myDate.getTime = function () {
  return "I'm shadowing the original!";
};

console.log(myDate.getTime()); // "I'm shadowing the original!"
```

- JS finds `getTime` on `myDate` itself (the own property) at step 1 of lookup — it never even checks the prototype.
- `Date.prototype.getTime` is **completely unchanged** — other `Date` instances still use it normally.
- The shadow can be removed with `delete myDate.getTime`, restoring access to the prototype version.

---

**A4.**

**`Object.create(proto)` approach:**
```js
const vehicleProto = {
  describe() { console.log(`${this.make} ${this.model}`); }
};

const car = Object.create(vehicleProto);
car.make = "Toyota";
car.model = "Corolla";
car.describe(); // "Toyota Corolla"
```

**Constructor with `new` approach:**
```js
function Vehicle(make, model) {
  this.make = make;
  this.model = model;
}
Vehicle.prototype.describe = function() {
  console.log(`${this.make} ${this.model}`);
};

const car = new Vehicle("Toyota", "Corolla");
car.describe(); // "Toyota Corolla"
```

Both achieve the same prototype relationship (`car → vehicleProto/Vehicle.prototype → Object.prototype`).

| | `Object.create()` | Constructor + `new` |
|---|---|---|
| **Constructor logic** | None; set properties manually | Runs inside the function body |
| **Multiple instances** | Verbose (set props each time) | Clean; reuse `new Fn(args)` |
| **Choose when** | Explicit prototype delegation, single objects | Creating many instances of the same shape |

---

**A5.**

```js
// Constructor — own properties set per-instance
function Vehicle(make, model) {
  this.make = make;    // own
  this.model = model;  // own
}

// Shared method on the prototype
Vehicle.prototype.describe = function () {
  console.log(`${this.make} ${this.model}`);
};

// Create instances
const car1 = new Vehicle("Toyota", "Corolla");
const car2 = new Vehicle("Honda", "Civic");

car1.describe(); // "Toyota Corolla"
car2.describe(); // "Honda Civic"

// Verify own vs. inherited
console.log(Object.hasOwn(car1, "make"));     // true  ← own property
console.log(Object.hasOwn(car1, "model"));    // true  ← own property
console.log(Object.hasOwn(car1, "describe")); // false ← on Vehicle.prototype

// Confirm shared method (same function reference for all instances)
car1.describe === car2.describe;              // true (not copied per instance)
Object.getPrototypeOf(car1) === Vehicle.prototype; // true
```

`make` and `model` are **own** (each instance has independent copies); `describe` is **inherited** (one shared function on `Vehicle.prototype`, saving memory).
