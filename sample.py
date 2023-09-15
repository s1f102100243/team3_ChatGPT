import openai
openai.api_key = "BYVqECvhL8ZQ3L9uD-WGAUCYvV817AMIIxjAEpXdawn7tgqxa98kRo-66crUFj8gU_h6OxThlCZL9UZ5mZlkT2w"
openai.api_base="https://api.openai.iniad.org/api/v1"

question = input('Question:')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "語頭には「ふむ。」、すべての語尾に「じゃ」か「のじゃ。」をつけて質問に短く答えてください"},
        {'role':'user','content':question},
    ],
)

print(response['choices'][0]['message']['content'])