# 📚 Object-Oriented Programming — Exam Study Guide
**Source:** [MDN Web Docs — Object-oriented programming](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object-oriented_programming)

---

## Executive Summary

This article introduces the foundational concepts of **class-based (classical) object-oriented programming (OOP)** — the style used by Java, C++, Python, and many other languages — and then contrasts it with how JavaScript handles OOP through its **prototype-based** model. The four concepts explained are: **classes**, **instances**, **inheritance**, and **encapsulation**. The critical exam insight is that JavaScript is *not* a classical OOP language at its core — it uses **prototype delegation** rather than copied class hierarchies — and while JavaScript's `class` syntax (covered in the next article) makes it *look* classical, the underlying mechanism is fundamentally different.

> **Note:** All code examples in this article are written in **pseudocode** — not real JavaScript. The actual JavaScript implementation is covered in the next article ("Classes in JavaScript").

---

## Core Pillars

### 1. What Is OOP?

Object-oriented programming is a **programming paradigm** that models a system as a **collection of objects**. Each object:
- Represents a particular **aspect** of the system.
- Contains both **data** (properties/state) and **functions** (methods/behaviour).
- Exposes a **public interface** to outside code.
- Maintains its own **private, internal state** — other parts of the system don't need to know how it works internally.

This separation of public interface from private implementation allows each object to be changed internally without breaking the code that uses it.

---

### 2. Classes and Instances

#### Class
A **class** is an abstract template or **blueprint** that defines:
- The **data properties** every object of this type will have.
- The **methods** every object of this type can perform.

A class by itself does nothing — it is a definition, not a living object.

```
class Professor
  properties
    name
    teaches
  methods
    grade(paper)
    introduceSelf()
```

#### Instance
An **instance** is a **concrete object** created from a class. Creating an instance is called **instantiation**, performed by a **constructor**.

```
class Professor
  properties
    name
    teaches
  constructor Professor(name, teaches)
  methods
    grade(paper)
    introduceSelf()
```

- The constructor has the **same name as the class**.
- It accepts parameters to initialise the new instance's internal state.
- The keyword **`new`** is used to signal that a constructor is being called.

```
walsh   = new Professor("Walsh",   "Psychology")
lillian = new Professor("Lillian", "Poetry")

walsh.teaches        // 'Psychology'
walsh.introduceSelf()// 'My name is Professor Walsh and I will be your Psychology professor.'

lillian.teaches        // 'Poetry'
lillian.introduceSelf()// 'My name is Professor Lillian and I will be your Poetry professor.'
```

- `walsh` and `lillian` are two separate **instances** of the `Professor` class.
- They share the same structure and methods but have **independent data** (`name`, `teaches`).

---

### 3. Inheritance

When multiple classes share common properties or behaviour, **inheritance** avoids duplication by extracting the shared parts into a **parent (super) class** and having specific classes **extend** it.

#### Without Inheritance — Problem

Both `Professor` and `Student` have `name` and `introduceSelf()`. Without inheritance, both classes define these separately — duplicating code.

#### With Inheritance — Solution

Extract shared features into a `Person` superclass:

```
class Person
  properties
    name
  constructor Person(name)
  methods
    introduceSelf()

class Professor : extends Person
  properties
    teaches
  constructor Professor(name, teaches)
  methods
    grade(paper)
    introduceSelf()     ← overrides Person's version

class Student : extends Person
  properties
    year
  constructor Student(name, year)
  methods
    introduceSelf()     ← overrides Person's version
```

- **`Person`** is the **superclass** / **parent class**.
- **`Professor`** and **`Student`** are **subclasses** / **child classes**.
- Both subclasses **inherit** `name` and the base `introduceSelf()` from `Person`, then **override** `introduceSelf()` with their own implementation.
- `Professor` adds `teaches` and `grade()`; `Student` adds `year`.

#### Demonstrating the Override

```
pratt   = new Person("Pratt")
walsh   = new Professor("Walsh",   "Psychology")
summers = new Student("Summers",   1)

pratt.introduceSelf()   // 'My name is Pratt.'
walsh.introduceSelf()   // 'My name is Professor Walsh and I will be your Psychology professor.'
summers.introduceSelf() // 'My name is Summers and I'm in the first year.'
```

The same method name (`introduceSelf`) produces **different behaviour** depending on the class — this is **polymorphism**.

---

