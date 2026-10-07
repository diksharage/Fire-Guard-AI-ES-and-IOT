import urllib.request
import re
import os

def download_image(wiki_url, filename):
    try:
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'"(https://upload\.wikimedia\.org/wikipedia/commons/thumb/[^"]+)"', html)
        if match:
            img_url = match.group(1)
            # Fix URL if it's too large, get the 500px version or original
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(img_req).read()
            os.makedirs('public/images', exist_ok=True)
            with open(f'public/images/{filename}', 'wb') as f:
                f.write(img_data)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to find image in {wiki_url}")
    except Exception as e:
        print(f"Error for {wiki_url}: {e}")

download_image('https://commons.wikimedia.org/wiki/File:NodeMCU_ESP8266.jpg', 'esp8266.jpg')
download_image('https://commons.wikimedia.org/wiki/File:Solderless_breadboard.jpg', 'breadboard.jpg')
download_image('https://commons.wikimedia.org/wiki/File:MQ-2_Gas_Sensor.jpg', 'mq2.jpg')
download_image('https://commons.wikimedia.org/wiki/File:DHT11_sensor.jpg', 'dht11.jpg')
download_image('https://commons.wikimedia.org/wiki/File:5mm_Green_LED.jpg', 'led_g.jpg')
download_image('https://commons.wikimedia.org/wiki/File:5mm_Yellow_LED.jpg', 'led_y.jpg')
download_image('https://commons.wikimedia.org/wiki/File:5mm_Red_LED.jpg', 'led_r.jpg')
download_image('https://commons.wikimedia.org/wiki/File:Resistor_220_ohm.jpg', 'resistor.jpg')
download_image('https://commons.wikimedia.org/wiki/File:Piezoelectric_buzzer.jpg', 'buzzer.jpg')
