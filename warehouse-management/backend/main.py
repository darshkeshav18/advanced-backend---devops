from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date

import function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#E1
@app.post("/packages")
def register_package(id , name, destination, weight, arrival_date , status):
    return function.register_package(id=id , name=name, destination=destination, weight=weight, arrival_date=arrival_date , status=status)


#E2
@app.get("/packages/{package_id}")
def get_package_details(id):
    return function.get_package_by_id(id)


#E3
@app.patch("/packages/{package_id}")
def update_package_details(id):
    return function.update_package_details(id)


#E4
@app.delete("/packages/{package_id}")
def delete_package(id):
    return function.delete_package(id)


#E5
@app.get("/packages?destination=&status=&arrival_date=")    
def search_package(destination, status, arrival_date):
    return function.search_package(destination, status, arrival_date)



#E6
@app.get("/dispatch-batches?destination=&vehicle_number=&dispatch_status=")
def view_dispatchBatches(destination, vehicle_nuber, dispatch_status):
    return function.view_dispatchBatches(destination, vehicle_nuber, dispatch_status)



#E7
@app.get("/warehouse/summary")
def warehouse_summary():
    return function.get_all_dispatchBatches()

#E8
@app.post("/dispatchBatches")
def add_dispatch(destination, vehicle_number, created_at):
    return function.create_dispatchBatches(destination= destination, vehicle_number= vehicle_number, created_at= created_at)