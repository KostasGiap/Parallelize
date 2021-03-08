import requests
import sys
import random
import datetime

def main(client_id):
	while True:
		time = datetime.datetime.now()
		show(seconds=str(time.second))
		if time.second == 0:
			electicity_counter = str(random.randint(1, 1000))
			payload = {'ip': client_id, 'data': electicity_counter}
			r = requests.post("http://127.0.0.1:8080", data=payload)
			while time.second == 0:
				time = datetime.datetime.now()

# Shows current seconds
def show(seconds):
    if len(seconds) < 2:
        seconds = "0"+seconds
    sys.stdout.write('\r')
    sys.stdout.write("seconds: "+seconds)
    sys.stdout.flush()

if __name__ == '__main__':
	client_id=random.randint(1, 10000)
	main(client_id)