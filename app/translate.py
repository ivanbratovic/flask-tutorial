import requests
from flask import current_app
from flask_babel import _


def translate(text, src_language, dst_language):
    ms_key = current_app.config["MS_TRANSLATOR_KEY"]
    goog_key = current_app.config["GOOG_TRANSLATOR_KEY"]
    if not ms_key and not goog_key:
        return _("Error: the translation service is not configured.")

    success = False
    if not success:
        success, response_ms = _translate_ms(text, src_language, dst_language)
    if not success:
        success, response_goog = _translate_goog(text, src_language, dst_language)
    if not success:
        return (
            _("Error: translation service failed.")
            + f" MS: {response_ms}. Google: {response_goog}."
        )
    if response_ms:
        return response_ms
    if response_goog:
        return response_goog


def _translate_ms(text, src_language, dst_language):
    auth_headers = {
        "Ocp-Apim-Subscription-Key": current_app.config["MS_TRANSLATOR_KEY"],
        "Ocp-Apim-Subscription-Region": "westeurope",
    }
    r = requests.post(
        f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={src_language}&to={dst_language}",
        headers=auth_headers,
        json=[{"Text": text}],
    )
    if r.status_code != 200:
        return False, _("Recieved response: %(code)d", code=r.status_code)
    return True, r.json()[0]["translations"][0]["text"]


def _translate_goog(text, src_language, dst_language):
    return False, _("Google Translate is not implemented")
