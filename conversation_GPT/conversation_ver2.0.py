import csv
import requests

# トークン数の上限と最大ターン回数を設定
MAX_TOKENS = 2048
COUNT = 15

# 会話をスタートさせる関数
def start_conversation():
    bot_config = read_bot_config()
    initial_message = read_initial_message()

    message_history = [{"role": "user", "content": initial_message}]
    have_conversation(bot_config, message_history, COUNT)

# Configシートからボットの設定を読み込む関数
def read_bot_config():
    bot_config = []
    with open('config.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] and row[1]:
                bot_config.append([row[0], row[1]])
    return bot_config

# Outputシートから初期メッセージを読み込む関数
def read_initial_message():
    with open('output.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == 'A1':
                return row[1]
    return ""

# 会話を継続させる再帰関数
def have_conversation(bot_config, message_history, turns):
    if turns <= 0:
        return

    current_message_history = message_history.copy()
    for bot_index, (bot_name, bot_system_prompt) in enumerate(bot_config):
        # トークン数が上限を超える場合、古いメッセージを削除
        while count_tokens(current_message_history + [{"role": "system", "content": bot_system_prompt}]) > MAX_TOKENS:
            current_message_history.pop(0)

        # systemPromptを適切な場所に挿入
        new_message_history = current_message_history.copy()
        bot_response = get_chat_gpt_response(bot_system_prompt, new_message_history, bot_index)

        # トークン数が上限を超える場合、古いメッセージを削除
        while count_tokens(new_message_history + [{"role": "assistant", "content": bot_response}]) > MAX_TOKENS:
            new_message_history.pop(0)

        write_to_output_sheet(bot_name, bot_response)

        # ボットの応答でmessage_historyを更新
        current_message_history.append({"role": "user", "content": bot_response})

        if len(current_message_history) > 1:
            # 以前のメッセージの役割を入れ替える
            current_message_history = [
                {"role": "assistant" if msg["role"] == "user" else "user", "content": msg["content"]}
                for msg in current_message_history[:-1]
            ] + [current_message_history[-1]]

        print(f"Bot Index: {bot_index}, Message History: {current_message_history}, Bot Response: {bot_response}")

    # 更新されたmessage_historyでhave_conversationを呼び出す
    have_conversation(bot_config, current_message_history, turns - 1)

# トークン数の計算関数
def count_tokens(message_history):
    total_tokens = 0
    for msg in message_history:
        total_tokens += len(msg["content"])
    return total_tokens

# ChatGPT呼出関数
def get_chat_gpt_response(system_prompt, message_history, bot_index):
    api_key = "BYVqECvhL8ZQ3L9uD-WGAUCYvV817AMIIxjAEpXdawn7tgqxa98kRo-66crUFj8gU_h6OxThlCZL9UZ5mZlkT2w"
    url = "https://api.openai.iniad.org/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "presence_penalty": 0,
        "messages": [{"role": "system", "content": system_prompt}] + message_history,
    }

    response = requests.post(url, headers=headers, json=payload)
    json_response = response.json()
    chat_response = json_response["choices"][0]["message"]["content"]

    return chat_response.strip()

# Outputシートに結果を書き込む関数
def write_to_output_sheet(bot_name, bot_response):
    with open('output.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([bot_name, bot_response])

# メイン関数
def main():
    start_conversation()

if __name__ == '__main__':
    main()
