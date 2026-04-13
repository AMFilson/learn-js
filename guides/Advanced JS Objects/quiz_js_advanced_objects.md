# 🧠 Practice Quiz: Advanced JS Objects

## Section 1: Prototypes & The Prototype Chain

### Question 1: The Core Mechanism of Inheritance

What is the primary mechanism by which JavaScript objects inherit features from one another?

- A) Class-based copying
- B) Prototypes and the Prototype Chain
- C) Function cloning
- D) Variable shadowing

<details>
<summary><b>Hint</b></summary>
Even though modern JavaScript uses the `class` keyword, underlyingly it still uses a system of "links" between objects.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** JavaScript inheritance is prototype-based. Every object has a link to another object (its prototype), forming a chain. When a property is accessed, JavaScript searches this chain rather than copying features from a blueprint to an instance.
- **Why A is incorrect:** While JavaScript has `class` syntax, it is "syntactic sugar" over the existing prototype system; it does not perform class-based copying like Java or C++.
- **Why C/D are incorrect:** These are either non-existent concepts (function cloning) or specific behaviors (shadowing) rather than the foundational mechanism.
</details>

---

### Question 2: The Property Lookup Sequence

What happens if you try to access `myObj.greet()` and `greet` is not defined on `myObj`?

- A) The browser throws an immediate `ReferenceError`.
- B) JavaScript returns `null`.
- C) JavaScript checks the prototype of `myObj` for the `greet` method.
- D) The global `window` object is searched for a function named `greet`.

<details>
<summary><b>Hint</b></summary>
JavaScript doesn't give up immediately when a property is missing on an object. It looks at the "parent" object in the chain first.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** This is the definition of the prototype chain. If a property is not an "own property" of the object, JavaScript moves up the chain to the object's prototype. It repeats this until the property is found or the chain ends at `null`.
- **Why A is incorrect:** A `ReferenceError` only happens if you try to access a variable that hasn't been declared, not a missing property on an existing object.
- **Why B is incorrect:** JavaScript returns `undefined` (not `null`) if the property is never found on the entire chain.
- **Why D is incorrect:** The global object is not part of the standard prototype chain for plain objects.
</details>

---

### Question 3: Identifying the Root Prototype

Which object serves as the "end of the chain" for almost all plain JavaScript objects?

- A) `Function.prototype`
- B) `Array.prototype`
- C) `Object.prototype`
- D) `null`

<details>
<summary><b>Hint</b></summary>
While the chain *ends* at a specific primitive value, there is a common object sitting right before that final step.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `Object.prototype` is the root prototype. It provides basic methods like `toString()` and `hasOwnProperty()` to nearly all objects.
- **Why D is incorrect:** While the chain terminates at `null`, `Object.prototype` is the final object *before* that termination. The question asks for the object, not the terminator value.
- **Why A/B are incorrect:** These are intermediate prototypes for functions and arrays, but they themselves eventually link back to `Object.prototype`.
</details>

---

### Question 4: Accessing an Object's Prototype

What is the standard, modern method to retrieve the prototype of an existing object `myObj`?

- A) `myObj.prototype`
- B) `myObj.__proto__`
- C) `Object.getPrototypeOf(myObj)`
- D) `Object.prototypeOf(myObj)`

<details>
<summary><b>Hint</b></summary>
Be careful: `prototype` is a property found on *functions*, not instances. `__proto__` is legacy. There's a static method on the `Object` constructor.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** `Object.getPrototypeOf(obj)` is the official ECMAScript standard method for accessing the hidden `[[Prototype]]` link of an object.
- **Why A is incorrect:** `.prototype` is a property found only on function objects (like constructors). It is used to *set* the prototype of future instances, but is not the prototype of the instance itself.
- **Why B is incorrect:** While widely supported, `__proto__` is a legacy accessor property and is considered non-standard in modern production code.
- **Why D is incorrect:** This is a fictitious method name.
</details>

---

