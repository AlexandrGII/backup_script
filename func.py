import telnetlib, os, signal, time, difflib


def upload_to_tftp(ip, today_date, users):
    def bulk(self, cmd, opt):
        pass

    # Design for creating a timeout.
    def handler(signum, frame):
        raise Exception("end of time")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(90) 

    try:
        tn = telnetlib.Telnet(ip, 23, 5)
        tn.set_option_negotiation_callback(bulk)
        tn.read_until(':')
        
        # Search for the correct password.
        for user in users.items():
            tn.write(user[0] + "\n")
            time.sleep(1)
            tn.write(user[1] + "\n")
            time.sleep(1)

        # Save the config.
        tn.write("save\n")
        time.sleep(4)

        # Download the config, trying different versions, for different models.
        tn.write("upload cfg_toTFTP 10.0.8.40 folder_{0}/{1}.cfg\n".format(ip,today_date))
        time.sleep(1)

        tn.write("upload cfg_toTFTP tftp://10.0.8.40/folder_{0}/{1}.cfg\n".format(ip,today_date))
        time.sleep(1)

        tn.write("upload cfg_toTFTP 10.0.8.40 dest_file folder_{0}/{1}.cfg\n".format(ip,today_date))
        time.sleep(1)

        tn.write("upload configuration 10.0.8.40 folder_{0}/{1}.cfg\n".format(ip,today_date))
        time.sleep(1)

        tn.read_until('#')
        tn.write("logout\n")
        
        print("Telnet Ok")
        return True

    except:
        print("Telnet Error \n ------------------------ \n")
        return False
    
    # If the previous block isn't executed within 90 seconds, the "Alarm" signal is sent.    
    signal.alarm(0)


def ping(ip):
    response = os.system("ping -c 3 {0} > /dev/null 2>&1".format(ip))
    if response == 0:
        return True
    else:
        return False


def diff(path, f1, f2):
    f1 = path + '/' + f1
    f2 = path + '/' + f2

    # Open configs line by line, and write to the list.
    f1 = open(f1)
    sf1 = []
    for line in f1.readlines():
        sf1.append(line)
    
    f2 = open(f2)
    sf2 = []
    for line in f2.readlines():
        sf2.append(line)     

    # We are looking for a common intersection, and calculate the added and deleted rows. 
    set_text_one = set(sf1)
    set_text_two = set(sf2)
    common = set_text_one & set_text_two
    deleted = set_text_two - common
    added = set_text_one - common 

    changes = str()

    # Set is an unordered sequence, so we compare the rows from the ordered list
    # to order the output.
    if deleted:
        changes += '!!Deleted rows: \n'
        for i in sf2:
            if i in deleted:
                changes += '---- ' + str(i)
    
    if added:
        changes += '!!Added rows: \n'
        for i in sf1:
            if i in added:
                changes += '++++ ' + str(i)

    return changes


def files_in_dir(path):
    dict_time = {}
    files = os.listdir(path) # Look at the files in the folder.

    # We establish the correspondence between the file and the time.
    for file in files:
        time = os.stat(path + '/' + file).st_ctime
        dict_time[time] = file
    
    
    # We find the two max times and return the files corresponding to them.
    list_time = dict_time.keys()
    max_1 = max(list_time)
    list_time.remove(max_1)
    max_2 = max(list_time)
    
    return (dict_time[max_1], dict_time[max_2])
