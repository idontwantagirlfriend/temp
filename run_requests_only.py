from dataset_adapters.batch_query import batch_query
from worker import RequestParams, Worker
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = "yi-lightning"
QUERY_KEY = "question"
OUTPUT_DIR = "results/batch_query"
QUERY_FILE_PATH = "example_query_file.xlsx"
SYSTEM_PROMPT = "你是一位审题专家，请根据选择题内容，根据对应的专业知识，在A/B/C/D四个选项中，选出最合适的选项。直接给出选项前对应的字母，不要给出任何其他内容。"

async def run_requests_only():
    """
    Run requests only, without score judging
    
    - query_file_path
    - workers: Evaluation multiple models together against the file. Read README for more worker details.
    - output_dir: The directory to store the result file. e.g. "results/batch_query/example_query_file_responses.xlsx"
    - query_key: The key for evaluation queries. Default to "query".
    - test_mode: Only run first 10 queries from the file. For debuf purposes. Default to False.
    """
    worker_profile={
        "model": MODEL,
        "base_url": BASE_URL,
        "api_key": API_KEY,
        "max_tokens": 128,
        "system_prompt": SYSTEM_PROMPT
    }
    
    industrious_worker = Worker(RequestParams(**worker_profile))
    
    await batch_query(QUERY_FILE_PATH, [industrious_worker], output_dir=OUTPUT_DIR, query_key=QUERY_KEY, test_mode=True)
    
if __name__ == "__main__":
    asyncio.run(run_requests_only())