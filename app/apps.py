# Import python modules
import os, logging, time, sys

# Import django modules
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'app'

    def ready(self):
    	# Ensure startup code only runs once
        if os.environ.get('RUN_MAIN') != 'true':
        	return

        # Spawn device thread if enabled
        if os.environ.get('NO_DEVICE') == 'true':
        	print("\n~~~Running app without device~~~\n")
        else:
	        from device.device import Device
	        self.device = Device()
	        self.device.spawn(delay=1)