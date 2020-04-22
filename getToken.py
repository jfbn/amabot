import requests
import requests.auth
from creds import secret, client_id

client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
post_data = {"grant_type": "password", "username": "reddit_bot", "password": "snoo"}