### Question 5: Understanding Property Shadowing

What is specifically occurring in the following code?

```js
const d = new Date();
d.getTime = function() { return "Hack!"; };
console.log(d.getTime()); // "Hack!"
```

- A) The `Date` prototype's `getTime` method has been permanently deleted.
- B) This is "shadowing"—the own property on `d` takes precedence over the inherited one.
- C) This throws a `TypeError` because built-in methods are read-only.
- D) All `Date` objects created after this will now return "Hack!".

<details>
<summary><b>Hint</b></summary>
Did we change the "blueprint" of all Dates, or just this one specific "car" (instance)?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Shadows happen when an object defines a property with the same name as one on its prototype. Because lookup starts at the object itself, the own property is found first and the prototype's version is "shadowed" (hidden).
- **Why A is incorrect:** The prototype's version still exists; it can be restored by running `delete d.getTime`.
- **Why C is incorrect:** Most prototype methods are not read-only by default on instances.
- **Why D is incorrect:** Only the specific instance `d` was modified.
</details>

---

### Question 6: Using `Object.create()`

What does the command `const newObj = Object.create(myProto)` do?

- A) It copies all properties from `myProto` into `newObj`.
- B) It creates a new object and sets its internal prototype to `myProto`.
- C) It converts `myProto` into a constructor function.
- D) It checks if `newObj` is a child of `myProto`.

<details>
<summary><b>Hint</b></summary>
This method is a way to set up inheritance manually without using a constructor function or `new` keyword.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `Object.create(proto)` is a fundamental method that creates a new, empty object and directly links its `[[Prototype]]` to the `proto` argument. No constructor logic is run.
- **Why A is incorrect:** It does not copy properties; it creates a link so properties are accessed via the prototype chain.
- **Why C/D are incorrect:** These describe completely different features of the language.
</details>

---

### Question 7: Constructors and the `prototype` Property

When you run `const user = new Person("Bob")`, where does the browser look to find the prototype for the `user` object?

- A) `Person.prototype`
- B) `Person.__proto__`
- C) `user.prototype`
- D) `Object.Person`

<details>
<summary><b>Hint</b></summary>
The "blueprint" object for instances of a constructor is stored on a specific property of the *constructor function* itself.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** A

**Rationale:**

- **Why A is optimal/correct:** Every function has a `prototype` property. When a function is called as a constructor (with `new`), this specific property acts as the "source" for the prototype link of the new instance.
- **Why B is incorrect:** `Person.__proto__` is the prototype of the function itself (usually `Function.prototype`), not the prototype of its instances.
- **Why C is incorrect:** Ordinary objects (like `user`) do not have a `.prototype` property; only functions do.
</details>

---

### Question 8: Own Properties vs. Inherited Properties

Which method should you use to check if a property `name` exists directly on an object `obj` and was **not** inherited from the prototype chain?

- A) `"name" in obj`
- B) `Object.hasOwn(obj, "name")`
- C) `obj.isPrototypeOf("name")`
- D) `obj.prototype.includes("name")`

<details>
<summary><b>Hint</b></summary>
There's an operator (`in`) that checks the *whole* chain, and a static method that checks *only* the specific object.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `Object.hasOwn(obj, prop)` is the modern, standard static method for checking "own properties." It returns true only if the property was defined on that specific object.
- **Why A is incorrect:** The `in` operator returns true if the property exists anywhere in the object's entire prototype chain (inherited or not).
- **Why C/D are incorrect:** These are misuses of the `isPrototypeOf` method or fictitious syntax.
</details>

---

### Question 9: Memory Efficiency of Prototypes

Why is it generally better to put a method like `greet()` on `Person.prototype` rather than inside the `Person` constructor via `this.greet = ...`?

- A) Prototype methods run faster.
- B) It prevents the `this` keyword from changing value.
- C) It saves memory because the function is shared by all instances instead of being redefined for each one.
- D) Methods inside constructors cannot access private data.

