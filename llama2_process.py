# from transformers import LlamaForCausalLM, CodeLlamaTokenizer

# tokenizer = CodeLlamaTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
# model = LlamaForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")

# PROMPT = '''def remove_non_ascii(s: str) -> str:
# """ <FILL_ME>
#     return result
# '''

# input_ids = tokenizer(PROMPT, return_tensors="pt")["input_ids"]
# generated_ids = model.generate(input_ids, max_new_tokens=128)

# filling = tokenizer.batch_decode(generated_ids[:, input_ids.shape[1]:], skip_special_tokens = True)[0]
# print(PROMPT.replace("<FILL_ME>", filling))

# from transformers import pipeline
# import torch

# generator = pipeline("text-generation",model="codellama/CodeLlama-7b-hf",torch_dtype=torch.float16, device_map="auto")
# generator('def remove_non_ascii(s: str) -> str:\n    """ <FILL_ME>\n    return result', max_new_tokens = 128, return_type = 1)

import vault
import os
import replicate

token = vault.get_Secret("replicate_key")
os.environ["REPLICATE_API_TOKEN"] = token

output = replicate.run(
  "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
  input={
    "debug": False,
    "top_k": 50,
    "top_p": 1,
    "prompt": "Can you write a poem about open source machine learning? Let's make it in the style of E. E. Cummings.",
    "temperature": 0.5,
    "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
    "max_new_tokens": 500,
    "min_new_tokens": -1
  }
)
print(output)

print(*output, sep='')
# full_response = ''
# for item in output:
#     print("Inside for")
#     full_response += item
# print(full_response)
