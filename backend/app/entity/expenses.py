from pydantic import BaseModel
from datetime import date, datetime

class baseexpenses(BaseModel):
    title:str
    description:str
    amount:float
    date:date

class expensesModel(baseexpenses):
    id:int
    user_id:int
    created_at:datetime
