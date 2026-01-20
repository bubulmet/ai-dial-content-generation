import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_content = BytesIO(image_bytes)
        attachment = await bucket_client.put_file(
            name=file_name,
            mime_type=mime_type_png,
            content=image_content
        )
        return Attachment(
            title=file_name,
            url=attachment.get("url"),
            type=mime_type_png
        )


def start(model_name='anthropic.claude-v3-haiku') -> None:
    model_client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name=model_name,
    )
    attachment = asyncio.run(_put_image())
    print(attachment)

    message = Message(
        role=Role.USER,
        content="What do you see on this picture?",
        custom_content=CustomContent(attachments=[attachment])
    )
    reply = model_client.get_completion([message])
    print('=' * 10)
    print(reply.content)

# start(
#     model_name='anthropic.claude-v3-haiku'
#     # model_name='gpt-4o'
# )

#  ---------------------------------------------------------------------------------------------------------------
#  Note: This approach uploads the image to DIAL bucket and references it via attachment. The key benefit of this
#        approach that we can use Models from different vendors (OpenAI, Google, Anthropic). The DIAL Core
#        adapts this attachment to Message content in appropriate format for Model.
#  TRY THIS APPROACH WITH DIFFERENT MODELS!
