
> if response ends in a question `(?)`

`gtp`: "Hi Paul, how can I help you?"

  - request will be: 
  
`user`:
 - **{You asked me}**
 - *" Hi Paul, how can I help you?"*
 - **{and I'm responding with}**
 - *"I'm okay thank you"*
 - **{what do you say next?}**


> if response is a statement or an example `(!) or (ex.)`

`gtp`: A function in JavaScript is written as follows:

```javascript
function myFunction() {
    // code to be executed
}
```
  - request will be: 

`user`:
- **{You told me}**
- *"A function in JavaScript is written as follows:*
function myFunction() {
    // code to be executed
}" 
- **{and I'm responding with}** 
- "How do you use it?" 
- **{what do you say next?}**
