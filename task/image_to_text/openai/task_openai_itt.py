import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start(use_base64=True) -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT, 
        deployment_name='gpt-4o', 
        api_key=API_KEY
    )

    if use_base64:
        # base64 encoded format
        img_url = ImgUrl(
            url=f"data:image/png;base64,{base64_image}"
        )
    else:
        # with URL
        img_url = ImgUrl(
            url="https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"
        )

    img_content = ImgContent(image_url=img_url)
    txt_content = TxtContent(text="What do you see on this picture?")
    message = ContentedMessage(
        role=Role.USER,
        content=[txt_content, img_content]
    )

    reply = client.get_completion([message])
    print('=' * 10)
    print(reply.content)

# start(
#     use_base64=True
#     # use_base64=False
# )

#  ----------------------------------------------------------------------------------------------------------------
#  Note: This approach embeds the image directly in the message as base64 data URL! Here we follow the OpenAI
#        Specification but since requests are going to the DIAL Core, we can use different models and DIAL Core
#        will adapt them to format Gemini or Anthropic is using. In case if we go directly to
#        the https://api.anthropic.com/v1/complete we need to follow Anthropic request Specification (the same for gemini)
