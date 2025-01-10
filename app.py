from datetime import datetime
import argparse
import random
from storage.mongodb.mongo_utility import *
from config import *
from storage.database import Database
from models.model_domain import Domain

parser = argparse.ArgumentParser(description='Query MongoDB for domains with a specific registration date.')
parser.add_argument('--date', type=str, help='Target registration date in YYYY-MM-DD format')
parser.add_argument('--output_file', type=str, help='output file is .txt containing domains')
parser.add_argument('--job_number', type=int, help='output file is .txt containing domains')
parser.add_argument('--job_index', type=int, help='output file is .txt containing domains')

args = parser.parse_args()
print(f"----> {str(args.date)}")
#target_date_str = dt_obj = datetime.strptime(str(args.date), "%Y-%m-%dT%H:%M:%S.%f%z")
#dt_obj_at_midnight = target_date_str.replace(hour=0, minute=0, second=0, microsecond=0)

dt_obj = datetime.strptime(args.date, "%Y-%m-%dT%H:%M:%S.%f%z")
dt_obj_at_midnight = dt_obj.replace(hour=0, minute=0, second=0, microsecond=0)
utc_timezone = pytz.timezone('UTC')
dt_obj_at_midnight_utc = dt_obj_at_midnight.astimezone(utc_timezone)
#formatted_date = dt_obj_at_midnight_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-0] + 'Z'  # Trim microseconds to three digits
formatted_date = dt_obj_at_midnight_utc.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")[:-7]

mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource={mongo_db}"
database = Database.instance()
print(mongo_uri)
database.create_connection(mongo_uri)

# Query for domains with the specific registration date
_start  = (dt_obj - timedelta(days=0)).replace(microsecond=0, tzinfo=None)
query_result_init : list[Domain] = find_domain(_start,args.job_number,args.job_index)
print(f"Start to write domains in the output file : {args.output_file}")

if query_result_init is not None:
    query_result = list(query_result_init)
    with open(args.output_file, 'w') as fout:
        if query_result is not None:
            if save_limit>0:
                if len(query_result) > save_limit:
                    selected_results = random.sample(query_result, save_limit)
                else:
                    selected_results = query_result
                print(f"-----> {len(selected_results)}")
                for doc in selected_results:
                    fout.write(doc.domain.strip() + '\n')
            else:
                for doc in query_result:
                    fout.write(doc.domain.strip() + '\n')
else:
    print("*************** NO RECCORDES!!!!!")
