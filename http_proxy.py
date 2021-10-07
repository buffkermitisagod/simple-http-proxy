import socket
import requests
import os

'''
remove the # for verbrose
this is a very simple script and can be improves
it also can't handle https request's or anything else than GET requests

TO DO:
add https and make it faster
'''


def get_data(url):
    url = "http://"+url
    data = requests.get(url)
    if data.status_code == 200:
        #print("[OK] client url code 200")
        return data.text
    else:
        #print("[ERROR] client url didn't respond code("+str(data.status_code)+")")
        raise "200 error"

def parse_req(data):
    try:
        req = data.split("Host: ")
        r = req[1]
        r = r.split("\n")

        url = r[0]
        url = url.replace("\n","")
        url = url.replace(" ","")
        url = url.replace("\r","")
        req_url = url

        #print("[OK] got client url")
        text = get_data(req_url)
        return text
    except Exception as e:
        #print("[ERROR] invalid request by client, sending error")
        er = """
        INTERNAL SERVER ERROR
        server error: """+str(e)+"""
        """
        return er




def proxy(port=int(), buff=int(4048)):
    r = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("",port))
        print("proxy server running on port "+str(port))

        while True:
            os.system("clear")

            #print("[+] waiting for connection")
            #print("[+] req num: "+str(r))
            s.listen()
            conn, addr = s.accept()

            #print("[OK] client connected ip: "+str(addr[0]))

            with conn:
                t = True
                while t:
                    data = conn.recv(buff)
                    req_url = parse_req(data.decode())
                    r += 1
                    try:
                        conn.send(req_url.encode())

                    # get rid of any common issue error preventing the program to run
                    except BrokenPipeError:
                        pass
                    except UnicodeDecodeError:
                        pass
                    except AttributeError:
                        pass

                    # un accounted for error
                    except Exception as e:
                        raise("ERROR: "+str(e))

                    t = False
