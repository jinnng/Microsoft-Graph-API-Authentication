import random
import string
from msal import ConfidentialClientApplication


client_id = 'your client id'
client_secret = 'your client secret'
redirect_uri = 'your azure service redirect url'
scopes = ['https://graph.microsoft.com/.default']


def generate_random_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


def authenticate_user(client_id, client_secret, redirect_uri, scopes):
    authority = 'https://login.microsoftonline.com/9c5df620-ac96-4343-883d-e2fac493dcc0'
    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    state = generate_random_state()
    auth_url = app.initiate_auth_code_flow(
        scopes=scopes,
        redirect_uri=redirect_uri,
        state=state
    )

    print(f'Please access the URL to authenticate your identity: {auth_url}')

    redirect_response = input('Please paste the redirect URL: ')
    code = app.acquire_token_by_auth_code_flow(
        redirect_response,
        scopes=scopes,
        redirect_uri=redirect_uri,
    )

    user_oid = code.get('id_token_claims').get('oid')

    return code['access_token'], user_oid


if __name__ == '__main__':
    access_token, user_oid = authenticate_user(client_id, client_secret, redirect_uri, scopes)
    print(f"User OID: {user_oid}")