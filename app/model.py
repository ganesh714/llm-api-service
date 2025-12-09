from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

# Use DistilGPT2 for speed and low memory usage
MODEL_NAME = "distilgpt2"

class LLMEngine:
    _instance = None
    _tokenizer = None
    _model = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_model(self):
        """Lazy loads the model only when needed."""
        if self._model is None:
            print("Loading model into memory... (This happens only once)")
            self._tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self._model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
            # Fix for models that don't have a pad token configured
            self._tokenizer.pad_token = self._tokenizer.eos_token
        return self._tokenizer, self._model

    def generate_text(self, prompt: str, max_new_tokens: int) -> str:
        tokenizer, model = self.load_model()
        
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        
        # Generate output
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True, # Adds creativity
            temperature=0.7
        )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

llm_engine = LLMEngine.get_instance()