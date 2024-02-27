from rich.console import Console
from rich.table import Table

class OptionsTable:
    def __init__(self, title, column_names):
        self.console = Console()
        self.title = title
        self.column_names = column_names
        self.data = []  # Initialize an empty list to track row data
        self._rebuild_table()

    def _rebuild_table(self):
        """Rebuilds the table from the stored data."""
        self.table = Table(title=self.title, title_style="bold",)
        for name in self.column_names:
            self.table.add_column(name, style="light_green", no_wrap=True)
        for row_data in self.data:
            self.table.add_row(*row_data)

    def add_row(self, option, current_setting="", required="", description=""):
        """Add a row to the table and update the data list."""
        self.data.append([option, current_setting, required, description])
        self._rebuild_table()
    
    def modify_row(self, row_index, option=None, current_setting=None):
        """Modify a row based on the index and given values."""
        if 0 <= row_index < len(self.data):
            if option is not None:
                self.data[row_index][1] = option
            if current_setting is not None:
                self.data[row_index][1] = current_setting
            self._rebuild_table()

    def display(self):
        """Display the table."""
        self.console.print(self.table)