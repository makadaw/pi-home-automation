import appdaemon.plugins.hass.hassapi as hass
import datetime


class VacationMode(hass.Hass):
  """
  Vacation mode settings. Home Alone inspired.

  This app turn on lights and switchers if the system is in the vacation mode.
  This can be usefull if you want to mimic inside home activity while on vacation.

  App use the sunset to adopt for any time of the year.
  """

  def initialize(self):
    self.set_namespace("hass")
    self.vacation_switch = self.args["vacation_switch"]
    self.switch = self.args["switch"]
    self.lights = self.args["lights"]

    # Run every quarter
    self.run_hourly(self.time_callback, datetime.time(0, 0, 0))
    self.run_hourly(self.time_callback, datetime.time(0, 15, 0))
    self.run_hourly(self.time_callback, datetime.time(0, 30, 0))
    self.run_hourly(self.time_callback, datetime.time(0, 45, 0))

  def is_vacation(self):
    return self.get_state(self.vacation_switch) == "on"

  def time_callback(self, time):
    self.log(time)
    # Do anything only on vacation
    if self.is_vacation():
      # Turn on lights when is dark
      is_time = self.now_is_between("sunset - 01:00:00", "01:00:00")
      if is_time:
        self.turn_on_all()
      else:
        self.turn_off_all()

  def turn_on_all(self):
    if self.get_state(self.switch) == "off":
      self.turn_on(self.switch)
    for light in self.lights:
      if self.get_state(light) == "off":
        self.turn_on(light)

  def turn_off_all(self):
    if self.get_state(self.switch) == "on":
      self.turn_off(self.switch)
    for light in self.lights:
      if self.get_state(light) == "on":
        self.turn_off(light)
