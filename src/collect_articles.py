from typing import List
import requests
import json
from newspaper import Article, news_pool
from newspaper import ArticleException
import nltk
from tqdm import tqdm
from .llm import ask_llm
import warnings
from datetime import datetime


import newspaper
from concurrent.futures import ThreadPoolExecutor


initialized = False


def init():
    global initialized
    if not initialized:
        nltk.download("punkt_tab")
        initialized = True


def fetch_articles(url) -> List[Article]:
    init()
    np = newspaper.build(
        f"http://{url.replace('http://', '').replace('https://', '').replace('www.', '')}",
        memoize_articles=False,
        fetch_images=False,
    )

    with ThreadPoolExecutor(max_workers=2) as executor: # 2 workers so that we don't overload the server
        futures = [executor.submit(fetch_and_parse_article, article) for article in np.articles]
        for future in tqdm(futures):
            try:
                future.result()
                # articles.append(article_in_home)
            except ArticleException as e:
                warnings.warn(f"Error while fetching article: {e}")

    return np.articles

def fetch_and_parse_article(article):
    article.download()
    article.parse()


# def fetch_articles_batch(urls) -> List[List[Article]]:
#     init()
#     papers = [
#         newspaper.build(
#             f"http://{url.replace('http://', '').replace('https://', '').replace('www.', '')}",
#         )
#         for url in urls
#     ]
#     news_pool.set(papers, threads_per_source=2)
#     news_pool.join()
#     for paper in papers:
#         for article in paper.articles:
#             article.parse()
#     return [paper.articles for paper in papers]


def article_to_dict(article: Article) -> dict:
    # try until it works, max 3 times
    for _ in range(3):
        try:
            enrich = json.loads(
                ask_llm(
                    article.text,
                    system="""Return a json with the following fields, according to the content of the prompt:
                - category: one of Politics, Economy, Tech&Science, Environment, Education, Transport, Sports, Culture, BadNews, Weather, Society
                - geoarea: the geographic area of interest: may be a country name, a broader geographic area, or "World"
                - topic: five keywords, two very broad, the others more specific, representing the topic
            """,
                )
            )
            break
        except Exception as e:
            warnings.warn(f"\nError while enriching article: {e}")
            enrich = {"category": "", "geoarea": "", "topic": []}

    return {
        "title": article.title,
        "url": article.url,
        "authors": article.authors,
        "publish_date": (
            article.publish_date.strftime("%Y-%m-%d")
            if isinstance(article.publish_date, datetime)
            else article.publish_date
        ),
        "body": article.text,
        # "top_image": article.top_image,
        # "summary": article.summary,
        # "keywords": article.keywords,
        "category": enrich["category"],
        "geoarea": enrich["geoarea"],
        "topics": enrich["topic"],
    }



def transform_articles(articles: List[Article], newspaper_name: str) -> List[dict]:
    filtered_articles = [article for article in articles if article.text and len(article.text) > 10]
    results = []
    with ThreadPoolExecutor(3) as executor:
        futures = [executor.submit(lambda article: {"newspaper": newspaper_name, **article_to_dict(article)}, article) for article in filtered_articles]
        for future in tqdm(futures):
            try:
                results.append(future.result())
            except Exception as e:
                warnings.warn(f"Error while transforming article: {e}")
    return results