### 4. Polymorphism

**Polymorphism** (literally "many forms") occurs when:
- Multiple classes define a **method with the same name**.
- Each class provides its **own implementation** of that method.
- The correct version is called automatically based on the **type of the object**.

When a subclass replaces a superclass method with its own implementation, the subclass is said to **override** the superclass method.

---

### 5. Encapsulation

**Encapsulation** is the practice of:
1. **Keeping an object's internal state private** — only the object's own methods can access or modify it.
2. **Exposing a clear public interface** — other code interacts with the object only through this interface.

#### The Problem Without Encapsulation

Suppose students can study archery only if they are in year 2 or above. Without encapsulation, external code checks `student.year` directly:

```
if (student.year > 1) {
  // allow the student into the class
}
```

**Problem:** If the rule changes (e.g., also requiring parental permission), every place in the codebase that performs this check must be found and updated.

#### The Solution With Encapsulation

Add a `canStudyArchery()` method to `Student` that centralises the logic:

```
class Student : extends Person
  properties
    private year
  constructor Student(name, year)
  methods
    introduceSelf()
    canStudyArchery() { return this.year > 1 }
```

```
if (student.canStudyArchery()) {
  // allow the student into the class
}
```

**Benefits:**
- The logic lives in **one place** — easy to update.
- `year` is marked **`private`** — external code cannot access it directly; only `Student`'s own methods can.
- Changing the internal logic requires updating only the `Student` class, not every consumer.

#### Access Control

In classical OOP languages (Java, C++), `private` is enforced by the compiler:

```
student = new Student('Weber', 1)
student.year  // ERROR: 'year' is a private property of Student
```

In languages without strict enforcement (e.g., older JS), developers used **naming conventions** like `_year` (underscore prefix) to signal "treat this as private."

---

### 6. OOP and JavaScript — How They Compare

JavaScript has constructors and prototypes that *relate* to OOP concepts, but with important differences from classical OOP.

#### Similarities

| Classical OOP Concept | JavaScript Equivalent |
|---|---|
| Class definition | Constructor function (or `class` syntax) |
| Instance creation | `new ConstructorFn()` |
| Shared methods | Methods on `Constructor.prototype` |
| Inheritance | Prototype chain (`Student.prototype` → `Person.prototype`) |

#### Key Differences

**Difference 1: No separate class/object distinction.**

In classical OOP, classes and objects are rigidly separate constructs. In JavaScript, you can create useful objects *without any class at all* — using an object literal or `Object.create()`. This makes JS objects much more lightweight.

**Difference 2: Prototype chain ≠ classical inheritance hierarchy.**

In classical OOP, when a subclass is instantiated, **a single object is created** that combines all properties from the entire hierarchy (child + parent + grandparent) into one flat object.

In JavaScript prototype chaining, **each level of the hierarchy is a separate object**, linked via `[[Prototype]]`. When you call a method on an instance, JS *delegates* the lookup up the chain — it doesn't copy properties down.

**Difference 3: Delegation vs. Inheritance.**

JavaScript's prototype model is more accurately described as **delegation** than inheritance:

> **Delegation:** When an object is asked to perform a task, it can either perform it itself or ask another object (its *delegate*) to perform it on its behalf.

Classical inheritance: Properties and methods are **copied** into each instance at creation time.

Prototype delegation: Properties and methods remain on the prototype; instances simply **reference** them and ask the prototype to handle them at lookup time.

**Delegation is more flexible than inheritance** because you can change or replace the delegate object at runtime.

---

## Technical Deep-Dive

### Logic Walkthrough: Building the Class Hierarchy in Pseudocode

**Scenario:** Model a school with `Person`, `Professor`, and `Student`.

**Step 1 — Identify shared properties:**
- Both professors and students have `name` and want to `introduceSelf()`.

**Step 2 — Create the superclass:**
```
class Person
  properties
    name
  constructor Person(name)
  methods
    introduceSelf()   // "My name is [name]."
```

**Step 3 — Create subclasses that extend Person:**
```
class Professor : extends Person
  properties
    teaches           // professor-specific
  constructor Professor(name, teaches)
  methods
    grade(paper)      // professor-specific
    introduceSelf()   // override: "My name is Professor [name] and I will be your [teaches] professor."
```