<details>
<summary><b>Hint</b></summary>
If you create 1,000 instances, do you want 1,000 copies of the exact same function code in memory, or just one reference?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** This is a major engineering benefit of prototypes. Methods on the prototype exist in only one place in memory. Every instance simply "references" that one version. Putting it in the constructor creates a new unique function object for every single instance, which is wasteful for large numbers of objects.
- **Why A/B/D are incorrect:** These are not technical benefits of prototype delegation; they are either false or unrelated to the scope of prototypes.
</details>

---

### Question 10: Prototype of Protoypes (The Chain Termination)

What is the result of `Object.getPrototypeOf(Object.prototype)`?

- A) `Object.prototype`
- B) `undefined`
- C) `null`
- D) `ReferenceError`

<details>
<summary><b>Hint</b></summary>
The prototype chain must end somewhere to prevent an infinite lookup loop.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The root prototype, `Object.prototype`, has no prototype of its own. Its internal `[[Prototype]]` link is set to `null`, marking the definitive end of the prototype chain.
- **Why B is incorrect:** JavaScript property lookup returns `undefined` for properties, but the *link* itself is set to `null`.
- **Why A/D are incorrect:** This would either cause an infinite loop or throw an error for a standard, valid check.
</details>

---

## Section 2: OOP Principles & Delegation

### Question 11: Classes vs. Instances

In object-oriented programming, what is the best description of the relationship between a **class** and an **instance**?

- A) A class is a specific object, and an instance is its name.
- B) A class is a blueprint/template, and an instance is a concrete object created from that blueprint.
- C) They are the same thing; the terms are used interchangeably.
- D) An instance is a parent, and a class is its child.

<details>
<summary><b>Hint</b></summary>
Think of a cookie cutter and a cookie. Which one is the "definition" and which one is the "result"?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** A **class** defines the structure (properties) and behavior (methods) that all objects of that type will share, but it contains no data itself. An **instance** is an actual object in memory created using that class, containing its own specific data.
- **Why A is incorrect:** This reverses the concepts; the instance is the specific object.
- **Why C is incorrect:** They are fundamentally different; one is a definition and the other is an implementation.
- **Why D is incorrect:** This confuses instantiation with inheritance.
</details>

---

### Question 12: The Purpose of Inheritance

What is the primary technical motivation for using **inheritance** (subclasses extending superclasses)?

- A) To make the code run faster in the browser.
- B) To ensure that all objects have different method names.
- C) To avoid code duplication by sharing common features in a parent class.
- D) To prevent the use of the `new` keyword.

<details>
<summary><b>Hint</b></summary>
If both "Student" and "Professor" classes need a `name` and an `introduceSelf()` method, where should you put that code to avoid writing it twice?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** Inheritance allows multiple specific classes (subclasses) to "extend" a general class (superclass). This means you only have to write and maintain the shared code (like a `Person` class's `name` property) once.
- **Why A is incorrect:** Inheritance is a code-organization tool; it doesn't inherently increase execution speed (and can theoretically be slightly slower due to chain lookups).
- **Why B is incorrect:** Inheritance actually encourages objects to have the *same* method names (polymorphism).
- **Why D is incorrect:** Inheritance still relies heavily on constructors and the `new` keyword.
</details>

---

### Question 13: Defining Polymorphism

A `Person` class has an `introduceSelf()` method. Both `Student` and `Professor` subclasses provide their own unique versions of `introduceSelf()`. What is this concept called?

- A) Encapsulation
- B) Shadowing
- C) Polymorphism
- D) Instantiation

<details>
<summary><b>Hint</b></summary>
The word literally means "many forms." One method name, many different behaviors.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** **Polymorphism** allows different types of objects to be treated as the same general type. When you call `.introduceSelf()`, the system automatically picks the correct version based on the specific type of object (Student or Professor) without the caller needing to know the difference.
- **Why A is incorrect:** Encapsulation is about hiding internal state, not varying method behavior.
- **Why B is incorrect:** While "shadowing" is the technical mechanism in JavaScript prototypes that *enables* this, "Polymorphism" is the higher-level OOP principle being described.
- **Why D is incorrect:** Instantiation is simply the act of creating an object.
</details>

