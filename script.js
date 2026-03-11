/* This is an external javascript file */
alert("Hello world from an external file");
console.log("Hello world from an external file");

/* If you have embedded script and an
    external script file both running code
    The external script file runs first since it
    appears in the HTML head instead of the body
    but both will run*/

/* You can also affect the DOM using javascript */
document.body.style.backgroundColor = "red";
/* This makes the page red */
/* DOM stands for Document Object Model  */
/* It is a programming interface that represents the
structure of an HTML or XML document as a tree of objects(nodes)
where each object represents a part of the document
(like an element, attribute, or text)
 
This allows programming languages like javascript to
interact with, modify, and update the content structure,
and style of a web page dynamically.*/

/* You can also run scripts from a cdn or remote server */

/* To get user input in a browsert youcan use the prompt function */
prompt("This instructs the browser to display a message and get input");
/* Like when you want to signinto a host server and you need
admin name and admin pass to get inside a router */

