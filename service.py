#!/usr/bin/env python3
from cmath import pi
import math
import threading
import time
import sched
from pathlib import Path
from threading import Lock
from time import sleep
from tokenize import Double
from typing import Dict, Any, List
from datetime import datetime

import paho.mqtt.client as mqtt
import yaml

class InverterSimulator:
    def __init__(self, num_cells, num_modules):
        config = self.get_config('config.yaml')
        credentials = self.get_config('credentials.yaml')
        prefix = 'modbus4mqtt'
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_message = self.mqtt_on_message
        self.mqtt_client.username_pw_set(credentials['username'], credentials['password'])
        self.mqtt_client.connect(host=config['mqtt_server'], port=config['mqtt_port'], keepalive=60)
        self.mqtt_client.loop_start()


    def publish_inverter_state(self):
        self.mqtt_client.publish(self.prefix + 'available', 'online', retain=True)
        self.mqtt_client.publish(self.prefix + 'start_stop', 'start', retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_maintenance', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'export_power_limitation', 'enable', retain=True)
        self.mqtt_client.publish(self.prefix + 'reserved_soc_for_backup', 30, retain=True)
        self.mqtt_client.publish(self.prefix + 'device_type_code', 'sh10rt', retain=True)
        self.mqtt_client.publish(self.prefix + 'nominal_output_power', 10.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'output_type', 1, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_output_energy', 2.5, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_output_energy', 4628.2, retain=True)
        self.mqtt_client.publish(self.prefix + 'inside_temperature', 12.3, retain=True)
        self.mqtt_client.publish(self.prefix + 'mppt1_voltage', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'mppt1_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'mppt2_voltage', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'mppt2_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_dc_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_a_voltage', 227.2, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_b_voltage', 226.5, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_c_voltage', 228.1, retain=True)
        self.mqtt_client.publish(self.prefix + 'reactive_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'power_factor', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'grid_frequency', 49.9, retain=True)
        self.mqtt_client.publish(self.prefix + 'system_state', 'standby', retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state', 40, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_pv_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_battery_charging', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_battery_discharging', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_positive_load_power', 1, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_feed_in_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_import_power_from_grid', 1, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_reserved', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'running_state_negative_load_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_pv_generation', 2.4, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_pv_generation', 4628.5, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_export_power_from_pv', 0.7, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_export_energy_from_pv', 3453.8, retain=True)
        self.mqtt_client.publish(self.prefix + 'load_power', 250, retain=True)
        self.mqtt_client.publish(self.prefix + 'export_power', -250, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_battery_charge_energy_from_pv', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_battery_charge_energy_from_pv', 47.6, retain=True)
        self.mqtt_client.publish(self.prefix + 'co2_reduction', 3239.9, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_direct_energy_consumption', 1.7, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_direct_energy_consumption', 1127.1, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_voltage', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_level', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_state_of_health', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_temperature', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_battery_discharge_energy', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_battery_discharge_energy', 33.4, retain=True)
        self.mqtt_client.publish(self.prefix + 'self_consumption_of_today', 70.8, retain=True)
        self.mqtt_client.publish(self.prefix + 'grid_state', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_a_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_b_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'phase_c_current', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_active_power', 0, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_import_energy', 6.9, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_import_energy', 5192.6, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_capacity', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_charge_energy', 0.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_charge_energy', 47.1, retain=True)
        self.mqtt_client.publish(self.prefix + 'daily_export_energy', 0.7, retain=True)
        self.mqtt_client.publish(self.prefix + 'total_export_energy', 3463.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'bms_status', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'max_charging_current', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'max_discharging_current', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'warning', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'protection', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'fault_1', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'fault_2', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'soc', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'soh', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_current_2', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_voltage_2', 655.35, retain=True)
        self.mqtt_client.publish(self.prefix + 'cycle_count', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'average_cell_voltage', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'max_cell_voltage', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'min_cell_voltage', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_pack_voltage', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'average_cell_temp', -1, retain=True)
        self.mqtt_client.publish(self.prefix + 'max_cell_temp', -1, retain=True)
        self.mqtt_client.publish(self.prefix + 'min_cell_temp', -1, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_type', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'export_power_limitation_value', 7000, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_nominal_voltage', 6553.5, retain=True)
        self.mqtt_client.publish(self.prefix + 'battery_capacity_specified', 65535, retain=True)
        self.mqtt_client.publish(self.prefix + 'max_soc', 100.0, retain=True)
        self.mqtt_client.publish(self.prefix + 'min_soc', 5.0, retain=True)

scheduler = sched.scheduler = sched.scheduler(time.time, time.sleep)
inverter_simulator = InverterSimulator()

def mqtt_job(sc):
    inverter_simulator.mqtt_publish()
    scheduler.enter(3, 10, mqtt_job, (sc,))

if __name__ == '__main__':
    scheduler.enter(3, 10, mqtt_job, (scheduler,))
    scheduler.run()