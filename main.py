# main.py
import products # Importiert das Modul mit der Product-Klasse
import store    # Importiert das Modul mit der Store-Klasse
import promotions # Importiert das Modul mit den Promotion-Klassen

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
                        # Uses the show() method which now includes promotion info
                        print(f"{i + 1}. {product.show()}")
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
                                shopping_list.append((chosen_product, amount))
                                print("Produkt zur Liste hinzugefügt!") # User message in German
                            else:
                                print("Die Menge muss positiv sein.") # User message in German
                        else:
                            print("Ungültige Produktnummer.") # User message in German

                    except ValueError:
                        print("Ungültige Eingabe. Bitte geben Sie Zahlen für Produktnummer und Menge ein.") # User message in German
                    except IndexError:
                         print("Ungültige Produktnummer.")

                # If the shopping list is not empty, try to place the order
                if shopping_list:
                    print("********")
                    try:
                        # store.order() uses product.buy(), which now applies promotions!
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
    # Setup initial inventory - Same as Step 2 test
    try:
        product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                         products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                         products.Product("Google Pixel 7", price=500, quantity=250),
                         products.NonStockedProduct("Windows License", price=125),
                         products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                       ]

        # Create promotion catalog - NEW for Step 3 test
        second_half_price = promotions.SecondHalfPrice("Second Half price!")
        third_one_free = promotions.ThirdOneFree("Third One Free!")
        thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

        # Add promotions to products - NEW for Step 3 test
        # Note: Indices match the order in product_list above
        product_list[0].set_promotion(second_half_price)  # MacBook
        product_list[1].set_promotion(third_one_free)     # Bose
        product_list[3].set_promotion(thirty_percent)     # Windows License (index 3)

        # Create the Store instance with the modified product list
        best_buy = store.Store(product_list)

        # Start the user interface
        start(best_buy)

    except ValueError as ve:
         print(f"Fehler beim Initialisieren der Produkte/Promotions: {ve}") # Error message in German
    except TypeError as te:
         print(f"Fehler beim Initialisieren des Stores/Promotions: {te}") # Error message in German
    except Exception as ex:
         print(f"Ein unerwarteter Fehler beim Starten des Programms ist aufgetreten: {ex}") # Error message in German
