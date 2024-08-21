import os
from supabase import create_client, Client
from datetime import datetime, timedelta
from dotenv import load_dotenv



load_dotenv()
url: str = os.environ.get("SUPABASE_URL", '')
key: str = os.environ.get("SUPABASE_KEY", '')
supabase: Client = create_client(url, key)

def select_last_week_articles_by_source(source):
    one_week_ago: str = (datetime.now() - timedelta(days=7)).isoformat()
    return supabase.table("articles").select("url").eq("newspaper", source).gte("publish_date", one_week_ago).execute()

def insert_articles(articles_as_dicts):
    supabase.table("articles").upsert(articles_as_dicts).execute()
    print('done')