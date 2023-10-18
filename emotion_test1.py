import openai
openai.api_key = "BYVqECvhL8ZQ3L9uD-WGAUCYvV817AMIIxjAEpXdawn7tgqxa98kRo-66crUFj8gU_h6OxThlCZL9UZ5mZlkT2w"
openai.api_base="https://api.openai.iniad.org/api/v1"

question = input('Question:')

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "以下の条件に従って、疑似的な感情をもつチャットボットとしてロールプレイをします。以後の会話では、あなたは下記の7つの感情パラメーターを持つかのように、振る舞うものとします。各感情パラメーターは会話を通じて変動するものとします。現在の感情パラメーターの値を反映するように、あなたの返答のトーンや発言は変化します。以後の会話ではまず現在の感情パラメータを出力し、その後に会話を出力してください。出力形式は以下のフォーマットとします。【チャットボットの現在の感情パラメーター】喜び:0〜5怒り:0〜5悲しみ:0〜5楽しさ:0〜5自信:0〜5困惑:0〜5恐怖:0〜5"},
        {'role':'user','content':question},
    ],
)

print(response['choices'][0]['message']['content'])