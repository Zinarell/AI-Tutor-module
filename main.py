from groq import Groq
import os
import dotenv

dotenv.load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq()


completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Сколько яблок в корзине, если у носорога 2 рога?"}
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    stream=True,
    stop=None
)

print("Ответ: ", end="")
for chunk in completion:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()  # перевод строки в конце