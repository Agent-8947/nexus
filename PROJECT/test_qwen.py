import torch

# Fix for Torch 2.6 / Unsloth conflict on Windows
if not hasattr(torch.utils._pytree, 'register_constant'):
    torch.utils._pytree.register_constant = lambda *args, **kwargs: None

from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-1.5B-bnb-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

FastLanguageModel.for_inference(model)
inputs = tokenizer(["What is NEXUS?"], return_tensors = "pt").to("cuda")

outputs = model.generate(**inputs, max_new_tokens = 64)
print("\n[QWEN2.5 OUTPUT]:\n")
print(tokenizer.batch_decode(outputs)[0])
