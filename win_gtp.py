import openai
import api_key

openai.api_key = api_key.OPENAI_API_KEY

response = openai.Completion.create(
    engine='text-davinci-003', # The model being used.
    prompt='Hi, How can I help you?', # The input.
    max_tokens=200, # Max tokens allowed in each response.
    n=1 # Number of responses returned.
)

print(response.choices[0].text.strip())
