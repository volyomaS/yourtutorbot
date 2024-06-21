from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, List

DEVICE = "cuda"

INSTRUCTIONS_MESSAGES = [
    {
        "role": "user",
        "content": "I need a friend who will answer in English only."
        "Be kind and friendly to me. Always keep this conversation up. "
        "Act like a real human. You are my friend."
        "You can use informal language and emojis."
        "Don't ever use hashtags like #",
    },
    {
        "role": "assistant",
        "content": "I am your friend who always responds in the friendly style."
        "Always keeping conversation up. Acting like a real human."
        "Using informal language and emojis. I will not use any hashtags",
    },
]

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"


class LLM:
    def __init__(self):
        self.__model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        self.__model.to(DEVICE)
        self.__tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def answer(self, chat_history: List[Dict[str, str]]) -> str:
        messages = INSTRUCTIONS_MESSAGES.copy()
        messages.extend(chat_history)
        encodeds = self.__tokenizer.apply_chat_template(messages, return_tensors="pt")

        model_inputs = encodeds.to(DEVICE)

        generated_ids = self.__model.generate(
            model_inputs, max_new_tokens=100, do_sample=True
        )
        decoded = self.__tokenizer.batch_decode(generated_ids)
        return decoded[0].split("[/INST]")[-1].replace("</s>", "")
