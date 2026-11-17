import base64
from io import BytesIO

from PIL import Image

from config import settings


def _image_to_data_url(image: Image.Image) -> str:
    buf = BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def _stub_describe(image: Image.Image) -> str:
    width, height = image.size
    thumb = image.resize((1, 1))
    r, g, b = thumb.getpixel((0, 0))[:3]
    return (
        f"[stub] screenshot {width}x{height}, "
        f"average color rgb({r},{g},{b})"
    )


def _vllm_describe(image: Image.Image) -> str:
    from openai import OpenAI

    client = OpenAI(base_url=settings.vllm_base_url, api_key=settings.vllm_api_key)
    response = client.chat.completions.create(
        model=settings.vllm_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe what is visible on this screen in 1-3 sentences: open apps, visible text/UI, and what the user appears to be doing.",
                    },
                    {"type": "image_url", "image_url": {"url": _image_to_data_url(image)}},
                ],
            }
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()


def describe_image(image: Image.Image) -> str:
    if settings.stub_vlm:
        return _stub_describe(image)
    return _vllm_describe(image)
