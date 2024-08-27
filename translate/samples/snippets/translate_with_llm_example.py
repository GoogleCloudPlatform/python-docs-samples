import os
from google.cloud import translate_v3 as translate

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


def translate_text(
    text: str, source_language_code: str = "en", target_language_code: str = "fr"
):
    # Create a client with the endpoint
    # Avaliable endpoints: https://cloud.google.com/translate/docs/advanced/endpoints
    client = translate.TranslationServiceClient(
        client_options={"api_endpoint": "translate.googleapis.com"}
    )

    parent = f"projects/{PROJECT_ID}/locations/us-central1"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
        model=f"projects/{PROJECT_ID}/locations/us-central1/models/general/translation-llm",
    )

    print("Translation results:")
    for translation in response.translations:
        print(translation.translated_text)


if __name__ == "__main__":
    translate_text("Hello, how are you?")