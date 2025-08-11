from enum import Enum
class OptionTypeEnum(str, Enum):
    SIZE = "Size"
    SUGAR = "Sugar"
    ICE = "Ice"
    TOPPING = "Topping"

class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class PaymentStatus(str,Enum):
     PENDING = "pending"
     CANCELED = "canceled"
     CONFIRMED = "confirmed"

class Method(str,Enum):
    CASH = "Cash"
    BANK_TRANSFER = "bank_transfer"