from rich.console import Console
from rich.table import Table

class HelpTable:
    def __init__(self, title, column_names):
        self.console = Console()
        self.title = title
        self.column_names = column_names
        self.data = []  

        self._rebuild_table()

    def _rebuild_table(self):
        """Rebuilds the table from the stored data."""
        self.table = Table(title=self.title)
        for name in self.column_names:
            self.table.add_column(name, style="blue", no_wrap=True)
        for row_data in self.data:
            self.table.add_row(*row_data)

    def add_row(self, option, description=""):
        """Add a row to the table and update the data list."""
        self.data.append([option, description])
        self._rebuild_table()
    
    

    def display(self):
        """Display the table."""
        self.console.print(self.table)