# main.py
import products
import store
# promotions import moved to setup_store function

# The start() function remains the same as before, allowing menu interaction
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
                        print(f"{i + 1}. {product}")
                print("------")

            # --- Option 2: Show total quantity ---
            elif choice == '2':
                total_quantity = store_instance.get_total_quantity()
                print("------")
                print(f"Gesamtmenge aller lagernden Produkte im Laden: {total_quantity}")
                print("------")

            # --- Option 3: Make an order ---
            elif choice == '3':
                print("------")
                active_products = store_instance.get_all_products()
                if not active_products:
                    print("Keine Produkte zum Bestellen verfügbar.")
                    print("------")
                    continue

                for i, product in enumerate(active_products):
                     print(f"{i + 1}. {product}")
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
                    # Renamed exception variable 'e' to 've' to avoid shadowing
                    except ValueError as ve:
                        print(f"Ungültige Eingabe: {ve}")
                    # Renamed exception variable 'e' to 'ie' to avoid shadowing
                    except IndexError as ie:
                         # This specific error message might not be needed if the index check above works
                         print(f"Fehler bei Produktindex: {ie}")

                if shopping_list:
                    print("********")
                    try:
                        total_cost = store_instance.order(shopping_list)
                        print(f"Bestellung aufgegeben! Gesamtbetrag: ${total_cost:.2f}")
                    # Renamed inner exception variable 'e' to 'order_ex' to avoid shadowing
                    except Exception as order_ex:
                        print(f"Fehler bei der Bestellung: {order_ex}")
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

        # Renamed outer exception variable 'e' to 'menu_ex' to avoid shadowing
        except Exception as menu_ex:
            print(f"Ein unerwarteter Fehler im Menü ist aufgetreten: {menu_ex}")


def setup_store() -> store.Store:
    """Sets up the initial store inventory and promotions."""
    # Import promotions only where needed
    import promotions

    # Setup initial inventory with different product types
    product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                     products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                     products.Product("Google Pixel 7", price=500, quantity=250),
                     products.NonStockedProduct("Windows License", price=125),
                     products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                   ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price  # MacBook
    product_list[1].promotion = third_one_free     # Bose
    product_list[3].promotion = thirty_percent     # Windows License

    # Create and return the Store instance
    return store.Store(product_list)


# --- Main execution block: Now calls setup function ---
if __name__ == "__main__":
    print("--- Best Buy Store 2.0 ---")
    try:
        # Get the initialized store from the setup function
        best_buy = setup_store()
        # Start the user interface
        start(best_buy)

    # Keep 'e' here, as it's the top-level exception handler for setup
    except Exception as e:
        # Catch potential errors during setup
        print(f"Ein Fehler ist beim Initialisieren des Shops aufgetreten: {e}")

