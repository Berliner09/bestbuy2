# store.py
import products
from typing import List, Tuple, Any # Added Any for __add__ type hint

class Store:
    """
    Represents a store using magic methods for 'in' and '+'.
    """
    def __init__(self, product_list: List[products.Product]):
        """Initializes the store with a list of products."""
        if not isinstance(product_list, list):
             raise TypeError("Initial product list must be a list.")
        # Store the list internally
        self.products = product_list

    def add_product(self, product: products.Product):
        """Adds a product to the store."""
        if not isinstance(product, products.Product):
            raise TypeError("Only Product objects can be added.")
        self.products.append(product)
        # print(f"Product '{product.name}' added.") # Optional confirmation

    def remove_product(self, product: products.Product):
        """Removes a product from the store."""
        try:
            self.products.remove(product)
            # print(f"Product '{product.name}' removed.") # Optional confirmation
        except ValueError:
            raise ValueError(f"Product '{product.name}' not found.")

    def get_total_quantity(self) -> int:
        """Returns the total quantity of all stocked items in the store."""
        total_quantity = 0
        for product in self.products:
            # Use the quantity property
            # We should probably only sum quantities of products that track stock
            # Let's assume NonStockedProduct correctly returns 0 via its property
            total_quantity += product.quantity
        return total_quantity

    def get_all_products(self) -> List[products.Product]:
        """Returns a list of all active products in the store."""
        active_products = []
        for product in self.products:
            # Use the active property
            if product.active:
                active_products.append(product)
        return active_products

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """Processes an order."""
        total_order_price = 0.0
        if not isinstance(shopping_list, list):
            raise TypeError("Shopping list must be a list of tuples.")

        for item in shopping_list:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("Each item must be a tuple (Product, quantity).")

            product, quantity = item

            if not isinstance(product, products.Product):
                 raise TypeError("First element must be a Product.")
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")

            try:
                # Call the product's buy method (which uses properties/promotions)
                item_total_price = product.buy(quantity)
                total_order_price += item_total_price
            except Exception as e:
                raise Exception(f"Order failed for '{product.name}': {e}")

        return total_order_price

    # --- Magic Methods ---
    def __contains__(self, product: products.Product) -> bool:
        """Checks if a product exists in the store using 'in' operator."""
        # This relies on Product instances being comparable for equality,
        # which they are by default (object identity). If we needed
        # equality based on name/price, we'd need to implement __eq__ in Product.
        return product in self.products

    def __add__(self, other: Any) -> 'Store':
        """Combines two stores using the '+' operator."""
        if not isinstance(other, Store):
            # Return NotImplemented to indicate the operation is not supported
            # for the given type 'other'. This allows Python to try other.__radd__(self)
            return NotImplemented

        # Create a new list containing products from both stores
        # This creates a shallow copy; the Product objects themselves are not duplicated.
        combined_list = self.products + other.products

        # Return a new Store instance with the combined list
        return Store(combined_list)

