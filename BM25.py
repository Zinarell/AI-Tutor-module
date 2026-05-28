# Установка: pip install rank-bm25
import csv
from rank_bm25 import BM25Okapi
import re

def load_corpus_from_csv(filepath):
    corpus = []
    # utf-8-sig убирает BOM, если файл создан в Excel
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ожидаем колонку "text" или "chunk"
            text = row.get('text') or row.get('chunk')
            if text and text.strip():
                corpus.append(text.strip())
    return corpus

# 1. Подготовка базы знаний
knowledge_base = load_corpus_from_csv('knowledge.csv')

# 2. Простая токенизация (для русского можно добавить pymorphy2)
def tokenize_ru(text):
    return re.findall(r'[а-яёa-z0-9]+', text.lower())

tokenized_corpus = [tokenize_ru(doc) for doc in knowledge_base]

# 3. Индексируем BM25
bm25 = BM25Okapi(tokenized_corpus)

# 4. Поиск
def search_bm25(query, top_k=2):
    query_tokens = tokenize_ru(query)
    scores = bm25.get_scores(query_tokens)
    top_idx = scores.argsort()[-top_k:][::-1]  # топ по убыванию
    return [(knowledge_base[i], scores[i]) for i in top_idx]

# Тест
results = search_bm25("question")
for doc, score in results:
    print(f"⭐ {score:.3f} | {doc}")