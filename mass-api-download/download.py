import urllib2
import json

def connection_loop():
    result = None
    url = "http://marsweather.ingenology.com/v1/archive/?terrestrial_date_start=2015-10-01"
    while True:
        connection = urllib2.urlopen(url)
        data = json.loads(connection.read())
        if data["next"] == None:
            break
        elif result == None:
            result = data["results"]
            url = data["next"];
        else:
            result = result + data["results"]
            url = data["next"];
    return result;

def main():
    print("[+] API Data Being Gathered...")
    result = connection_loop()
    if result == None:
        print("[-] Error, No Data Found.")
    else:
        with open('data.json', 'w') as outfile:
            json.dump(result, outfile)
        print("[+] Success, Data Found See JSON File.")

if __name__ == "__main__":
    print("[+] Download MAAS API Data.")
    raw_input("[*] Press Enter Key To Start: ")
    main()
