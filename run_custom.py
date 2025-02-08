from dataset_adapters.custom_test import run_test
from worker import RequestParams, Worker
import asyncio
from judgers.presets import TEXT_SIMILARITY, STRICT_MATCH, MODEL_SCORING
from dotenv import load_dotenv
import os

load_dotenv()

# Worker parameters
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = "yi-lightning"
SYSTEM_PROMPT = "你是一位审题专家，请根据选择题内容，根据对应的专业知识，在A/B/C/D四个选项中，选出最合适的选项。直接给出选项前对应的字母，不要给出任何其他内容。"

OUTPUT_DIR = "results/custom_tests"
QUERY_FILE_PATH = "example_query_file.xlsx"

async def run_custom():
    """
    As the test contains custom fields, you need to specify them explicitly.
    
    - query_file_path
    - workers: Evaluation multiple models together against the file. Read README for more worker details.
    - output_dir: The directory to store the result file. e.g. OUTPUT_DIR/example_query_file_results.xlsx
    - test_mode: Only evaluate first 10 queries. For debug purposes. Default to False.
    
    Moreover, you need to specify the following test-specific fields in custom_test.py:
    
    - query_key: The key for evaluation queries. Set as your query file requires.
    - answer_key: Conduct score judging based on this key. Required for score judging.
    - response_preprocessor: Preprocess the response before score judging. Default to as_is.
    - judging_algorithm: The judging algorithm used for score judging. Preset: STRICT_MATCH (for A == A), TEXT_SIMILARITY (based on minimal editing steps), and MODEL_SCORING (submitted to a judger model).
    
    See method docstring for more details.
    """
    worker_profile=RequestParams(
        model=MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        max_tokens=128,
        system_prompt=SYSTEM_PROMPT
    )    
    worker1= Worker(worker_profile)
    
    await run_test(QUERY_FILE_PATH, 
                   [worker1], 
                   output_dir=OUTPUT_DIR, test_mode=True)
if __name__ == "__main__":
    asyncio.run(run_custom())