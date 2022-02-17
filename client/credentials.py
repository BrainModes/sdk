class Credentials:
    """Storing the user login tokens."""

    def __init__(self, access_token, refresh_token=None):
        if not access_token:
            raise ValueError('Access token is required')

        # here the refresh token might not be necessary

        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token
