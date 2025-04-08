# promotions.py
from abc import ABC, abstractmethod
# Use forward reference for type hint to avoid circular import if Product needs Promotion
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import products

class Promotion(ABC):
    """
    Abstract base class for all promotions.
    """
    def __init__(self, name: str):
        if not name:
            raise ValueError("Promotion name cannot be empty.")
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: 'products.Product', quantity: int) -> float:
        """
        Applies the promotion to a given product and quantity.

        Args:
            product (Product): The product instance the promotion is applied to.
                               We use the product's price from this instance.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The total discounted price for the given quantity.
        """
        pass

class PercentDiscount(Promotion):
    """Applies a percentage discount to the total price."""
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        if not 0 <= percent <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percent = percent

    def apply_promotion(self, product: 'products.Product', quantity: int) -> float:
        """Calculates the price after applying the percentage discount."""
        discount_multiplier = 1 - (self.percent / 100)
        total_price = product.price * quantity * discount_multiplier
        return total_price

class SecondHalfPrice(Promotion):
    """Second item purchased is half price."""
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product: 'products.Product', quantity: int) -> float:
        """Calculates the price where every second item is half price."""
        full_price_items = (quantity + 1) // 2  # Integer division rounds down
        half_price_items = quantity // 2
        total_price = (full_price_items * product.price) + (half_price_items * product.price * 0.5)
        return total_price

class ThirdOneFree(Promotion):
    """Third item purchased is free (buy 2, get 1 free)."""
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product: 'products.Product', quantity: int) -> float:
        """Calculates the price where every third item is free."""
        # Number of free items
        free_items = quantity // 3
        # Number of paid items
        paid_items = quantity - free_items
        total_price = paid_items * product.price
        return total_price
