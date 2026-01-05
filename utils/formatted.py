from tabulate import tabulate as tb

def list_with_dict_to_str(l: list, table: str = "pipe") -> str:
    if len(l) == 0:
        return ""
    
    return tb(l, headers="keys", tablefmt=table)

def dict_to_str(d: dict, table: str = "pipe") -> str:
    if d == {}:
        return ""
    
    l = [d]
    return tb(l, headers="keys", tablefmt=table)