import os
import httpx
from app.models.wallet import Wallet

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
if not ALCHEMY_API_KEY:
    raise RuntimeError("ALCHEMY_API_KEY is missing.")

ALCHEMY_URLS = {
    "ETH": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
}


def get_url_for_wallet(wallet: Wallet) -> str:
    """
    Gets the url to fetch the data for a wallet.
    :param wallet: Wallet
    :return: str
    """
    try:
        return ALCHEMY_URLS[wallet.chain]
    except KeyError:
        raise RuntimeError(f"Chain '(wallet.chain)' is not supported for yet.")


def fetch_transfers_for_wallet(wallet: Wallet, direction: str):
    """Gets all the trades for a wallet.
    Checks if the transfer is going in or out."""
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
        "category": ["external", "erc20"],  # only ETH
        "maxCount": "0x3e8"  # 1000 transactions
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "alchemy_getAssetTransfers",
        "params": [params]
    }

    all_transfers = []

    with httpx.Client(timeout=20.0) as client:
        while True:
            #requesting
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            #processing
            result = data.get("result") or {}
            transfers = result.get("transfers") or []
            all_transfers.extend(transfers)

            #pages
            page_key = result.get("pageKey")
            if not page_key:
                break

            params["pageKey"] = page_key
            payload["params"] = [params]

    return all_transfers
