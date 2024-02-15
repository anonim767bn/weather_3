class ForeignApiError(Exception):
    def __init__(self, api_name: str, status_code: int):
        super().__init__(f'Request to API {api_name} ended with {status_code}')