---

### Question 14: Encapsulation and Data Protection

Which of the following scenarios best demonstrates the benefit of **Encapsulation**?

- A) Storing a user's password in a global variable so every function can see it.
- B) Making an object's `age` property private and providing a `birthday()` method to update it correctly.
- C) Creating a constructor that accepts 10 different arguments.
- D) Using an object literal instead of a class.

<details>
<summary><b>Hint</b></summary>
Encapsulation is about "hiding the guts." If you want to make sure an `age` can't accidentally be set to -500, how should you control access to it?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Encapsulation involves hiding the internal data (properties) and exposing only a "public interface" (methods). By making `age` private, you prevent outside code from setting invalid values. The logic stays inside the object where it belongs.
- **Why A is incorrect:** This is the opposite of encapsulation; global variables break security and modularity.
- **Why C/D are incorrect:** These are standard programming tasks but don't specifically relate to the principle of data hiding or interface design.
</details>

---

### Question 15: Delegation vs. Inheritance

The study guide notes that JavaScript's prototype model is more accurately described as **Delegation** than classical "copy-based" inheritance. Why?

- A) Because JavaScript copies all properties into the child object at runtime.
- B) Because an instance "asks" its prototype to perform a task it cannot do itself.
- C) Because JavaScript doesn't support the `extends` keyword.
- D) Because delegation is an older, less efficient way to handle objects.

<details>
<summary><b>Hint</b></summary>
In Java, a child object contains its own copies of all parent features. In JS, the features stay on the prototype, and the child just has a link or "reference" to them.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** In classical inheritance, properties are *copied* to the new object. In JavaScript, they are not. Instead, if an object doesn't have a method, it **delegates** the search to its prototype. The method actually runs on the prototype object while `this` points to the instance.
- **Why A is incorrect:** This describes classical inheritance, which JS does *not* do.
- **Why C is incorrect:** JavaScript *does* support `extends` in its `class` syntax.
- **Why D is incorrect:** Delegation is actually considered more flexible because you can change an object's behavior at runtime by modifying its prototype.
</details>

---

### Question 16: The Public Interface

In the context of Encapsulation, what is a **Public Interface**?

- A) The physical monitor the user looks at.
- B) The set of methods and properties an object makes available for other parts of the program to use.
- C) A special type of class that has no properties.
- D) The HTML code that displays the object's data.

<details>
<summary><b>Hint</b></summary>
If you think of a car, the "interface" is the steering wheel and pedals. You don't need to know how the engine works to use them.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** The public interface is the "contract" between the object and the rest of the world. It consists of the methods you call to interact with the object's hidden internal state.
- **Why A/D are incorrect:** These confuse programming interfaces with user interfaces (UI).
- **Why C is incorrect:** This is a misunderstanding of the term "interface" which exists as a specific keyword in some other languages, but for JS objects, it refers to the available methods.
</details>

---

### Question 17: Method Overriding

What is the effect of **Method Overriding** in a subclass?

- A) It deletes the method from the parent class entirely.
- B) It allows the subclass to provide a specific implementation of a method that is already defined in its parent class.
- C) It prevents the subclass from inheriting any other features from the parent.
- D) It causes a syntax error if the names match.

<details>
<summary><b>Hint</b></summary>
A `Professor` class is a `Person`. Both have `introduceSelf()`. If `Professor` defines its own `introduceSelf()`, does it "break" the `Person` class or just "change" the behavior for Professors?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** Overriding is a key part of inheritance and polymorphism. It lets a subclass refine a behavior for its specific needs (e.g., a `Professor`'s introduction includes their subject) while still using the same method name.
- **Why A is incorrect:** The parent class method remains unchanged for other instances.
- **Why C/D are incorrect:** These are incorrect assertions about how inheritance works.
</details>

---

### Question 18: Identifying the Constructor

In OOP theory, what is the specific role of a **Constructor**?

- A) To delete an object when it is no longer needed.
- B) To define the CSS styles for an object.
- C) To initialize a new instance's data (state) when it is first created.
- D) To prevent other objects from inheriting properties.

