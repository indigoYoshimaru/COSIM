space_char = "    "
from prettytable import PrettyTable

class SymbolTable:
    table = {}
    clean_table = PrettyTable()    

    # def look_up_symbol(self, token):
    #     pass

    # def write_to_table(self, level, token):
    #     symbol_array = {}
    #     token_props = [token.__class__.__name__, level]
    #     symbol_array.update({token: token_props})
    #     self.global_table.update({symbol_array: level})

    # def visualize(self):
    #     pass

    # def write_identifier(identifier):
    #     pass

    # def write_constant(constant):
    #     pass

    # def write_variable(variable):
    #     pass

    # def write_function(function):
    #     pass

    # def write_table(self, sym_name, type, level, scope): # scope is level 
    #     print(space_char*level,'symbol: ', sym_name)
    #     print(space_char*level,'type: ', type)
    #     print(space_char*level,'scope: ', scope)
    #     print()

    def write_table(self, sym_name, sym_type, scope):
        if scope not in self.table.keys():
            self.table[scope]=[]
            
        self.table[scope].append((sym_name,sym_type,scope))

    def visualize(self):
        self.clean_table.field_names = ['Symbol', 'Type', 'Scope']
        print(self.table)
        for rows in self.table:
            values=self.table[rows]
            for row in values:
                self.clean_table.add_row([row[0], row[1], row[2]])

        print(self.clean_table)