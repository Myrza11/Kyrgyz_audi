import http.client
import json

def get_tts_response(text, speaker_id, token):
    conn = http.client.HTTPSConnection("tts_domen")
    payload = json.dumps({
      "text": text,
      "speaker_id": speaker_id
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}'
    }
    conn.request("POST", "/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

text_to_convert = "Привет, как дела?"
speaker_id = "1"
access_token = "<ulut token>"

tts_response = get_tts_response(text_to_convert, speaker_id, access_token)

