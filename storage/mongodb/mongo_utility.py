from models.model_domain import *
from typing import Optional
from datetime import datetime, timedelta
import pytz

def find_domain(start_date: datetime,total_part:int,part:int) -> Optional[list[Domain]]:
    end_date = (start_date - timedelta(days=1)).replace(microsecond=0, tzinfo=None)
    try:
        print(f"total_part : {total_part} , part : {part}")
        print(f"start : {start_date} , end : {end_date}")
        # domain = Domain.objects.filter(register_date__gte=end_date, register_date__lte=start_date)
        domain = Domain.objects.filter(register_date=start_date)
        total_documents = domain.count()
        print(f"len main q :{total_documents}")        
        _section_size = total_documents // total_part
        start_index = _section_size * part
        end_index = start_index + _section_size
        print(f"start_index : {start_index} , end_index : {end_index}")
        _my_part = domain.order_by('id')[start_index:end_index]

        if domain:
            print(f"Found domain: {len(_my_part)}")
            return _my_part
        else:
            print("Domain not found.")
            return None
    except Exception as e:
        print(f"Error finding domain: {e}")
        return None