```
class Student : extends Person
  properties
    year              // student-specific
  constructor Student(name, year)
  methods
    introduceSelf()   // override: "My name is [name] and I'm in the [year] year."
    canStudyArchery() // { return this.year > 1 }
```

**Step 4 — Instantiate:**
```
walsh   = new Professor("Walsh",   "Psychology")  // has name, teaches, grade(), introduceSelf()
summers = new Student("Summers",   1)             // has name, year, introduceSelf(), canStudyArchery()
pratt   = new Person("Pratt")                     // has name, introduceSelf() only
```

**Polymorphism in action:**
- Calling `introduceSelf()` on any of these three objects works — but each produces different output.
- The code calling `introduceSelf()` doesn't need to know *which* type of object it has.

---

### Logic Walkthrough: Encapsulation — Before vs. After

**Before — logic scattered in caller code:**
```js
// Check 1: In the course registration module
if (student.year > 1) { registerForArchery(student); }

// Check 2: In the class scheduler module
if (student.year > 1) { addToSchedule(student, "archery"); }

// Check 3: In the admin dashboard
if (student.year > 1) { showArcheryButton(); }
```

**Problem:** Rules about archery eligibility are spread across the codebase. If the rule changes to `year > 1 AND hasParentalConsent`, all three locations must be updated — easy to miss one.

**After — logic encapsulated in the class:**
```
class Student : extends Person
  properties
    private year
    private hasParentalConsent
  methods
    canStudyArchery() {
      return this.year > 1 && this.hasParentalConsent
    }
```

```js
// Check 1: In course registration
if (student.canStudyArchery()) { registerForArchery(student); }

// Check 2: In class scheduler
if (student.canStudyArchery()) { addToSchedule(student, "archery"); }

// Check 3: In admin dashboard
if (student.canStudyArchery()) { showArcheryButton(); }
```

**Result:** The eligibility rule changed — only the `Student` class needed updating. All three callers automatically get the new behaviour.

---

### Logic Walkthrough: Delegation vs. Classical Inheritance

**Classical inheritance (Java/C++ mental model):**
```
When `new Professor("Walsh", "Psychology")` is created:
  → The runtime "flattens" the hierarchy:
  → The instance contains: { name, teaches, grade(), introduceSelf(), ... }
  → One flat object. All properties copied in.
```

**JavaScript prototype delegation:**
```
When `new Professor("Walsh", "Psychology")` is created:
  → walsh = { name: "Walsh", teaches: "Psychology" }   ← own properties only
  → walsh.__proto__ = Professor.prototype               ← linked to prototype
  → walsh.__proto__.__proto__ = Person.prototype        ← another link
  → walsh.__proto__.__proto__.__proto__ = Object.prototype

  When walsh.grade(paper) is called:
    → "Do I (walsh) have grade? No."
    → "Does Professor.prototype have grade? Yes → call it."
    → grade is never copied — it's found via delegation.
```

The prototype chain is a **linked list of objects**, not a flat copied structure. This has runtime implications: you can modify `Professor.prototype.grade` after instances are created, and all existing instances immediately reflect the change.

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **OOP (Object-Oriented Programming)** | A programming paradigm that models a system as a collection of interacting objects, each with its own data and behaviour. |
| **Class** | An abstract template/blueprint that defines the properties and methods every object of that type will have. |
| **Instance** | A concrete object created (instantiated) from a class; each instance has independent data but shares the class's methods. |
| **Constructor** | A special function called with `new` that initialises a new instance's internal state; typically named after the class. |
| **`new` keyword** | Signals construction of a new instance from a class/constructor function. |
| **Instantiation** | The process of creating a concrete instance from a class. |
| **Superclass / Parent class** | The class from which other classes inherit; contains shared properties and methods. |
| **Subclass / Child class** | A class that extends a superclass, inheriting its features and potentially adding or overriding them. |
| **Inheritance** | An OOP feature allowing a subclass to acquire the properties and methods of a superclass, enabling code reuse. |
| **`extends`** | Pseudocode/real keyword used to declare that one class inherits from another. |
| **Method overriding** | When a subclass defines a method with the same name as one in the superclass, replacing its behaviour for instances of the subclass. |
| **Polymorphism** | The ability for different classes to implement the same method name with different behaviour; code calling the method doesn't need to know the object's specific type. |
| **Encapsulation** | The practice of keeping an object's internal state private and exposing only a well-defined public interface. |
| **Private property** | A property marked so it can only be accessed by the object's own methods, not from outside code. |
| **Public interface** | The set of methods and properties an object exposes to external code; the "contract" for how to interact with the object. |
| **Class-based OOP (Classical OOP)** | The OOP style used by Java, C++, and Python, where classes and instances are distinct constructs and properties are inherited by copying. |
| **Prototype-based OOP** | JavaScript's OOP model, where inheritance is achieved through a chain of linked prototype objects rather than copying. |
| **Delegation** | A programming pattern where an object, instead of having a method itself, asks another object (its delegate) to perform a task on its behalf. Prototype chains implement delegation, not traditional inheritance. |
| **Pseudocode** | Language-agnostic, human-readable code notation used to describe algorithms and designs without being tied to any specific programming language syntax. |

