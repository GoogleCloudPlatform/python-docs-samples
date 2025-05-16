# from http import HTTPStatus

# from google.auth.transport import requests
# from google.oauth2 import id_token

'''
@app.route("/info")
def info() -> str:
    """Show instance information for debugging."""

    target_audience = SERVICE_URL
    auth_req = requests.Request()

    token_client_library = id_token.fetch_id_token(auth_req, target_audience)

    response = f"{SERVICE_NAME=}<br>\n{PROJECT_ID=}<br>\n" \
        + f"{PROJECT_NUMBER=}<br>\n{REGION=}<br>\n" \
        + f"{SERVICE_URL=}<br>\n{TOKEN_JSON_RESPONSE=}<br>\n" \
        + f"{token_client_library}<br>\n"

    return response, HTTPStatus.OK
'''

# https://cloud.google.com/run/docs/container-contract#metadata-server
# https://cloud.google.com/compute/docs/access/authenticate-workloads#applications
