from __future__ import annotations
import uuid
from requests import Response, request

class TestBase:
    def __init__(self, url: str) -> None:
        self.url = url

    def _send(
        self,
        method: str,
        endpoint: str,
        access_token: str | None = None,
        data: str | dict | None = None,
        params: dict | None = None,
        headers: dict | None = None
    ) -> Response:
        request_url = f"{self.url}{endpoint}"
        request_headers = {
            "Authorization": str(access_token) if access_token else "",
            "Content-Type": "application/fhir+json",
            "AORTA-ID": f"initialRequestID={uuid.uuid4()}; requestID={uuid.uuid4()}",
            "XLSPFQDNINFO": "ncare-test.ezorg.aorta-zorg.nl"
        }
        
        if headers:
            request_headers.update(headers)

        request_kwargs = {
            "method": method,
            "url": request_url,
            "headers": request_headers,
            "params": params
        }

        if isinstance(data, dict):
            request_kwargs["json"] = data
        else:
            request_kwargs["data"] = data

        self.input_request = {
            "method": method,
            "url": request_url,
            "headers": request_headers,
            "params": params,
            "input": data
        }

        response = request(**request_kwargs)

        self.output = {
            "headers": dict(response.headers),
            "status_code": response.status_code,
            "response": self._parse_response(response)
        }

        return response

    @staticmethod
    def _parse_response(response: Response):
        """Helper method to safely parse JSON responses."""
        try:
            return response.json()
        except ValueError:
            return response.text
