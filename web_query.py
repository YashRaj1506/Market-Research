import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an intelligent web research assistant that converts natural language user queries into precise, diverse, and informative web search queries.

Your goal:
- Understand the user's intent and topic context deeply.
- Generate 5-10 diverse, high-quality search queries that would retrieve the most relevant, recent, and insightful web results.
- Focus on queries that cover trends, reports, data, competitors, market insights, and recent developments.

### CRITICAL RULES:
1. You MUST return only a valid JSON array of strings.
2. Do NOT include any explanations, reasoning, or extra text before or after the JSON.
3. Do NOT include tags like <think>, markdown code blocks, or commentary.
4. The output MUST be directly parseable as JSON.

### Example Output:
[
  "current trends in Indian coffee market 2025",
  "coffee consumption statistics India",
  "popular coffee brands and preferences in India",
  "growth of coffee startups in India",
  "Indian coffee export and production data",
  "consumer behavior coffee India",
  "specialty coffee market size India",
  "digital marketing strategies for coffee brands India",
  "emerging coffee cafes and chains India",
  "sustainability in Indian coffee industry"
]
"""

def generate_search_queries(user_query: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=512,
        top_p=0.95,
        stream=True,
        stop=None
    )

    # Collect streamed output
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    # Attempt to extract clean JSON
    try:
        # Optional cleanup in case the model emits extra text
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        if json_start != -1 and json_end != -1:
            response_text = response_text[json_start:json_end]
        search_queries = json.loads(response_text)
    except json.JSONDecodeError:
        print("Failed to parse JSON from model output:\n", response_text)
        search_queries = []

    return search_queries


if __name__ == "__main__":
    user_input = "I wanna learn about sweet market in India, who are the top competitors, what are the latest trends and consumer preferences"
    queries = generate_search_queries(user_input)

    print(queries)
    
    # print("\n Generated Web Search Queries:")
    # for i, q in enumerate(queries, start=1):
    #     print(f"{i}. {q}")
