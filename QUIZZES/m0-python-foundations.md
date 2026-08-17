# M0 · Python Foundations quiz

## Multiple choice

1. Why is Python useful for AI engineering?
   - A. It is readable and has many useful libraries.
   - B. It only runs on servers.
   - C. It removes the need for testing.
   - D. It can only work with numbers.

2. What does a package provide?
   - A. Reusable code
   - B. A user password
   - C. A database server
   - D. A model answer

3. What is a function?
   - A. A named piece of reusable behavior
   - B. A saved API key
   - C. A type of database
   - D. A notebook cell only

4. What is the purpose of a type hint?
   - A. To communicate what kind of value is expected
   - B. To encrypt a value
   - C. To run a model
   - D. To create a server

5. What is a class useful for?
   - A. Grouping related data and behavior
   - B. Installing packages
   - C. Counting tokens
   - D. Replacing tests

6. What is a database useful for?
   - A. Storing data so it can be used later
   - B. Generating Python syntax
   - C. Choosing a model
   - D. Hiding errors

7. What does a web server do?
   - A. Receives requests and sends responses
   - B. Trains every model
   - C. Converts all text to tokens
   - D. Replaces source code

8. Why should invalid input be rejected?
   - A. To keep incorrect data from moving through the application
   - B. To make the code longer
   - C. To avoid using functions
   - D. To increase model size

9. What does a test check?
   - A. Whether code behaves as expected
   - B. Whether a user likes the font
   - C. Whether a model is conscious
   - D. Whether a package is popular

10. Why use logging?
    - A. To understand what an application did
    - B. To replace all error handling
    - C. To store API keys
    - D. To make code run offline

## Code reading and debugging

11. What does this return for positive inputs?

    ```python
    def add_tax(price: float, rate: float) -> float:
        return price * (1 + rate)
    ```

12. What is wrong with this function?

    ```python
    def divide(total, count):
        return total / count
    ```

    Name one input that should be checked before division.

13. A Python program says `NameError: name 'value' is not defined`. What is the
    simplest meaning of this error?

## Scenario

14. You are building a small portfolio application. It must accept a purchase,
    save it, and show it through an HTTP endpoint. Name the three basic parts
    you would build and test.

## Capstone transfer

15. Name one Python boundary you would use in Chronos and state what it should
    return.
