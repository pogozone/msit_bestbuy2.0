"""Erstellt das Sortiment und startet die Anwendung."""

import product
import promotion
import store


def go_ahead(this_store, choice):
    """Verarbeitet eine Menüauswahl und meldet, ob es weitergeht."""
    try:
        choice = int(choice)
    except ValueError:
        print("\nBitte gib eine Zahl von 1 bis 7 ein.\n")
        return True

    if choice == 1:
        print("\nVerfügbare Produkte im Shop:\n")
        this_store.show_all_products()

    elif choice == 2:
      
        print(f"\nGesamtmenge im Shop: {this_store.get_total_quantity()}")

    elif choice == 3:
        make_order(this_store)

    elif choice == 4:
        this_store.show_basket()
        return True

    elif choice == 5:
        this_store.clear_order()
        print("\nBestellung abgebrochen. Bestand wurde wiederhergestellt.")
        return True

    elif choice == 6:
        checkout_basket(this_store)
        return True

    elif choice == 7:
        print("\nAuf Wiedersehen!")
        return False

    else:
        print("\nBitte gib eine Zahl von 1 bis 7 ein.\n")

    return True


def checkout_basket(this_store):
    """Finalisiert die Bestellung und gibt den Beleg aus."""
    receipt = this_store.checkout_basket()
    if receipt is None:
        print("\nDein Warenkorb ist leer. Es gibt nichts zu bestellen.")
        return

    print("\n===== Bestellbeleg =====")
    for index, item in enumerate(receipt["items"], start=1):
        print(
            f"{index}. {item['name']} | "
            f"Menge: {item['amount']} | "
            f"Zwischensumme: {item['total_price']:.2f} €"
        )
    print("------------------------")
    print(f"Gesamtbetrag: {receipt['total']:.2f} €")
    print("Vielen Dank für deine Bestellung! Der Warenkorb ist nun leer.")


def make_order(this_store):
    """Erlaubt mehrere Artikel und behandelt ungültige Eingaben."""
    while True:
        # Nach jedem Kauf die aktuelle Liste neu laden.
        available_products = this_store.get_all_products()
        if not available_products:
            print("\nKeine Produkte verfügbar.")
            return

        print("\nVerfügbare Produkte:\n")
        this_store.show_all_products()

        try:
            number = int(input("\nProduktnummer wählen: "))
            if not 1 <= number <= len(available_products):
                print("Dieses Produkt gibt es nicht.")
                continue
            amount = int(input("\nGewünschte Menge: "))
        except ValueError:
            print("Bitte gib eine ganze Zahl ein.")
            continue

        this_product = available_products[number - 1]
        try:
            total = this_store.order([(this_product, amount)])
        except ValueError as error:
            print(f"Bestellung nicht möglich: {error}")
            continue

        print(f"\nWarenkorb-Summe: {total:.2f} €")
        this_store.show_basket()

        while True:
            answer = input(
                "\nWeiteren Artikel hinzufügen? (j/n): "
            ).strip().lower()
            if answer in ("n", "no", "nein"):
                return
            if answer in ("y", "yes", "j", "ja"):
                break
            print("Bitte j oder n eingeben.")


def start(this_store):
    """Zeigt das Hauptmenü."""
    menu = [
        "Alle Produkte im Shop anzeigen",
        "Gesamtmenge im Shop anzeigen",
        "In den Warenkorb legen",
        "Warenkorb anzeigen",
        "Warenkorb leeren",
        "Bestellung abschließen",
        "Beenden",
    ]
    while True:
        print("\n===== Best Buy =====\n")
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item}")
        choice = input("\nBitte wähle eine Nummer: ").strip()
        if not go_ahead(this_store, choice):
            break


def main():

    # setup initial stock of inventory
    """Erstellt das Sortiment und startet die Anwendung."""
    product_list = [
        product.Product("MacBook Air M2", price=1450, quantity=100),
        product.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        product.Product("Google Pixel 7", price=500, quantity=250),
        product.NonStockedProduct("Windows License", price=125),
        product.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = promotion.SecondHalfPrice("Zweites Stück zum halben Preis!")
    third_one_free = promotion.ThirdOneFree("Jedes dritte Stück gratis!")
    thirty_percent = promotion.PercentDiscount("30 % Rabatt!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)

    start(best_buy)


if __name__ == "__main__":
    main()