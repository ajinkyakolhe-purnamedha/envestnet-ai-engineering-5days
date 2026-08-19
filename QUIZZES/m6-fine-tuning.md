# M6 · LLM fine-tuning quiz

**Ten questions, one per essential idea in the module.**

Every option is a true statement about building AI applications that this course has taught. Only the option that answers *the question actually asked* is correct. Some questions have more than one right answer; each of those says so.

---

1. Which requirement is a reason to fine-tune a model rather than to retrieve?
   - A. The answer has to reflect prices and holdings exactly as they stand this morning, not as they stood last month.
   - B. A regulator will ask which document a particular sentence in the answer was taken from, and expect a real one.
   - C. Every reply has to arrive in the same valid schema, on every call, across tens of thousands of calls a day.
   - D. A client may ask for their own records to be removed from the system, and you must be able to show that they were.

2. **Select all that apply.** Which of these does a fine-tuning project involve?
   - A. Collecting and cleaning several thousand training examples that show the task being done correctly.
   - B. Choosing a base model to start from, since its size sets the cost of every step that comes after it.
   - C. Provisioning hardware, because training needs far more memory than serving the same model ever does.
   - D. Building a held-out evaluation set, because a score on unseen data is the only evidence of a gain.

3. Serving a model needs roughly one byte of memory per parameter. Why does training that same model need at least four times as much?
   - A. Training loads every weight at a higher precision than serving that same model would ever require.
   - B. Training keeps four things per parameter — the weight, its gradient, its activation, and its optimizer state.
   - C. Training has to hold the whole dataset in memory so that shuffling between epochs stays properly random.
   - D. Training runs for several epochs, and each one of them keeps its own separate copy of all the weights.

4. Full fine-tuning updates every weight in the model. LoRA freezes almost all of them and trains a small set of added weights instead. Why does that make training fit on much smaller hardware?
   - A. No gradient and no optimizer state has to be kept for any weight that has been frozen, and almost all of them are.
   - B. Full fine-tuning can move the model's behaviour further, because every weight in it is free to shift during training.
   - C. The frozen weights are held at a lower precision than they were before, which cuts the memory that they occupy.
   - D. The result is a small file that can be swapped in per client, so one base model serves many different teams.

5. **Select two.** Which two are true of the adapter that a LoRA run produces?
   - A. It is a small fraction of the base model's parameter count, often well under one percent of the total.
   - B. It is small enough that a single base model can serve many of them, with one adapter loaded per client.
   - C. It replaces the base weights that it was trained against, which is why the base is no longer needed.
   - D. It stores the facts that were present in the examples it trained on, so they can be recalled later.

6. A team has a prompt that mostly works but gives inconsistent results. Following this module's recommended order, what should they try next?
   - A. Fine-tune a small model, since the behaviour they want is stable and they can demonstrate it many times.
   - B. Add retrieval, so that the model has the reference material it needs in front of it at the time it answers.
   - C. Move to a larger frontier model, since more capability closes most gaps of this kind without extra work.
   - D. Add a few worked examples to the prompt, which is the next step up and takes about an hour to try.

7. A manager asks whether fine-tuning will make the assistant "smarter". What is the accurate answer?
   - A. Yes, because training on your own domain examples adds knowledge that the base model did not previously hold.
   - B. Yes, because a model trained on your data reasons more effectively about the kind of problem your team has.
   - C. No, it makes the model more reliable at one narrow job, and usually a little worse at everything else.
   - D. No, because overall quality is fixed by the base model and fine-tuning only alters the wording it chooses.

8. A domain expert has one day to spend on a fine-tuning project. Where does this module say that day is best spent?
   - A. Generating as many synthetic training rows as the budget for that batch job will allow them to produce.
   - B. Writing a few hundred careful examples by hand, including the awkward edge cases nobody else will invent.
   - C. Comparing candidate base models, so that the training run starts from the strongest one that is available.
   - D. Tuning the training settings across a sweep of short runs, to find the best combination before committing.

9. A client exercises their right to erasure. Their documents are in your retrieval index, and their records were in the data your adapter trained on. Why is deleting the documents not sufficient?
   - A. Because the index keeps stored embeddings, which have to be rebuilt before the deletion takes full effect.
   - B. Because the provider of the base model retains its own copy of whatever data was used during training.
   - C. Because the adapter would go on citing a document that it is no longer able to read from the index.
   - D. Because a trained weight cannot be edited to remove one example's contribution; you retrain without it.

10. **Select two.** In a production system that uses both, which two jobs belong to the fine-tuned adapter rather than to retrieval?
    - A. Turning a messy free-text note into the strict schema that the code downstream of it expects to receive.
    - B. Holding the compliance-approved wording that your reviewers have already read and signed off on.
    - C. Supplying the closing price for whichever symbol the advisor's note happened to mention that morning.
    - D. Supplying the policy text that is actually in force at the moment the request is being handled.
