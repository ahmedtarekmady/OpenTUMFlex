
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import ems and devices modules
from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.ems_mod import update_time_data
from ems.devices.devices import devices
from ems.devices.devices import device_write

# import forecast model for weather and price data
from forecast.fcst import load_data

# import optimization module
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.Bat import Batflex
from ems.flex.PV import PVflex

# import plot module
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results

# load the predefined ems data, initialization by user input is also possible:
my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

# change the time interval
my_ems['time_data']['t_inval'] = 15
my_ems['time_data']['d_inval'] = 15
my_ems['time_data']['start_time'] = '2019-12-18 02:00'
my_ems['time_data']['end_time'] = '2019-12-19 12:59'
my_ems['time_data']['days'] = 1
my_ems.update(update_time_data(my_ems))

# load the weather and price data
my_ems['fcst'] = load_data(my_ems)

# add or change the utility/devices
# if deleting one specific device please use del my_ems['devices']['hp']
# my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=2))
my_ems['devices']['sto']['stocap'] = 15
my_ems['devices']['boiler']['maxpow'] = 2
my_ems['devices']['chp']['maxpow'] = 0
my_ems['devices']['pv']['maxpow'] = 5
my_ems['devices']['bat']['stocap'] = 5
my_ems['devices']['bat']['maxpow'] = 3
my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, init_soc=[20, 35, 30],
                                 end_soc=[50, 50, 40], eta=0.98,
                                 ev_aval=["2019-12-18 4:00", "2019-12-18 9:00",
                                          "2019-12-18 13:45", "2019-12-18 18:15",
                                          "2019-12-19 9:30", "2019-12-19 11:15"],
                                 # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                 timesetting=my_ems['time_data']))


# plt.plot(my_ems['devices']['ev']['consm'])
# my_ems['devices']['ev']['maxpow'] = 5

# write the device parameter data in JSON file for reuse,
# device_write(my_ems, 'pv', '../ems/devices/pv_test.txt')
# device_write(my_ems, 'ev', '../ems/devices/ev_test.txt')

# calculate the timetable for all the devices
my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

# calculate the flexibility of one device
my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)
# my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)
my_ems['flexopts']['bat'] = Batflex(my_ems)
# my_ems['flexopts']['pv'] = PVflex(my_ems)

# plot the results#
plot(my_ems, "hp")
# plot(my_ems, "pv")
plot(my_ems, "bat")

# store the data of the whole ems for reuse
# ems_write(my_ems, path='data/test_Nr_02.txt')
