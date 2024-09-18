# utils.py

def calculate_cart_total(cart_items):
    total = 0
    for cart_item in cart_items:
        # Get the price, default to 0 if not present
        price = float(cart_item.get('price', 0))
        # Get the quantity, default to 0 if not present
        quantity = int(cart_item.get('quantity', 0))
        # Calculate the total price for the item
        total += price * quantity
    return total
