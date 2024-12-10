import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('us_inflation_rates_2000_to_2024.csv', index_col = 0)


class Expense:
    """
    Stores individual expenses and its details.

    Attributes:
        amount (float): the amount of the expense
        category (str): category of the expense (e.g. food, rent, etc)
        month (str): the month of the expense, ideally typed as only the first 3 letters of the month
        year (int): the year of the expense
        
    """
    def __init__(self, amount, category, month, year):
        """
        Initializes an Expense instance.

        Args:
            amount (float): the amount of the expense
            category (str): category of the expense (e.g. food, rent, etc)
            month (str): the month of the expense (e.g. 'Jan', 'Feb', 'Mar')
            year (int): the year of the expense
        """
        self.amount = float(amount)
        self.category = str(category)
        self.month = month.capitalize()[:3]
        self.year = int(year)

    def adjust_for_inflation(self):
        """
        Calculates the adjusted amount for inflation based on month and year

        Returns:
            adjusted_expense (str): the inflation-adjusted expense amount
        """
        inflation_rate = df.loc[self.year, self.month]
        adjusted_expense = self.amount * (1 + (inflation_rate/100))
        
        return f'your inflation adjusted expense is {adjusted_expense}' 

    def get_lst(self):
        """
        Instance attributes stored in list to be used in Tracker for further analysis

        Returns:
            list: contains the expense amount, category, month, and year
        """
        return [self.amount, self.category, self.month, self.year]


class Tracker:
    """
    Manages and analyzes all expenses.
    You can add new expenses, receive monthly and yearly summaries,
    and find the inflation-adjusted amount for your expenses.

    Attributes:
        expenses (pd.DataFrame): a DataFrame that stores expense details with
                                 the columns 'Amount', 'Category', 'Month', 
                                 'Year'
    """
    def __init__(self):
        """
        Initalizes an empty DataFrame to store expenses.
        The DataFrame columns are: 'Amount', 'Category', 'Month', 'Year'.
        """
        self.expenses = pd.DataFrame({'Amount': pd.Series(dtype='float'),
                                        'Category': pd.Series(dtype='str'),
                                        'Month': pd.Series(dtype='str'),
                                        'Year': pd.Series(dtype='int')})
        
    def add_expenses(self, expense):
        """
        Adds a new expense to the Tracker instance by appending the expense to the
        DataFrame.

        Args:
            expense (Expense): an Expense object
        """
        # create dataframe for new expense to be added to the main dataframe
        new_expense = pd.DataFrame([expense.get_lst()], columns=self.expenses.columns)
        self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
        
    def get_expense_by_category(self, category):
        """
        Finds and prints all expenses of a specified category

        Args:
            category (str): the category to filter expenses
        """
        temp = self.expenses[self.expenses['Category'] == category]
        print(temp)
                
    def get_monthly_summary(self, month, year):
        """
        Creates a bar chart displaying the amount spent for expenses in every category 
        for a specified month and year.

        Args:
            month (str): month for the summary
            year (int): year for the summary

        ValueError: If there are no expenses with the specified month and year
        """
        # filter by both month and year
        filtered_expenses = self.expenses[
            (self.expenses['Month'] == month.capitalize()[:3]) &
            (self.expenses['Year'] == year)
        ]

        if filtered_expenses.empty == True:
            print(f"No data found for {month} {year}.")

        # group by category
        category_totals = filtered_expenses.groupby('Category')['Amount'].sum()

        plt.bar(category_totals.index, category_totals.values)
        plt.xlabel('Category')
        plt.ylabel('Amount Spent')
        plt.title(f'Expense Summary for {month.capitalize()} {year}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def get_yearly_summary(self, year):
        """
        Creates a bar chart displaying the amount spent for expenses in every category 
        for a specified year.

        Args:
            year (int): year for the summary

        ValueError: 
            If there are no expenses for the specified year
        """
        filtered_expenses = self.expenses[
            (self.expenses['Year'] == year)
        ]

        if filtered_expenses.empty == True:
            print(f"No data found for {year}.")

        yearly_totals = filtered_expenses.groupby('Month')['Amount'].sum().reindex(
                                                    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 
                                                     'Jun',  'Jul', 'Aug', 'Sep', 'Oct', 
                                                     'Nov', 'Dec'])

        plt.bar(yearly_totals.index, yearly_totals.values)
        plt.xlabel('Category')
        plt.ylabel('Amount Spent')
        plt.title(f'Expense Summary for {year}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def calc_inflation_adj_expenses(self, year):
        """
        Calculates and returns a DataFrame including the inflation-adjusted expenses for
        a specified year.

        The inflation rate is the annual inflation rate for the given year and will be
        applied to all expenses in that year, except for 2024.

        Args:
            year (int): year for which expenses will be adjusted for inflation

        Returns:
            calc_expenses (pd.DataFrame): a DataFrame containing the original and
                                          inflation-adjusted expenses

        ValueError:
            If there isn't data for the specified year or
            if there isn't an annual inflation rate average for that year
        """
        # create empty dataframe to avoid UnboundLocalError
        calc_expenses = pd.DataFrame(columns=self.expenses.columns)
        
        # sort dataframe by year
        if year < 2024:
            calc_expenses = self.expenses[(self.expenses['Year'] == year)]
            calc_expenses = calc_expenses.copy()
            
            if calc_expenses.empty == True:
                print(f"No data found for {year}.")

            inflation_avg = df.loc[year, 'Ave'] / 100
            # apply inflation avg of that year to all cells in the 'Amount' column
            calc_expenses['Adjusted Amount'] = calc_expenses['Amount'] * (1 + inflation_avg)

        else:
            print(f"No inflation average calculated yet for {year}.")
                
        return calc_expenses