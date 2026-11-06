import json
import os

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def create_product_from_dict(d: dict, suppliers: dict[str, Supplier]) -> Product:
    s = d.get("supplier", {"supplier_id": "S000", "name": "Unknown", "contact_email": ""})
    if s["supplier_id"] not in suppliers:
        suppliers[s["supplier_id"]] = Supplier(s["supplier_id"], s["name"], s["contact_email"])
    supplier = suppliers[s["supplier_id"]]

    stock = d.get("stock", d.get("quantity", 0))
    if d.get("type") == "digital":
        return DigitalProduct(d.get("id"), d.get("name"), d.get("price"),
                              stock, supplier, d.get("download_size", 0.0))
    return PhysicalProduct(d.get("id"), d.get("name"), d.get("price"),
                           stock, supplier, d.get("weight", 0.0))


class Inventory:
    def __init__(self):
        self._products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self._products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for p in self._products:
            if p.get_id() == product_id:
                return p
        return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(new_stock)
        return True

    def search_product(self, query: str) -> list[Product]:
        query = query.strip().lower()
        return [p for p in self._products
                if query == p.get_id().lower() or query in p.get_name().lower()]

    def get_all_products(self) -> list[Product]:
        return self._products

    def get_all_suppliers(self) -> dict[str, Supplier]:
        return {p.get_supplier().get_id(): p.get_supplier() for p in self._products}

    def display_all_products(self) -> None:
        if not self._products:
            print("\nInventory is empty.\n")
            return
        print("\nCurrent Inventory:")
        for p in self._products:
            p.display_information()
            print(f"    {p.get_fulfilment_info()}")
        print()

    def save(self) -> None:
        data = [p.to_dict() for p in self._products]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Saving inventory before exit...")
        print("Inventory saved to inventory.json")

    def load(self) -> None:
        self._products = []
        if not os.path.exists(INVENTORY_FILE):
            return
        with open(INVENTORY_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        suppliers: dict[str, Supplier] = {}
        for d in data:
            self._products.append(create_product_from_dict(d, suppliers))