---

## Watch Out For...

1. **JavaScript does not use classical OOP at its core.** The `class` keyword (next article) makes JavaScript *look* classical, but it is syntactic sugar over the prototype system. When you `new` a class in JS, you don't get a flattened copy of the hierarchy — you get an object linked to prototype chains.

2. **Classes are blueprints, not objects.** A class definition alone creates nothing you can use. You must call the constructor with `new` to create an actual instance. Confusing the class (the template) with its instances (the concrete objects) is a classic early error.

3. **Polymorphism requires the same method name, not the same implementation.** The power of polymorphism is that calling code can call `obj.introduceSelf()` without caring whether `obj` is a `Person`, `Professor`, or `Student`. The correct version runs automatically based on the actual type of the object.

4. **Overriding ≠ deleting.** When `Professor` overrides `introduceSelf()`, the `Person` version still exists on the parent class — other `Person` instances still use it. The override only affects `Professor` instances.

5. **Encapsulation is about access control, not just grouping.** Many beginners think encapsulation just means "putting related things in a class." True encapsulation means the internal state is *private* and can only be changed through the object's own methods. The `private` keyword (or equivalent) is what enforces this.

6. **JavaScript's prototype chain is delegation, not inheritance.** Methods are not copied to each instance — they are looked up on the prototype at call time. This means: (a) modifying a prototype method affects all existing instances immediately, and (b) the prototype chain is traversed at runtime, not baked in at instantiation.

7. **Underscore prefix (`_property`) is a convention, not enforcement.** In older JavaScript (before private class fields with `#`), `_year` was used to signal "don't access this externally." But nothing in the language actually prevents access. True private enforcement requires `#` (private class fields, covered in the `class` syntax article).

8. **Subclass constructors must handle parent properties.** In pseudocode, `Professor(name, teaches)` still passes `name` up to `Person`. In real languages this is done via `super(name)`. Forgetting to call the parent constructor means parent-managed properties aren't initialised.

9. **Not all languages use OOP.** OOP is one paradigm among several (functional, procedural, declarative). JavaScript is multi-paradigm — you don't have to use OOP in JS, and many modern JS codebases use functional patterns instead.

10. **Delegation is more flexible than classical inheritance.** Because prototype delegation resolves method calls at runtime, you can swap out or modify prototypes after creation. Classical inheritance is "baked in" at instantiation — you can't change which class an object belongs to at runtime.

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** Define in your own words: class, instance, constructor, and the relationship between them. Use a school domain example.

**Q2.** Explain inheritance using the `Person → Professor / Student` model. What does the superclass define? What do the subclasses add? What does "overriding" mean in this context?

**Q3.** What is polymorphism? Give a concrete example from the school model showing how three different objects can respond to the same method call differently.

**Q4.** What is encapsulation and why is it valuable? Use the archery registration scenario to illustrate the problem it solves and how it solves it.

**Q5.** The article says JavaScript's prototype chain is more like "delegation" than classical inheritance. Explain what this means. How does property lookup differ in JavaScript from classical inheritance, and why is delegation considered more flexible?

---

## Answer Key

---

**A1.**

- **Class:** An abstract blueprint that defines the *structure* (properties) and *behaviour* (methods) of a category of objects. Example: `Professor` defines that all professors have a `name`, a `teaches` subject, and can `grade(paper)` and `introduceSelf()`. The class itself is just a template — no actual professor exists yet.

- **Instance:** A concrete object created *from* a class. Example: `walsh = new Professor("Walsh", "Psychology")` creates a specific professor named Walsh who teaches Psychology. `walsh` is one instance; `lillian = new Professor("Lillian", "Poetry")` is a separate instance with different data.

