/* You can use node.js to run javascript code on your pc/backend */
console.log("Hello world from node.js");

/* You can run code in the terminal by navingating to
the same directory as the script you wish to run
then using the command

"node .\insertscriptname.js"*/

/* You wont be referring to any html file this way
so remember this otherwise you may get reference errors
when you try to run code that refers to the DOM */

// A single line comment
/* A multi-line comment */

/* Console messages are printed to the terminal when run in
the backend */
/* console.log is just a normal logging message */
console.log("This is a logging message");
/* console.error is for logging errors */
console.error("This is an error message");
/* console.warn is for logging warnings */
console.warn("This is a warning message");
/* console.info is for logging information */
console.info("This is an information message");
/* console.table is for logging tables */
console.table({ name: "John", age: 30, city: "New York" });
/* console.group is for grouping messages */
console.group("My Group");
console.log("Message 1");
console.log("Message 2");
console.groupEnd();
/* console.time is for timing code */
console.time("My Timer");
console.timeEnd("My Timer");
/* You have to add both liness of code for the timer to work */

/* You can declare variables in js using keyword const */
const variableName = 64;
/* To do formatted console outputs you use ` ` instead of " " 
Then you set a variable with ${variableName}*/
console.log(`The value of variableName is ${variableName}`);
/* This is basically an fstring from python or java */

/* Now we move onto getting user input in the backend. 
we do this  by installing the npm module "node package manager" 
This is used in JS projects to handle different dependencies

first you want to creat a new npm project
"npm init -y" in the terminal*/
/* This creates a package.json file which will manage
your different dependencies and their versions 

then we install readline-sync package for collecting user input
also creates package-lock file and node _modules folder*/

/* Now to get user input first we must initialize and create the
input tool (this is like making a Scanner) then collect input */
const readline = require("readline-sync");
/* Get the input */
const userName = readline.question("What is your username? ");
/* print input to console */
console.log(`Your username is ${userName}`);
const areYouTired = readline.keyInYN("Are you tired? : ");
/* built in yes or no function. you have to enter y or n
if you enter anything else it passes and returns nothing */
console.log(areYouTired);
/* Strict version forces valid input before proceeding */
const areYouStrict = readline.keyInYNStrict("Are you sure? :");
console.log(areYouStrict);


/* Now time for variables and data types */
/* primitive data types are the most basic in JS */
String; /* anything surrounded by "" or ' ' or ` ` */
Boolean; /* just true or false in lowercase */
Number; /* This includes both integer and floats */
undefined; /* this is a condition where an expression
        does not have a correct value despite having correct syntax 
        use this when you havent yet set a value for something
        but you will later on*/
null; /* you use null instead of undefined to explicity set
        the value of something as nothing */
/* semicolons are not necessary in JS, they are a line finisher
but not necessary to make the scripts run */
BigInt; /* For numbers too large to be stored in Number datatype */

/* There are 3 ways to define variables */
/* for variables use camelCase, no spaces, no leadingnumbers, no !$# */
/* var keyword allows you to declare changeable variables */
var thisIsAVariable = "hello"
// var variables are mutable and the value stored within can change
thisIsAVariable = "This has been changed"
// note: var is function scoped and hoisted

/* The let keyword also allows you to declare a variable
that can be changed later on */
let secondVariable = 6969; 
/* no need to explicitly declare datatype when defining variables */
secondVariable ++;

/* The const keyword allows you to declare immutable constants */
const FIRSTCONSTANT = true;
/* The naming convention used depends on the type of constant
that it is  */
/* You should use camelCase for const variables that are local to 
a function, or values that are calculated while 
the program is running (like user input). */
const myName = readline.question("Name: "); // Calculated at runtime

/* You should use ALL_UPPER_CASE (with underscores) 
for constants that are hard-coded and known before 
the program even starts. 
These are "Configuration" or "Static" values. */
const PI = 3.14159;
const MAX_RETRY_ATTEMPTS = 5;
const DEFAULT_COLOR = "blue";

/* let & const are block-scoped keep this in mind when
using if statements, while and for loops*/
if (FIRSTCONSTANT){
    let exampleVariable = 10
    /* exampleVaiable will not work outside of the {} */
}

/* var is function scope so a tier higher than block scope
if not inside of a function then it is global scope*/
if (FIRSTCONSTANT) {
    var exampleVaiable2 = 10
}
/* We can use this outside of the {} */
console.log(`${exampleVaiable2}`)

/* To declare a function */
function firstFunction() {
    console.log(exampleVaiable3)
    var exampleVaiable3 = "holy moly donut shop"
    console.log(exampleVaiable3)
    /* so you can actually use variables before initalizing them
    when declared with var
    This is because var variables are hoisted to the top
    of the function block, so it doesnt crash your code
    it becomes initialized but set to undefined because the
    variable hasn't been provided a value yet 
    
    this only works with var, let and const do not work*/
}

