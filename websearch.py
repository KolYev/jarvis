from ddgs import DDGS

# поиск информации в DuckDuckGo
def websearch(query, max_results=3):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "Ничего не найдено."
    snippets = []
    for r in results:
        snippets.append(f"Заголовок: {r['title']}\nСсылка: {r['href']}\nТекст: {r['body']}")
    return "\n\n".join(snippets)