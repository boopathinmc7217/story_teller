from openai import OpenAI
import requests
client = OpenAI(api_key="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")

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

response_image = requests.get(image_url)
with open("image.jpg", 'wb') as file:
    file.write(response_image.content)
print(image_url)