import enum


class BlockchainEnum(str, enum.Enum):
    ETH = "ETH"


class ActivityEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"
