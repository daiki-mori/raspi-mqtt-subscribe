"""
MQTT Subscribe

Folder Structure
/
┗ mqtt_subscribe.py
┗ cert/
  ┗　AmazonRootCA1.Pem
  ┗ <id>-certificatie.pem.crt
  ┗ <id>-private.pem.key

Requeired Library
- paho-mqtt
"""

import ssl
import paho.mqtt.client as mqtt

#####変更が必要な値#####
# AWS IoT settings
ENDPOINT = ""
CERT_ID = ""
## AWS IoTで利用するトピック名
TOPIC = ""
#####変更が必要な値#####

## マネージメントコンソール→AWS IoT→設定→カスタムエンドポイント にあるエンドポイント名をコピー
HOST = ENDPOINT + ".iot.ap-northeast-1.amazonaws.com"
## ポート番号は以下、固定
PORT = 8883
## AWS IoTで作成した証明書
ROOT_CA = "./cert/AmazonRootCA1.pem"
CLIENT_CERT = "./cert/" + CERT_ID + "-certificate.pem.crt"
PRIVATE_KEY = "./cert/" + CERT_ID + "-private.pem.key"
## MQTTクライアント
CLIENT = None

def on_connect(client, userdata, flags, response_code):
    print("on_connect")
    print("response_code:" + str(response_code))
    print("TOPIC:" + TOPIC)
    CLIENT.subscribe(TOPIC,1)

def on_message(client, userdata, msg):
    print(msg.topic  + ":" + str(msg.payload))

if __name__ == "__main__":
    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_message = on_message
    CLIENT.tls_set(ROOT_CA, certfile=CLIENT_CERT, keyfile=PRIVATE_KEY,
                   cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    CLIENT.connect(HOST, port=PORT, keepalive=60)
    CLIENT.loop_forever()
