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
        st_insert('output', 'void', 0, 0, 0)

def pop_st():
    global currentSymbolTable
    currentSymbolTable = symbolTableStack.pop()

def st_insert(name, type, scope, lineno, location, value=None, size=None, params=False, params_num=None):
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
            "params_num": params_num
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

# Procedure st_insert inserts line numbers and
# memory locations into the symbol table
# loc = memory location is inserted only the
# first time, otherwise ignored
# def st_insert(name, type, scope, lineno, loc, value=None, size=None, params=None):
#     if name in SymbolTable:
#         SymbolTable[name].append(lineno)
#     else:
#         SymbolTable[name] = [loc, type, scope, lineno, value, size, params]

        

# # Function st_lookup returns the memory 
# # location of a variable or -1 if not found
# def st_lookup(name):
#     if name in SymbolTable:
#         return SymbolTable[name][0]
#     else:
#         return -1

# Procedure printSymTab prints a formatted 
# listing of the symbol table contents 
# to the listing file

def printSymbolTableStack():
    print("=" * 80)
    print("Symbol Table Stack:\n")
    for i, table in enumerate(reversed(symbolTableStack + [currentSymbolTable])):
        if table is not None:
            print(f"Scope {table.scope_name if hasattr(table, 'scope_name') else i}:")
            print("-" * 80)
            print(f"{'Name':15} {'Type':10} {'Scope':10} {'Lines':20} {'Loc':6} {'Value':10} {'Size':6} {'Params'} {'No. Params'}")
            print("-" * 80)
            for name, entry in table.entries.items():
                # Convert lines list to string, e.g., [2, 4] → "2,4"
                lines_str = ','.join(str(line) for line in entry.get('lines', []))
                print(f"{name:15} {str(entry.get('type')):10} {entry.get('scope'):10} "
                    f"{lines_str:20} {entry.get('location'):6} "
                    f"{str(entry.get('value')):10} {str(entry.get('size')):6} "
                    f"{str(entry.get('params'))} {str(entry.get('params_num')):6}")
            print("-" * 80)
    print("=" * 80)

