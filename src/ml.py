import torch
import re

from PIL import UnidentifiedImageError
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
from main import LogoResult
from utils import load_svg_from_url


DEVICE = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

MODEL_NAME = "HuggingFaceTB/SmolVLM-Instruct"

processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForVision2Seq.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
).to(DEVICE)


def infer_logo_name(logo_result: LogoResult) -> str:
    try:
        image = load_image(logo_result.url)
    except UnidentifiedImageError:
        # Likely an SVG in this case
        image = load_svg_from_url(logo_result.url)

    # Create input messages
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "type": "text",
                    "text": "What is the name of the company represented by this logo? Return the full and complete name, no other text. If there are multiple words, return all of them. If you can't tell, return 'unknown'.",
                },
            ],
        },
    ]

    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    # This could be improved
    generated_ids = model.generate(**inputs, max_new_tokens=20)
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )

    result = generated_texts[0]
    match = re.search(r"Assistant: (.*?)$", result)
    return match.group(1).strip(". ")
