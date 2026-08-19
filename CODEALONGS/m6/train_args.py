"""The knobs, and the values to start from."""

from trl import SFTConfig

# #region args
args = SFTConfig(
    learning_rate=2e-4,        # 100x the pretraining rate
    lr_scheduler_type="cosine",
    warmup_steps=50,          # ease in, then decay
    num_train_epochs=3,        # more -> it memorises
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,   # effective batch 16
    completion_only_loss=True,       # mask the prompt
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    output_dir="out/trade-parser",
)
# #endregion args

print(args.learning_rate, args.num_train_epochs)
print("effective batch:",
      args.per_device_train_batch_size
      * args.gradient_accumulation_steps)

# Then the trainer is four lines:
#
#   trainer = SFTTrainer(
#       model=model,           # the PEFT-wrapped model
#       args=args,
#       train_dataset=train,
#       eval_dataset=held_out,
#   )
#   trainer.train()
#   trainer.save_model()       # -> adapter_model.safetensors
#
# Watch two curves, not one. Training loss falling is not
# success -- validation loss RISING while training loss
# falls is overfitting. That is why eval_strategy and
# load_best_model_at_end are in the config above: the
# best checkpoint is rarely the last one.
