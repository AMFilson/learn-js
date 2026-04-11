# 📦 JavaScript Object Basics — Exam Study Guide
**Source:** [MDN Web Docs — JavaScript object basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Object_basics)

---

## Executive Summary

A JavaScript **object** is a collection of related data and functionality grouped together under a single variable — consisting of **properties** (data) and **methods** (functions), accessed via a name/value pair structure. Objects can be created as **object literals** (written directly in code) or produced by **constructors** (functions called with `new` that act as templates for creating multiple objects of the same shape). Mastering the two access syntaxes (**dot notation** vs. **bracket notation**), understanding the `this` keyword in methods, and knowing how constructors work are the core skills tested in this topic.

---

## Core Pillars

### 1. What Is an Object?

- An object is a **collection of related data and/or functionality** stored together in a single structure.
- Objects contain **members**, each of which is a **name/value pair** (also called key/value pair).
- Members that hold data are called **properties**; members that hold functions are called **methods**.
- Objects help organise code by keeping related data and behaviour together — and protect against naming conflicts with other variables.

```js
const person = {
  name: ["Bob", "Smith"],  // property — value is an array
  age: 32,                 // property — value is a number
  bio() {                  // method — shorthand for bio: function() {}
    console.log(`${this.name[0]} ${this.name[1]} is ${this.age} years old.`);
  },
  introduceSelf() {
    console.log(`Hi! I'm ${this.name[0]}.`);
  },
};
```

---

### 2. Object Literals

- An **object literal** is an object written directly in your code, enclosed in `{ }`, with name/value pairs separated by commas and each name/value pair separated by a colon.
- The most common way to create a single object.
- Property values can be any type: strings, numbers, arrays, booleans, other objects, or functions.
- Best used when you need **one instance** of a structured data object (e.g., sending data to a server).

```js
// Object literal syntax
const objectName = {
  member1Name: member1Value,
  member2Name: member2Value,
};

// Shorthand method syntax (preferred over bio: function() {})
const person = {
  name: "Alice",
  greet() {             // ← shorthand method
    console.log("Hi!");
  },
};
```

---

### 3. Dot Notation — The Preferred Access Method

- Access properties and methods using a dot (`.`) between the object name and the member name.
- The **object name acts as a namespace** — it must come first.
- **Preferred** over bracket notation for its conciseness and readability.
- Can be **chained** to access nested object properties.

```js
person.age;           // access a property → 32
person.bio();         // call a method
person.name[0];       // access index inside an array property

// Nested object — chained dot notation
const person = {
  name: { first: "Bob", last: "Smith" },
};
person.name.first;    // → "Bob"
person.name.last;     // → "Smith"
```

---

### 4. Bracket Notation — Dynamic Property Access

- Access properties using `["propertyName"]` syntax — like accessing an array with an index, but with a string name.
- **Required** when the property name is stored in a variable (dot notation cannot use variables as property names — it only accepts literal names).
- Also required when a property name contains spaces or special characters.
- Objects are sometimes called **associative arrays** because of this — they map string keys to values just as arrays map number indexes to values.

```js
person["age"];             // same as person.age → 32
person["name"]["first"];   // same as person.name.first → "Bob"

// ✅ Bracket notation with a variable — only way to do this
function logProperty(propertyName) {
  console.log(person[propertyName]);  // propertyName is a variable
}
logProperty("name");  // → ["Bob", "Smith"]
logProperty("age");   // → 32

// ❌ Cannot use dot notation with a variable
console.log(person.propertyName);  // looks for literal member named "propertyName" → undefined
```

---

### 5. Setting (Creating and Updating) Object Members

- You can **update existing properties** using either dot or bracket notation and the assignment operator (`=`).
- You can also **add entirely new properties and methods** to an existing object after it was created.
- Bracket notation is needed to set a member whose name is held in a variable.

```js
// Updating existing members
person.age = 45;
person["name"]["last"] = "Cratchit";

// Adding brand new members
person["eyes"] = "hazel";                          // new property
person.farewell = function() { console.log("Bye!"); }; // new method

// Adding a member with a dynamic name (must use bracket notation)
const myDataName = "height";
const myDataValue = "1.75m";
person[myDataName] = myDataValue;  // equivalent to person["height"] = "1.75m"
person.height;  // → "1.75m"
```

---

### 6. The `this` Keyword

- Inside an object method, **`this`** refers to the **current object** the method was called on.
- Allows the same method definition to work correctly across multiple different objects — each object's `this` resolves to itself.
- Critical for constructors: when `new` is used, `this` is bound to the **newly created object**.

```js
const person1 = {
  name: "Chris",
  introduceSelf() {
    console.log(`Hi! I'm ${this.name}.`);
    //                        ↑ refers to person1
  },
};

