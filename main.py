# main.py
import products # Import the module with the Product class
import store    # Import the module with the Store class

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
                        # Display product with index + 1 (user-friendly)
                        print(f"{i + 1}. {product.show()}")
                print("------")

            # --- Option 2: Show total quantity ---
            elif choice == '2':
                total_quantity = store_instance.get_total_quantity()
                print("------")
                print(f"Gesamtmenge aller Produkte im Laden: {total_quantity}")
                print("------")

            # --- Option 3: Make an order ---
            elif choice == '3':
                print("------")
                active_products = store_instance.get_all_products()
                if not active_products:
                    print("Keine Produkte zum Bestellen verfügbar.")
                    print("------")
                    continue # Back to main menu

                # Display available products for ordering
                for i, product in enumerate(active_products):
                    print(f"{i + 1}. {product.show()}")
                print("------")
                print("Wenn Sie die Bestellung abschließen möchten, geben Sie leeren Text ein.")

                shopping_list = [] # List to collect order items [(Product, quantity), ...]

                while True:
                    # Ask for product number
                    product_choice_str = input("Welche Produktnummer möchten Sie? ")
                    if not product_choice_str: # Empty input finishes selection
                        break

                    # Ask for quantity
                    amount_choice_str = input("Welche Menge möchten Sie? ")
                    if not amount_choice_str: # Empty input finishes selection
                         break

                    try:
                        product_index = int(product_choice_str) - 1 # Index is number - 1
                        amount = int(amount_choice_str)

                        # Validate product number
                        if 0 <= product_index < len(active_products):
                            chosen_product = active_products[product_index]

                            # Validate quantity (must be positive)
                            if amount > 0:
                                # Add chosen product and quantity to the shopping list
                                shopping_list.append((chosen_product, amount))
                                print("Produkt zur Liste hinzugefügt!") # User message in German
                            else:
                                print("Die Menge muss positiv sein.") # User message in German
                        else:
                            print("Ungültige Produktnummer.") # User message in German

                    except ValueError:
                        print("Ungültige Eingabe. Bitte geben Sie Zahlen für Produktnummer und Menge ein.") # User message in German
                    except IndexError:
                         print("Ungültige Produktnummer.") # Should be caught by the check above, but just in case

                # If the shopping list is not empty, try to place the order
                if shopping_list:
                    print("********")
                    try:
                        total_cost = store_instance.order(shopping_list)
                        print(f"Bestellung aufgegeben! Gesamtbetrag: ${total_cost:.2f}") # User message in German
                    except Exception as e:
                        print(f"Fehler bei der Bestellung: {e}") # User message in German
                    print("********")
                else:
                    print("Bestellvorgang abgebrochen.") # User message in German
                print("------")


            # --- Option 4: Quit ---
            elif choice == '4':
                print("Programm wird beendet. Auf Wiedersehen!") # User message in German
                break # Exit loop

            # --- Invalid input ---
            else:
                print("Ungültige Auswahl. Bitte wählen Sie eine Nummer von 1 bis 4.") # User message in German

        except Exception as e:
            # General error handling for unexpected issues
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}") # User message in German


# --- Main execution block ---
if __name__ == "__main__":
    # Setup initial inventory
    try:
        product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                         products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                         products.Product("Google Pixel 7", price=500, quantity=250)
                       ]
        # Create the Store instance
        best_buy = store.Store(product_list)

        # Start the user interface
        start(best_buy)

    except ValueError as ve:
         # Error during product initialization
         print(f"Fehler beim Initialisieren der Produkte: {ve}") # Error message in German
    except TypeError as te:
         # Error during store initialization
         print(f"Fehler beim Initialisieren des Stores: {te}") # Error message in German
    except Exception as ex:
         # Any other unexpected error during startup
         print(f"Ein unerwarteter Fehler beim Starten des Programms ist aufgetreten: {ex}") # Error message in German
