from base64 import b64encode
import requests


class Client:
    def __init__(self, host, client_id, client_secret, refresh_token) -> None:
        self.access_token = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.refresh_token = refresh_token

    def get(self, path):
        if self.access_token == None:
            self._refresh()

        r = requests.get(
            f"{self.host}{path}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )

        return r.json()

    def _refresh(self):
        credentials = b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        r = requests.post(
            f"{self.host}/api/public/v1/authorization/oauth2/refresh",
            headers={"Authorization": f"Basic {credentials}"},
            json={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
        )

        self.access_token = r.json()["access_token"]
