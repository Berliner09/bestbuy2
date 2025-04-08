# products.py
# Import the promotions module and Optional type hint
import promotions
from typing import Optional

class Product:
    """
    Represents a standard product in the store with name, price, quantity,
    active status, and an optional promotion.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a new Product instance.

        Args:
            name (str): The name of the product. Cannot be empty.
            price (float): The price of the product. Must be non-negative.
            quantity (int): The initial quantity of the product. Must be non-negative.

        Raises:
            ValueError: If name is empty, or price/quantity are negative.
        """
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Product price cannot be negative.")
        if quantity < 0:
            raise ValueError("Product quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = (quantity > 0)
        # Add promotion attribute, initially None
        self.promotion: Optional[promotions.Promotion] = None

    # --- Promotion Methods ---
    def get_promotion(self) -> Optional[promotions.Promotion]:
        """Returns the current promotion applied to the product, or None."""
        return self.promotion

    def set_promotion(self, promotion: Optional[promotions.Promotion]):
        """Sets or removes the promotion for the product."""
        if promotion is not None and not isinstance(promotion, promotions.Promotion):
            raise TypeError("Invalid promotion type provided.")
        self.promotion = promotion

    # --- Existing Methods (potentially updated) ---
    def get_quantity(self) -> int:
        """Returns the current quantity."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """Sets the quantity and updates active status."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        self.active = (self.quantity > 0)

    def is_active(self) -> bool:
        """Checks if the product is currently active."""
        return self.active

    def activate(self):
        """Activates the product."""
        self.active = True

    def deactivate(self):
        """Deactivates the product."""
        self.active = False

    def show(self) -> str:
        """Returns a string representation including promotion info if available."""
        base_info = f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base_info += f" (Promotion: {self.promotion.name})"
        return base_info

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase, applying promotion if available.

        Args:
            quantity (int): The quantity to buy. Must be positive.

        Returns:
            float: The total price for the purchased quantity (potentially discounted).

        Raises:
            ValueError: If quantity is invalid (<= 0).
            Exception: If product is inactive.
            Exception: If not enough stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        if not self.is_active():
             raise Exception(f"Cannot buy '{self.name}', product is inactive.")

        if self.quantity < quantity:
            raise Exception(f"Not enough stock for '{self.name}'. Available: {self.quantity}, Requested: {quantity}")

        # Calculate price: Use promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        # Update quantity AFTER price calculation and checks
        new_quantity = self.quantity - quantity
        self.set_quantity(new_quantity)

        return total_price

# --- Inherited Classes (Potentially updated for promotion display) ---

class NonStockedProduct(Product):
    """
    Represents a non-stocked product. Quantity is always 0.
    Can have promotions applied.
    """
    def __init__(self, name: str, price: float):
        super().__init__(name, price, 0)
        self.active = True # Always active for purchase

    def set_quantity(self, quantity: int):
        """Overrides set_quantity to prevent changing the quantity."""
        pass # Do nothing

    def buy(self, quantity: int) -> float:
        """
        Processes the 'purchase', applying promotion if available.
        Quantity doesn't change.

        Args:
            quantity (int): The quantity to 'buy'. Must be positive.

        Returns:
            float: The total price (potentially discounted).

        Raises:
            ValueError: If quantity is invalid (<= 0).
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        # Calculate price: Use promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity

        # No quantity update needed
        return total_price

    def show(self) -> str:
        """Returns a string representation including promotion info."""
        base_info = f"{self.name}, Price: ${self.price} (Non-Stocked)"
        if self.promotion:
            base_info += f" (Promotion: {self.promotion.name})"
        return base_info

class LimitedProduct(Product):
    """
    Represents a product with a maximum purchase quantity per transaction.
    Can have promotions applied.
    """
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum purchase quantity must be positive.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase, checking limit first, then applying promotion via super().buy().

        Args:
            quantity (int): The quantity to buy. Must be positive and <= maximum.

        Returns:
            float: The total price (potentially discounted).

        Raises:
            ValueError: If quantity is invalid (<= 0).
            Exception: If quantity exceeds the maximum limit.
            Exception: If product is inactive or not enough stock (from super().buy).
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        if quantity > self.maximum:
            raise Exception(f"Cannot buy {quantity} of '{self.name}'. Maximum allowed is {self.maximum}.")

        # If limit is okay, call the parent buy method which now handles promotions
        return super().buy(quantity)

    def show(self) -> str:
        """Returns a string representation including limit and promotion info."""
        # Call parent show() which includes base info + promotion
        base_info = super().show()
        # Find where the promotion info might start to insert the limit info correctly
        promo_part = ""
        if self.promotion:
            promo_part = f" (Promotion: {self.promotion.name})"
            # Remove the promotion part temporarily from base_info if it exists
            if base_info.endswith(promo_part):
                 base_info = base_info[:-len(promo_part)]

        # Add the limit info and then add the promotion info back
        return f"{base_info} (Max per purchase: {self.maximum}){promo_part}"