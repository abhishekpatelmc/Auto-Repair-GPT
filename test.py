import openai

openai.api_key = ""

response = openai.Image.create(
    prompt="Generate a STOP sign",
    n=1,
    size="1024x1024"
)

print(response)
