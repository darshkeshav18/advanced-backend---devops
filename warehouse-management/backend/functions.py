from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import date, datetime;
from fastapi import HTTPException;


DB_PATH = "study_room.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class packages(Base):
    __tablename__="packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(Integer)
    arrival_date = Column(DateTime)
    status = Column(String)
    dispatchBatchID = Column(Integer, ForeignKey("DispatchBatch.id"), nullable=True)

class DispatchBatch(Base):
    __tablename__="DispatchBatch"
    id = Column(Integer, primary_key=True)
    destination = Column(String)
    vehicle_number = Column(Integer)
    dispatch_status = Column(String, default="Pending")
    dispatch_date = Column(DateTime)
    created_at = Column(String)

Base.metadata.create_all(engine)

# E1
def register_package(id, name, destination, weight, arrival_date, status):
    session = Session(engine)
    
    if session.get(packages, id) is not None:
        session.close()
        raise HTTPException(status_code=409, detail="Package already exists")
    
    new_package = packages(
        id=id,
        name=name,      
        destination=destination,
        weight=weight,
        arrival_date=arrival_date,
        status=status, 
    )
    session.add(new_package)
    session.commit()
    session.close()
    return {"message": "Package registered successfully"}

# E2
def get_package_by_id(id):
    session = Session(engine)
    
    # Fixed: Safely handle ID conversion to prevent AttributeError
    package_id = int(id)
    if package_id.strip().isdigit() == False :
        session.close()
        raise HTTPException(status_code=400, detail="Package ID must be a number")
        
    package = session.get(packages, package_id)
    
    if not package:
        session.close()
        raise HTTPException(status_code=404, detail="Package not found")
        
    response = {
        "id": package.id,
        "name": package.name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status
    }
    session.close()
    return response

# E3
def update_package_details(id, name=None, destination=None, weight=None):
    session = Session(engine)
    package = session.get(packages, id)
    
    if not package:
        session.close()
        raise HTTPException(status_code=404, detail="Package not found")
    
    if name is not None:
        package.name = name
    if destination is not None:
        package.destination = destination
    if weight is not None:
        package.weight = weight
              
    session.commit()
    session.close()
    return {"message": "Package updated successfully"}

# E4
def delete_package(id):
    session = Session(engine)
    package = session.get(packages, id)
    
    if not package:
        session.close()
        raise HTTPException(status_code=404, detail="Package not found")
    
    if package.status == "Dispatched":
        session.close()
        raise HTTPException(status_code=400, detail="Cannot delete a package that has already been dispatched")
    
    # Fixed: Correct SQLAlchemy delete syntax
    session.delete(package)
    session.commit()
    session.close()
    return {"message": "Package deleted successfully"}

# E5
def search_package(destination=None, status=None, arrival_date=None):
    session = Session(engine)
    query = session.query(packages)

    if destination is not None:
        query = query.filter(packages.destination == destination)
    if status is not None:
        query = query.filter(packages.status == status)
    if arrival_date is not None:
        query = query.filter(packages.arrival_date == arrival_date)

    package_list = query.all()

    if not package_list:
        session.close()
        raise HTTPException(status_code=404, detail="Package not found")

    response = []
    for package in package_list:
        response.append({
            "id": package.id,
            "name": package.name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status,
        })

    session.close()
    return response

# E6
def view_dispatchBatches(destination=None, vehicle_number=None, dispatch_status=None):
    session = Session(engine)
    query = session.query(DispatchBatch)

    if destination is not None:
        query = query.filter(DispatchBatch.destination == destination)
    if vehicle_number is not None:
        query = query.filter(DispatchBatch.vehicle_number == vehicle_number)
    if dispatch_status is not None:
        query = query.filter(DispatchBatch.dispatch_status == dispatch_status)

    dispatch_batches_list = query.all()

    if not dispatch_batches_list:
        session.close()
        raise HTTPException(status_code=404, detail="DispatchBatch not found")

    response = []
    for dispatch_batch in dispatch_batches_list:
        response.append({
            "id": dispatch_batch.id,
            "destination": dispatch_batch.destination,
            "vehicle_number": dispatch_batch.vehicle_number,
            "dispatch_status": dispatch_batch.dispatch_status,
            "dispatch_date": dispatch_batch.dispatch_date,
            "created_at": dispatch_batch.created_at,
        })

    session.close()
    return response


# E7
def get_all_dispatchBatches():
    session = Session(engine)
    query = session.query(DispatchBatch)

    dispatch_batches_list = query.all()
    response = []
    for dispatch_batch in dispatch_batches_list:
        response.append({
            "id": dispatch_batch.id,
            "destination": dispatch_batch.destination,
            "vehicle_number": dispatch_batch.vehicle_number,
            "dispatch_status": dispatch_batch.dispatch_status,
            "dispatch_date": dispatch_batch.dispatch_date,
            "created_at": dispatch_batch.created_at,
        })
    session.close()
    return response


# E8
def create_dispatchBatches(id, destination, vehicle_number, dispatch_status="Pending", dispatch_date=None, created_at=None):
    session = Session(engine)

    batch_id = int(id)

    if session.get(DispatchBatch, batch_id) is not None:
        session.close()
        raise HTTPException(status_code=409, detail="DispatchBatch already exists")

    new_dispatch_batch = DispatchBatch(
        id=batch_id,
        destination=destination,
        vehicle_number=vehicle_number,
        dispatch_status=dispatch_status or "Pending",
        dispatch_date=dispatch_date,
        created_at=created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    session.add(new_dispatch_batch)
    session.commit()
    session.close()

    return {"message": "Dispatch successfully"}