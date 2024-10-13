from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URI = 'mongodb+srv://gilvaldezarreola:3p5d3XRxRmlGjoNx@cluster0.uyyqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)


db = client["HOSPITAL"]  
heart_rate_collection = db["HeartRate"]  


def send_heart_rate(beats_minute, user_id,time):
    
    heart_rate_data = {
        "beats_minute": beats_minute,
        "time": time,  
        "id": user_id  
    }

    
    result = heart_rate_collection.insert_one(heart_rate_data)
    
    
    print(f"Heart rate data inserted with ID: {result.inserted_id}")


if __name__ == "__main__":
    
    beats_minute = 72
    user_id = 77

    send_heart_rate(beats_minute, user_id)
