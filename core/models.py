def create_report(success: bool, sys_mes: str, data: str = "") -> dict:
    report = {
        "success": success,
        "sMessage": sys_mes,
        "data": data
    }

    return report  

def try_make_product(name: str, quantity: int, unit: str, category: str, location: str, added_at: str, expires_at: str, note: str) -> list:
    product = {
        "id": 0,
        "name" : name.strip().capitalize(),
        "quantity" : quantity,
        "unit" : unit,
        "category" : category,
        "location" : location,
        "added_at" : added_at,
        "expires_at" : expires_at,
        "note" : note.strip()
    }

    valid = validate_product(product)
    return [valid[0], valid[1], product]

def try_update_product(product: dict, new_data: dict) -> list:
    new_product = {
            "id": product.get("id"),
            "name": product.get("name"),
            "quantity": new_data.get("quantity", product.get("quantity")),
            "unit": product.get("unit"),
            "category": product.get("category"),
            "location": new_data.get("location", product.get("location")),
            "added_at": product.get("added_at"),
            "expires_at": product.get("expires_at"),
            "note": new_data.get("note", product.get("note")).strip()
        }

    valid = validate_product(new_product)
    return [valid[0], valid[1], new_product]

def validate_product(product: dict) -> list:
    if product.get("id") < 0:
        return [False, "The ID must not be negative."]
    if len(product.get("name")) <= 3:
        return [False, "The name must be longer than 3 characters."]
    if product.get("quantity") <= 0:
        return [False, "The number must be greater than 0"]
    if len(product.get("unit")) <= 0:
        return [False, "The unit of measurement should not be empty."]
    if len(product.get("category")) <= 3:
        return [False, "The category must be more than 3 somboles."]
    if len(product.get("location")) <= 3:
        return [False, "The storage location must be more than 3 somboles."]
    if len(product.get("added_at")) != 10:
        return [False, "The date added must be in the YYYY-MM-DD format."]
    if len(product.get("expires_at")) != 10:
        return [False, "The expiration date must be in the YYYY-MM-DD format."]
    if len(product.get("note")) > 20:
        return [False, "Notes should not be more than 20 characters long"]

    return [True, "Product has been validated and create"]