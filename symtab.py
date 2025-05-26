# SymbolTable class
class SymbolTable:
    def __init__(self, scope_name, parent=None):
        self.scope_name = scope_name
        self.entries = {}
        self.parent = parent

    def insert(self, name, info):
        self.entries[name] = info

    def update(self, name, info):
        table = self
        if name in table.entries:
            self.entries[name] = info

    def lookup(self, name, local_search=False):
        table = self

        if local_search:
            if name in table.entries:
                return table.entries[name]
            return None

        while table is not None:
            if name in table.entries:
                return table.entries[name]
            table = table.parent
        return None
    
    def search_main(self):
        table = self
        while table is not None:
            if table.scope_name == 'global':
                if 'main' in table.entries:
                    return True
            table = table.parent
        return False
    
    def upt_gbl(self, name, entry):
        table = self
        while table is not None:
            if table.scope_name == 'global' and name not in table.entries:
                table.insert(name, entry)
                return True
            table = table.parent
        return False
    
    def upt_offset(self, scope_name, symbol, offset):
        table = self
        while table is not None:
            if table.scope_name == scope_name and symbol in table.entries:
                entry = table.entries[symbol]
                entry["offset"] = offset
                table.update(symbol, entry)
                return True
            table = table.parent
        return False
    
    def get_offset(self, scope_name, symbol):
        table = self
        while table is not None:
            if table.scope_name == scope_name and symbol in table.entries:
                entry = table.entries[symbol]
                return entry["offset"]
            table = table.parent
        return None

# Symbol table stack
symbolTableStack = []
currentSymbolTable = None

def push_st(scope_name):
    global currentSymbolTable
    new_table = SymbolTable(scope_name, currentSymbolTable)
    symbolTableStack.append(currentSymbolTable)
    currentSymbolTable = new_table
    if scope_name == 'global':
        st_insert('input', 'int', 0, 0, 0)
        st_insert('output', 'void', 0, 0, 0, params=True, params_num=1)

def pop_st():
    global currentSymbolTable
    if currentSymbolTable.parent is not None:
        currentSymbolTable = currentSymbolTable.parent

def st_insert(name, type, scope, lineno, location, value=None, size=None, params=False, params_num=None, offset=None):
    entry = currentSymbolTable.lookup(name, True)
    if entry is None:
        entry = {
            "type": type,
            "scope": scope,
            "lines": [lineno],
            "location": location,
            "value": value,
            "size": size,
            "params": params,
            "params_num": params_num,
            "offset": offset
        }
        currentSymbolTable.insert(name, entry)
    else:
        print("entry: ", name, " already exists")

def st_update(name, entry):
    currentSymbolTable.update(name, entry)
    
def st_lookup(name, local_search = False):
    if local_search:
        return currentSymbolTable.lookup(name, local_search)
    return currentSymbolTable.lookup(name)

def st_search_main():
    return currentSymbolTable.search_main()

def upt_global(name, entry):
    return currentSymbolTable.upt_gbl(name, entry)

def upt_offset(scope_name, name, offset):
    return currentSymbolTable.upt_offset(scope_name, name, offset)

def get_offset(scope_name, symbol):
    return currentSymbolTable.get_offset(scope_name, symbol)
        
# Procedure printSymTab prints a formatted 
# listing of the symbol table contents 
# to the listing file

def printSymbolTableStack():
    print("=" * 80)
    print("Symbol Table Stack:\n")
    for i, table in enumerate(reversed(symbolTableStack + [currentSymbolTable])):
        if table is not None:
            print(f"Scope {table.scope_name if hasattr(table, 'scope_name') else i}:")
            print("-" * 120)
            print(f"{'Name':15} {'Type':10} {'Scope':15} {'Lines':20} {'Loc':6} {'Size':6} {'Params':10} {'No. Params':5} {'offset'}")
            print("-" * 120)
            for name, entry in table.entries.items():
                # Convert lines list to string, e.g., [2, 4] → "2,4"
                lines_str = ','.join(str(line) for line in entry.get('lines', []))
                print(f"{name:15} {str(entry.get('type')):6} {entry.get('scope'):10} \t"
                    f"{lines_str:15} {entry.get('location'):10} \t"
                    f"{str(entry.get('size')):6} "
                    f"{str(entry.get('params')):10} {str(entry.get('params_num')):6} \t"
                    f"{str(entry.get('offset')):6} ")
            print("-" * 120)
    print("=" * 120)
