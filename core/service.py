from fridge.data.repository import Repository
import fridge.core.models as models
import fridge.utils.dates as dates
import fridge.utils.formatted as frm


class Service:
    def __init__(self, rep: Repository):
        self.__rep = rep

    def add_product(self,name: str,quantity: int,unit: str,category: str,location: str,added_at: str,expires_at: str, note: str,) -> dict:
        new_product = models.try_make_product(
            name, quantity, unit, category, location, added_at, expires_at, note
        )
        if new_product[0] == False:
            return models.create_report(new_product[0], new_product[1])

        self.__rep.add(new_product[2])
        return models.create_report(
            new_product[0], "Product added", frm.dict_to_str(new_product[2])
        )

    def all_products(self, filter: dict = {}) -> dict:
        products = self.__rep.all_products()
        if filter == {}:
            return models.create_report(
                True,
                f"All products({len(products)}):",
                frm.list_with_dict_to_str(products),
            )

        try:
            filtred_products = [
                p
                for p in products
                if p[filter["field"]].lower() == filter["value"].lower()
            ]
            return models.create_report(
                True,
                f"Filtred products({len(filtred_products)}) by '{filter["field"]}={filter["value"]}':",
                frm.list_with_dict_to_str(filtred_products),
            )
        except Exception:
            return models.create_report(False, "Incorrect filter")

    def update_product(self, id: int, new_data: dict) -> dict:
        product = self.__rep.product_by_id(id)
        if product[0] == False:
            return models.create_report(False, f"There is no product with id = {id}")

        new_product = models.try_update_product(product[1], new_data)
        if new_product[0] == False:
            return models.create_report(new_product[0], new_product[1])

        result = self.__rep.update(new_product[2])
        if result:
            return models.create_report(
                result, "The product has been updated", frm.dict_to_str(new_product[2])
            )

        return models.create_report(result, f"Couldn't update product with id = {id}")

    def expiring_products(self, day: int) -> dict:
        products = self.__rep.all_products()

        expiring = []
        for p in products:
            date = dates.date_from_str(p.get("expires_at"))
            if dates.expiring(day, date):
                expiring.append(p)

        return models.create_report(
            True,
            f"Expiring products({len(expiring)})({day} day):",
            frm.list_with_dict_to_str(expiring),
        )

    def expired_products(self) -> dict:
        products = self.__rep.all_products()

        expired = []
        for p in products:
            date = dates.date_from_str(p.get("expires_at"))
            if dates.expired(date):
                expired.append(p)

        return models.create_report(
            True,
            f"Expired products({len(expired)}):",
            frm.list_with_dict_to_str(expired),
        )

    def delete(self, id: int) -> dict:
        result = self.__rep.delete(id)
        if result:
            return models.create_report(
                result, f"The product with id = {id}, has been deleted"
            )

        return models.create_report(result, f"Couldn't delete product with id = {id}")

    def save_data(self) -> dict:
        self.__rep.commit()
        return models.create_report(True, "The data is saved")
