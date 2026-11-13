class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id: str = supplier_id
        self._name: str = name
        self._contact_email: str = contact_email

    def get_id(self) -> str:
        return self._supplier_id

    def get_name(self) -> str:
        return self._name

    def get_contact_email(self) -> str:
        return self._contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self._supplier_id}, Name: {self._name}, "
              f"Email: {self._contact_email}")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self._supplier_id,
            "name": self._name,
            "contact_email": self._contact_email
        }