<details>
<summary><b>Hint</b></summary>
The constructor is the function that runs at the exact moment you use the `new` keyword.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** A constructor's job is to set up the starting data for an object. It typically accepts parameters and assigns them to the new object (e.g., `this.name = name`).
- **Why A is incorrect:** That is the role of a "destructor," which JavaScript handles automatically via garbage collection.
- **Why B/D are incorrect:** These are unrelated to the technical purpose of a constructor.
</details>

---

### Question 19: Private Properties by Convention

Before JavaScript introduced formal private properties (like `#name`), developers used a **naming convention** to signal that a property should be treated as private. What was this common convention?

- A) ALL_CAPS_NAMES
- B) name$ (ending with a dollar sign)
- C) _name (starting with an underscore)
- D) name! (ending with an exclamation point)

<details>
<summary><b>Hint</b></summary>
You might see code like `this._age = 20`. The prefix doesn't actually stop you from accessing it, but it warns other developers, "Don't touch this!"
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The underscore prefix (`_`) was the universal signifier in the JS community for a "private" or "internal" property. While the language didn't enforce it, developers agreed not to access such properties directly from outside the class.
- **Why A is incorrect:** All caps is typically used for constants (e.g., `MAX_SPEED`).
- **Why B/D are incorrect:** These were never standard community conventions for privacy.
</details>

---

### Question 20: The Power of OOP Paradigms

Which of the following is considered a major benefit of using the OOP paradigm?

- A) It makes every line of code shorter.
- B) It allows you to model complex real-world systems as discrete, manageable "things" (objects).
- C) It removes the need for `if/else` statements.
- D) It ensures that only one person can work on the code at a time.

<details>
<summary><b>Hint</b></summary>
Think about building a game with characters, weapons, and levels. Is it easier to manage as a giant list of variables or as a collection of "Player" and "Enemy" objects?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** OOP is an "organizational" paradigm. By breaking a large, messy system into self-contained objects that know how to manage their own data, programs become easier to understand, debug, and expand.
- **Why A is incorrect:** OOP often adds boilerplate (class definitions, constructors), so it rarely makes code "shorter" in terms of line count.
- **Why C/D are incorrect:** These are false claims; logic blocks like `if/else` are still essential, and OOP actually makes teamwork *easier* by separating code into modules.
</details>

---

## Section 3: Classes & Practical Application

### Question 21: The `class` Keyword Reality

Which statement best describes what the `class` keyword actually does in JavaScript?

- A) It introduces a new engine that ignores prototypes.
- B) It is "syntactic sugar" that makes writing prototype-based inheritance cleaner and easier to read.
- C) It converts JavaScript into a strictly typed language like Java.
- D) It prevents objects from being created with literals.

<details>
<summary><b>Hint</b></summary>
If you check `typeof MyClass`, it returns "function." If you check an instance's prototype, it's still there. What does that tell you?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** JavaScript classes do not change how the language works internally. Under the hood, they still use the same constructor functions and prototype chains. The `class` syntax is simply a "sweeter" (cleaner) way for developers to write the same logic.
- **Why A is incorrect:** The prototype system is still the foundation; classes rely on it to work.
- **Why C is incorrect:** JavaScript remains a dynamically typed language; `class` has no effect on type safety.
- **Why D is incorrect:** Object literals (`{}`) are still valid and widely used alongside classes.
</details>

---

### Question 22: Inheritance with `extends` and `super()`

In a subclass constructor, what is the strict rule regarding the `super()` call?

