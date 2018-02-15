import json
import getpass

def load_file_object():
    open("./config.json", "w").close()
    return open("./config.json", "w")

def load_file_content():
    f = open("./config.json", "r")
    data = json.loads(f.read())
    return data

def close_file(file):
    file.close()

def update_account(file, data, email, password):
    data["email"] = email
    data["password"] = password
    file.write(json.dumps(data))

def add_local(file, data, name, lat, lon):
    data["locations"].append({"name": name, "latitude": lat, "longitude": lon})
    file.write(json.dumps(data))

def remove_local(file, data, name):
    index = -1
    for i in range(0, len(data["locations"])):
        if (data["locations"][i]["name"] == name):
            index = i
            break
    if index != -1:
        del data["locations"][index]
    file.write(json.dumps(data))

def main():
    print "[+] Staring Config Editor"
    while True:
        print "[*] Please Input Option Or h For Options"
        user_input = raw_input(">> ")

        if user_input == "h":
            print "[**] Options: u <update email>, a <add location>, r <remove location>, q <quit>"

        elif user_input == "u":
            email = ""
            while email == "":
                print "[*] Input Email"
                email = raw_input(">> ")

            password = ""
            while password == "":
                print "[*] Input Password"
                password = getpass.getpass(">> ")

            data = load_file_content()
            f = load_file_object()
            update_account(f, data, email, password)
            close_file(f)
            print "[+] Success Email Update"

        elif user_input == "a":
            name = ""
            while name == "":
                print "[*] Input Location Name"
                name = raw_input(">> ")

            lat = ""
            while lat == "":
                print "[*] Input Latitude"
                lat = raw_input(">> ")

            lon = ""
            while lon == "":
                print "[*] Input Longitude"
                lon = raw_input(">> ")

            data = load_file_content()
            f = load_file_object()
            add_local(f, data, name, lat, lon)
            close_file(f)
            print "[+] Success Location: %s Added" % name

        elif user_input == "r":
            name = ""
            while name == "":
                print "[*] Input Name Of Location"
                name = raw_input(">> ")
            data = load_file_content()
            f = load_file_object()
            remove_local(f, data, name)
            close_file(f)
            print "[+] Success Location: %s Removed" % name

        elif user_input == "q":
            print "[+] Goodbye"
            break





if __name__ == "__main__":
    main()
