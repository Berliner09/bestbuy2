# store.py
import products # Import the products module to use the Product class

# Type hinting for clearer code (optional but good practice)
from typing import List, Tuple

class Store:
    """
    Represents a store that holds a list of products and allows managing them
    and processing orders.
    """
    def __init__(self, product_list: List[products.Product]):
        """
        Initializes the store with a list of products.

        Args:
            product_list (List[products.Product]): A list containing Product objects.
        """
        # Input validation: Check if product_list is actually a list
        if not isinstance(product_list, list):
             raise TypeError("Initial product list must be a list.")
        # Optional: Check if all items in the list are Product instances
        # for item in product_list:
        #     if not isinstance(item, products.Product):
        #         raise TypeError("All items in product_list must be Product objects.")

        self.products = product_list

    def add_product(self, product: products.Product):
        """
        Adds a product to the store's list of products.

        Args:
            product (products.Product): The Product object to add.
        """
        # Input validation: Check if the item to add is a Product instance
        if not isinstance(product, products.Product):
            raise TypeError("Only Product objects can be added to the store.")

        self.products.append(product)
        print(f"Product '{product.name}' added to the store.") # Optional confirmation

    def remove_product(self, product: products.Product):
        """
        Removes a product from the store's list of products.

        Args:
            product (products.Product): The Product object to remove.

        Raises:
            ValueError: If the product is not found in the store.
        """
        try:
            self.products.remove(product)
            print(f"Product '{product.name}' removed from the store.") # Optional confirmation
        except ValueError:
            # This happens if the product object is not in the list
            raise ValueError(f"Product '{product.name}' not found in the store.")

    def get_total_quantity(self) -> int:
        """
        Calculates and returns the total quantity of all items in the store.

        Returns:
            int: The sum of quantities of all products in the store.
        """
        total_quantity = 0
        for product in self.products:
            total_quantity += product.get_quantity()
        return total_quantity

    def get_all_products(self) -> List[products.Product]:
        """
        Returns a list of all *active* products currently in the store.

        Returns:
            List[products.Product]: A list containing only the active Product objects.
        """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        """
        Processes an order based on a shopping list.

        The shopping list is a list of tuples, where each tuple contains:
        (Product object, quantity to buy)

        Args:
            shopping_list (List[Tuple[products.Product, int]]):
                A list of tuples, e.g., [(product1, quantity1), (product2, quantity2)].

        Returns:
            float: The total price of the completed order.

        Raises:
            ValueError: If the shopping list format is invalid or quantities are invalid.
            Exception: If any product in the list cannot be purchased (e.g., not enough stock, inactive).
                      Note: This implementation doesn't automatically handle rollback
                      if a later item in the order fails after earlier items succeeded.
                      A more robust implementation might check all items first or
                      implement a rollback mechanism.
        """
        total_order_price = 0.0

        # Basic validation of the shopping list format
        if not isinstance(shopping_list, list):
            raise TypeError("Shopping list must be a list of tuples.")

        for item in shopping_list:
            # Check if each item in the list is a tuple with 2 elements
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("Each item in the shopping list must be a tuple (Product, quantity).")

            product, quantity = item

            # Check if the first element is a Product instance
            if not isinstance(product, products.Product):
                 raise TypeError("First element in shopping list tuple must be a Product.")
            # Check if the second element is a positive integer
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Quantity in shopping list tuple must be a positive integer.")

            # Attempt to buy the product using the Product's buy method
            try:
                item_total_price = product.buy(quantity)
                total_order_price += item_total_price
                # Optional: print confirmation for each item bought
                # print(f"Bought {quantity} of '{product.name}' for ${item_total_price:.2f}")
            except Exception as e:
                # If buy() raises an error (e.g., not enough stock, inactive),
                # re-raise it to indicate the order failed.
                raise Exception(f"Order failed for '{product.name}': {e}")

        return total_order_price

# --- Test Code ---

"""
if __name__ == "__main__":
    try:
        print("--- Testing Store Class ---")

        # Create some products first (requires Product class from products.py)
        product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                        products.Product("Google Pixel 7", price=500, quantity=250),
                       ]

        # Create a store instance
        best_buy = Store(product_list)

        # Test get_all_products (should show all 3 initially)
        print("\nInitial active products:")
        all_prods = best_buy.get_all_products()
        for prod in all_prods:
            print(prod.show())

        # Test get_total_quantity
        print(f"\nTotal quantity in store: {best_buy.get_total_quantity()}") # Expected: 100 + 500 + 250 = 850

        # Test ordering
        print("\nPlacing an order: 1 MacBook, 2 Bose Earbuds...")
        # We need to use the product objects from the list we got
        order_list = [(all_prods[0], 1), (all_prods[1], 2)]
        try:
            total_price = best_buy.order(order_list)
            print(f"Order successful! Total cost: ${total_price:.2f}") # Expected: (1*1450) + (2*250) = 1450 + 500 = 1950
        except Exception as e:
            print(f"Order failed: {e}")

        # Check quantities after order
        print("\nProducts after order:")
        all_prods_after = best_buy.get_all_products()
        for prod in all_prods_after:
            print(prod.show())
        # Expected: Mac quantity 99, Bose quantity 498

        print(f"\nTotal quantity in store after order: {best_buy.get_total_quantity()}") # Expected: 99 + 498 + 250 = 847

        # Test adding a product
        print("\nAdding a new product...")
        samsung_tv = products.Product("Samsung Neo QLED TV", price=2000, quantity=50)
        best_buy.add_product(samsung_tv)
        print("\nProducts after adding TV:")
        all_prods_after_add = best_buy.get_all_products()
        for prod in all_prods_after_add:
            print(prod.show())

        # Test removing a product
        print("\nRemoving Google Pixel...")
        # Find the Pixel object to remove (assuming it's the third one initially)
        pixel_to_remove = None
        for p in best_buy.products: # Search in the full list, not just active ones
            if p.name == "Google Pixel 7":
                pixel_to_remove = p
                break
        if pixel_to_remove:
            best_buy.remove_product(pixel_to_remove)
        else:
            print("Could not find Google Pixel to remove.")

        print("\nProducts after removing Pixel:")
        all_prods_after_remove = best_buy.get_all_products()
        for prod in all_prods_after_remove:
            print(prod.show())


        # Test order that should fail (not enough stock)
        print("\nPlacing an order that should fail (150 MacBooks)...")
        fail_order_list = [(all_prods_after_remove[0], 150)] # Assuming Mac is still the first active product
        try:
            total_price = best_buy.order(fail_order_list)
            print(f"Order successful! Total cost: ${total_price:.2f}") # Should not reach here
        except Exception as e:
            print(f"Caught expected order failure: {e}")


        print("\n--- Store Testing Complete ---")

    except Exception as e:
        print(f"An unexpected error occurred during store testing: {e}")

"""
