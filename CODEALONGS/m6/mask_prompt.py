"""Learn the answer, not the question."""

from transformers import AutoTokenizer

PATH = "../OFFLINE-AI-Models/smollm2-135m-instruct"
tok = AutoTokenizer.from_pretrained(
    PATH, local_files_only=True
)

# A prompt-completion row. TRL masks on this boundary.
row = {
    "prompt": "### Note:\nSell 40 AAPL for Mrs Rao\n\n"
              "### Trades:\n",
    "completion": '[{"symbol":"AAPL","action":"sell",'
                  '"shares":40}]',
}


# #region mask
prompt_ids = tok(row["prompt"])["input_ids"]
full_ids = tok(row["prompt"] + row["completion"])["input_ids"]

# Everything before the completion is labelled -100, and
# the loss function skips every -100.
labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]
# #endregion mask


for token, label in list(zip(full_ids, labels))[:6]:
    print(f"{tok.decode([token])!r:>14}  {label}")
print("   ...")
for token, label in list(zip(full_ids, labels))[-4:]:
    print(f"{tok.decode([token])!r:>14}  {label}")

print(f"\n{labels.count(-100)} ignored, "
      f"{len(labels) - labels.count(-100)} learned from")

# In TRL you do not build this by hand -- you pass
# prompt/completion rows and set one flag:
#
#     SFTConfig(completion_only_loss=True)
#
# (Older tutorials use DataCollatorForCompletionOnlyLM.
#  That class was removed in TRL 1.x. Same idea, and the
#  flag is now the supported way to get it.)
#
# Without masking, half the capacity goes into learning
# to WRITE advisor notes, which nobody asked for. It is
# the most common silent bug in a first fine-tune: it
# trains, the loss falls, and the model is quietly worse.
