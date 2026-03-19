"""
The Train Captain - Passenger Manager
Handles passenger data validation, management, and operations
"""

import re
from datetime import datetime, date
import json
from typing import List, Dict, Optional, Tuple

class Passenger:
    """Passenger class representing a single passenger"""
    
    def __init__(self, name: str, age: int, gender: str, 
                 id_type: str, id_number: str, concession: bool = False):
        self.name = name
        self.age = age
        self.gender = gender
        self.id_type = id_type
        self.id_number = id_number
        self.concession = concession
        self.berth_allocation = None
        self.booking_status = "Confirmed"
        self.passenger_id = self.generate_passenger_id()
    
    def generate_passenger_id(self) -> str:
        """Generate unique passenger ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        name_part = self.name[:3].upper() if self.name else "XXX"
        return f"{name_part}{timestamp[-6:]}"
    
    def to_dict(self) -> Dict:
        """Convert passenger to dictionary"""
        return {
            'passenger_id': self.passenger_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'id_type': self.id_type,
            'id_number': self.id_number,
            'concession': self.concession,
            'berth_allocation': self.berth_allocation,
            'booking_status': self.booking_status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Passenger':
        """Create passenger from dictionary"""
        passenger = cls(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            id_type=data['id_type'],
            id_number=data['id_number'],
            concession=data.get('concession', False)
        )
        passenger.passenger_id = data.get('passenger_id', passenger.passenger_id)
        passenger.berth_allocation = data.get('berth_allocation')
        passenger.booking_status = data.get('booking_status', 'Confirmed')
        return passenger
    
    def validate(self) -> Tuple[bool, str]:
        """Validate passenger data"""
        # Name validation
        if not self.name or len(self.name.strip()) < 3:
            return False, "Name must be at least 3 characters long"
        
        if not re.match(r"^[A-Za-z\s\.]+$", self.name):
            return False, "Name can only contain letters, spaces and dots"
        
        # Age validation
        if not isinstance(self.age, int) or self.age < 1 or self.age > 120:
            return False, "Age must be between 1 and 120"
        
        # Gender validation
        if self.gender not in ["Male", "Female", "Other"]:
            return False, "Invalid gender selection"
        
        # ID validation
        if not self.id_number or len(self.id_number.strip()) < 4:
            return False, "ID number must be at least 4 characters"
        
        # ID type specific validation
        if self.id_type == "Aadhar Card":
            if not re.match(r"^\d{4}\s?\d{4}\s?\d{4}$", self.id_number):
                return False, "Invalid Aadhar number format (should be 12 digits)"
        
        elif self.id_type == "PAN Card":
            if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", self.id_number.upper()):
                return False, "Invalid PAN number format (e.g., ABCDE1234F)"
        
        elif self.id_type == "Passport":
            if not re.match(r"^[A-Z]{1}[0-9]{7}$", self.id_number.upper()):
                return False, "Invalid Passport number format"
        
        # Concession validation
        if self.concession and self.age < 60:
            return False, "Senior citizen concession requires age 60 or above"
        
        return True, "Valid"


class PassengerManager:
    """Manages multiple passengers for a booking"""
    
    def __init__(self, max_passengers: int = 6):
        self.passengers: List[Passenger] = []
        self.max_passengers = max_passengers
        self.concession_count = 0
        self.child_count = 0
        self.infant_count = 0
    
    def add_passenger(self, passenger: Passenger) -> Tuple[bool, str]:
        """Add a passenger to the booking"""
        # Check max limit
        if len(self.passengers) >= self.max_passengers:
            return False, f"Cannot add more than {self.max_passengers} passengers"
        
        # Validate passenger
        is_valid, message = passenger.validate()
        if not is_valid:
            return False, message
        
        # Check for duplicate ID
        for p in self.passengers:
            if p.id_type == passenger.id_type and p.id_number == passenger.id_number:
                return False, f"Passenger with same {passenger.id_type} already exists"
        
        # Add passenger
        self.passengers.append(passenger)
        
        # Update counts
        if passenger.concession:
            self.concession_count += 1
        if passenger.age < 12:
            self.child_count += 1
        if passenger.age < 5:
            self.infant_count += 1
        
        return True, "Passenger added successfully"
    
    def remove_passenger(self, passenger_id: str) -> bool:
        """Remove a passenger by ID"""
        for i, passenger in enumerate(self.passengers):
            if passenger.passenger_id == passenger_id:
                # Update counts before removing
                if passenger.concession:
                    self.concession_count -= 1
                if passenger.age < 12:
                    self.child_count -= 1
                if passenger.age < 5:
                    self.infant_count -= 1
                
                self.passengers.pop(i)
                return True
        return False
    
    def update_passenger(self, passenger_id: str, **kwargs) -> bool:
        """Update passenger details"""
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                # Update fields
                if 'name' in kwargs:
                    passenger.name = kwargs['name']
                if 'age' in kwargs:
                    old_age = passenger.age
                    passenger.age = kwargs['age']
                    
                    # Update counts based on age change
                    if old_age < 12 and passenger.age >= 12:
                        self.child_count -= 1
                    elif old_age >= 12 and passenger.age < 12:
                        self.child_count += 1
                    
                    if old_age < 5 and passenger.age >= 5:
                        self.infant_count -= 1
                    elif old_age >= 5 and passenger.age < 5:
                        self.infant_count += 1
                    
                    if old_age < 60 and passenger.age >= 60 and passenger.concession:
                        self.concession_count += 1
                    elif old_age >= 60 and passenger.age < 60 and passenger.concession:
                        self.concession_count -= 1
                
                if 'gender' in kwargs:
                    passenger.gender = kwargs['gender']
                if 'id_type' in kwargs:
                    passenger.id_type = kwargs['id_type']
                if 'id_number' in kwargs:
                    passenger.id_number = kwargs['id_number']
                if 'concession' in kwargs:
                    old_concession = passenger.concession
                    passenger.concession = kwargs['concession']
                    
                    # Update concession count
                    if old_concession and not passenger.concession:
                        self.concession_count -= 1
                    elif not old_concession and passenger.concession:
                        self.concession_count += 1
                
                return True
        return False
    
    def get_passenger(self, passenger_id: str) -> Optional[Passenger]:
        """Get passenger by ID"""
        for passenger in self.passengers:
            if passenger.passenger_id == passenger_id:
                return passenger
        return None
    
    def get_all_passengers(self) -> List[Dict]:
        """Get all passengers as dictionaries"""
        return [p.to_dict() for p in self.passengers]
    
    def clear_all(self):
        """Remove all passengers"""
        self.passengers.clear()
        self.concession_count = 0
        self.child_count = 0
        self.infant_count = 0
    
    def get_count(self) -> int:
        """Get total passenger count"""
        return len(self.passengers)
    
    def get_summary(self) -> Dict:
        """Get passenger summary"""
        return {
            'total': len(self.passengers),
            'adults': len(self.passengers) - self.child_count,
            'children': self.child_count,
            'infants': self.infant_count,
            'senior_citizens': self.concession_count,
            'male': sum(1 for p in self.passengers if p.gender == "Male"),
            'female': sum(1 for p in self.passengers if p.gender == "Female")
        }
    
    def allocate_berths(self, preference: str = None) -> bool:
        """Allocate berths to passengers"""
        if not self.passengers:
            return False
        
        # Berth allocation logic
        berths = ['L', 'M', 'U', 'SL', 'SU']
        available_berths = berths.copy()
        
        # Sort passengers by age for priority
        sorted_passengers = sorted(self.passengers, 
                                  key=lambda x: (-x.age if x.concession else x.age))
        
        for i, passenger in enumerate(sorted_passengers):
            # Priority for seniors and children
            if passenger.age >= 60 or passenger.age <= 5:
                # Give lower berth preference
                if 'L' in available_berths:
                    passenger.berth_allocation = 'L'
                    available_berths.remove('L')
                elif 'SL' in available_berths:
                    passenger.berth_allocation = 'SL'
                    available_berths.remove('SL')
                else:
                    passenger.berth_allocation = available_berths[0] if available_berths else 'L'
                    if available_berths:
                        available_berths.pop(0)
            else:
                # Normal allocation
                if preference and preference in available_berths:
                    passenger.berth_allocation = preference
                    available_berths.remove(preference)
                else:
                    passenger.berth_allocation = available_berths[0] if available_berths else 'L'
                    if available_berths:
                        available_berths.pop(0)
            
            # Reset available berths if empty
            if not available_berths:
                available_berths = berths.copy()
        
        return True
    
    def validate_all(self) -> Tuple[bool, List[str]]:
        """Validate all passengers"""
        valid = True
        errors = []
        
        for i, passenger in enumerate(self.passengers, 1):
            is_valid, message = passenger.validate()
            if not is_valid:
                valid = False
                errors.append(f"Passenger {i}: {message}")
        
        return valid, errors
    
    def calculate_fare(self, base_fare: int, quota: str = "GN") -> Dict:
        """Calculate total fare for all passengers"""
        total_fare = 0
        passenger_fares = []
        
        for passenger in self.passengers:
            fare = base_fare
            
            # Apply quota charges
            if quota == "TQ":  # Tatkal
                fare = int(fare * 1.3)  # 30% extra
            elif quota == "SS" and passenger.concession:  # Senior citizen
                fare = int(fare * 0.6)  # 40% discount
            
            # Child discount (age 5-12)
            if 5 <= passenger.age < 12:
                fare = int(fare * 0.75)  # 25% discount
            
            # Infant (age < 5)
            if passenger.age < 5:
                fare = 0  # No fare for infants
            
            passenger_fares.append({
                'passenger_id': passenger.passenger_id,
                'name': passenger.name,
                'base_fare': base_fare,
                'final_fare': fare,
                'concession_applied': passenger.concession and quota == "SS",
                'child_discount': 5 <= passenger.age < 12,
                'infant': passenger.age < 5
            })
            
            total_fare += fare
        
        # Calculate GST (5%)
        gst = int(total_fare * 0.05)
        total_with_gst = total_fare + gst
        
        return {
            'passenger_fares': passenger_fares,
            'subtotal': total_fare,
            'gst': gst,
            'total': total_with_gst,
            'passenger_count': len(self.passengers)
        }
    
    def save_to_file(self, filename: str) -> bool:
        """Save passengers to file"""
        try:
            data = {
                'passengers': [p.to_dict() for p in self.passengers],
                'summary': self.get_summary(),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving passengers: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Load passengers from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.clear_all()
            for p_data in data.get('passengers', []):
                passenger = Passenger.from_dict(p_data)
                self.passengers.append(passenger)
                
                # Update counts
                if passenger.concession:
                    self.concession_count += 1
                if passenger.age < 12:
                    self.child_count += 1
                if passenger.age < 5:
                    self.infant_count += 1
            
            return True
        except Exception as e:
            print(f"Error loading passengers: {e}")
            return False


class BerthAllocator:
    """Handles berth allocation logic"""
    
    BERTH_TYPES = {
        'L': 'Lower',
        'M': 'Middle',
        'U': 'Upper',
        'SL': 'Side Lower',
        'SU': 'Side Upper'
    }
    
    @staticmethod
    def get_available_berths(coach_type: str = "3A") -> List[str]:
        """Get available berth types based on coach"""
        if coach_type == "1A":
            return ['L', 'U']  # First AC has only Lower and Upper
        elif coach_type == "2A":
            return ['L', 'U', 'SL', 'SU']  # Second AC has all except Middle
        elif coach_type == "3A":
            return ['L', 'M', 'U', 'SL', 'SU']  # Third AC has all types
        elif coach_type == "SL":
            return ['L', 'M', 'U', 'SL', 'SU']  # Sleeper has all types
        elif coach_type == "CC":
            return ['W']  # Chair Car has window seats only
        return ['L', 'M', 'U']
    
    @staticmethod
    def allocate_optimal_berths(passengers: List[Passenger], 
                                coach_type: str = "3A",
                                preferences: Dict[str, str] = None) -> Dict[str, str]:
        """Allocate berths optimally"""
        available = BerthAllocator.get_available_berths(coach_type)
        allocation = {}
        
        # Priority 1: Special needs (senior citizens, pregnant women, etc.)
        special_needs = [p for p in passengers if p.age >= 60 or 
                        (hasattr(p, 'special_needs') and p.special_needs)]
        
        for passenger in special_needs:
            if 'L' in available:
                allocation[passenger.passenger_id] = 'L'
                available.remove('L')
            elif 'SL' in available:
                allocation[passenger.passenger_id] = 'SL'
                available.remove('SL')
        
        # Priority 2: Preferences
        if preferences:
            for passenger in passengers:
                if passenger.passenger_id in allocation:
                    continue
                    
                pref = preferences.get(passenger.passenger_id)
                if pref and pref in available:
                    allocation[passenger.passenger_id] = pref
                    available.remove(pref)
        
        # Priority 3: Remaining passengers
        remaining = [p for p in passengers if p.passenger_id not in allocation]
        for passenger in remaining:
            if available:
                # Try to distribute evenly
                if len(available) > 1:
                    # Alternate between upper and lower
                    if len(allocation) % 2 == 0:
                        berth = 'L' if 'L' in available else available[0]
                    else:
                        berth = 'U' if 'U' in available else available[0]
                else:
                    berth = available[0]
                
                allocation[passenger.passenger_id] = berth
                available.remove(berth)
            
            # Reset available if empty
            if not available:
                available = BerthAllocator.get_available_berths(coach_type)
        
        return allocation