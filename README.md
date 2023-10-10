# Pulse-Ox-BLE

Stream and visualize plethysmogram (PPG) data from Wellue Bluetooth Pulse Oximeter using Pygatt and Lab Streaming Layer (LSL)

![pleth_live](./images/pleth_live.gif)


---


## Requirements

### Hardware

* [Wellue Bluetooth Pulse Oximeter](https://www.amazon.com/gp/product/B085ZFDMMX/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1): To collect pulse oximetry data.
* [BLED112 USB dongle](https://www.digikey.com/en/products/detail/silicon-labs/BLED112-V1/4245505): Because most computers do not have a built-in Bluetooth Low Energy (BLE) radio.

### Software

* The basics: python, numpy, matplotlib, scipy.
* `pygatt`: To connect to the BLE device.
* `pylsl`: the interface to the Lab Streaming Layer (LSL), a protocol for real-time streaming of biosignal over a network. Here is their [documentation](https://labstreaminglayer.readthedocs.io/). Here are some [example code](https://github.com/labstreaminglayer/pylsl/tree/master/pylsl/examples). Here is a [YouTube tutorial on LSL](https://youtu.be/Y1at7yrcFW0?si=V298gu2gYSO6tr3a).

---


## Tutorial







![pleth_live_screen](./images/pleth_live_screen.gif)