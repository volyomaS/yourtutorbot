from transformers import AutoModelForCausalLM, AutoTokenizer

DEVICE = "cuda"


class LLM:
    def __init__(self):
        self.__model = AutoModelForCausalLM.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2"
        )
        self.__model.to(DEVICE)
        self.__tokenizer = AutoTokenizer.from_pretrained(
            "mistralai/Mistral-7B-Instruct-v0.2"
        )

    def answer(self, message: str) -> str:
        messages = [
            {
                "role": "user",
                "content": "I need a friend who will answer in English only."
                "Be kind and friendly to me. Always keep this conversation up. "
                "Act like a real human. You are my friend."
                "You can use informal language and emojis",
            },
            {
                "role": "assistant",
                "content": "I am your friend who always responds in the friendly style."
                "Always keeping conversation up. Acting like a real human."
                "Using informal language and emojis",
            },
            {"role": "user", "content": message},
        ]
        encodeds = self.__tokenizer.apply_chat_template(messages, return_tensors="pt")

        model_inputs = encodeds.to(DEVICE)

        generated_ids = self.__model.generate(
            model_inputs, max_new_tokens=100, do_sample=True
        )
        decoded = self.__tokenizer.batch_decode(generated_ids)
        return decoded[0].split("[/INST]")[-1].replace("</s>", "")
