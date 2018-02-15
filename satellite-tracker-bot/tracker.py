import requests
import hashlib
import os
import time
import smtplib
import json

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

with open("./config.json", "r") as content_file:
    config = json.loads(content_file.read())

# Notify when imagery has changed
def send_alert(location, sha1hash):
    from_address = config["email"]
    to_address = config["email"]
    password = config["password"]

    msg = MIMEMultipart()
    msg["Subject"] = "New Satellite Imagery Detected for %s" % location
    msg["From"] = from_address
    msg["To"] = to_address

    # read in the image
    fd = open("%s/%s.png" % (location, sha1hash), "rb")
    img = MIMEImage(fd.read())
    fd.close()

    msg.attach(img)

    # send email with attachment
    server = smtplib.SMTP("smtp.gmail.com", 25)
    server.ehlo()
    server.starttls()
    server.login(from_address, password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

    return True

def main():
    "[+] Starting Satellite Imagery Tracker"
    locations = config["locations"]
    while True:
        for location in locations:
            latitude = float(location["latitude"])
            longitude = float(location["longitude"])
            map_url = "http://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=18&scale=false&size=600x300&maptype=satellite&format=png&visual_refresh=true" % (latitude, longitude)
            print "[*] Checking %s" % map_url

            # grab url image
            response = requests.get(map_url)

            if response.status_code == 200:

                # create dir for this location
                if not os.path.exists(location["Name"]):
                    os.mkdir(location["Name"])

                # hash the file
                hasher = hashlib.sha1()
                hasher.update(response.content)
                sha1hash = hasher.hexdigest()

                # check image already exists
                if not os.path.exists("%s/%s.png" % (location["Name"], sha1hash)):
                    fd = open("%s/%s.png" % (location["Name"], sha1hash), "wb")
                    fd.write(response.content)
                    fd.close()

                    print "[*] Image update for %s (%s) => %s.png" % (location["Name"], map_url, sha1hash)
                    send_alert(location["Name"], sha1hash)
        time.sleep(1500)

if __name__ == "__main__":
    main()
