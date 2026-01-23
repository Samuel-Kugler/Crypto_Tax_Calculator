class WalletNotFoundException(Exception):
    def __init__(self, details: str = "Wallet not found"):
        self.details = details
        super().__init__(details)


class UnsupportedChainException(Exception):
    def __init__(self, chain: str):
        self.chain = chain
        self.details = f"Chain '{chain}' is not supported."
        super().__init__(self.details)


class DatabaseWriteException(Exception):
    def __init__(self, details: str = "Failed to write data to databse"):
        self.details = details
        super().__init__(self.details)
