from my_classes import Expense
from my_classes import Tracker
import pandas as pd
import matplotlib.pyplot as plt

expense = Expense(100, 'food', 'March', 2019)


class TestExpense:
    
    def test_init(self):
        # checks if Expense object is initialized correctly
        assert expense.amount == 100
        assert expense.category == 'food'
        assert expense.month == 'Mar'
        assert expense.year == 2019
        
    def test_adjust_for_inflation(self):
        # create global df as a mock for the df containing the real inflation rates 
        global df

        df = pd.DataFrame(
            {
                'Jan': [2],
                'Feb': [2.5],
                'Mar': [3],
                'Apr': [1.8],
                'May': [2.3],
                'Jun': [2.7],
                'Jul': [2.2],
                'Aug': [1.9],
                'Sep': [2.6],
                'Oct': [2.8],
                'Nov': [3.1],
                'Dec': [3.0],
                'Ave': [3]
            },
            index=[2019],
        )
        
        expense = Expense(100, 'food', 'March', 2019)
        result = expense.adjust_for_inflation()

        # checks if output and inflation calculation are correct
        assert 'your inflation adjusted expense is', result == True
        

    def test_get_lst(self):
        # checks if Expense attributes are correctly represented in a list
        assert type(expense.get_lst()) == list


test_expense = TestExpense()
test_expense.test_init()
test_expense.test_adjust_for_inflation()
test_expense.test_get_lst()


class TestTracker:
    def setup_method(self):
        """dummy dataframe"""
        self.mock_data = pd.DataFrame({
            'Amount': [100.0, 200.0, 300.0],
            'Category': ['food', 'travel', 'food'],
            'Month': ['Mar', 'Apr', 'May'],
            'Year': [2019, 2019, 2020]
        })
        self.tracker = Tracker()
        self.tracker.expenses = self.mock_data.copy()
        
    def test_tracker_init(self):
        # checks if DataFrame to store expenses is initialized correctly
        column_names = ['Amount', 'Category', 'Month', 'Year']
        
        assert type(self.tracker.expenses) == pd.DataFrame
        assert list(self.tracker.expenses.columns) == column_names
        # pandas 64 bit float thingy
        assert self.tracker.expenses['Amount'].dtype == 'float64'
        # pandas uses object for strings
        assert self.tracker.expenses['Category'].dtype == object 
        assert self.tracker.expenses['Month'].dtype == object
        assert self.tracker.expenses['Year'].dtype == int

    def test_add_expenses(self):
        # reset dummy dataframe to empty before checking its empty
        self.tracker.expenses = pd.DataFrame(columns=['Amount', 'Category', 'Month', 'Year'])
        
        # check if tracker instance is empty before expense is added
        assert self.tracker.expenses.empty == True

        # expense object
        expense = Expense(100.0, 'food', 'Mar', 2019)
        self.tracker.add_expenses(expense)
        
        # checks if the expense appended is appended to the main dataframe
        assert len(self.tracker.expenses) == 1

    def test_get_expense_by_category(self):
        # defining category, filtering df
        category = 'food'
        filtered_expenses = self.tracker.expenses[self.tracker.expenses['Category'] == category]

        # checking that rows match category
        assert all(filtered_expenses['Category'] == category)

    def test_get_monthly_summary(self):
        # test 1: normal case - valid month and year
        try:
            self.tracker.get_monthly_summary('March', 2019)  
        except ValueError:
            assert False, "ValueError raised unexpectedly for valid input."

        # test 2: invalid case - no data for specified month and year
        try:
            self.tracker.get_monthly_summary('June', 2019)  
            assert False, "ValueError was not raised for missing data."
        except ValueError as e:
            assert str(e) == "No data found for June 2019.", "Unexpected error message."

    def test_get_yearly_summary(self):
        # test 1: normal case - valid year
        try:
            self.tracker.get_yearly_summary(2019)  
        except ValueError:
            assert False, "ValueError raised unexpectedly for valid input."

        # test 2: invalid case - no data for specified year
        try:
            self.tracker.get_yearly_summary(2027)  
            assert False, "ValueError was not raised for missing data."
        except ValueError as e:
            assert str(e) == "No data found for 2027.", "Unexpected error message."

    def test_calc_inflation_adj_expenses(self):
        # test 1: normal case - valid year
        try:
            print(self.tracker.calc_inflation_adj_expenses(2019))
        except ValueError:
            assert False, "ValueError raised unexpectedly for valid input."

        # test 2: invalid case - no data for specified year
        try:
            self.tracker.calc_inflation_adj_expenses(2027)  
            assert False, "ValueError was not raised for missing data."
        except ValueError as e:
            assert str(e) == "No data found for 2027.", "Unexpected error message."
        

test_t = TestTracker()
test_t.setup_method()  # Initialize mock data for each test
test_t.test_tracker_init()
test_t.setup_method()
test_t.test_add_expenses()
test_t.setup_method()
test_t.test_get_expense_by_category()
test_t.setup_method()
test_t.test_get_monthly_summary()
test_t.setup_method()
test_t.test_calc_inflation_adj_expenses()