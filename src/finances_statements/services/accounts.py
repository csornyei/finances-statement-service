import os

import httpx
from finances_shared.models import Account
from pydantic import BaseModel

ACCOUNTS_URL = os.getenv("ACCOUNTS_URL")


class CreateAccount(BaseModel):
    name: str
    iban: str
    nickname: str


def get_account_by_iban(iban: str) -> list[Account]:
    """
    Fetch account details by IBAN from the external accounts service.
    """

    if not ACCOUNTS_URL:
        raise ValueError("ACCOUNTS_URL environment variable is not set.")

    url = f"{ACCOUNTS_URL}/api/v1/accounts?iban={iban}"

    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Error fetching account: {e.response.text}")
    except Exception as e:
        raise ValueError(f"An error occurred while fetching account: {str(e)}")


def get_account_by_name_and_iban(name: str, iban: str) -> list[Account]:
    """
    Fetch account details by name and IBAN from the external accounts service.
    """

    if not ACCOUNTS_URL:
        raise ValueError("ACCOUNTS_URL environment variable is not set.")

    url = f"{ACCOUNTS_URL}/api/v1/accounts?name={name}&iban={iban}"

    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Error fetching account: {e.response.text}")
    except Exception as e:
        raise ValueError(f"An error occurred while fetching account: {str(e)}")


def create_account(account_data: dict):
    """
    Create a new account in the external accounts service.
    """

    if not ACCOUNTS_URL:
        raise ValueError("ACCOUNTS_URL environment variable is not set.")

    url = f"{ACCOUNTS_URL}/api/v1/accounts"

    validated_account = CreateAccount(**account_data)

    try:
        response = httpx.post(url, json=validated_account.model_dump())
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"Error creating account: {e.response.text}")
    except Exception as e:
        raise ValueError(f"An error occurred while creating account: {str(e)}")