const person2 = {
  name: "Deepti",
  introduceSelf() {
    console.log(`Hi! I'm ${this.name}.`);
    //                        ↑ refers to person2
  },
};

person1.introduceSelf();  // "Hi! I'm Chris."
person2.introduceSelf();  // "Hi! I'm Deepti."
// Same method code, different output — because 'this' adapts to the object
```

---

### 7. Constructors — Creating Multiple Objects from One Template

- When you need many objects of the same "shape", writing individual object literals is repetitive and unmanageable.
- A **constructor** is a function that acts as a template — called with the `new` keyword to produce new object instances.
- By convention, constructors are **capitalised** (e.g., `Person`, not `person`).

**What `new` does when calling a constructor:**
1. Creates a **new empty object**.
2. Binds **`this`** to that new object inside the constructor.
3. Runs the **constructor code** (assigning values via `this`).
4. **Returns the new object** automatically (no `return` statement needed).

```js
// Constructor definition — capitalised by convention
function Person(name) {
  this.name = name;
  this.introduceSelf = function() {
    console.log(`Hi! I'm ${this.name}.`);
  };
}

// Creating instances with 'new'
const salva   = new Person("Salva");
const frankie = new Person("Frankie");

salva.introduceSelf();    // "Hi! I'm Salva."
frankie.introduceSelf();  // "Hi! I'm Frankie."
```

---

### 8. Factory Function vs. Constructor (Two Approaches Compared)

Both produce objects with the same structure, but constructors are cleaner:

```js
// ── FACTORY FUNCTION (older, more verbose) ─────────────────────────
function createPerson(name) {
  const obj = {};            // manually create empty object
  obj.name = name;           // manually attach properties
  obj.introduceSelf = function() {
    console.log(`Hi! I'm ${this.name}.`);
  };
  return obj;                // manually return object
}
const salva = createPerson("Salva");

// ── CONSTRUCTOR (cleaner — 'new' handles create + attach + return) ──
function Person(name) {
  this.name = name;          // 'this' = new object (auto-created by 'new')
  this.introduceSelf = function() {
    console.log(`Hi! I'm ${this.name}.`);
  };
  // no return needed — 'new' returns 'this' automatically
}
const frankie = new Person("Frankie");
```

---

### 9. Everything Is (Essentially) an Object

- In JavaScript, **most things you have already used are objects** — you just didn't know it.
- Every string is an instance of `String` → has methods like `.split()`, `.toUpperCase()`.
- Every array is an instance of `Array` → has methods like `.push()`, `.join()`, `.map()`.
- `document` is an instance of `Document` → has methods like `.querySelector()`, `.createElement()`.
- `Math` is a built-in object → has methods like `Math.random()`, `Math.floor()`.
- Some objects (like `Notification`) require explicit instantiation with `new`.

```js
// You've been using object methods all along:
myString.split(",");                    // String object method
myArray.join(" ");                      // Array object method
document.querySelector("button");       // Document object method
Math.random();                          // Math object method

// Explicit instantiation required for some APIs:
const myNotification = new Notification("Hello!");
```

---

## Technical Deep-Dive

### Logic Walkthrough: The Full `person` Object — Anatomy

```js
const person = {
  //── PROPERTIES ────────────────────────────────────────────
  name: { first: "Bob", last: "Smith" }, // nested object
  age: 32,                               // number

  //── METHODS ───────────────────────────────────────────────
  bio() {
    // 'this.name' = the name object above (same object as 'person')
    // 'this.age'  = 32
    console.log(`${this.name.first} ${this.name.last} is ${this.age} years old.`);
  },

  introduceSelf() {
    console.log(`Hi! I'm ${this.name.first}.`);
  },
};

// Access patterns:
person.age;              // 32          — dot, simple property
person.name.first;       // "Bob"       — dot, chained (nested object)
person["age"];           // 32          — bracket, string key
person["name"]["first"]; // "Bob"       — bracket, chained

// Update:
person.age = 33;
person["name"]["last"] = "Jones";

