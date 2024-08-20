import os
from supabase import create_client, Client

from dotenv import load_dotenv

from .collect_articles import article_to_dict


load_dotenv()
url: str = os.environ.get("SUPABASE_URL", '')
key: str = os.environ.get("SUPABASE_KEY", '')
supabase: Client = create_client(url, key)

def insert_articles(articles_as_dicts):
    supabase.table("articles").upsert(articles_as_dicts).execute()
    print('done')