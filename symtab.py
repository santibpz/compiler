# SymbolTable class
class SymbolTable:
    def __init__(self, scope_name, parent=None):
        self.scope_name = scope_name
        self.entries = {}
        self.parent = parent

    def insert(self, name, info):
        self.entries[name] = info

    def lookup(self, name):
        table = self
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

def pop_st():
    global currentSymbolTable
    currentSymbolTable = symbolTableStack.pop()

def st_insert(name, type, scope, lineno, location, value=None, size=None, params=False):
    entry = currentSymbolTable.lookup(name)
    if entry is None:
        entry = {
            "type": type,
            "scope": scope,
            "line": lineno,
            "location": location,
            "value": value,
            "size": size,
            "params": params
        }
        currentSymbolTable.insert(name, entry)
    else:
        print("entry: ", name, " already exists")

def st_lookup(name):
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
def printSymTab():
    print("Var Name  Location   type   scope   lineno   value   size   params")
    print("--------  --------   ----   -----   ------   -----   ----   ------")
    for name in SymbolTable:
        print(f'{name:8}\t{SymbolTable[name][0]}\t', end = '')
        for i in range(len(SymbolTable[name])-1):
            print(f'{SymbolTable[name][i+1]}\t', end = '')
        print()

def printSymbolTableStack():
    print("=" * 80)
    print("Symbol Table Stack:\n")
    for i, table in enumerate(reversed(symbolTableStack + [currentSymbolTable])):
        if table is not None:
            print(f"Scope {table.scope_name if hasattr(table, 'scope_name') else i}:")
            print("-" * 80)
            print(f"{'Name':15} {'Type':10} {'Scope':10} {'Lines':15} {'Loc':6} {'Value':10} {'Size':6} {'Params'}")
            print("-" * 80)
            for name, entry in table.entries.items():
                print(f"{name:15} {str(entry.get('type')):10} {entry.get('scope'):10} "
                    f"{str(entry.get('lines')):15} {entry.get('location'):6} "
                    f"{str(entry.get('value')):10} {str(entry.get('size')):6} "
                    f"{str(entry.get('params'))}")
            print("-" * 80)
    print("=" * 80)
