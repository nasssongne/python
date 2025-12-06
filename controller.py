import csv
import os
from PyQt6.QtWidgets import *

class Controller:
    # Maximum number of items allowed in the truck
    MAX_ITEMS = 10

    def __init__(self, view):
        self.view = view
        # Load product data
        self.products = self.load_products()
        self.order_items = []

        # Add a color to the add item button.
        self.view.addButton.setStyleSheet(
            """
            QPushButton {
                background-color: #1E90FF;  
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #1C86EE;
            }
            """
        )

        #Add a color to the delete item button.
        self.view.deleteButton.setStyleSheet(
            """
            QPushButton {
                background-color: #FF4C4C;  
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #FF3333;
            }
            """
        )

        # Add a color to the send order button.
        self.view.sendButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4169E1;  
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #3558C0;
            }
            """
        )
        self.view.productDropdown.clear()
        self.view.productDropdown.addItems(list(self.products.keys()))
        self.view.productDropdown.currentTextChanged.connect(self.update_product_info)
        self.view.addButton.clicked.connect(self.add_item)
        self.view.deleteButton.clicked.connect(self.delete_item)
        self.view.sendButton.clicked.connect(self.send_order)


    def load_products(self):
        """Load products from products.csv."""
        products = {}
        folder = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(folder, "products.csv")

        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row["product"]
                    products[name] = {
                        "gin": row["gin"],
                        "price": float(row["price"]),
                    }
        except FileNotFoundError:
            QMessageBox.critical(None, "Error", f"products.csv not found at:\n{csv_path}")
            return {}

        return products

    def update_product_info(self, name):
        """Update the product name and GIN when selected"""
        if name in self.products:
            info = self.products[name]
            self.view.ginLabel.setText(info["gin"])
            self.view.priceLabel.setText(str(info["price"]))
        else:
            self.view.ginLabel.setText("")
            self.view.priceLabel.setText("")


    def add_item(self):
        """"Add product to the truck order."""""
        quantity_text = self.view.quantityInput.text().strip()

        # Validation of the quantity entered
        if not quantity_text.isdigit() or int(quantity_text) <= 0:
            QMessageBox.warning(None, "Error", "Please enter a valid quantity.")
            return
        quantity = int(quantity_text)
        current_load = sum(i["quantity"] for i in self.order_items)

        # Check the capacity of the truck
        if current_load + quantity > self.MAX_ITEMS:
            QMessageBox.warning(
                None,
                "Truck Full",
                f"The truck can only carry {self.MAX_ITEMS} items.\n"
                f"You already have {current_load} items loaded.",
            )
            return

        entered_gin = self.view.ginInput.text().strip()
        selected_name = self.view.productDropdown.currentText().strip()
        # Validate when the GIN is entered instead of the product name
        if entered_gin:
            product_name = None
            for name, info in self.products.items():
                if info["gin"] == entered_gin:
                    product_name = name
                    break
            if product_name is None:
                QMessageBox.warning(None, "Error", "GIN not found.")
                return
        else:
            product_name = selected_name

        if product_name not in self.products:
            QMessageBox.warning(None, "Error", "Please select a product or enter a valid GIN.")
            return

        info = self.products[product_name]

        # Merge if item already in cart
        for item in self.order_items:
            if item["product"] == product_name:
                item["quantity"] += quantity
                item["price"] = item["quantity"] * info["price"]
                self._refresh_items_list()
                return

        # Added new item to the truck order
        self.order_items.append(
            {
                "product": product_name,
                "gin": info["gin"],
                "quantity": quantity,
                "price": quantity * info["price"],
            }
        )

        self._refresh_items_list()


    def delete_item(self):
        """Delete item in the truck"""""
        quantity_text = self.view.quantityInput.text().strip()
        entered_gin = self.view.ginInput.text().strip()
        entered_name = self.view.productDropdown.currentText().strip()

        if not quantity_text.isdigit():
            QMessageBox.warning(None, "Error", "Enter the number of items to delete.")
            return

        qty_to_delete = int(quantity_text)
        target_item = None

        # Use the GIN first
        if entered_gin:
            for item in self.order_items:
                if item["gin"] == entered_gin:
                    target_item = item
                    break
        else:
            # Use the product name
            for item in self.order_items:
                if item["product"] == entered_name:
                    target_item = item
                    break

        if target_item is None:
            QMessageBox.warning(None, "Error", "Item not found.")
            return

        if qty_to_delete > target_item["quantity"]:
            QMessageBox.warning(None, "Error", "Cannot delete more than the quantity available.")
            return

        target_item["quantity"] -= qty_to_delete

        # Remove completely if quantity = 0
        if target_item["quantity"] == 0:
            self.order_items.remove(target_item)
        else:
            # Recalculate price
            unit_price = self.products[target_item["product"]]["price"]
            target_item["price"] = target_item["quantity"] * unit_price

        self._refresh_items_list()


    def _refresh_items_list(self):
        """Refreshing the items already in the truck order."""
        self.view.itemsList.clear()
        for item in self.order_items:
            text = f"{item['product']} — {item['quantity']} pcs — ${item['price']:.2f}"
            self.view.itemsList.addItem(text)


    def save_order(self, total_price):
        """Save the order to the order.csv"""
        folder = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(folder, "orders.csv")

        file_exists = os.path.exists(file_path)

        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)



            for item in self.order_items:
                writer.writerow(
                    [
                        item["product"],
                        item["gin"],
                        item["quantity"],
                        f"{item['price']:.2f}",
                        f"{total_price:.2f}",
                    ]
                )


    def send_order(self):
        """Send the order"""
        if not self.order_items:
            QMessageBox.warning(None, "Error", "No items to send.")
            return

        total_items = sum(i["quantity"] for i in self.order_items)
        total_price = sum(i["price"] for i in self.order_items)
        # Save to CSV
        self.save_order(total_price)

        self.order_items.clear()
        self._refresh_items_list()

        QMessageBox.information(None, "Success", "Order saved and sent!")