# Expense Tracker
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
file_name = "Expense.txt"

expenses = []

class Expense(BaseModel):
    id: int
    amount: float
    category: str

@app.post("/addExpense")
def add_expense(expense: Expense):
        file = open(file_name, "a")
        file.write(f"{expense.id},{expense.amount},{expense.category}\n")       
        file.close()
        return {
            "message": "Expense added successfully",
            "data": expense
        }
@app.get("/getAllExpenses")
def get_all_expenses():
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")

        data.append({
            "id": int(value[0]),
            "amount": float(value[1]),
            "category": value[2]
        })
    file.close()
    return {
        "data": data
    }

@app.get("/getExpenseByID/{expense_id}")
def get_expense_by_id(expense_id: int):
    file = open(file_name, "r")
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) == expense_id:
            file.close()
            return {
                "id": int(value[0]),
                "amount": float(value[1]),
                "category": value[2]
            }
    return {
        "message": "Expense not found"
    }

@app.put("/updateExpense/{expense_id}")
def update_expense(expense_id: int, updated_expense: Expense):  
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) == expense_id:
            data.append(f"{updated_expense.id},{updated_expense.amount},{updated_expense.category}\n")
        else:
            data.append(i)
    file.close()
    file = open(file_name, "w")
    for line in data:
        file.write(line)
    file.close()
    return {
        "message": "Expense updated successfully",
    }

@app.delete("/deleteExpenseByID/{expense_id}")
def delete_expense_by_id(expense_id: int):
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) != expense_id:
            data.append(i)
    file.close()
    file = open(file_name, "w")
    for line in data:
        file.write(line)
        file.close()
    return {
        "message": "Expense deleted successfully"
    }

@app.delete("/deleteAllExpenses")
def delete_all_expenses():
    file = open(file_name, "w")
    file.close()
    return {
        "message": "All expenses deleted successfully"
    }