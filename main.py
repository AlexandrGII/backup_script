import os, pwd, grp
from datetime import datetime
from func import upload_to_tftp, ping, diff, files_in_dir
from config import ips, def_path, users, mail
from sendMail import send

#ips = ['10.0.8.126', ]
uid, gid = (99, 99)
today_date = datetime.strftime(datetime.now(), '%d-%m-%Y')
report = str()


for ip in ips:
    print('Start {0}'.format(ip))
    full_path = def_path + u'folder_{0}'.format(ip)
    

    if not ping(ip):
        print('Host {0} unreachable \n ------------------------ \n'.format(ip))
        report += 'Host {0} unreachable \n ------------------------ \n'.format(ip)
        continue


    if not os.path.exists(full_path):
        os.mkdir(full_path)
        os.chown(full_path, uid, gid)

    
    # Add the ending "new" if the file already exists.
    if os.path.exists(def_path + u'folder_{0}/{1}.cfg'.format(ip, today_date)):
        today_date = today_date + '_new' 
        
    # Download config. Or not.
    if not upload_to_tftp(ip, today_date, users):
        report += 'Unknow error with backup on {0}\n ------------------------ \n'.format(ip)
        continue

    # Check if the files are different, and if not, delete the downloaded file.
    if len(os.listdir(full_path)) > 1:
        f = files_in_dir(full_path)
        difference = diff(full_path, f[0], f[1])
        if difference:
            report += '!!Config has been changed on switch {0} \n'.format(ip)
            report += difference
        else:
            if len(f) == 2:
                print('Duplicate deleted from folder {0}'.format(full_path))
                os.remove(full_path + '/' + f[0])

    print 'Backup on {0}  completed \n'.format(ip), '-' * 35
    report += 'Backup on {0}  completed \n  ------------------------ \n'.format(ip)

# Send the report by email.
report += 'End of report\n'.format(ip)
send(report, mail)
