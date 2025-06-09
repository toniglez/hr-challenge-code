from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Load(Base):
    __tablename__ = "loads"

    load_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Unique identifier for the load

    # Origin location
    origin_county = Column(String, nullable=False)  # Starting county
    origin_state = Column(String, nullable=False)   # Starting state

    # Destination location
    destination_county = Column(String, nullable=False)  # Delivery county
    destination_state = Column(String, nullable=False)   # Delivery state

    # Date & time
    pickup_datetime = Column(DateTime, nullable=False)   # Date and time for pickup
    delivery_datetime = Column(DateTime, nullable=False) # Date and time for delivery

    # Load details
    equipment_type = Column(String)           # Type of equipment needed
    loadboard_rate = Column(Float)            # Listed rate for the load
    max_loadboard_rate = Column(Float)        # Maximum rate for the load
    notes = Column(String)                    # Additional information
    weight = Column(Float)                    # Load weight
    commodity_type = Column(String)           # Type of goods
    num_of_pieces = Column(Integer)           # Number of items
    miles = Column(Float)                     # Distance to travel

    # Dimensions
    length = Column(Float)                    # Length of the load
    width = Column(Float)                     # Width of the load
    height = Column(Float)                    # Height of the load



class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, index=True,
                      comment="When the call occurred")
    created_at = Column(DateTime, default=datetime.utcnow,
                       comment="When the record was created")
    
    # Carrier info
    carrier_mc_number = Column(String(20), index=True,
                              comment="Motor Carrier number of the carrier", nullable=True, default=None)
    authorized = Column(Boolean, default=False)

    # Carrier preferences
    origin_state = Column(String, nullable=True, default=None)
    weight_max = Column(Float, nullable=True, default=None)

    # Call outcome and classification
    call_outcome = Column(String, nullable=True, default=None)
    sentiment = Column(String, nullable=True, default=None)
    summary = Column(Text, nullable=True, default=None)

    # Negotiation
    negotiation_attempts = Column(Integer, default=0)
    original_price = Column(Float, nullable=True, default=None)
    final_offer = Column(Float, nullable=True, default=None)

    # Load (if booked)
    selected_load_id = Column(Integer, nullable=True, default=None)
    
    # Optional metadata
    transcript = Column(Text, nullable=True, default=None)
    notes = Column(Text, nullable=True, default=None)
