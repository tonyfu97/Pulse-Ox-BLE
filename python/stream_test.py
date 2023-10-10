import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_byprop


if __name__ == "__main__":

    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL stream
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    if len(streams) == 0:
        raise RuntimeError('Can\'t find Pulse Ox stream.')

    # Set active stream to inlet
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=10)

    """ 2. PLOT PULSE OXIMETRY DATA """

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    y = np.array([])  # Initialize an empty array for y-data (pulse_ox_data)

    line, = ax.plot([], [])
    ax.set_ylim([0, 128])  # Set y-axis limits; adjust as needed
    ax.set_xlim([0, 200])  # Set x-axis limits; adjust as needed

    buffer_size = 200  # Size of the buffer to keep the most recent samples

    print('Press Ctrl-C in the console to break the while loop.')

    try:
        i = 0  # Counter for current data point within buffer
        while True:
            pulse_ox_data, _ = inlet.pull_chunk(timeout=1, max_samples=10)

            for j, data_point in enumerate(pulse_ox_data):
                ch_data = data_point[0]  # Assuming data_point is an array and the required data is the first element
                # print(ch_data)

                # Update y data
                if i < buffer_size:
                    y = np.append(y, ch_data)
                else:
                    y[i % buffer_size] = ch_data

                # Generate x data based on y data length
                x = np.linspace(0, len(y) - 1, len(y))

                # Update the plot
                line.set_xdata(x)
                line.set_ydata(y)
                ax.relim()
                ax.autoscale_view(True, True, True)
                
                if j % 1 == 0:
                    plt.draw()
                    plt.pause(0.005)

                # Update counter and possibly reset
                i += 1
                if i >= buffer_size:
                    i = 0  # Reset counter
                    y = np.array([])  # Reset data array to restart from the left

    except KeyboardInterrupt:
        print('Closing!')
