#railway ticket booking system
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
file_name = "Ticket.txt"

tickets = []

class Ticket(BaseModel):
    id: Optional[int] = None
    passenger_name: str
    age: int
    gender: str
    train_number: str
    source: str
    destination: str
    journey_date: str
    seat_type: str
    
@app.post("/bookTicket")
def book_ticket(ticket: Ticket):
    file = open(file_name, "a")
    file.write(f"{ticket.id},{ticket.passenger_name},{ticket.age},{ticket.gender},{ticket.train_number},{ticket.source},{ticket.destination},{ticket.journey_date},{ticket.seat_type}\n")
    file.close()
    return {
        "message": "Ticket booked successfully",    
        "data": ticket
    }        
    
@app.get("/getAllTickets")
def get_all_tickets():
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        data.append({
            "id": int(value[0]),
            "passenger_name": value[1],
            "age": int(value[2]),
            "gender": value[3],
            "train_number": value[4],
            "source": value[5],
            "destination": value[6],
            "journey_date": value[7],
            "seat_type": value[8]
        })
    file.close()
    return {
        "message": "Tickets retrieved successfully",
        "data": data
    }
    
    
@app.get("/getTicketByid/{ticket_id}")
def get_ticket_by_id(ticket_id: int):
    file = open(file_name, "r")
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) == ticket_id:
            file.close()
            return {
                "message": "Ticket retrieved successfully",
                "data": {
                    "id": int(value[0]),
                    "passenger_name": value[1],
                    "age": int(value[2]),
                    "gender": value[3],
                    "train_number": value[4],
                    "source": value[5],
                    "destination": value[6],
                    "journey_date": value[7],
                    "seat_type": value[8]
                }
            }
    file.close()
    return {
        "message": "Ticket not found"
    }
    
    
@app.put("/updateTicket/{ticket_id}")
def update_ticket(ticket_id: int, updated_ticket: Ticket):
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) == ticket_id:
            data.append(f"{updated_ticket.id},{updated_ticket.passenger_name},{updated_ticket.age},{updated_ticket.gender},{updated_ticket.train_number},{updated_ticket.source},{updated_ticket.destination},{updated_ticket.journey_date},{updated_ticket.seat_type}\n")
        else:
            data.append(i)
    file.close()
    file = open(file_name, "w")
    for i in data:
        file.write(i)
    file.close()
    return {
        "message": "Ticket updated successfully",
        "data": updated_ticket
    }
    
    
@app.delete("/deleteTicket/{ticket_id}")
def delete_ticket(ticket_id: int):
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        if int(value[0]) != ticket_id:
            data.append(i)
    file.close()
    file = open(file_name, "w")
    for i in data:
        file.write(i)
    file.close()
    return {
        "message": "Ticket deleted successfully"
    }
    
    
@app.get("/availableSeats/{train_number}/{journey_date}/{seat_type}")
def available_seats(train_number: str, journey_date: str, seat_type: str):
    file = open(file_name, "r")
    count = 0
    for i in file:
        value = i.strip().split(",")
        if value[4] == train_number and value[7] == journey_date and value[8] == seat_type:
            count += 1
    file.close()
    return {
        "message": "Available seats retrieved successfully",
        "data": {
            "train_number": train_number,
            "journey_date": journey_date,
            "seat_type": seat_type,
            "available_seats": 100 - count
        }
    } 
    
    
@app.get("/bookingHistory/{passenger_name}")
def booking_history(passenger_name: str):
    file = open(file_name, "r")
    data = []
    for i in file:
        value = i.strip().split(",")
        if value[1] == passenger_name:
            data.append({
                "id": int(value[0]),
                "passenger_name": value[1],
                "age": int(value[2]),
                "gender": value[3],
                "train_number": value[4],
                "source": value[5],
                "destination": value[6],
                "journey_date": value[7],
                "seat_type": value[8]
            })
    file.close()
    return {
        "message": "Booking history retrieved successfully",
        "data": data
    }