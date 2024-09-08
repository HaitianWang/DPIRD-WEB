import openai
openai.api_key = "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"  # This is api-key for OpenAI and it should be replaced by your own


# Function to analyze text using GPT
def analyze_text(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        gpt_reply = response.choices[0].text.strip()
        return gpt_reply

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Print OpenAI library version
    print("openai-version", openai.__version__)

    # Analyze text using GPT
    analysis_prompt = "tell me what is 1+1"
    weed_removal_suggestions = analyze_text(analysis_prompt)

    # Print suggestions
    print("suggestions:", weed_removal_suggestions)

if __name__ == "__main__":
    main()
