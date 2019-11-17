""" Lights controll script """

ARG_ENTITY_ID = "entity_id"
ARG_OPERATION = "operation"
ARG_LEVEL = "level"

OP_TOGGLE = "toggle" # Default operation
OP_TURN_ON = "turn_on"
OP_TURN_OFF = "turn_off"
OP_DIM_UP = "dim_up"
OP_DIM_DOWN = "dim_down"

# Get params
entity_id = data.get("entity_id")
op = data.get(ARG_OPERATION, OP_TOGGLE)
level = data.get(ARG_LEVEL, 5)

def min(a,b):
  return a if a < b else b

def max(a,b):
  return a if a > b else b

if entity_id is not None:
  if op == OP_TURN_ON:
    data = {"entity_id": entity_id, "brightness": 255, "transition": 1}
    hass.services.call("light", "turn_on", data)
  elif op == OP_TURN_OFF:
    data = {"entity_id": entity_id, "transition": 1}
    hass.services.call("light", "turn_off", data)
  elif op == OP_TOGGLE:
    data = {"entity_id": entity_id, "brightness": 255, "transition": 1}
    hass.services.call("light", "toggle", data, False)
  elif op == OP_DIM_UP or op == OP_DIM_DOWN:
    # Get current brightness value
    states = hass.states.get(entity_id)
    current = round((states.attributes.get('brightness') or 0) / 2.55)
    brightness = min(current+level, 100) if op == OP_DIM_UP else max(current-level, 0)
  
    logger.info("Set light brightness level to {}".format(brightness))
    data = {"entity_id": entity_id, "brightness": round(brightness * 2.55), "transition": 1}
    hass.services.call("light", "turn_on", data, False)
else:
  logger.warning("No entity_id provided")

