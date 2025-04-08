# products.py

class Product:
    """
    Represents a standard product in the store with name, price, quantity,
    and active status.
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
        # A new product is active by default, unless quantity is 0 initially
        self.active = (quantity > 0)

    def get_quantity(self) -> int:
        """Returns the current quantity."""
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Sets the quantity of the product.

        If the new quantity is 0 or less, the product is deactivated.
        If the new quantity is positive, the product is activated.

        Args:
            quantity (int): The new quantity. Must be non-negative.

        Raises:
            ValueError: If the provided quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        self.active = (self.quantity > 0) # Update active status based on quantity

    def is_active(self) -> bool:
        """Checks if the product is currently active."""
        return self.active

    def activate(self):
        """Activates the product."""
        # We might want activation to depend on quantity > 0 as well
        # For now, let's keep the simple activation flag logic
        # but set_quantity handles the quantity-based activation/deactivation
        self.active = True

    def deactivate(self):
        """Deactivates the product."""
        self.active = False

    def show(self) -> str:
        """Returns a string representation of the product."""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase of a given quantity of the product.

        Args:
            quantity (int): The quantity to buy. Must be positive.

        Returns:
            float: The total price for the purchased quantity.

        Raises:
            ValueError: If the requested quantity is invalid (<= 0).
            Exception: If the product is inactive (and quantity > 0).
                       Note: We allow buying 0 quantity of inactive items, maybe? Let's stick to raising error if inactive.
            Exception: If there is not enough stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        # Check if active *before* checking quantity, standard products must be active to be bought
        if not self.is_active():
             raise Exception(f"Cannot buy '{self.name}', product is inactive.")

        if self.quantity < quantity:
            raise Exception(f"Not enough stock for '{self.name}'. Available: {self.quantity}, Requested: {quantity}")

        total_price = self.price * quantity
        new_quantity = self.quantity - quantity
        self.set_quantity(new_quantity) # Updates quantity and active status

        return total_price

# --- New Inherited Classes ---

class NonStockedProduct(Product):
    """
    Represents a product that doesn't have a physical stock (e.g., software license).
    Quantity is always considered 0 and it's always active for purchase.
    """
    def __init__(self, name: str, price: float):
        """
        Initializes a NonStockedProduct. Quantity is fixed at 0.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
        """
        # Call the parent constructor, but force quantity to 0
        super().__init__(name, price, 0)
        # Non-stocked products are always considered 'purchasable', so set active=True
        # even though quantity is 0. This overrides the logic in the parent __init__.
        self.active = True

    def set_quantity(self, quantity: int):
        """Overrides set_quantity to prevent changing the quantity."""
        # Do nothing, quantity always stays 0 for NonStockedProduct
        # We could also raise an error here if desired:
        # raise TypeError("Cannot set quantity for NonStockedProduct")
        pass # Keep quantity at 0

    def buy(self, quantity: int) -> float:
        """
        Processes the 'purchase' of a non-stocked item.
        Quantity doesn't decrease, just calculates price.

        Args:
            quantity (int): The quantity to 'buy'. Must be positive.

        Returns:
            float: The total price for the purchased quantity.

        Raises:
            ValueError: If the requested quantity is invalid (<= 0).
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        # No stock check needed, no quantity update needed.
        # Always active, so no active check needed either.
        total_price = self.price * quantity
        return total_price

    def show(self) -> str:
        """Returns a string representation indicating it's non-stocked."""
        # Get the base representation from the parent class
        # base_info = super().show() # This would show Quantity: 0
        # return f"{base_info} (Non-Stocked)"
        # Or create a custom string without quantity:
        return f"{self.name}, Price: ${self.price} (Non-Stocked)"

class LimitedProduct(Product):
    """
    Represents a product that can only be purchased up to a maximum
    quantity per single purchase transaction.
    """
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a LimitedProduct.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            quantity (int): The initial quantity of the product.
            maximum (int): The maximum allowed quantity per purchase. Must be positive.
        """
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum purchase quantity must be positive.")
        self.maximum = maximum

    def buy(self, quantity: int) -> float:
        """
        Processes the purchase, checking against the maximum limit first.

        Args:
            quantity (int): The quantity to buy. Must be positive and <= maximum.

        Returns:
            float: The total price for the purchased quantity.

        Raises:
            ValueError: If quantity is invalid (<= 0).
            Exception: If quantity exceeds the maximum allowed limit.
            Exception: If product is inactive or not enough stock (from super().buy).
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        # Check the purchase limit specific to this class
        if quantity > self.maximum:
            raise Exception(f"Cannot buy {quantity} of '{self.name}'. Maximum allowed is {self.maximum}.")

        # If limit is okay, proceed with the normal buy logic (stock check, quantity update)
        # by calling the parent class's buy method.
        return super().buy(quantity)

    def show(self) -> str:
        """Returns a string representation including the purchase limit."""
        # Get the base representation from the parent class
        base_info = super().show()
        return f"{base_info} (Max per purchase: {self.maximum})"

