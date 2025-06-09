from fastapi import FastAPI, Depends, Query, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from api.database import SessionLocal, engine
from api.models import Base, Load, Call
from api import schemas
from datetime import datetime
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, case

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Load Management API",
    description="API for managing transportation loads",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key authentication dependency
def verify_api_key(x_api_key: str = Header(...)):
    expected_key = os.getenv("API_KEY")
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")
    finally:
        db.close()

@app.post("/loads", response_model=schemas.LoadRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
def create_load(load: schemas.LoadCreate, db: Session = Depends(get_db)):
    try:
        db_load = Load(**load.dict())
        db.add(db_load)
        db.commit()
        db.refresh(db_load)
        return db_load
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to create load: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create load")

@app.get("/loads", response_model=List[schemas.LoadRead], dependencies=[Depends(verify_api_key)])
def get_all_loads(db: Session = Depends(get_db)):
    try:
        now = datetime.utcnow()
        loads = db.query(Load).filter(Load.pickup_datetime > now).all()
        return loads
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve loads: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve loads")

@app.get("/loads/search", response_model=List[schemas.LoadRead], dependencies=[Depends(verify_api_key)])
def search_loads(
    origin_state: Optional[str] = Query(None),
    destination_state: Optional[str] = Query(None),
    pickup_from: Optional[datetime] = Query(None),
    pickup_to: Optional[datetime] = Query(None),
    delivery_from: Optional[datetime] = Query(None),
    delivery_to: Optional[datetime] = Query(None),
    equipment_type: Optional[str] = Query(None),
    weight_min: Optional[float] = Query(None),
    weight_max: Optional[float] = Query(None),
    miles_min: Optional[float] = Query(None),
    miles_max: Optional[float] = Query(None),
    show_past: bool = Query(False),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Load)
        if not show_past:
            query = query.filter(Load.pickup_datetime > datetime.utcnow())
        if origin_state:
            query = query.filter(Load.origin_state == origin_state)
        if destination_state:
            query = query.filter(Load.destination_state == destination_state)
        if pickup_from:
            query = query.filter(Load.pickup_datetime >= pickup_from)
        if pickup_to:
            query = query.filter(Load.pickup_datetime <= pickup_to)
        if delivery_from:
            query = query.filter(Load.delivery_datetime >= delivery_from)
        if delivery_to:
            query = query.filter(Load.delivery_datetime <= delivery_to)
        if equipment_type:
            query = query.filter(Load.equipment_type.ilike(f"%{equipment_type}%"))
        if weight_min:
            query = query.filter(Load.weight >= weight_min)
        if weight_max:
            query = query.filter(Load.weight <= weight_max)
        if miles_min:
            query = query.filter(Load.miles >= miles_min)
        if miles_max:
            query = query.filter(Load.miles <= miles_max)
        results = query.all()
        return results
    except SQLAlchemyError as e:
        logger.error(f"Search query failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to search loads")

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/calls/update/{call_id}", response_model=schemas.CallRead, dependencies=[Depends(verify_api_key)])
async def update_call_via_post(call_id: int, call_update: schemas.CallUpdate, db: Session = Depends(get_db)):
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if not call:
            raise HTTPException(status_code=404, detail=f"Call {call_id} not found")
        update_data = call_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(call, field, value)
        db.commit()
        db.refresh(call)
        return call
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error updating call {call_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update call record")

@app.post("/calls", response_model=schemas.CallRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
async def create_call(call: schemas.CallCreate, db: Session = Depends(get_db)):
    try:
        call_data = call.dict()
        if not call.timestamp:
            call_data["timestamp"] = datetime.now()
        db_call = Call(**call_data)
        db.add(db_call)
        db.commit()
        db.refresh(db_call)
        return db_call
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error creating call: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create call record")

@app.get("/calls", response_model=List[schemas.CallRead], dependencies=[Depends(verify_api_key)])
async def get_all_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        calls = db.query(Call).order_by(Call.timestamp.desc()).offset(skip).limit(limit).all()
        return calls
    except SQLAlchemyError as e:
        logging.error(f"Database error retrieving calls: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve call records")

@app.get("/calls/{call_id}", response_model=schemas.CallRead, dependencies=[Depends(verify_api_key)])
async def get_call(call_id: int, db: Session = Depends(get_db)):
    try:
        call = db.query(Call).filter(Call.id == call_id).first()
        if call is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Call with ID {call_id} not found")
        return call
    except SQLAlchemyError as e:
        logging.error(f"Database error retrieving call {call_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve call record")

@app.delete("/calls", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_api_key)])
async def delete_all_calls(db: Session = Depends(get_db)):
    try:
        count = db.query(Call).count()
        db.query(Call).delete()
        db.commit()
        return {"message": f"Successfully deleted {count} call records"}
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error deleting calls: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete call records")

@app.get("/metrics/agent", dependencies=[Depends(verify_api_key)])
def agent_metrics(db: Session = Depends(get_db)):
    try:
        total_calls = db.query(func.count(Call.id)).scalar()
        booked_calls = db.query(func.count(Call.id)).filter(Call.selected_load_id.isnot(None)).scalar()
        conversion_rate = (booked_calls / total_calls) if total_calls else 0

        avg_negotiation_attempts = db.query(func.avg(Call.negotiation_attempts)).scalar() or 0

        avg_price_increase = db.query(
            func.avg(
                func.coalesce(Call.final_offer, 0) - func.coalesce(Call.original_price, 0)
            )
        ).scalar() or 0

        avg_increase_pct = db.query(
            func.avg(
                case(
                    (Call.original_price > 0,
                     (Call.final_offer - Call.original_price) / Call.original_price * 100),
                    else_=0
                )
            )
        ).scalar() or 0

        sentiment_counts = dict(
            db.query(Call.sentiment, func.count()).group_by(Call.sentiment).all()
        )

        return {
            "total_calls": total_calls,
            "booked_calls": booked_calls,
            "conversion_rate": round(conversion_rate, 3),
            "avg_negotiation_attempts": round(avg_negotiation_attempts, 2),
            "avg_price_increase": round(avg_price_increase, 2),
            "avg_price_increase_pct": round(avg_increase_pct, 2),
            "sentiment_distribution": sentiment_counts,
        }

    except Exception as e:
        logging.exception("Failed to compute agent metrics")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compute agent metrics"
        )
