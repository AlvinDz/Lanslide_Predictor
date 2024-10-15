import requests # type: ignore
import json
import joblib
import numpy as np
import pandas as pd

model = joblib.load("Land_Slide_Model_Predictor.pkl")

app_id = "a26baac9-bd90-4613-ad40-d3ea16e844de"
rest_api_key = "YzMzODY2MjUtZTNjYS00YzdhLTkwYmItZjY4NjY5MjdjMTll"

id = "t1"
vibration = 234.5
inclination = 34
humidity = 0.38
precipitation = 2.55

if id == "t1":
  path="titik1"
  tikum = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
  lat = -6.842157109211024
  lng = 107.56864072401038
  nama = "Lokasi 1"
  penjelasan = "Titik 1 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."
elif id =="t2":
  path="titik2"
  nama = "Lokasi 2"
  tikum = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
  lat = -6.832474922745673
  lng = 107.58112551641517
  penjelasan = "Titik 2 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."
elif id == "t3":
  path="titik3"
  nama = "Lokasi 3"
  tikum = "https://www.google.com/maps/place/Faculty+of+Technology+And+Vocational+Education/@-6.8630224,107.5934674,18z/data=!4m6!3m5!1s0x2e68e6bef5a6548d:0xa4d65b8ffd0bbc48!8m2!3d-6.8641594!4d107.5938877!16s%2Fg%2F1hm21mlwh?entry=ttu"
  lat = -6.811430435230934
  lng = 107.53326722506678
  penjelasan = "Titik 3 ini terletak tepatnya di RT/RW **, Desa **, Kelurahan **, dengan titik latitude -6.842157109211024 dan longitude 107.56864072401038. Titik 1 ini memiliki karakteristik jenis tanah merah dengan sedikit campuran pasir. ...."
  
data_input = np.array([[vibration, inclination, humidity, precipitation]])
probability = model.predict_proba(data_input)
value = probability[0,1]
print(f"Probabilitas : {value}")

buttons = [
    {"id": path, "text": "Detail"},
    {"id": path + "_maps", "text": "Titik kumpul"}
    ]
   
def sendNotif() :
   header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {rest_api_key}"
    }
   
   payload = {
        "app_id": app_id,
        "included_segments": ["Total Subscriptions"],
        "contents": {"en": f"{nama} Terdeteksi Status {status}, Segera evakuasi ke titik kumpul apabila berada di sekitar area"},
        "headings": {"en": f"{nama} Rawan Longsor !"},
        "big_picture" : url_gambar,
        "buttons" : buttons,
        "data" : {"titik": f"{path}"}
    }
   
   req = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=header,
        data=json.dumps(payload)
    )
   
   return req.status_code, req.text

if   value > 0.75 or value >= 1 :
    url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
    status = "AWAS"
    status_code, response = sendNotif()
    print(f"Response: {response}")
elif value > 0.5  or value >= 0.75 :
    url_gambar = "https://firebasestorage.googleapis.com/v0/b/mitigasi-longsor-d25c1.appspot.com/o/alert_banner.png?alt=media&token=fcbb4ac9-ee1e-45eb-8fc5-27f115f22313"
    status = "SIAGA"
    status_code, response = sendNotif()
    print(f"Response: {response}")
elif value > 0.25 or value >= 0.5 :
    status = "WASPADA"
else :
    status = "NORMAL"

data = {
          "aktifkan": True,
          "tikum": tikum,
          "lat": lat,
          "lng": lng,
          "lokasi": nama,
          "penjelasan": penjelasan,
          "sensor": {
            "curah hujan": precipitation,
            "getaran": vibration,
            "kelembapan": humidity*100,
            "kemiringan": inclination
          },
          "status": status
        }

response = requests.put(f"https://sidasibelo-default-rtdb.firebaseio.com/Data/{path}.json", json=data)

if response.status_code == 200:
  print("Data berhasil dikirim")
else:
  print("Gagal mengirim data:", response.text)
