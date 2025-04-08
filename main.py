# main.py
import products
import store
import promotions # Keep promotions import if needed, though test code doesn't use it directly

# The start() function remains the same as before, allowing menu interaction
# if you want to test manually after the specific bonus tests.
def start(store_instance: store.Store):
    """
    Starts the main loop for user interaction with the store.

    Args:
        store_instance (store.Store): The store instance to operate on.
    """
    while True:
        # Display menu
        print("\n   Store Menü")
        print("   ----------")
        print("1. Alle Produkte im Laden auflisten")
        print("2. Gesamtmenge im Laden anzeigen")
        print("3. Eine Bestellung aufgeben")
        print("4. Beenden")

        # Get user input
        choice = input("Bitte wählen Sie eine Nummer: ")

        try:
            # --- Option 1: List products ---
            if choice == '1':
                print("------")
                active_products = store_instance.get_all_products()
                if not active_products:
                    print("Der Laden hat derzeit keine aktiven Produkte.")
                else:
                    for i, product in enumerate(active_products):
                        # Now uses __str__ implicitly via print()
                        print(f"{i + 1}. {product}") # Use print(product) directly
                print("------")

            # --- Option 2: Show total quantity ---
            elif choice == '2':
                total_quantity = store_instance.get_total_quantity()
                print("------")
                print(f"Gesamtmenge aller lagernden Produkte im Laden: {total_quantity}")
                print("------")

            # --- Option 3: Make an order ---
            # (Order logic remains the same, uses updated Product/Store methods)
            elif choice == '3':
                print("------")
                active_products = store_instance.get_all_products()
                if not active_products:
                    print("Keine Produkte zum Bestellen verfügbar.")
                    print("------")
                    continue

                for i, product in enumerate(active_products):
                     print(f"{i + 1}. {product}") # Uses __str__
                print("------")
                print("Wenn Sie die Bestellung abschließen möchten, geben Sie leeren Text ein.")

                shopping_list = []

                while True:
                    product_choice_str = input("Welche Produktnummer möchten Sie? ")
                    if not product_choice_str: break
                    amount_choice_str = input("Welche Menge möchten Sie? ")
                    if not amount_choice_str: break

                    try:
                        product_index = int(product_choice_str) - 1
                        amount = int(amount_choice_str)
                        if 0 <= product_index < len(active_products):
                            chosen_product = active_products[product_index]
                            if amount > 0:
                                shopping_list.append((chosen_product, amount))
                                print("Produkt zur Liste hinzugefügt!")
                            else:
                                print("Die Menge muss positiv sein.")
                        else:
                            print("Ungültige Produktnummer.")
                    except ValueError:
                        print("Ungültige Eingabe.")
                    except IndexError:
                         print("Ungültige Produktnummer.")

                if shopping_list:
                    print("********")
                    try:
                        total_cost = store_instance.order(shopping_list)
                        print(f"Bestellung aufgegeben! Gesamtbetrag: ${total_cost:.2f}")
                    except Exception as e:
                        print(f"Fehler bei der Bestellung: {e}")
                    print("********")
                else:
                    print("Bestellvorgang abgebrochen.")
                print("------")

            # --- Option 4: Quit ---
            elif choice == '4':
                print("Programm wird beendet. Auf Wiedersehen!")
                break

            # --- Invalid input ---
            else:
                print("Ungültige Auswahl. Bitte wählen Sie eine Nummer von 1 bis 4.")

        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


# --- Main execution block: UPDATED FOR BONUS STEP TESTING ---
if __name__ == "__main__":
    print("--- Testing Bonus Features ---")
    try:
        # Setup products
        mac = products.Product("MacBook Air M2", price=1450, quantity=100)
        bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
        # Test code from assignment used 'maximum=1' which implies LimitedProduct,
        # but didn't instantiate it as such. Let's create a standard product
        # as the test focuses on price comparison and store operations here.
        pixel = products.Product("Google Pixel 7", price=500, quantity=250)

        # Test setting price via property (should fail for negative)
        print("\nTesting price property setter (negative value):")
        try:
            mac.price = -100
            print("ERROR: Setting negative price did not raise exception!")
        except ValueError as e:
            print(f"OK: Caught expected error: {e}")

        # Test __str__ magic method
        print("\nTesting __str__ (print product):")
        print(mac) # Should print product info via __str__

        # Test comparison magic methods
        print("\nTesting comparison (mac > bose):")
        print(mac > bose) # Should print True

        # Test Store __contains__ magic method
        print("\nTesting 'in' operator (Store __contains__):")
        best_buy = store.Store([mac, bose])
        print(f"Is mac in best_buy? {mac in best_buy}")   # Should print True
        print(f"Is pixel in best_buy? {pixel in best_buy}") # Should print False

        # Test Store __add__ magic method
        print("\nTesting '+' operator (Store __add__):")
        other_store = store.Store([pixel])
        combined_store = best_buy + other_store
        print(f"Products in combined store ({len(combined_store.products)} items):")
        # Optionally print products in combined store
        # for prod in combined_store.products:
        #    print(f"- {prod}")

        print("\n--- Bonus Feature Testing Complete ---")

        # Optional: Start the interactive menu with the original 'best_buy' store
        # print("\n--- Starting Menu with Original Store ---")
        # start(best_buy) # Uncomment if you want to run the menu after tests

    except Exception as e:
        print(f"An error occurred during bonus testing: {e}")
