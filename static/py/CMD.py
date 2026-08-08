import subprocess
from static.py.Input import Input_validator
import math

class Cli(Input_validator):
  def __init__(self, brightness_level):
    super().__init__(brightness_level=brightness_level)

  def __bool__(self):
    return super().__bool__()

  def device_name(self):
    return subprocess.run(
      ['ls', '/sys/class/backlight/'],
      capture_output=True,
      text=True
    ).stdout.removesuffix('\n')

  def max_brightness(self):
    return subprocess.run(
      ['cat', f'/sys/class/backlight/{self.device_name().removesuffix("\n")}/max_brightness'],
      capture_output=True,
      text=True
    ).stdout.removesuffix('\n')

  def change_the_brightness(self, password):
    actual_level = int((int(self.brightness_level) / 100) * int(self.max_brightness()))
    root_password = str(password)
    subprocess.run(['sudo', '-k'])
    subprocess.run(
      ['sudo', '-S', 'tee', f'/sys/class/backlight/{self.device_name()}/brightness'],
      input=f'{root_password}\n{actual_level}\n',
      text=True
    )