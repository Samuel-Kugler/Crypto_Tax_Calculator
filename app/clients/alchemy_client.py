import os
import httpx

from app.models.wallet import Wallet
from app.exceptions.domain import UnsupportedChainException


def get_url_for_wallet(wallet: Wallet) -> str:
    api_key = os.getenv("ALCHEMY_API_KEY")
    if not api_key:
        raise RuntimeError("ALCHEMY_API_KEY is missing.")

    if wallet.chain == "ETH":
        return f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"

    raise UnsupportedChainException(wallet.chain)


def fetch_transfers_for_wallet(wallet: Wallet, direction: str):
    url = get_url_for_wallet(wallet)

    if direction == "IN":
        filter_field = "toAddress"
    elif direction == "OUT":
        filter_field = "fromAddress"
    else:
        raise ValueError("direction must be 'IN' or 'OUT'.")

    params = {
        filter_field: wallet.address,
        "fromBlock": "0x0",
        "toBlock": "latest",
        "withMetadata": True,
        "excludeZeroValue": False,
        "category": ["external", "erc20"],
        "maxCount": "0x3e8",
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "alchemy_getAssetTransfers",
        "params": [params],
    }

    all_transfers = []

    with httpx.Client(timeout=20.0) as client:
        while True:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            result = data.get("result") or {}
            transfers = result.get("transfers") or []
            all_transfers.extend(transfers)

            page_key = result.get("pageKey")
            if not page_key:
                break

            params["pageKey"] = page_key
            payload["params"] = [params]

    return all_transfers
