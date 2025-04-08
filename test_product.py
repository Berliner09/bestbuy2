# test_product.py
import pytest
# Stelle sicher, dass products.py im selben Verzeichnis oder im Python-Pfad ist
import products

def test_create_normal_product():
    """Test creating a product with valid details."""
    product = products.Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True

def test_create_product_invalid_details():
    """Test creating a product with invalid details raises ValueError."""
    # Test empty name
    with pytest.raises(ValueError, match="Product name cannot be empty"):
        products.Product("", price=1450, quantity=100)

    # Test negative price
    with pytest.raises(ValueError, match="Product price cannot be negative"):
        products.Product("MacBook Air M2", price=-10, quantity=100)

    # Test negative quantity
    with pytest.raises(ValueError, match="Product quantity cannot be negative"):
        products.Product("MacBook Air M2", price=1450, quantity=-5)

def test_product_becomes_inactive_at_zero_quantity():
    """Test that a product becomes inactive when its quantity reaches 0."""
    product = products.Product("Test Item", price=10, quantity=1)
    assert product.is_active() is True
    product.buy(1) # Buy the last item
    assert product.get_quantity() == 0
    assert product.is_active() is False # Should now be inactive

def test_product_purchase_modifies_quantity_and_returns_correct_output():
    """Test that buying a product updates quantity and returns the total price."""
    product = products.Product("Test Item", price=25, quantity=10)
    purchase_quantity = 3
    expected_total_price = 25 * purchase_quantity
    actual_total_price = product.buy(purchase_quantity)

    assert actual_total_price == expected_total_price
    assert product.get_quantity() == 10 - purchase_quantity
    assert product.is_active() is True # Should still be active

def test_buy_larger_quantity_than_exists_raises_exception():
    """Test that attempting to buy more quantity than available raises an Exception."""
    product = products.Product("Test Item", price=50, quantity=5)
    with pytest.raises(Exception, match="Not enough stock"):
        product.buy(6) # Try to buy more than available

    # Also test buying from an inactive product (which might happen if quantity was 0)
    product.set_quantity(0) # Make it inactive
    assert product.is_active() is False
    with pytest.raises(Exception, match="product is inactive"):
        product.buy(1)

# Optional: Test setting quantity directly
def test_set_quantity_updates_status():
    """Test set_quantity updates quantity and active status correctly."""
    product = products.Product("Another Test", price=5, quantity=10)
    product.set_quantity(0)
    assert product.get_quantity() == 0
    assert product.is_active() is False

    product.set_quantity(5)
    assert product.get_quantity() == 5
    assert product.is_active() is True

    # Test setting negative quantity via set_quantity
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        product.set_quantity(-1)

