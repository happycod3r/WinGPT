import openai

def getImage():
    openai.api_key = "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"
    response = openai.Image.create(
        prompt="a white siamese cat",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url

print(getImage())
