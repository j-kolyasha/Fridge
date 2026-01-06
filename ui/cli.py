from fridge.core.service import Service
import fridge.ui.models as models
import fridge.utils.dates as dates
import msvcrt
import os
import sys

MENU = """
======================================================MENU=====================================================
                  1. Add a product    2. Show all products    3. It will go bad soon  4. Overdue                  
                                                                                                
                      5. Change the quantity    6. Remove the product    7. Search (filter)          
                                                                                                
                                                    0. Exit    
                                                                                 
"""
BORDER = "==============================================================================================================="
MENU_WIDHT = 111

MESSAGE_TEMPLATE = "-%(message)s-"
DEFAULT_MESSAGE = "Press the menu item number"
NON_EXISTENT_NUMBER_MESSAGE = "You have selected a non-existent menu item number"


class CLI:
    def __init__(self, srv: Service, units: list, category: list, locations: list, fields_for_filtering: list):
        self.__srv = srv
        self.__units = units
        self.__category = category
        self.__locations = locations
        self.__fields_for_filtering = fields_for_filtering

    def menu(self):
        self.__update_main_menu(DEFAULT_MESSAGE)

        while True:
            key = self.__getch_key()
            res = dict()

            match key:
                case "1":
                    data = self.__input_new_product_data()
                    res = self.__srv.add_product(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                    )
                case "2":
                    res = self.__srv.all_products()
                case "3":
                    days = self.__input_number("Enter the number of days:", True)
                    res = self.__srv.expiring_products(days)
                case "4":
                    res = self.__srv.expired_products()
                case "5":
                    data = self.__change_quantity()
                    res = self.__srv.update_product(data[0], data[1])
                case "6":
                    id = self.__input_number("Enter the product id:", True)
                    res = self.__srv.delete(id)
                case "7":
                    f = self.__search_products()
                    res = self.__srv.all_products(f) 
                case "0":
                    self.__srv.save_data()
                    sys.exit()
                case _:
                    self.__update_main_menu(NON_EXISTENT_NUMBER_MESSAGE)
                    continue

            self.__update_main_menu(res.get("sMessage"))
            if res.get("success"):
                print(res.get("data"))

    def __update_main_menu(self, mes: str = DEFAULT_MESSAGE):
        os.system("cls" if os.name == "nt" else "clear")
        message = (MESSAGE_TEMPLATE % {"message": mes}).center(MENU_WIDHT, " ")

        menu = MENU + BORDER + "\n" + message + "\n" + BORDER
        print(menu)

    def __change_quantity(self) -> list:
        message = "Change the quantity. "

        id = self.__input_number(message + "Enter the product id that you want to change:", True)
        new_quantity = self.__input_number(message + "Enter the new quantity product:", True)
        
        data = {"quantity" : new_quantity}
        return [id, data]


    def __search_products(self) -> dict:
        message = "Filter search. "

        field = self.__select_from_list(message + "Select a field from the list:", self.__fields_for_filtering)
        value = self.__input_str(message + "Enter the value for filter:")

        return models.create_filter(field, value)


    def __input_new_product_data(self) -> dict:
        message = "Adding a product. "

        name = self.__input_str(message + "Enter the product name:")
        quantity = self.__input_number(message + "Enter the number of products:")
        unit = self.__select_from_list(
            message + "Select a unit from the list:", self.__units
        )
        category = self.__select_from_list(
            message + "Select a category from the list:", self.__category
        )
        location = self.__select_from_list(
            message + "Select a location from the list:", self.__locations
        )
        added_at = dates.today_str()
        expires_at = self.__input_date("Enter the expires date:")
        note = self.__input_str(message + "Enter the note:")

        return [name, quantity, unit, category, location, added_at, expires_at, note]

    def __getch_key(self) -> str:
        return msvcrt.getch().decode()

    def __input_number(self, message: str, positive: bool = False) -> int:
        self.__update_main_menu(message)
        while True:
            try:
                i = int(input("Enter: "))
                if positive and i < 0:
                    self.__update_main_menu(
                        "Incorrect data entry. The number must not be negative. "
                        + message
                    )
                    continue
                return i
            except ValueError:
                self.__update_main_menu("Incorrect data entry. " + message)

    def __input_str(self, message: str) -> str:
        self.__update_main_menu(message)
        while True:
            text = input("Enter: ")
            if len(text) > 0:
                return text

            self.__update_main_menu("Incorrect data entry. " + message)

    def __input_date(self, message: str) -> str:
        self.__update_main_menu(message + " The date must be in the YYYY-MM-DD format.")
        while True:
            date = input("Enter: ")
            if dates.valid_date(date):
                return date

            self.__update_main_menu("Incorrect data entry. " + message)

    def __select_from_list(self, message: str, l: list) -> str:
        count_elements = len(l)
        if count_elements == 0:
            return ""

        message = message + " Press the item number:"
        self.__update_main_menu(message)

        text = ""
        temp_text = ""
        for i in range(count_elements):
            temp_text += f"{i+1}. {l[i]}    "

            if i == count_elements - 1 or len(temp_text) + len(l[i + 1]) >= MENU_WIDHT:
                text += temp_text.center(MENU_WIDHT, " ") + "\n"
                temp_text = ""

        while True:
            print(text)
            key = self.__getch_key()
            try:
                id = int(key)
                id_in_list = id - 1
                if id_in_list < count_elements:
                    return l[id_in_list]

                self.__update_main_menu(
                    "There is no element with this id. "
                    + message
                )
            except:
                self.__update_main_menu(
                    "The id must be a number. " + message
                )
