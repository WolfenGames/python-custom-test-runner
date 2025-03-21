from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from requests import Response, request
from typing import Optional, Dict, Union, Any


class IRequestSender(ABC):
    """Abstraction for sending HTTP requests to enable dependency injection."""
    
    @abstractmethod
    def send(self, method: str, url: str, **kwargs) -> Response:
        pass


class RequestsSender(IRequestSender):
    """Concrete implementation using `requests` library."""
    
    def send(self, method: str, url: str, **kwargs) -> Response:
        return request(method=method, url=url, **kwargs)


class IResponseParser(ABC):
    """Abstraction for response parsing to allow different implementations."""

    @abstractmethod
    def parse(self, response: Response) -> Any:
        pass


class JsonResponseParser(IResponseParser):
    """Default response parser handling JSON responses gracefully."""

    def parse(self, response: Response) -> Any:
        try:
            return response.json()
        except ValueError:
            return response.text


class IHeaderGenerator(ABC):
    """Abstraction for custom header generation."""

    @abstractmethod
    def generate_headers(self, access_token: Optional[str], extra_headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        pass


class DefaultHeaderGenerator(IHeaderGenerator):
    """Concrete header generator with default behavior."""

    def generate_headers(self, access_token: Optional[str], extra_headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        headers = {
            "Authorization": str(access_token) if access_token else "",
            "Content-Type": "application/fhir+json",
            "AORTA-ID": f"initialRequestID={uuid.uuid4()}; requestID={uuid.uuid4()}",
            "XLSPFQDNINFO": "ncare-test.ezorg.aorta-zorg.nl"
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers


class TestBase:
    """Base class for making API requests while adhering to SOLID principles."""

    def __init__(
        self,
        url: str,
        sender: IRequestSender = None,
        response_parser: IResponseParser = None,
        header_generator: IHeaderGenerator = None
    ) -> None:
        self.url = url
        self.sender = sender or RequestsSender()
        self.response_parser = response_parser or JsonResponseParser()
        self.header_generator = header_generator or DefaultHeaderGenerator()

    def send_request(
        self,
        method: str,
        endpoint: str,
        access_token: Optional[str] = None,
        data: Union[str, Dict, None] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Response:
        request_url = f"{self.url}{endpoint}"
        request_headers = self.header_generator.generate_headers(access_token, headers)

        request_kwargs = {
            "headers": request_headers,
            "params": params
        }

        request_kwargs["data"] = data

        # Log input request
        self.input_request = {
            "method": method,
            "url": request_url,
            "headers": request_headers,
            "params": params,
            "input": data
        }

        # Send request via dependency-injected sender
        response = self.sender.send(method, request_url, **request_kwargs)

        # Parse response using injected parser
        parsed_response = self.response_parser.parse(response)

        # Log output response
        self.output = {
            "headers": dict(response.headers),
            "status_code": response.status_code,
            "response": parsed_response
        }

        return response
