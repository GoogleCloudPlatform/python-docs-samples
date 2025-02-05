
def generate_content():
    from google import genai

    client = genai.Client(http_options={'api_version': 'v1'})
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="How does AI work?"
    )
    return response.text
    # Example response:
    # Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
    #
    # Here's a simplified overview:
    # ...