- A) It is optional and only needed if the parent has no constructor.
- B) It must be called at the very end of the constructor.
- C) It must be called **before** you can use the `this` keyword.
- D) It should be called instead of the `constructor()` name.

<details>
<summary><b>Hint</b></summary>
If you try to set `this.myProp = 10` before calling `super()`, JavaScript will throw a `ReferenceError`. Why?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** When a class extends another, the subclass constructor must call `super()` to initialize the parent part of the object. Until `super()` is finished, the `this` object is not considered "born" in the subclass, so any attempt to use it will fail.
- **Why A is incorrect:** If you have a constructor in a subclass, `super()` is mandatory.
- **Why B/D are incorrect:** These are incorrect syntax rules.
</details>

---

### Question 23: Genuine Private Fields

Which of the following is the correct syntax for declaring a truly private field that cannot be accessed from outside the class?

- A) `this._name = name;`
- B) `private name;`
- C) `#name;`
- D) `hidden name;`

<details>
<summary><b>Hint</b></summary>
JavaScript recently added a specific character prefix that the engine uses to block external access.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The hash symbol (`#`) is the official ES2022+ syntax for private class fields. These fields must be declared at the top of the class body and are enforced by the JavaScript engine—accessing them from outside results in a `SyntaxError`.
- **Why A is incorrect:** The underscore (`_`) is a naming convention but does not actually prevent access.
- **Why B/D are incorrect:** These keywords exist in other languages but are not valid JavaScript for private members.
</details>

---

### Question 24: Methods in Class Bodies

When you define a method inside a class body (e.g., `greet() { ... }`), where is that function physically stored in memory?

- A) On every individual instance of the class.
- B) On the class's `prototype` object.
- C) In the global `window` scope.
- D) Inside the constructor function only.

<details>
<summary><b>Hint</b></summary>
Recall the memory efficiency of prototypes. Do we want 100 copies of a function, or 100 links to one shared function?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** This is how classes maintain the efficiency of the prototype system. All methods declared in the class body are added to the class's `.prototype`. When an instance calls the method, it finds it there via delegation.
- **Why A is incorrect:** Copying methods to every instance is what happens when you define them inside the constructor via `this.method = ...`, but not when using standard class method syntax.
- **Why C/D are incorrect:** These are incorrect locations for class method storage.
</details>

---

### Question 25: Canvas Context Retrieval

When building a graphical application like "Bouncing Balls," what does `const ctx = canvas.getContext("2d")` provide?

- A) A reference to the HTML `<canvas>` element itself.
- B) The CSS styles of the drawing surface.
- C) The "drawing context"—the object used to issue actual drawing commands (like `arc` or `fill`).
- D) The pixel data of the entire computer screen.

<details>
<summary><b>Hint</b></summary>
The `canvas` is the paper, but `ctx` is the "hand" holding the "pen" that does the actual work.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** The `canvas` element is just a container. To actually draw, you must get its "context." For 2D games and simulations, the `2d` context provides a specialized object (`ctx`) that contains all the methods for drawing shapes, text, and images.
- **Why A is incorrect:** That is what the `canvas` variable holds, not `ctx`.
- **Why B/D are incorrect:** These are not what the drawing context is responsible for.
</details>

---

### Question 26: Positioning on a Canvas

In the "Bouncing Balls" exercise, why do boundary checks use `this.x + this.size` instead of just `this.x` when checking if a ball hit the right wall?

- A) Because the `x` coordinate represents the top-left corner of the ball.
- B) Because `x` is the center of the ball, and we must account for the radius (`size`) to see if the edge touched the wall.
- C) Because the canvas is 10 pixels wider than the window.
- D) To prevent the ball from moving too fast.

