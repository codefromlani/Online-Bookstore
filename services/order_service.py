from models import OrderItem 


 # This method calculates the total amount dynamically from OrderItems
def calculate_total_amount(order_items):
    total = sum(item.quantity * item.price_at_time for item in order_items)
    return total

# Assuming you have an order and want to calculate its total amount

# Query to get all order items related to a specific order
# order_items = session.query(OrderItem).filter_by(order_id=order.id).all()

# # Call the function to calculate the total amount
# total_amount = calculate_total_amount(order_items)

# # Optionally, you could update the order with the calculated total amount
# order.total_amount = total_amount
# session.commit()