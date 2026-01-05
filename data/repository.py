from fridge.data.json_storage import JSONStore

class Repository:
    def __init__(self, path: str): 
        self.__js = JSONStore(path)
        self.__data = self.__js.load_data()

    def add(self, product: dict):
        products = self.all_products()
        nextId = self.product_count() + 1
        
        product["id"] = nextId
        products.append(product)
        self.__data["products"] = products
        self.__data["last_id"] = nextId

    def product_by_id(self, id: int) -> list:
        p_exists = self.__product_exists(id)
        return [p_exists[0], p_exists[1]]

    def all_products(self) -> list:
        return self.__data.get("products").copy()

    def product_count(self) -> int:
        return self.__data.get("last_id")

    def update(self, new_product: dict) -> bool:
        p_exists = self.__product_exists(new_product.get("id"))
        if p_exists[0] == False:
            return p_exists[0]
        
        products = self.all_products()
        products[p_exists[2]] = new_product

        self.__data["products"] = products
        return p_exists[0]

    def delete(self, id: int) -> bool:
        p_exists = self.__product_exists(id)
        if p_exists[0] == False:
            return p_exists[0]

        products = self.all_products()
        products.remove(p_exists[1])
        
        self.__data["products"] = products
        self.__data["last_id"] = len(products)
        self.__normalize_id()
        return p_exists[0]

    def commit(self):
        self.__js.save_data(self.__data)

    def __normalize_id(self, start_id: int = 0):
        if start_id < 0:
            return
        
        products = self.all_products()
        for i in range(start_id, self.product_count() - 1):
            current_id = products[i].get("id")
            next_id = products[i + 1].get("id")

            if current_id != i + 1:
                products[i]["id"] = i + 1  
                current_id = i + 1
                
            if next_id != current_id + 1:
                products[i + 1]["id"] = current_id + 1
        
        self.__data["products"] = products

    def __product_exists(self, id: int) -> list:
        products = self.all_products()
        for i in range(self.product_count()):
            p = products[i]
            if p.get("id") == id:
                return True, p, i

        return False, {}, 0