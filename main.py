import requests
import datetime as dt
import os
import csv
import warnings
import serial
import pandas as pd
import numpy as np
import joblib
import json
print(f"\n\n========== PROGRAM DIMULAI ==========")


warnings.filterwarnings("ignore", category=UserWarning)
model = joblib.load("Land_Slide_Model_Predictor.pkl")

app_id = "a26baac9-bd90-4613-ad40-d3ea16e844de"
rest_api_key = "YzMzODY2MjUtZTNjYS00YzdhLTkwYmItZjY4NjY5MjdjMTll"

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

# csv_path =

# TITIK 1
nama1 = "Lokasi 1"
tikum1 = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
lat1 = -6.842157109211024
lng1 = 107.56864072401038
penjelasan1 = "Titik 1 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."

# TITIK 2
nama2 = "Lokasi 2"
tikum2 = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
lat2 = -6.832474922745673
lng2 = 107.58112551641517
penjelasan2 = "Titik 2 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."


# TITIK 3
nama3 = "Lokasi 3"
tikum3 = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
lat3 = -6.811430435230934
lng3 = 107.53326722506678
penjelasan3 = "Titik 3 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."

awas1 = False
siaga1 = False
awas2 = False
siaga2 = False
awas3 = False
siaga3 = False

now = datetime.now()


def write_csv(var1, var2, var3, var4, node):
    with open(database_local.csv, 'w', newline='') as csvfile:
        field = ['date', 'vibration', 'inclination', 'humidity', 'node']
        variables = [['date', 'vibration', 'inclination', 'humidity', 'node'],
                     [now.strftime("%d/%m/%Y %H:%M:%S"), var1, var2, var3, var4, node]]
        write = csv.writer(csvfile, fieldnames=field)
        write.writeheader()
        write.writerows(variables)


def detail(path):
    buttons = [
        {"id": path, "text": "Detail"},
        {"id": path + "_maps", "text": "Titik kumpul"}
    ]
    return buttons


def sendNotif(path, nama, status, url_gambar, buttons):
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {rest_api_key}"
    }

    payload = {
        "app_id": app_id,
        "included_segments": ["Total Subscriptions"],
        "contents": {"en": f"{nama} Terdeteksi Status {status}, Segera evakuasi ke titik kumpul apabila berada di sekitar area"},
        "headings": {"en": f"{nama} Rawan Longsor !"},
        "big_picture": url_gambar,
        "buttons": buttons,
        "data": {"titik": f"{path}"}
    }

    req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=header,
        data=json.dumps(payload)
    )

    return req.status_code, req.text