// Add new:
person["hair"] = "brown";
person.wave = function() { console.log("👋"); };
```

---

### Logic Walkthrough: Why `this` Is Essential in Constructors

Without `this`, there's no way to make each instance hold its own data:

```js
function Person(name) {
  this.name = name;         // ← 'this' will be the specific new object
  this.greet = function() {
    console.log(`Hello, I'm ${this.name}`);
    //                          ↑
    // When salva.greet() runs: this = salva → "Hello, I'm Salva"
    // When deepti.greet() runs: this = deepti → "Hello, I'm Deepti"
  };
}

const salva  = new Person("Salva");   // new object: { name: "Salva", greet: fn }
const deepti = new Person("Deepti"); // new object: { name: "Deepti", greet: fn }

// The same function body produces personalised output
// because 'this' is bound differently for each instance
salva.greet();   // "Hello, I'm Salva"
deepti.greet();  // "Hello, I'm Deepti"
```

---

### Logic Walkthrough: Dot vs. Bracket — When Each Is Required

```js
const person = { name: "Bob", age: 32, "home town": "London" };

// ✅ Dot notation — simple, readable
person.name;       // "Bob"
person.age;        // 32

// ❌ Dot notation fails with spaces in property name
person.home town;  // SyntaxError

// ✅ Bracket notation — required for special characters
person["home town"]; // "London"

// ✅ Bracket notation — required when property name is in a variable
const field = "age";
person[field];        // 32
person.field;         // undefined (looks for a property literally named "field")

// ✅ Bracket notation — setting a member with a dynamic name
const customKey  = "nickname";
const customVal  = "Bobby";
person[customKey] = customVal;   // adds person.nickname = "Bobby"
person.nickname;                 // "Bobby"
```

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **Object** | A collection of related data and functionality, stored as named members (properties and methods) inside `{ }`. |
| **Object literal** | An object created by directly writing its contents in code using `{ key: value }` syntax. Not instantiated from a class or constructor. |
| **Property** | A member of an object whose value is data (a string, number, array, another object, etc.). |
| **Method** | A member of an object whose value is a function. Called using `objectName.methodName()`. |
| **Member** | Any name/value pair inside an object — the collective term for both properties and methods. |
| **Dot notation** | Accessing or setting an object member using a dot: `person.age`. Preferred for readability. Only works with literal property names. |
| **Bracket notation** | Accessing or setting an object member using square brackets and a string: `person["age"]`. Required when the property name is stored in a variable or contains special characters. |
| **Chaining** | Accessing a nested member by appending additional dot or bracket notation: `person.name.first`. |
| **Associative array** | An alternative name for an object, because it maps string keys to values in the same way arrays map numbers to values. |
| **`this`** | A keyword that, inside an object method, refers to the object the method was called on. In constructors, `this` refers to the new object being created. |
| **Constructor** | A function called with the `new` keyword that creates and returns a new object. By convention, constructors are capitalised (e.g., `Person`). |
| **`new`** | An operator used to call a constructor. It: (1) creates a new empty object, (2) binds `this` to it, (3) runs the constructor code, (4) returns the object. |
| **Instance** | A specific object created by a constructor. `const salva = new Person("Salva")` — `salva` is an instance of `Person`. |
| **Factory function** | A regular function that manually creates, populates, and returns an object. A precursor to constructors — more verbose, less conventional. |
| **Object scope** | Variables and methods defined inside an object are accessed via the object — they are not loose global variables. |
| **Namespace** | The object name serves as a namespace — `person.age` makes it clear `age` belongs to `person`, preventing conflicts with other `age` variables. |

---

## Watch Out For...

1. **Dot notation cannot use variables as property names.** `person.myVar` looks for a member literally called `myVar`, not for the member whose name is stored in `myVar`. Use `person[myVar]` when the name is dynamic.

2. **Methods need `this` to access sibling properties.** Inside a method, you cannot just write `name` or `age` — you must write `this.name` and `this.age`. Omitting `this` will cause a `ReferenceError` (if no global variable `name` exists) or silently access the wrong value.

3. **`new` must be used with constructors — calling without it won't create an instance.** `Person("Alice")` (without `new`) runs the function normally; `this` inside will refer to the global object (or be `undefined` in strict mode), and no new object is returned.

4. **Constructors should be capitalised — but this is a convention, not a rule.** JavaScript won't enforce it, but failing to capitalise signals to other developers that something is wrong and makes code harder to maintain.

5. **Shorthand method syntax vs. property + function.** `bio() { }` and `bio: function() { }` are equivalent — but the shorthand is preferred in modern JavaScript. Do not confuse the shorthand with an arrow function: `bio: () => { }` behaves differently with `this`.

6. **`const` objects are still mutable.** Declaring `const person = { }` prevents you from reassigning the variable (`person = somethingElse` throws an error), but you can still freely **add, update, or delete properties** on the object itself.

7. **Nested objects require chained access.** If `name` holds an object (`{ first: "Bob", last: "Smith" }`), you must use `person.name.first`, not `person.name` (which returns the whole nested object).

8. **Objects are passed by reference, not by value.** If you assign an object to a new variable (`const copy = person`), both variables point to the **same** object — modifying `copy.age` also changes `person.age`. To get a true independent copy, you need to clone the object.

9. **Forgetting `()` when calling a method.** `person.bio` is just a reference to the function; `person.bio()` actually calls it. Without parentheses, you get the function itself as a value — not its output.

10. **Methods defined with arrow functions do not bind their own `this`.** Arrow functions in object methods (`bio: () => { console.log(this.name) }`) will have `this` referring to the outer (usually global) scope — not the object. Always use regular functions or shorthand methods for object methods that use `this`.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** What is the difference between a **property** and a **method** in a JavaScript object? Give a code example of each.

**Q2.** When must you use **bracket notation** instead of **dot notation** to access an object property? Give two scenarios.

**Q3.** What does the `this` keyword refer to inside an object method? Write a short example demonstrating why `this` is necessary.

**Q4.** What are the **four things** that the `new` keyword does when used with a constructor?

**Q5.** The following code has a bug — the method doesn't correctly log the person's name. Identify the problem and fix it.
```js
const person = {
  name: "Alice",
  greet() {
    console.log(`Hello, I'm ${name}.`);
  },
};
person.greet();
```

---

## Answer Key

---

**A1.**
- **Property**: A member whose value is data. Can be a string, number, array, boolean, or even another object.
- **Method**: A member whose value is a function. Called with parentheses `()`.

```js
const car = {
  brand: "Toyota",   // ← PROPERTY — holds data
  drive() {          // ← METHOD — holds a function
    console.log("Vroom!");
  },
};

