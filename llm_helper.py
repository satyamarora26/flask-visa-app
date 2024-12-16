import os
import openai

# Set your API key
openai.api_key = "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"


def refine_answer_with_llm(user_query, raw_answer):
    """
    Refine the raw answer using OpenAI's GPT-3.5.
    """
    prompt = f"""
    The user asked: "{user_query}"

    The database returned this raw information: "{raw_answer}"

    Please provide a concise, helpful, and user-friendly answer to the user’s query, considering the provided data. 
    If additional relevant context is needed based on general knowledge of the Visitor Visa (Subclass 600), you may include it, 
    but ensure accuracy and clarity.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant specialized in Australian visas."},
                      {"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        # Extract and return the refined response
        refined_answer = response.choices[0].message['content'].strip()
        return refined_answer
    except Exception as e:
        return f"Error in refining answer: {str(e)}"
