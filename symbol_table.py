from prettytable import PrettyTable
space_char = "    "


class SymbolTable:
    table = {}
    clean_table = PrettyTable()

    def write_table(self, sym_name, sym_type, scope):
        if scope not in self.table.keys():
            self.table[scope] = []

        self.table[scope].append((sym_name, sym_type, scope))

    def visualize(self):
        self.clean_table.field_names = ['Symbol', 'Type', 'Scope']
        print(self.table)
        for rows in self.table:
            values = self.table[rows]
            for row in values:
                self.clean_table.add_row([row[0], row[1], row[2]])

        print(self.clean_table)