/* most of the arithmetic operators in JS 
are the same as other languages */
// +  /* addition */
// -  /* subtract */
// /  /* division */
// * /* multiplication */

// ** /* exponential */
// % /* modulus */

// -- /* decrement */
// ++ /* increment */

// += /* add equals */
// -= /* minus equals */
// *= /* multiply equals */
// /= /* divide equals */

/* JS is unique in how it handles arithmetic */
const xValue = 6
const yValue = "7"
console.log(xValue + yValue) 
/* this will not result in an error = 67
despite xValue and yValue being different data types
xValue gets converted into a string
Then both numbers are added & printed to 
the console as a single string

This happens because JS performs type coersion
(implicit type conversion) when you attempt to perform
arithmetic on values of different data types*/

/* Same thing happens even with boolean values */
const xxValue = 6
const yyValue = true /* true = 1 */
const zValue = false /* false = 0 */
console.log(xxValue + yyValue + zValue) /* =7 */

/* it happens with every combination */
const xxxValue = "love"
const yyyValue = true /* true = 1 */
const zzValue = false /* false = 0 */
console.log(xxxValue + yyyValue + zzValue) /* = lovetruefalse */

/* with multiplication JS will try to convert strings into numbers 
instead of concatenation*/
const aValue = 3
const bValue = "dog 123" 
console.log(aValue * bValue)  /* in this case it fails because
dog cannot be converted into numbers resulting in =NaN
NaN = not a number */
const aaValue = 3
const bbValue = "123" 
console.log(aaValue * bbValue) /* here it succeeds =369 */
/* same idea for division and subtraction etc. 
Any operator that is not + (concatenation) 
java will try to convert strings
into numbers and perform arithmetic */

/* To avoid conversion issues we look into explicit type conversion */
/* first method is to use constructors and wrap values */
const cValue = 6
const dValue = "7"
console.log(cValue + Number(dValue)) /* =13 */
/* wrap with desired data typeconstructor */

/* ParseInt/ParseFloat function converts its first argument to a string,
parses that string, then returns an integer or NaN  */
const ccValue = 6
const ddValue = "10 dog"
console.log(ccValue + parseFloat(ddValue)) /* =16
parseInt takes what can be converted into a num and ignores chars */
/* parseFloat won't add decimal places if not already present */
/* both constructors and parsing works on boolean values too */

/* converting to a string */
const eValue = 3
const fValue = "dog 123" 
console.log(String(eValue) + fValue)/* = 3dog 123
remember to add spaces manually */
console.log(eValue + "") /* This also converts to string
just by adding an emppty string */
/* last way to convert to string is the .toString() method */
console.log(eValue.toString())

/* Comparison operators */
// /*
// == /* equality operator */
// === /* strict equality operator */
// != /* not-equal-to operator */
// !== /* not-equal-to-strict operator */
// < /* less-than operator */
// > /* greater-than operator */
// <= /* less than or equal to */
// >= /* greater than or equal to */

// == this is the loose equality operator
/* it is what performs the implicit type conversion we saw 
when doing arithmetic*/
console.log("1" == 1)
/* java will attempt to convert them into the same datatype
then compare them ex. "1" == 1 returns true */
console.log(true == 1)
/* this also returns true because true = 1 and false = 0 */
console.log(null == undefined)/* This is true */
console.log(" " == 0)/* This is true */
console.log("1,2" == [1,2]) /* this is true lmao */
/* now the strict equality operator will look at
both the value and the datatype */
console.log("1" === 1) /* this is false */
console.log(true === 1) /* false */
console.log(" " === 0)/* This is false */
console.log(null === undefined)/* This is false */
/* The source of many bugs come from the type of equality operator
that you use so typicallys it is recommended to use strict */
console.log("3" < "2") /* returns true, but both are 1 char strings
They are equal but type conversion turns them into integers */
/* The same logic applies to the > < >= too, 
implicit type conversion will be attempted so make sure
if you use them to manually convert the types to avoid bugs */

/* Logical operators */
// && AND
//  || OR
// ! NOT
/* function the same as any other language */
console.log(true || false) /* returns true */
console.log(true && false) /* returns false as both arent equal*/
console.log(!(true && false)) /* returns true */

/* Where things get weird is using logical operators on 
non-boolean values*/
/* Examples with || */
console.log("hello" || true) /* prints hello */
console.log(" " || true) /* prints whitespace " " */
console.log("" || true) /* prints true because nothing is inside */
console.log("" || 7) /* prints right value always b/c nothing inside left */
/* Examples with && */
console.log(false && "hello") /* if this is true it will print
the value on the right, else it will print false */
console.log(true && "hello") /* this is true, thus it prints the
value on the right */
console.log(!false && "hello") /* false becomes true thanks to !not
and prints value to the right */
/* So be mindful when using logical operators on Non-boolean values */
/* Convert values to boolean */
console.log(Boolean("hello") && Boolean(2)) /* This resolves to true
because both values are boolean on both sides */

