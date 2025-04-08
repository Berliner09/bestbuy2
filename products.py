# products.py
import promotions
from typing import Optional, Any # Added Any for comparison type hint

class Product:
    """
    Represents a product using properties and magic methods.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """Initializes a Product instance."""
        if not name:
            raise ValueError("Product name cannot be empty.")
        # Use setters for initial validation and setup
        self.name = name # Keep name as a direct attribute for simplicity
        self.price = price
        self.quantity = quantity # This will also set initial active status via the setter
        self._promotion: Optional[promotions.Promotion] = None # Internal storage for promotion

    # --- Price Property ---
    @property
    def price(self) -> float:
        """Gets the product price."""
        return self._price

    @price.setter
    def price(self, value: float):
        """Sets the product price, ensuring it's non-negative."""
        if value < 0:
            raise ValueError("Product price cannot be negative.")
        self._price = value

    # --- Quantity Property (also manages active status) ---
    @property
    def quantity(self) -> int:
        """Gets the product quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """Sets the product quantity and updates active status accordingly."""
        if value < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = value
        # Automatically update active status based on quantity
        self._active = (self._quantity > 0)

    # --- Active Property (Read-Only) ---
    @property
    def active(self) -> bool:
        """Gets the active status (derived from quantity > 0)."""
        # Note: The _active attribute is managed by the quantity setter
        return self._active

    # --- Promotion Property ---
    @property
    def promotion(self) -> Optional[promotions.Promotion]:
        """Gets the current promotion."""
        return self._promotion

    @promotion.setter
    def promotion(self, value: Optional[promotions.Promotion]):
        """Sets or removes the promotion."""
        if value is not None and not isinstance(value, promotions.Promotion):
            raise TypeError("Invalid promotion type provided.")
        self._promotion = value

    # --- Magic Methods ---
    def __str__(self) -> str:
        """Returns a user-friendly string representation."""
        base_info = f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base_info += f" (Promotion: {self.promotion.name})"
        return base_info

    def __lt__(self, other: Any) -> bool:
        """Compares product price using < operator."""
        if not isinstance(other, Product):
            return NotImplemented # Indicate comparison is not supported
        return self.price < other.price

    def __gt__(self, other: Any) -> bool:
        """Compares product price using > operator."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    # --- Buy Method (uses properties internally) ---
    def buy(self, quantity: int) -> float:
        """Processes purchase, applying promotions if available."""
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        # Use the 'active' property for the check
        if not self.active:
             raise Exception(f"Cannot buy '{self.name}', product is inactive.")

        # Use the 'quantity' property for the check
        if self.quantity < quantity:
            raise Exception(f"Not enough stock for '{self.name}'. Available: {self.quantity}, Requested: {quantity}")

        # Calculate price using promotion property
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity # Use price property

        # Update quantity using the property setter (which also updates active status)
        self.quantity -= quantity

        return total_price

# --- Inherited Classes (Updated to use properties and __str__) ---

class NonStockedProduct(Product):
    """Non-stocked product using properties."""
    def __init__(self, name: str, price: float):
        # Initialize with quantity 0, price setter handles validation
        super().__init__(name, price, 0)
        # Non-stocked are always considered active for purchase, override status set by quantity setter
        self._active = True

    @property
    def quantity(self) -> int:
        """Quantity is always 0."""
        return 0 # Override getter

    @quantity.setter
    def quantity(self, value: int):
        """Prevent setting quantity."""
        pass # Do nothing, quantity stays 0

    # Active property override (always True)
    @property
    def active(self) -> bool:
        return True

    def buy(self, quantity: int) -> float:
        """Processes 'purchase', applies promotion."""
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")
        # Calculate price using promotion property
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = self.price * quantity # Use price property
        # No quantity update
        return total_price

    def __str__(self) -> str:
        """String representation for non-stocked product."""
        base_info = f"{self.name}, Price: ${self.price} (Non-Stocked)"
        if self.promotion:
            base_info += f" (Promotion: {self.promotion.name})"
        return base_info

class LimitedProduct(Product):
    """Limited product using properties."""
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum purchase quantity must be positive.")
        self.maximum = maximum # Keep maximum as a direct attribute

    def buy(self, quantity: int) -> float:
        """Processes purchase, checking limit first."""
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")
        if quantity > self.maximum:
            raise Exception(f"Cannot buy {quantity} of '{self.name}'. Maximum allowed is {self.maximum}.")
        # Call parent buy method (which uses properties and handles promotions)
        return super().buy(quantity)

    def __str__(self) -> str:
        """String representation including limit and promotion."""
        # Get base string from parent (includes name, price, quantity, promotion)
        base_info = super().__str__()
        # Find where promotion info starts (if it exists) to insert limit info
        promo_part = ""
        if self.promotion:
            promo_part = f" (Promotion: {self.promotion.name})"
            if base_info.endswith(promo_part):
                base_info = base_info[:-len(promo_part)] # Remove promo temporarily

        # Add limit info and re-append promo info
        return f"{base_info} (Max per purchase: {self.maximum}){promo_part}"
