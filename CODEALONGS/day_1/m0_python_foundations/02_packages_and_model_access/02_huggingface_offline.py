from transformers import pipeline

model_path = "OFFLINE-AI-Models/smollm2-135m-instruct"
generate = pipeline("text-generation", model=model_path)

answer = generate("Say hello.", max_new_tokens=20, do_sample=False)
print(answer[0]["generated_text"])
