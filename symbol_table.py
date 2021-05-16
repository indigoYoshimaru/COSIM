class symbol_table:
    global_table = {}
    def __init__(self):
        super().__init__()

    def look_up_symbol(self, token):
        pass

    def write_to_table(self, level, token):
        symbol_array = {}
        token_props = [token.__class__.__name__, level]
        symbol_array.update({token: token_props})
        self.global_table.update({symbol_array: level})

    def visualize(self):
        pass

    def write_identifier(identifier):
        pass
    
    def write_constant(constant):
        pass
    
    def write_variable(variable):
        pass
    
    def write_function(function):
        pass
    