from reachscript.ai_client import GeminiClient


client = GeminiClient()

response = client.generate(
    "Give me one short sentence explaining what AI automation is."
)

print("\nGemini response:")
print(response)