from typing import List
import requests
import os
import anthropic
from openai import OpenAI
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()


def ask_llm_anthropic(question, system="provide a short answer"):

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        system=system,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": question}],
            }
        ],
    )

    return next(
        (block.text for block in message.content if isinstance(block, TextBlock)),
        '',
    )


def ask_llm_openai(question, system="provide a short answer"):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
    )
    return completion.choices[0].message



def ask_llm(question, system="provide a short answer"):
    return ask_llm_anthropic(question, system)