from dotenv import load_dotenv
from promptflow.core import tool
from openai.version import VERSION as OPENAI_VERSION
import os
import json

def get_client():
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    conn = dict(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    if api_key.startswith("sk-"):
        from openai import OpenAI as Client
    else:
        from openai import AzureOpenAI as Client
        conn.update(
            azure_endpoint=os.environ.get("AZURE_OPENAI_API_BASE", "azure"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-07-01-preview"),
        )
    return Client(**conn)

@tool
def call_llm(
    chapter_timeline: str,
    deployment_name: str,
    max_tokens: int = 2048,
    temperature: float = 0.5,
    top_p: float = 1.0,
    n: int = 1,
    echo: bool = False,
    presence_penalty: float = 0,
    frequency_penalty: float = 0,
    best_of: int = 1,
    logit_bias: dict = {},
    user: str = "",
    **kwargs,
) -> str:
    if "AZURE_OPENAI_API_KEY" not in os.environ or "AZURE_OPENAI_API_BASE" not in os.environ:
        # load environment variables from .env file
        load_dotenv()

    if "AZURE_OPENAI_API_KEY" not in os.environ:
        raise Exception("Please specify environment variables: AZURE_OPENAI_API_KEY")

    response = get_client().completions.create(
        prompt=chapter_timeline,
        model=deployment_name,
        max_tokens=int(max_tokens),
        temperature=float(temperature),
        top_p=float(top_p),
        n=int(n),
        echo=echo,
        presence_penalty=float(presence_penalty),
        frequency_penalty=float(frequency_penalty),
        best_of=int(best_of),
        # Logit bias must be a dict if we passed it to openai api.
        logit_bias=logit_bias if logit_bias else {},
        user=user,
    )

    chapter_timeline = response.choices[0].text
    return json.dumps(chapter_timeline, ensure_ascii=False, indent=4)

