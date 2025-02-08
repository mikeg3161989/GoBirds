from operator import truediv

from phue import Bridge
import time
import random

DURATION = 10
BRIDGE_IP = '192.168.50.40'
ROOM_NAME = 'Living room'
GREEN_HUE = 25500
GREEN_SAT = 254
MAX_BRI = 254

bridge = Bridge(BRIDGE_IP)
bridge.connect()

light_objects = bridge.get_light_objects('id')
groups = bridge.get_group()


room_group_id = None
for group_id, group_info in groups.items():
    if group_info['name'] == ROOM_NAME:
        room_group_id = group_id
        print('ROOM GROUP ID:', room_group_id)
        break

if room_group_id is None:
    print('ROOM GROUP ID NOT FOUND')
    exit(1)

room_light_ids = groups[room_group_id]['lights']
room_lights = [light_objects[int(light_id)] for light_id in room_light_ids]

#save original states to set back
original_states = {}
for light in room_lights:
    original_states[light.name] = {
        'on': light.on,
        'bri': light.brightness,
        'hue': getattr(light, 'hue', None),
        'sat': getattr(light, 'saturation', None)
    }

end_time = time.time() + DURATION
min_flash_duration = 0.2
max_flash_duration = 0.8
min_pause_duration = 0.1
max_pause_duration = 0.5

flash_probability = 0.5
while time.time() < end_time:
    flashing_lights = [light  for light in room_lights if random.random() < flash_probability]

    if not flashing_lights:
        flashing_lights.append(random.choice(room_lights))

    for light in flashing_lights:
        light.on = True
        light.hue = GREEN_HUE
        light.saturation = GREEN_SAT
        light.brightness = MAX_BRI

    flash_duration = random.uniform(min_flash_duration, max_flash_duration)
    time.sleep(flash_duration)

    for light in flashing_lights:
        state = original_states[light.name]
        light.on = state['on']
        if state['on']:
            if state['hue'] is not None:
                light.hue = state['hue']
            if state['sat'] is not None:
                light.saturation = state['sat']
            light.brightness = state['bri']

    pause_duration = random.uniform(min_pause_duration, max_pause_duration)
    time.sleep(pause_duration)

for light in room_lights:
    state = original_states.get(light.name, {})

    light.on = state.get('on', True)

    if state.get('on', True):
        if state.get('hue') is not None:
            light.hue = state.get('hue')
        if state.get('sat') is not None:
            light.saturation = state.get('sat')
        light.brightness = state.get('bri', light.brightness)

print("GO BIRDS")