import pymorphy3
import re
import pdfplumber
import csv

morph = pymorphy3.MorphAnalyzer()

# Простой список стоп-слов (можно расширить)
STOPWORDS = {"и", "в", "на", "с", "по", "а", "но", "или", "что", "как", "это", "не"}

def tokenize_and_lemmatize(text: str) -> list[str]:
    # 1. Вытаскиваем слова (кириллица + латиница + цифры)
    raw_tokens = re.findall(r'[а-яёa-z0-9]+', text.lower())
    # 2. Лемматизируем и убираем стоп-слова
    lemmas = [
        morph.parse(token)[0].normal_form
        for token in raw_tokens
        if token not in STOPWORDS
    ]
    return lemmas

# def open_pdf(filepath):
#     with pdfplumber.open(filepath) as pdf:
#         text = "\n".join(page.extract_text() for page in pdf.pages)

#         lemmas = tokenize_and_lemmatize(text)

#     return lemmas

# print(open_pdf('lesson.pdf'))

def load_pdf_chunks(filepath: str, min_chunk_len: int = 30) -> tuple[list[str], list[list[str]]]:
    # 1. Извлечение
    with pdfplumber.open(filepath) as pdf:
        raw_text = "\n".join(page.extract_text() for page in pdf.pages)

    # 2. Очистка от "ломаных" переносов строк (типичная проблема PDF)
    clean_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', raw_text)  # одиночные \n → пробел
    clean_text = re.sub(r'\n{2,}', '\n\n', clean_text)      # множественные \n → один абзац

    # 3. Разбиение на чанки (по абзацам)
    chunks = [c.strip() for c in clean_text.split('\n\n') if len(c.strip()) >= min_chunk_len]

    # 4. Параллельная обработка
    original_chunks = chunks
    tokenized_corpus = [tokenize_and_lemmatize(chunk) for chunk in chunks]

    return original_chunks, tokenized_corpus


def save_to_csv(filepath: str, data: list[list[str]]):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


data = load_pdf_chunks('lesson.pdf')
save_to_csv('data.csv', data)