car.brand;   // "Toyota"  — accessing a property
car.drive(); // "Vroom!"  — calling a method
```

---

**A2.**
Two scenarios where bracket notation is **required**:

1. **When the property name is stored in a variable:**
```js
const field = "age";
person[field];    // ✅ reads the value of 'age' property
person.field;     // ❌ looks for a property literally called "field" → undefined
```

2. **When the property name contains special characters or spaces:**
```js
const obj = { "home town": "London" };
obj["home town"]; // ✅
obj.home town;    // ❌ SyntaxError
```

Bonus: bracket notation is also required when **dynamically setting a property name** (e.g., `person[myDataName] = value`).

---

**A3.**
Inside an object method, **`this`** refers to the **object the method was called on** — i.e., the object to the left of the dot at the time of the call.

**Why it's necessary:** Without `this`, there's no way for a method to refer to other members of its own object. You can't just write the variable's name because that variable is outside the method's scope.

```js
const person = {
  name: "Bob",
  introduceSelf() {
    // ✅ 'this.name' correctly refers to "Bob"
    console.log(`Hi! I'm ${this.name}.`);

    // ❌ 'name' without 'this' would try to find a global variable 'name'
    //    — not the object's property
  },
};

person.introduceSelf(); // "Hi! I'm Bob."
```

---

**A4.**
When `new` is used with a constructor, it does **four things** in order:

1. **Creates a new empty object** `{}`.
2. **Binds `this`** to that new empty object inside the constructor function.
3. **Runs the constructor code** — properties and methods are attached to `this` (the new object).
4. **Returns the new object** automatically — no explicit `return` statement is needed.

```js
function Person(name) {
  // At this point, 'this' is the new empty object
  this.name = name;          // Step 3: attach property
  this.greet = function() { console.log("Hi!"); }; // Step 3: attach method
  // Step 4: 'this' (the new object) is returned automatically
}

const salva = new Person("Salva");   // Step 1+2: new object created, this = it
// salva → { name: "Salva", greet: [Function] }
```

---

**A5.**
**Bug:** Inside the `greet()` method, `name` is written without `this`. JavaScript looks for a variable called `name` in the outer scope, not the object's `name` property. This produces either the wrong value (a global `name` variable) or an error.

**Fix:** Use `this.name` to refer to the object's own property:

```js
const person = {
  name: "Alice",
  greet() {
    console.log(`Hello, I'm ${this.name}.`);
    //                          ↑ 'this' refers to the 'person' object
  },
};

person.greet();  // ✅ "Hello, I'm Alice."
```
