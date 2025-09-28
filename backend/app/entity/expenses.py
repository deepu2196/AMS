from pydantic import BaseModel
from datetime import date, datetime

class baseExpense(BaseModel):
    title:str
    description:str
    amount:float
    expense_date:date

class expenseCreate(baseExpense):
    user_id: int

class expensesModel(baseExpense):
    id:int
    user_id:int
    created_at:datetime

#outputmodels
class expenseCreatedResponse(BaseModel):
    id : int
