# products.py

class Product:
    """
    Represents a product in the store with name, price, quantity, and active status.
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
        # Validate inputs
        if not name: # Check if name is empty or None
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Product price cannot be negative.")
        if quantity < 0:
            raise ValueError("Product quantity cannot be negative.")

        # Assign validated inputs to instance variables
        self.name = name
        self.price = price
        self.quantity = quantity
        # A new product is active by default
        self.active = True

    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product.

        Returns:
            int: The current quantity.
        """
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Sets the quantity of the product.

        If the new quantity is 0 or less, the product is deactivated.
        If the new quantity is positive, the product is activated (in case it was inactive).

        Args:
            quantity (int): The new quantity. Must be non-negative.

        Raises:
            ValueError: If the provided quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity
        # Deactivate if quantity is 0, activate otherwise
        if self.quantity == 0:
            self.deactivate()
        else:
            # Ensure product is active if quantity is positive
            # This handles cases where quantity might be set back from 0
            self.activate()


    def is_active(self) -> bool:
        """
        Checks if the product is currently active.

        Returns:
            bool: True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """
        Activates the product, making it available for purchase.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivates the product, making it unavailable.
        """
        self.active = False

    def show(self) -> str:
        """
        Returns a string representation of the product.

        Example: "MacBook Air M2, Price: 1450, Quantity: 100"

        Returns:
            str: A formatted string describing the product.
        """
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
            Exception: If the product is inactive.
            Exception: If there is not enough stock to fulfill the purchase.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be positive.")

        if not self.is_active():
             raise Exception(f"Cannot buy '{self.name}', product is inactive.")

        if self.quantity < quantity:
            raise Exception(f"Not enough stock for '{self.name}'. Available: {self.quantity}, Requested: {quantity}")

        # Calculate total price
        total_price = self.price * quantity

        # Update the product quantity
        new_quantity = self.quantity - quantity
        self.set_quantity(new_quantity) # Use set_quantity to handle deactivation if needed

        return total_price

# --- Test Code ---

"""
if __name__ == "__main__":
    try:
        print("--- Testing Product Class ---")
        bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
        mac = Product("MacBook Air M2", price=1450, quantity=100)

        print(f"Initial Bose: {bose.show()}")
        print(f"Initial Mac: {mac.show()}")

        print("\nBuying 50 Bose...")
        price_bose = bose.buy(50)
        print(f"Cost for 50 Bose: ${price_bose}")
        print(f"Bose after purchase: {bose.show()}")

        print("\nBuying 100 Mac...")
        price_mac = mac.buy(100)
        print(f"Cost for 100 Mac: ${price_mac}")
        print(f"Mac after purchase: {mac.show()}")
        print(f"Is Mac active? {mac.is_active()}") # Should be False now

        print("\nSetting Bose quantity to 1000...")
        bose.set_quantity(1000)
        print(f"Bose after setting quantity: {bose.show()}")
        print(f"Is Bose active? {bose.is_active()}") # Should be True

        # Test invalid creation
        print("\nTesting invalid creation (negative price):")
        try:
            invalid_product = Product("Invalid", -100, 10)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        # Test buying too much
        print("\nTesting buying too many Bose:")
        try:
             bose.buy(2000)
        except Exception as e:
            print(f"Caught expected error: {e}")

        # Test buying inactive product
        print("\nTesting buying inactive Mac:")
        try:
            mac.buy(1) # Mac should be inactive
        except Exception as e:
             print(f"Caught expected error: {e}")

        print("\n--- Testing Complete ---")

    except Exception as e:
        print(f"An unexpected error occurred during testing: {e}")
"""