/* Conditionals (if/else if/ else) */
/* shortcut to type is "ifelse" */
/* Control Flow - If Statements */
if (true == 1) {
    console.log("This will always run");
} else if (false) {
    /* This code is unreachable because the first condition (true) 
       is already met. JS skips the rest of the chain. */
    console.log("This will never run");
} else {
    /* This is also unreachable */
    console.log("This also never runs");
}

/* To fix the unreachable code, we use variables */
let conditionValue = 20;

if (conditionValue > 30) {
    console.log("Value is greater than 30");
} else if (conditionValue > 15) {
    console.log("Value is greater than 15 but less than or equal to 30");
} else {
    console.log("Value is 15 or less");
}

/* if you have just a single statement to execute,
you do not need to add braces */
if (true) console.log("love")
/* this applies even if you have an else/else if statement
just make sure it does not exceed 1 line */
else console.log("poop")

/* JS also allows us to write ternary conditions */
const condition = 2 < 3 ? " okay cool" : "no"/* if this condition
is true then print the first value else print the 2nd value */
/* basically inline control flow rather than an if statement */
console.log(condition)

/* switch statements */
const switchCondition = 3

switch (switchCondition) {
    /* please remember indentation does not matter in JS
    so all code executes until the break otherwise you
    will get fallthrough */
    case 3:
        console.log("The number is 3")
        break;
        /* use break here not return else the code after
        the switch statement will not execute
        Unless you use it inside a function and want to 
        return a value from the function */
        /* remember its fallthrough not fall up
        so it will fallthrough all code AFTER the valid case
        any before the valid case will not be executed */
    case 4:
        console.log("The number is 4")
        break;

    default:
        console.log("dog cat mouse")
        break;
}

console.log("htes")

/* ARRAYS */
/* array declaration */
/* basic arrays in java are mutable */
/* arrays are zero-indexed */
const arrayExample = []
const arrayExample2 = [1,2,3,true] /* the elements in an array
do not need to be of the same datatype */
/* Another way to create an empty array of a size with no elements */
const arrayExample3 = new Array(4) /* must be a number or variable
with a number data type (or even mayble a .length) */
console.log(arrayExample3[3]) /* prints "undefined" 
since no value has been placed inside*/
/* Another way to produce an array from anything that can be
looped through to extract elements for the array */
const arrayExample4 = Array.from("hello")
console.log(arrayExample4) /* prints  [ 'h', 'e', 'l', 'l', 'o' ] */
/* .from() method is very useful so look into it */
/* adding an element in the array */
arrayExample2[4] = "yellow" /* this will add the element at the end */
console.log(arrayExample2)

console.log(arrayExample2.length) /* prints 5 */
/* you can also add an element at the end of the array */
arrayExample2.push("purple")
/* change the last value in an array */
arrayExample2[arrayExample2.length - 1] = "blue"
arrayExample2.pop() /* removes the last element */
console.log(arrayExample2)
/* add elements to a custom position beyond existing elements */
arrayExample2[arrayExample2.length -1 + 4] = "green"
console.log(arrayExample2) /* prints 
[ 1, 2, 3, true, 'blue', <3 empty items>, 'green' ]
 adds 3 empty items in between 
 and places green in the 4th & final position */
 /* Remove the first element in an array */
arrayExample2.shift()
console.log(arrayExample2) /* prints 
[ 2, 3, true, 'blue', <3 empty items>, 'green' ] */
/* You can also unshift an element to the start of an array */
arrayExample2.unshift("yellow")
console.log(arrayExample2) /* prints 
[ 'yellow', 2, 3, true, 'blue', <3 empty items>, 'green' ] */
/* You can also remove elements from a custom position */
arrayExample2.splice(2, 1) /* removes 1 element starting from index 2 */
console.log(arrayExample2) /* prints 
[ 'yellow', 2, true, 'blue', <3 empty items>, 'green' ] */
 /* You can identify the index of an element */
console.log(arrayExample2.indexOf("yellow")) /* prints 0 
It will return the first element it finds even if there are duplicates*/
console.log(arrayExample2.lastIndexOf("blue")) /* prints -1
because blue is not in the array */

/* get the last occurence of element in the array  */
console.log(arrayExample2.lastIndexOf("yellow")) /* prints 3*/
console.log(arrayExample2.includes("blue")) /* prints false
it will return true if the element is in the array */
console.log(arrayExample2.join(" ")) /* prints 
'yellow 2 true green' as a string,
empty items are not printed*/

