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

    buffer_size = 200  # Size of the buffer to keep the most recent samples

    print('Press Ctrl-C in the console to break the while loop.')

    try:
        while True:
            pulse_ox_data, _ = inlet.pull_chunk(timeout=1, max_samples=10)
            
            try:
                ch_data = np.array(pulse_ox_data)[:, 0]
            except:
                continue

            # Update y data
            y = np.concatenate((y, ch_data))

            # Keep only the most recent 'buffer_size' samples
            y = y[-buffer_size:]

            # Generate x data based on y data length
            x = np.linspace(0, len(y) - 1, len(y))

            # Update the plot
            line.set_xdata(x)
            line.set_ydata(y)
            ax.relim()
            ax.autoscale_view(True, True, True)
            plt.draw()
            plt.pause(0.1)

    except KeyboardInterrupt:
        print('Closing!')
