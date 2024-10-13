## PULSE RATE SIMULATOR WITH "FATIGUE" DETECTION - HACKVARD 2024

import numpy as np
import matplotlib.pyplot as plt
import time
import random
from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb+srv://gilvaldezarreola:3p5d3XRxRmlGjoNx@cluster0.uyyqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['HOSPITAL']
heart_rate_collection = db['HeartRate']

def send_heart_rate(beats_minute, user_id, fatigue_detected):
    heart_rate_data = {
        "pulse": beats_minute,
        "fatigue": fatigue_detected,
        "id": user_id
    }

    result = heart_rate_collection.insert_one(heart_rate_data)
    print(f"Heart rate data inserted with ID: {result.inserted_id}")

user = 55

# Parámetros de la simulación
n_samples = 150  # Número de muestras simuladas
time_interval = 0.5  # Intervalo de tiempo entre muestras (en segundos)
baseline_heart_rate = 75  # Frecuencia cardíaca promedio inicial (BPM)
variability = 2  # Variabilidad reducida (menos cambios a medida que aumenta la fatiga)
fatigue_factor = 0.15  # Tasa de decaimiento más pronunciada para simular fatiga
stress_peaks=[]
for i in range (3):
    stress_peaks.append(random.randint(1,round(n_samples/2)))  # Momentos de estrés (en muestras)

fatigue_threshold = 55  # Umbral de frecuencia cardíaca para detectar fatiga (BPM)
fatigue_duration_threshold = 8  # Tiempo en segundos para considerar fatiga
fatigue_counter = 0  # Contador para medir cuánto tiempo ha estado por debajo del umbral

# Inicializar el tiempo y la frecuencia cardíaca
time_vals = np.zeros(n_samples)
heart_rate = np.zeros(n_samples)
fatigue_detected = False  # Bandera para indicar si se ha detectado fatiga
total_heart_rate = []

# Bucle de simulación en tiempo real
for i in range(n_samples):
    # Simular fatiga: la frecuencia cardíaca disminuye progresivamente con el tiempo
    baseline_heart_rate -= fatigue_factor

    # Actualizar el tiempo y la frecuencia cardíaca
    time_vals[i] = i * time_interval
    heart_rate[i] = baseline_heart_rate + variability * np.random.randn()

    # Simular evento de estrés (aumento temporal de la frecuencia cardíaca)
    if i in stress_peaks:

        heart_rate[i] = heart_rate[i] + 20 + variability * np.random.randn()

    # Limitar la frecuencia cardíaca a un rango fisiológico razonable
    heart_rate[i] = np.clip(heart_rate[i], 30, 140)

    # Evaluar fatiga: Si la frecuencia está por debajo del umbral por cierto tiempo
    if heart_rate[i] < fatigue_threshold:
        fatigue_counter += time_interval
    else:
        fatigue_counter = 0  # Resetea el contador si sube por encima del umbral

    # Verificar si se ha alcanzado el tiempo bajo fatiga para alertar
    if fatigue_counter >= fatigue_duration_threshold and not fatigue_detected:
        print('¡Alerta: Fatiga detectada!')
        fatigue_detected = True
    
    total_heart_rate.append(float(heart_rate[i]))
    print(heart_rate[i])
    # Pausar para simular el tiempo real
    #send_heart_rate(heart_rate[i],user,time_vals[i]) GILBEEEEERTOOOOO QUIIIITAAAAA ESTEEEE COMMMMMMENTTTTTT
    #time.sleep(time_interval)



send_heart_rate(total_heart_rate,user,fatigue_detected)



#print(stress_peaks)
#print("\n\n")
#print(total_heart_rate)
#print(fatigue_detected)