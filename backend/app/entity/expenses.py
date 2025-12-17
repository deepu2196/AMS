from pydantic import BaseModel
from datetime import date, datetime

class BaseExpense(BaseModel):
    title:str
    description:str
    amount:float
    expense_date:date

class ExpenseCreate(BaseExpense):
    user_id: int

class ExpensesModel(BaseExpense):
    id:int
    user_id:int
    created_at:datetime

#outputmodels
class ExpenseCreatedResponse(BaseModel):
    id : int