<details>
<summary><b>Hint</b></summary>
Think about a circle. If the center is exactly at the edge of the screen, where is the other half of the circle?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** When drawing with `ctx.arc()`, the coordinates provided are for the **center** of the circle. If you only checked `this.x >= width`, the ball's center would reach the wall before it bounced, meaning half the ball would have already disappeared off-screen.
- **Why A is incorrect:** Rectangles use top-left coordinates, but arcs use center coordinates.
- **Why C/D are incorrect:** These are irrelevant to the geometry of the ball's position.
</details>

---

### Question 27: The Animation Loop Pattern

What is the advantage of using `requestAnimationFrame(loop)` over `setInterval(loop, 16)` for a smooth animation?

- A) It is easier to write.
- B) It automatically pauses the animation when the user switches to a different browser tab.
- C) It allows the code to run in the background even if the browser is closed.
- D) It doubles the speed of the JavaScript execution engine.

<details>
<summary><b>Hint</b></summary>
One of these is a "dumb" timer, while the other is "synchronized" with the display's own refresh cycle.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**

- **Why B is optimal/correct:** `requestAnimationFrame` is highly optimized. It tries to synchronize with the screen's refresh rate (usually 60fps) and, crucially, it stops calling the function when the tab is hidden, saving battery and CPU. `setInterval` will keep running regardless, wasting resources.
- **Why A is incorrect:** The syntax is slightly more complex as it requires recursion.
- **Why C/D are incorrect:** These are technically impossible or false claims.
</details>

---

### Question 28: Collision Detection Logic

In the formula `distance < this.size + ball.size`, what physical state is being mathematically detected?

- A) Two circles are exactly 100 pixels apart.
- B) Two circles are moving in the same direction.
- C) The edges of two circular objects are overlapping or touching.
- D) One circle is significantly larger than the other.

<details>
<summary><b>Hint</b></summary>
If the distance between two centers is exactly equal to the sum of their radii, they are touching perfectly. What if the distance is *less*?
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** This is the standard "Circle-Circle Collision" algorithm. If the straight-line distance between two centers is less than the sum of their two radii, there is no possible way for them *not* to be overlapping.
- **Why A/B/D are incorrect:** The formula does not measure speed, relative size, or fixed pixel distances.
</details>

---

### Question 29: The Purpose of `ctx.beginPath()`

What happens if you forget to include `ctx.beginPath()` at the start of your `draw()` method inside the animation loop?

- A) The ball will not be drawn at all.
- B) The canvas will turn completely black.
- C) Every previous frame's path will be "remembered" and redrawn, creating a massive performance lag and visual mess.
- D) The ball will always stay at coordinates (0, 0).

<details>
<summary><b>Hint</b></summary>
The "path" is a list of coordinates that the canvas "remembers" until you tell it to start a new list.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** Without `beginPath()`, the new circle path is just added onto the existing list of paths. Every time `ctx.fill()` is called, the browser attempts to re-fill every single circle ever drawn in that session. This quickly becomes a huge rendering burden and causes "streaking" artifacts.
- **Why A/B/D are incorrect:** The drawing still happens, but it happens incorrectly and with excessive overhead.
</details>

---

### Question 30: Pythagorean Theorem in Gaming

Which part of the following collision detection code represents the Pythagorean Theorem?

`const distance = Math.sqrt(dx * dx + dy * dy);`

- A) `Math.sqrt`
- B) `dx * dx + dy * dy`
- C) The entire line calculating the `distance`
- D) The `const` keyword

<details>
<summary><b>Hint</b></summary>
Remember `a² + b = c²`? To find the "c" (the hypotenuse or distance), you take the square root of the sum of the squares of the sides.
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** C

**Rationale:**

- **Why C is optimal/correct:** To find the distance between two points in 2D space, you treat the horizontal shift (`dx`) and vertical shift (`dy`) as the sides of a right-angled triangle. The distance is the hypotenuse. The formula `√(dx² + dy²)` is the direct application of the Pythagorean theorem.
- **Why A/B are only parts of the formula:** They are components, but "the theorem" as used for distance is the complete calculation.
- **Why D is incorrect:** `const` is just a variable declaration keyword.
</details>
