from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

MODEL_NAME = "prithivida/grammar_error_correcter_v1"


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model


def correct_grammar(text: str) -> str:
    tokenizer, model = load_model()
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(**inputs, max_length=512)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)
