# test_product.py
import pytest
# Stelle sicher, dass products.py im selben Verzeichnis oder im Python-Pfad ist
import products

def test_create_normal_product():
    """Test creating a product with valid details using properties."""
    product = products.Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    # Use the 'active' property instead of is_active() method
    assert product.active is True

def test_create_product_invalid_details():
    """Test creating a product with invalid details raises ValueError."""
    # Test empty name
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        products.Product("", price=1450, quantity=100)

    # Test negative price using property setter
    with pytest.raises(ValueError, match="Product price cannot be negative"):
        # Test setting via __init__ which uses the setter
        products.Product("MacBook Air M2", price=-10, quantity=100)
        # Optionally, test direct setting if needed (though covered by init)
        # p = products.Product("Test", 10, 10)
        # p.price = -10

    # Test negative quantity using property setter
    # Adjust expected error message to match the one raised by the property setter
    with pytest.raises(ValueError, match="Quantity cannot be negative."):
         # Test setting via __init__ which uses the setter
        products.Product("MacBook Air M2", price=1450, quantity=-5)
        # Optionally, test direct setting if needed
        # p = products.Product("Test", 10, 10)
        # p.quantity = -5

def test_product_becomes_inactive_at_zero_quantity():
    """Test that a product becomes inactive when its quantity reaches 0 using properties."""
    product = products.Product("Test Item", price=10, quantity=1)
    # Use 'active' property
    assert product.active is True
    product.buy(1) # Buy the last item
    # Use 'quantity' property
    assert product.quantity == 0
    # Use 'active' property
    assert product.active is False # Should now be inactive

def test_product_purchase_modifies_quantity_and_returns_correct_output():
    """Test buying updates quantity and returns correct output using properties."""
    product = products.Product("Test Item", price=25, quantity=10)
    purchase_quantity = 3
    expected_total_price = 25 * purchase_quantity
    actual_total_price = product.buy(purchase_quantity)

    assert actual_total_price == expected_total_price
    # Use 'quantity' property
    assert product.quantity == 10 - purchase_quantity
    # Use 'active' property
    assert product.active is True # Should still be active

def test_buy_larger_quantity_than_exists_raises_exception():
    """Test buying more than available raises Exception using properties."""
    product = products.Product("Test Item", price=50, quantity=5)
    with pytest.raises(Exception, match="Not enough stock"):
        product.buy(6) # Try to buy more than available

    # Also test buying from an inactive product
    # Use property setter to change quantity, which should update active status
    product.quantity = 0
    # Use 'active' property
    assert product.active is False
    with pytest.raises(Exception, match="product is inactive"):
        product.buy(1)

# Optional: Test setting quantity directly using property setter
def test_set_quantity_updates_status():
    """Test quantity property setter updates quantity and active status."""
    product = products.Product("Another Test", price=5, quantity=10)
    # Use property setter
    product.quantity = 0
    # Use properties for checks
    assert product.quantity == 0
    assert product.active is False

    # Use property setter
    product.quantity = 5
    # Use properties for checks
    assert product.quantity == 5
    assert product.active is True

    # Test setting negative quantity via property setter
    with pytest.raises(ValueError, match="Quantity cannot be negative."):
        product.quantity = -1

