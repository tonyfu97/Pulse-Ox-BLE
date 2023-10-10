from wellue_pulse_ox import WelluePulseOx
from time import sleep
from pylsl import StreamInfo, StreamOutlet

CHUNK_SIZE = 5
DEVICE_NAME = 'OxySmart 7956'  # Replace with your device name

info = StreamInfo(name=DEVICE_NAME,
                  type='EEG',  # It's not EEG, but there is no type for pulse ox
                  channel_count=1,
                  channel_format='float32',
                  source_id=DEVICE_NAME)

info.desc().append_child_value("manufacturer", "Wellue")

outlet = StreamOutlet(info=info, chunk_size=CHUNK_SIZE, max_buffered=360)

def process(data):
    for ii in range(CHUNK_SIZE):
        outlet.push_sample(data[:, ii])

pulseOx = WelluePulseOx(name=DEVICE_NAME, callback=process)
pulseOx.connect()
pulseOx.start()

while 1:
    try:
        sleep(1)
    except:
        break

pulseOx.stop()
pulseOx.disconnect()
