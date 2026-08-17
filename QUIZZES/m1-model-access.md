# M1 · Model access quiz

## Multiple choice

1. What is an AI model?
   - A. A system that produces outputs from inputs it receives
   - B. A complete finished application
   - C. A database table
   - D. A web browser

2. Why is a model not a complete product?
   - A. A product also needs data, rules, user interaction, and reliable software.
   - B. Models cannot produce text.
   - C. Products do not need users.
   - D. Models cannot run in applications.

3. What is a hosted model?
   - A. A model accessed through a service or API
   - B. A model stored only in a notebook cell
   - C. A model with no parameters
   - D. A database query

4. What is a local model?
   - A. A model run on hardware controlled by the application team
   - B. A model that can never be tested
   - C. A model that always has internet access
   - D. A model that needs no memory

5. What is one trade-off of using a hosted model?
   - A. Less infrastructure to operate, but a service dependency and usage cost
   - B. No network is needed
   - C. The team owns the model weights
   - D. It cannot be replaced

6. What is one trade-off of using a local model?
   - A. More control and privacy, but more hardware and operations responsibility
   - B. No setup is required
   - C. It always has the best quality
   - D. It cannot be monitored

7. What should guide model selection?
   - A. The task’s quality, speed, cost, privacy, and operating needs
   - B. The longest model name
   - C. The newest version only
   - D. The largest parameter count only

8. What is a model boundary?
   - A. A small application interface that hides provider-specific call details
   - B. A limit on Python files
   - C. A database password
   - D. A user interface color

9. Where should secrets normally be kept?
   - A. In protected configuration such as environment variables or a secret store
   - B. In a public slide
   - C. In a prompt
   - D. In a test name

10. What should an application do when a model returns no usable output?
    - A. Return a safe fallback and record what happened
    - B. Treat the empty output as a successful answer
    - C. Expose the secret key
    - D. Delete the conversation

## Code reading and debugging

11. What is the purpose of this check?

    ```python
    if api_key:
        call_model(api_key)
    else:
        print("Configuration is missing")
    ```

12. A function returns a provider response object, but the rest of the app
    expects text. What should the boundary do?

13. A local model fails because a setting meant for loading the model was passed
    into the generate call. What should you do?

## Scenario

14. You need to test an AI feature today without depending on a live provider,
    but the production version may use a hosted service. What should remain the
    same between the test version and production version?

## Capstone transfer

15. For a Chronos assistant, what should the model-call function accept and what
    should it return?
