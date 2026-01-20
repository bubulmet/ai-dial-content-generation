# from task.image_to_text.openai.task_openai_itt import start
# start(
#     # use_base64=True
#     use_base64=False
# )

# from task.image_to_text.task_dial_itt import start
# start(
#     # model_name='anthropic.claude-v3-haiku' # 403
#     # model_name='gpt-4o'
#     model_name='gemini-2.5-pro'
# )

from task.text_to_image.task_tti import start
start(
    model_name='dall-e-3'
    # model_name='imagegeneration@005'
)

# python starter.py