- **Constructor:** The special initialisation function called when `new` is used. It receives arguments and uses them to set the instance's initial state. The constructor is typically named after the class: `Professor(name, teaches)` sets `this.name = name` and `this.teaches = teaches` on the new object.

- **Relationship:** The class *describes* what a professor is; the constructor *creates* one; instances are the resulting live objects that exist in memory with their own data.

---

**A2.**

**Inheritance in the school model:**

The superclass `Person` defines what *all people* have in common: a `name` property and an `introduceSelf()` method. `Professor` and `Student` are subclasses that `extend Person` — meaning they automatically inherit `name` and the base `introduceSelf()`.

Each subclass then **adds** its own unique properties:
- `Professor` adds `teaches` and a `grade(paper)` method.
- `Student` adds `year` and a `canStudyArchery()` method.

Each subclass also **overrides** `introduceSelf()` with its own implementation because while all people introduce themselves, the format differs:
- `Person`: "My name is Pratt."
- `Professor`: "My name is Professor Walsh and I will be your Psychology professor."
- `Student`: "My name is Summers and I'm in the first year."

**Overriding** means the subclass defines a method with the *same name* as the parent, replacing the parent's version for instances of that subclass. The parent's version still exists and is still used by base `Person` instances.

---

**A3.**

**Polymorphism** = same method name, different implementations, correct version called automatically.

```
pratt   = new Person("Pratt")
walsh   = new Professor("Walsh", "Psychology")
summers = new Student("Summers", 1)

pratt.introduceSelf()
// "My name is Pratt."            ← Person's version

walsh.introduceSelf()
// "My name is Professor Walsh and I will be your Psychology professor."   ← Professor's version

summers.introduceSelf()
// "My name is Summers and I'm in the first year."   ← Student's version
```

All three objects respond to `introduceSelf()`. Calling code can treat them all as "things that can introduce themselves" without knowing the specific type. If you had an array `[pratt, walsh, summers]` and iterated calling `introduceSelf()` on each, each would automatically use the correct version. This is the core power of polymorphism — decoupling callers from specific types.

---

**A4.**

**Encapsulation** is the practice of hiding internal state (making it *private*) and exposing only a well-defined public interface (methods) through which state can be changed or queried.

**The problem (no encapsulation):**
The eligibility logic `student.year > 1` is scattered across multiple places in the codebase — course registration, the scheduler, the admin dashboard. When the rule changes to "year > 1 AND has parental consent," every location must be found and updated. Missing even one creates an inconsistent system.

**The solution (with encapsulation):**
`Student` gets a `canStudyArchery()` method that contains the rule. `year` is marked `private` so external code cannot read it directly. All callers now simply call `student.canStudyArchery()` — they don't depend on the internal `year` value at all.

**Value:**
- Rules are centralised in one place — easy to update consistently.
- The internal data (`year`) is protected — callers can't accidentally depend on its raw value.
- Changing the implementation (e.g., adding `hasParentalConsent`) requires no changes to any calling code — they all still call `canStudyArchery()` and get the correct result automatically.

---

**A5.**

**Classical inheritance (Java/C++ model):**
When a `Professor` is instantiated, all properties from the full hierarchy (`Person` + `Professor`) are **assembled into one flat object**. The instance contains copies of everything — it never needs to consult the parent class again. Properties are baked in at creation time.

**JavaScript prototype delegation:**
When a JS `Professor` instance is created, it contains **only its own properties** (e.g., `name`, `teaches`). Methods like `grade()` or `introduceSelf()` remain on `Professor.prototype` and `Person.prototype` — separate objects linked in a chain. When you call `walsh.grade(paper)`, JavaScript:
1. Looks for `grade` on `walsh` itself — not found.
2. Looks on `walsh`'s prototype (`Professor.prototype`) — found. Calls it.

This is **delegation**: `walsh` asks its prototype to handle the task.

**Why delegation is more flexible:**
- You can **modify a prototype at runtime** and all existing instances immediately see the change. In classical inheritance, instances are already "baked" and cannot be updated this way.
- You can **replace the delegate entirely** at runtime — swapping out the prototype object. This would be impossible in classical inheritance where the lineage is fixed at instantiation.
- JS objects can even have their prototype changed after creation using `Object.setPrototypeOf()` — something that isn't possible in strictly class-based languages.