def predict():
    global awas1, siaga1, awas2, siaga2, awas3, siaga3
    data_input = np.array([[float(vibration1), float(inclination1), (float(humidity1)/100), float(precipitation1)], [float(vibration2), float(inclination2),
                          (float(humidity2)/100), float(precipitation2)], [float(vibration3), float(inclination3), (float(humidity3)/100), float(precipitation3)]])
    probability = model.predict_proba(data_input)
    value1 = probability[0, 1]
    value2 = probability[1, 1]
    value3 = probability[2, 1]
    print(f"Probabilitas 1 : {value1}  Probabilitas 2 : {value2}  Probabilitas 3 : {value3}")
    if value1 > 0.75 and value1 <= 1:
        status1 = "AWAS"
        if not awas1:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik1")
            status_code, response = sendNotif(
                "titik1", nama1, status1, url_gambar, buttons)
            print(f"Notifikasi 1: {response}")
            awas1 = True

    elif value1 > 0.5 and value1 <= 0.75:
        status1 = "SIAGA"
        awas1 = False
        if not siaga1:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik1")
            status_code, response = sendNotif(
                "titik1", nama1, status1, url_gambar, buttons)
            print(f"Notifikasi 1: {response}")
            siaga1 = True
    elif value1 > 0.25 and value1 <= 0.5:
        status1 = "WASPADA"
        awas1 = False
        siaga1 = False
    else:
        status1 = "NORMAL"
        awas1 = False
        siaga1 = False

    if value2 > 0.75 and value2 <= 1:
        status2 = "AWAS"
        if not awas2:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik2")
            status_code, response = sendNotif(
                "titik2", nama2, status2, url_gambar, buttons)
            print(f"Notifikasi 2: {response}")
            awas2 = True
    elif value2 > 0.5 and value2 <= 0.75:
        status2 = "SIAGA"
        awas2 = False
        if not siaga2:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik2")
            status_code, response = sendNotif(
                "titik2", nama2, status2, url_gambar, buttons)
            print(f"Notifikasi 2: {response}")
            siaga2 = True
    elif value2 > 0.25 and value2 <= 0.5:
        status2 = "WASPADA"
        awas2 = False
        siaga2 = False
    else:
        status2 = "NORMAL"
        awas2 = False
        siaga2 = False

    if value3 > 0.75 and value3 <= 1:
        status3 = "AWAS"
        if not awas3:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik3")
            status_code, response = sendNotif(
                "titik3", nama3, status3, url_gambar, buttons)
            print(f"Notifikasi 3: {response}")
            awas3 = True
    elif value3 > 0.5 and value3 <= 0.75:
        status3 = "SIAGA"
        awas3 = False
        if not siaga3:
            url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
            buttons = detail("titik3")
            status_code, response = sendNotif(
                "titik3", nama3, status3, url_gambar, buttons)
            print(f"Notifikasi 3: {response}")
            siaga3 = True
    elif value3 > 0.25 and value3 <= 0.5:
        status3 = "WASPADA"
        awas3 = False
        siaga3 = False
    else:
        status3 = "NORMAL"
        awas3 = False
        siaga3 = False

    print(f"Status 1 : {status1}  Status 2 : {
          status2}  Status 3 : {status3}  ")

    data = {
        "titik1": {
            "aktifkan": True,
            "tikum": tikum1,
            "lat": lat1,
            "lng": lng1,
            "lokasi": nama1,
            "penjelasan": penjelasan1,
            "sensor": {
                "curah hujan": round(float(precipitation1)),
                "getaran": round(float(vibration1)),
                "kelembapan": round(float(humidity1)),
                "kemiringan": round(float(inclination1))
            },
            "status": status1
        },
        "titik2": {
            "aktifkan": True,
            "tikum": tikum2,
            "lat": lat2,
            "lng": lng2,
            "lokasi": nama2,
            "penjelasan": "",
            "sensor": {
                "curah hujan": round(float(precipitation2)),
                "getaran": round(float(vibration2)),
                "kelembapan": round(float(humidity2)),
                "kemiringan": round(float(inclination2))
            },
            "status": status2
        },
        "titik3": {
            "aktifkan": True,
            "tikum": tikum3,
            "lat": lat3,
            "lng": lng3,
            "lokasi": nama3,
            "penjelasan": penjelasan3,
            "sensor": {
                "curah hujan": round(float(precipitation3)),
                "getaran": round(float(vibration3)),
                "kelembapan": round(float(humidity3)),
                "kemiringan": round(float(inclination3))
            },
            "status": status3
        }
    }

    response = requests.put(
        f"https://sidasibelo-default-rtdb.firebaseio.com/Data.json", json=data)

    if response.status_code == 200:
        print("Firebase berhasil update..")
    else:
        print("Gagal mengirim data:", response.text)


try:
    while True:
        if ser.in_waiting > 0:
            dataSer = ser.readline().decode('utf-8').rstrip()
            print(f"\nInput Serial : {dataSer}")
            dataSers = dataSer.split(';')
            dataSer1 = dataSers[0]
            dataSer1 = dataSer1.split(',')
            dataSer2 = dataSers[1]
            dataSer2 = dataSer2.split(',')
            dataSer3 = dataSers[2]
            dataSer3 = dataSer3.split(',')
            id1 = dataSer1[0]
            vibration1 = dataSer1[1]
            inclination1 = dataSer1[2]
            humidity1 = dataSer1[3]
            precipitation1 = dataSer1[4]
            write_csv(vibration1, inclination1, humidity1, precipitation1, id1)
            id2 = dataSer2[0]
            vibration2 = dataSer2[1]
            inclination2 = dataSer2[2]
            humidity2 = dataSer2[3]
            precipitation2 = dataSer2[4]
            write_csv(vibration2, inclination2, humidity2, precipitation2, id2)
            id3 = dataSer3[0]
            vibration3 = dataSer3[1]
            inclination3 = dataSer3[2]
            humidity3 = dataSer3[3]
            precipitation3 = dataSer3[4]
            write_csv(vibration3, inclination3, humidity3, precipitation3, id3)
            predict()

except KeyboardInterrupt:
    print("Dihentikan")
finally:
    ser.close()