/* We can also concat multiple arrays together */
console.log(arrayExample2.concat(arrayExample3)) /* prints 
[ 2, 3, true, 'blue', <3 empty items>, 'green', <4 empty items> ] */
/* We can also reverse an array */
console.log(arrayExample2.reverse()) /* prints 
[ 'green', <3 empty items>, 'yellow', true, 2, 'yellow' ] */
/* We can also sort an array */
const arrayExample5 = [2, 1, 3]
console.log(arrayExample5.sort()) /* prints 
[ 1, 2, 3 ] */
/* We can also sort an array of strings */
const arrayExample6 = ["yellow", "blue", "green"]
console.log(arrayExample6.sort()) /* prints 
[ 'blue', 'green', 'yellow' ] 
 Remember that sort() mutates the array
 sort() orders strings alphabetically (lexicographically)*/
 /* We can also slice an element or a section of an array  
 starting from index 1 to index 2, you can alse use 
 negative numbers to start from the end of the array or 
 leave the second argument blank to slice from the first
 index to the end of the array */
 console.log(arrayExample5.slice(1, 2)) /* prints 
[ 2 ]  note this changes the length of the array*/

 /* ARRAY DESTRUCTURING AND SPREAD*/
 /* destructuring allows you to unpack values from arrays */
 const [first, second,third] = [1,2,3]
 console.log(first, second, third) /* prints 1 2 3 */   
 /* you can also skip values */
 const [fourth, ,sixth] = [4,5,6]
 console.log(fourth, sixth) /* prints 4 6 */
 /* you can also assign default values */
 const [seventh, eighth = 8] = [7]
 console.log(seventh, eighth) /* prints 7 8 */

 /* you can also use the spread operator (...variable) 
 to extract the rest of the array */
 const [ninth, ...tenth] = [9,10,11]
 console.log(ninth, tenth) /* prints 9 [ 10, 11 ] */
 /* you can also use the spread operator to copy an array */
 const arrayExample7 = [...arrayExample6]
 console.log(arrayExample7) /* prints [ 'blue', 'green', 'yellow' ] */
 /* you can also use the spread operator to merge arrays 
 or add elements to an array */
 const arrayExample8 = [1,2,3,...arrayExample6, ...arrayExample5]
 console.log(arrayExample8) /* prints 
 [ 1, 2, 3, 'blue', 'green', 'yellow', 1, 2, 3 ] */
 /* you can also use the spread operator to add elements to an array */
 arrayExample8.push(...arrayExample5) /* this works with unshift too */
 console.log(arrayExample8) /* prints 
 [ 'blue', 'green', 'yellow', 1, 2, 3, 1, 2, 3 ] */

 /* WHILE LOOPS/ DO WHILE LOOPS */
 let counter = 0
 while (counter < 5) {
     console.log(counter) /* prints 0 1 2 3 4 */
     counter++
 }
 /* do while loop */
 counter = 0
 do {
     console.log(counter) /* prints 0 1 2 3 4 */
     counter++
 } while (counter < 5)

 /* FOR LOOPS */
 for (let counter = 0; counter < 5; counter++) {
     console.log(counter) /* prints 0 1 2 3 4 */
 }
 /* for of loop */
 const arrayExample9 = [1,2,3,4,5]
 for (const element of arrayExample9) {
     console.log(element) /* prints 1 2 3 4 5 */
 }
 /* for in loop to enumerate through an object */
 const objectExample = {name: "John", age: 30, city: "New York"}
 for (const key in objectExample) {
     console.log(key) /* prints name age city */
 }
 /* for each loop is a method that takes a callback function */
 arrayExample9.forEach(element => { /* the arrow just means do this */
     console.log(element) /* prints 1 2 3 4 5 */
 })

 /* enumerate through an array using .entries() */
 for (const [index, element] of arrayExample6.entries()) {
     console.log(index, element) /* prints 0 blue 1 green 2 yellow */
 }

 /* OBJECTS */
 /* JSON stands for Javascript Object Notation */
 const personObject = {
    /* objects have properties associated with values (keys) */
    name: "Alice",
    age: 20,
    /* you can put functions inside objects */
    sayHello: function() {
        return "hello"
    },
    /* You can also have objects inside of objects*/
    occupation: {

    }
 }
 /*To access properties of an object you have two options
 first is dot notation  */
 personObject.name = "Scarlet" /* modify an existing property */
 personObject.city = "Toronto" /* add a new property to an object */
 delete personObject.occupation /* remove property from your object */
 /* The second method is bracket notation
 both ways work the same just pick your poison */
 personObject["age"] = 25
 console.log(personObject.name, personObject.age, personObject.city)
 /* prints "Scarlet 25 Toronto" */
 console.log(personObject) /* prints the blueprint
  {
  name: 'Scarlet',
  age: 25,
  sayHello: [Function: sayHello],
  city: 'Toronto'
}*/