from speedtest import Speedtest

from pythonping import ping

from gpiozero import Servo

import schedule
import time

import logging as logger
logger.basicConfig(level=logger.INFO)

dial_1_pin = 17
dial_2_pin = 19
amp_meter = 21

max_dl_bw = 42
max_up_bw = 14
max_ping = 120



def speedtest():
	servers = []
	threads = None
	s = Speedtest()
	s.get_servers(servers)
	s.get_best_server()
	s.download(threads=threads)
	s.upload(threads=threads)
	s.results.share()
	results_dict = s.results.dict()
	return results_dict

def pingtest():
	server = "192.168.0.1"
	response_list = ping(server, count=10)
	return response_list.rtt_avg_ms


def set_servo(pin, reading):
	logger.debug("Setting Servo")
	servo = Servo(pin)
	servo.value = reading
	servo.detach()


def set_amp_meter(ping, reading):
	logger.debug("Setting AMP Meter")
	servo = Servo(pin)
	servo.value = reading
	servo.detach()

def main():
	avg_ping = pingtest()
	info_dict = speedtest()
	upload_bw = info_dict['upload'] / 1000000
	download_bw = info_dict['download'] / 1000000
	upload_reading = upload_bw/max_up_bw
	download_reading = download_bw/max_dl_bw
	ping_reading = avg_ping/max_ping
	logger.info(f'Average ping {avg_ping} ({ping_reading}), Upload {upload_bw} ({upload_reading}), Download {download_bw} ({download_reading})')

	# Set download dial
	#set_servo(dial_1_pin, download_reading)

	# Set upload dial
	#set_servo(dial_2_pin, upload_reading)

	# Set ping meter
	#set_amp_meter(amp_meter, ping_reading)

schedule.every(1).minutes.do(main)

while 1:
    schedule.run_pending()
    time.sleep(1)