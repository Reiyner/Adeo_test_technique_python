import pytest 
import httpx
from adeo.client import Client

from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_do_not_retry_on_sucess():
    url  = 'https://test.org'
    max_retries = 2
    mock_client = AsyncMock()
    mock_client.get.side_effect = [
        httpx.Response(200, request=httpx.Request("GET",url)),
        ConnectionError('Connection Error')
    ]

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = Client(max_retries=max_retries)
        response = await client.get(url=url)

        assert response.status_code == 200


        assert mock_client.get.call_count == 1


@pytest.mark.asyncio
async def test_retries_true():
    url  = 'https://test.org'
    max_retries = 2
    mock_client = AsyncMock()
    mock_client.get.side_effect = [
        ConnectionError('Connection Error'),
        httpx.Response(200, request=httpx.Request("GET",url))
    ]

    with patch("httpx.AsyncClient", return_value=mock_client):
        client = Client(max_retries=max_retries)
        response = await client.get(url=url)

        assert response.status_code == 200

        assert mock_client.get.call_count == 2

@pytest.mark.asyncio
async def test_max_retries():
    mock_client = AsyncMock()
    mock_client.get.side_effect = ConnectionError("Connection error")

    with patch("httpx.AsyncClient",return_value=mock_client):
        url = "https://test.org"
        max_retires =  3
        client = Client(max_retries=max_retires)
        await client.get(url=url)

        assert mock_client.get.call_count == max_retires




