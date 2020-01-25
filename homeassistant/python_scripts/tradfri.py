""" Lights controll script """

ARG_ENTITY_ID = "entity_id"
ARG_OPERATION = "operation"
ARG_LEVEL = "level"
ARG_TRANSITION = "transition"
ARG_RGB_COLOR = "rgb_color"

OP_TOGGLE = "toggle" # Default operation
OP_TURN_ON = "turn_on"
OP_TURN_OFF = "turn_off"
OP_DIM_UP = "dim_up"
OP_DIM_DOWN = "dim_down"
OP_DIM_BUTTON_HOLD = "dim_button_hold"

# Get params
entity_id = data.get(ARG_ENTITY_ID)
op = data.get(ARG_OPERATION, OP_TOGGLE)
level = data.get(ARG_LEVEL, 10)
transition = data.get(ARG_TRANSITION, 1)

def min(a,b):
  return a if a < b else b

def max(a,b):
  return a if a > b else b

if entity_id is not None:
  # Turn on ligts
  if op == OP_TURN_ON:
    rgb = data.get(ARG_RGB_COLOR)
    data = {"entity_id": entity_id, "brightness": 255, "transition": transition}
    if rgb is not None: # Set RGB only if provided
      data["rgb_color"] = rgb
    hass.services.call("light", "turn_on", data)
  # Turn off lights
  elif op == OP_TURN_OFF:
    data = {"entity_id": entity_id, "transition": transition}
    hass.services.call("light", "turn_off", data)
  # On or off depend on the cirrent state
  elif op == OP_TOGGLE:
    data = {"entity_id": entity_id, "brightness": 255, "transition": transition}
    hass.services.call("light", "toggle", data, False)
  # Change brightness level
  elif op == OP_DIM_UP or op == OP_DIM_DOWN:
    # Get current brightness value
    states = hass.states.get(entity_id)
    current = (states.attributes.get('brightness') or 0)
    brightness = min(current+level, 255) if op == OP_DIM_UP else max(current-level, 0)
  
    logger.info("Set light brightness level to {}".format(brightness))
    data = {"entity_id": entity_id, "brightness": brightness, "transition": transition}
    hass.services.call("light", "turn_on", data, False)
  # Brightnes hold
  elif op == OP_DIM_BUTTON_HOLD:
    # Long press actions
    exit_service = False
    attribute_id = data.get("light_attribute", "brightness")
    input_boolean = data.get("input_boolean")
    delay = data.get("delay", 350)

    attribute_mapping = {
      "brightness": {"min": 1, "max": 255},
      "color_temp": {"min": 153, "max": 500},
    }
    
    # Start dim loop
    while True:
      switch_input = hass.states.get(input_boolean).state
      if switch_input == "off":
        break
      light = hass.states.get(entity_id)
      
      attr_value = light.attributes[attribute_id]
      attr_value = attr_value + level
      if attr_value < attribute_mapping[attribute_id]["min"]:
        attr_value = attribute_mapping[attribute_id]["min"]
        exit_service = True
      elif attr_value > attribute_mapping[attribute_id]["max"]:
        attr_value = attribute_mapping[attribute_id]["max"]
        exit_service = True

      service_data = {"entity_id": entity_id, attribute_id: attr_value}
      logger.info("Dim hold set level {}".format(service_data))
      hass.services.call("light", "turn_on", service_data)
      if exit_service:
        break
      time.sleep(delay / 1000)

else:
  logger.warning("No entity_id provided")

