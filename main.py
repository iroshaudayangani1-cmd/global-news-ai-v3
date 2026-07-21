from google import genai
import os


def main():

    print("===== GEMINI MODEL TEST =====")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=api_key)

    print("\nAvailable Models:\n")

    for model in client.models.list():
        print(model.name)


if __name__ == "__main__":
    main()
