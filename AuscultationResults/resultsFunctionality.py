import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal
import scipy.fftpack as fftpk
from scipy.signal import butter, filtfilt
import audiofile
from matplotlib import animation


class AuscultationResults(object):
    audio, Fs = None, None
    duration, channels = None, None
    time_axis = None
    maxs_df, section_idxs = None, None
    lub_idxs, dub_idxs = None, None
    lub_amp, dub_amp = None, None
    lub_length, dub_length = None, None
    systolic_times, diastolic_times = None, None
    systolic_length, diastolic_length = None, None
    bpm = None
    lpf_b, lpf_a = None, None
    hpf_b, hpf_a = None, None
    lp_filtered_audio, hp_filtered_audio = None, None
    beg_sys_times, beg_dias_times = [], []


    def __init__(self, file_path):
        self.audio, self.Fs = audiofile.read(file_path)
        self.duration = audiofile.duration(file_path)
        self.channels = audiofile.channels(file_path)
        self.time_axis = np.arange(0.0, self.duration, 1 / self.Fs)

    def downsample_to_16kHz(self):
        # Idk ab this one chief
        num_samples = 16000 * self.duration
        num_samples = int(num_samples)
        self.audio = scipy.signal.resample(self.audio, num_samples)
        self.time_axis = scipy.signal.resample(self.time_axis, num_samples)
        return

    def display_audio_time(self):
        """
        Plot audio vs time
        :return: nothing
        """

        # Make 1 channel if 2 channels
        if self.channels == 2:
            self.make_audio_one_channel()

        # Plot amplitude vs time
        fig, ax = plt.subplots()
        ax.plot(self.time_axis, self.audio, 'k-')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude (?)')
        ax.set_title('Audio vs Time', loc='left', variant='small-caps')
        ax.grid(True, 'both')
        fig.tight_layout()
        return

    def display_audio_frequency(self):
        """
        Plot audio vs frequency
        :return: nothing
        """
        audio_frequency = abs(scipy.fft.fft(self.audio))
        audio_freq_data = audio_frequency[range(len(audio_frequency) // 2)]

        # Convert to freqeuncy
        freq = fftpk.fftfreq(len(audio_frequency), (1.0 / self.Fs))
        freq_axis = freq[range(len(audio_freq_data))]
        freq_axis = freq_axis[(freq_axis < 600)]  # the 300 is hardcoded and kinda random, should probs

        # Plot amplitude vs time
        fig, ax = plt.subplots()
        ax.plot(freq_axis, audio_freq_data[range(len(freq_axis))], 'k-')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('')
        ax.set_title('Audio vs Frequency', loc='left', variant='small-caps')
        ax.grid(True, 'both')
        fig.tight_layout()
        return

    def make_audio_one_channel(self):
        self.audio = self.audio[0, :] + self.audio[1, :]
        self.channels = 1
        return

    def find_peaks(self):
        """
        Find all the maxs
        :return maxs_df: pandas dataframe of all maxs
        """
        amplitude_values = []
        times = []
        indexes = []
        maxs_dict = {'Amplitude Value': amplitude_values,
                     'Time': times,
                     'Index': indexes}
        max_value = np.amax(self.lp_filtered_audio)
        for i in range(1, self.lp_filtered_audio.size - 1):
            # Make sure its a worthy peak and not just like 0.00001 or something
            worthy = self.lp_filtered_audio[i] / max_value > 0.1
            if (self.lp_filtered_audio[i] > self.lp_filtered_audio[i - 1]) \
                    and (self.lp_filtered_audio[i] >= self.lp_filtered_audio[i + 1]) \
                    and worthy:
                amplitude_values.append(self.audio[i])
                times.append(self.time_axis[i])
                indexes.append(i)
        self.maxs_df = pd.DataFrame(maxs_dict)
        return self.maxs_df

    def get_beginning_of_section_indexes(self):
        """
        Iterates through maxs_df to find where time difference appropriate to separate
        lubs and dubs
        :return df_section_indexes: 1D np array of 1st index when lub or dub starts
        """
        df_section_indexes = [0]

        for i in range(1, len(self.maxs_df.index)):
            time_difference = self.maxs_df['Time'][i] - self.maxs_df['Time'][i - 1]
            # only save index if its the start of a new section (either lub or dub)
            # determined by if difference bw times of peaks is > 0.1 which should be reviewed
            if time_difference > 0.1:
                df_section_indexes.append(i)

        df_section_indexes.append(len(self.maxs_df.index))
        self.section_idxs = np.array(df_section_indexes)
        return self.section_idxs

    def get_lub_and_dub_indexes(self):
        """
        Get indexes of all max lubs and dubs
        :return: 2 1D numpy arrays of max lub and dub amplitude indexes
        """
        audio_lub_idxs = []
        audio_dub_idxs = []

        for i in range(1, self.section_idxs.size):
            beg_idx = self.section_idxs[i - 1]
            end_idx = self.section_idxs[i]

            df_idx_of_max = self.maxs_df['Amplitude Value'][beg_idx:end_idx].idxmax
            audio_idx_of_max = self.maxs_df['Index'][df_idx_of_max]

            # Append to lub or dub
            if i % 2 != 0:  # lubs
                audio_lub_idxs.append(audio_idx_of_max)
            else:  # dubs
                audio_dub_idxs.append(audio_idx_of_max)

        self.lub_idxs = np.array(audio_lub_idxs)
        self.dub_idxs = np.array(audio_dub_idxs)
        return self.lub_idxs, self.dub_idxs

    def get_sound_amplitude(self, indexes):
        """
        Get mean lub or dub amplitude
        :param indexes: either lub or dub indexes
        :return mean_amp: mean amplitude of lubs or dubs
        """
        amplitude_values = []
        for i in indexes:
            amplitude_values.append(self.audio[i])

        amplitude_values = np.array(amplitude_values)
        mean_amp = np.mean(amplitude_values)
        return mean_amp

    def get_lub_and_dub_amplitudes(self):
        """
        Gets lub and dub amplitudes
        :return: lub_amp, mean dub_amp
        """
        # Check if the variables are already defined or nah
        if self.lub_amp and self.dub_amp:
            pass
        elif self.bpm:  # Means maxs_df, section_idx, lub_idxs, and dub_idxs defined
            self.lub_amp = self.get_sound_amplitude(self.lub_idxs)
            self.dub_amp = self.get_sound_amplitude(self.dub_idxs)
        else:  # Nothing defined
            self.maxs_df = self.find_peaks()
            self.section_idxs = self.get_beginning_of_section_indexes()
            self.lub_idxs, self.dub_idxs = self.get_lub_and_dub_indexes()
            self.lub_amp = self.get_sound_amplitude(self.lub_idxs)
            self.dub_amp = self.get_sound_amplitude(self.dub_idxs)
        return self.lub_amp, self.dub_amp

    def get_lub_and_dub_lengths(self):
        """
        Get indexes of all max lubs and dubs
        ALSOOO getting systolic and diastolic times
        :return: 2 1D numpy arrays of max lub and dub amplitude indexes
        """
        audio_lub_lengths = []
        audio_dub_lengths = []

        systolic_times = []
        diastolic_times = []


        for i in range(1, self.section_idxs.size):
            beg_idx = self.section_idxs[i - 1]
            end_idx = self.section_idxs[i] - 1

            # Find beg of lub or dub
            beg_found = False
            beg_current_idx = self.maxs_df['Index'][beg_idx]
            #####print(self.time_axis[beg_current_idx])
            while beg_found == False:
                if self.audio[beg_current_idx] < 0:
                    beg_found = True
                else:
                    beg_current_idx -= 1

            # Find end of lub or dub
            end_found = False
            end_current_idx = self.maxs_df['Index'][end_idx]
            #####print(self.time_axis[end_current_idx])
            while end_found == False:
                if self.audio[end_current_idx] < 0:
                    end_found = True
                else:
                    end_current_idx += 1

            beg_time = self.time_axis[beg_current_idx]
            end_time = self.time_axis[end_current_idx]
            length = end_time - beg_time

            # Append to lub or dub
            if i % 2 != 0:  # lubs
                audio_lub_lengths.append(length)
                systolic_times.append(end_time)
                if i != 0:
                    diastolic_times.append(beg_time)
            else:  # dubs
                audio_dub_lengths.append(length)
                diastolic_times.append(end_time)
                if i != self.section_idxs.size - 1:
                    systolic_times.append(beg_time)

            #####print()

        self.lub_length = np.mean(np.array(audio_lub_lengths))  # MAX INSTEAD??
        self.dub_length = np.mean(np.array(audio_dub_lengths))  # MAX INSTEAD??
        self.systolic_times = np.array(systolic_times)
        self.diastolic_times = np.array(diastolic_times)
        return self.lub_length, self.dub_length

    def get_systolic_and_diastolic_lengths(self):
        # Make sure times defined
        if self.systolic_times.any() and self.diastolic_times.any():
            pass
        else:
            _,_ = self.get_lub_and_dub_lengths()

        systolic_lengths = []
        diastolic_lengths = []

        for i in range(1, self.systolic_times.size, 2):
            sys_length = self.systolic_times[i] - self.systolic_times[i-1]
            systolic_lengths.append(sys_length)
            print('Sys start', self.systolic_times[i-1])
            self.beg_sys_times.append(self.systolic_times[i-1])

            dias_length = self.diastolic_times[i] - self.diastolic_times[i - 1]
            diastolic_lengths.append(dias_length)
            self.beg_dias_times.append(self.diastolic_times[i - 1])
            print('Dias start', self.diastolic_times[i-1])
            print()

        self.systolic_length = np.mean(np.array(systolic_lengths))
        self.diastolic_length = np.mean(np.array(diastolic_lengths))
        return self.systolic_length, self.diastolic_length

    def get_bpm(self):
        """
        Get bpm by calculating mean length of heart cycle
        :return bpm: rounded int of bpm
        """
        # Make sure lub_idxs is defined
        if self.maxs_df is None:
            self.maxs_df = self.find_peaks()
            self.section_idxs = self.get_beginning_of_section_indexes()
            self.lub_idxs, self.dub_idxs = self.get_lub_and_dub_indexes()

        cycle_lengths = []
        for i in range(1, len(self.lub_idxs)):
            previous_lub = self.lub_idxs[i - 1]
            current_lub = self.lub_idxs[i]
            time_diff = self.time_axis[current_lub] - self.time_axis[previous_lub]
            cycle_lengths.append(time_diff)

        cycle_lengths = np.array(cycle_lengths)
        mean_cycle_length = np.mean(cycle_lengths)

        self.bpm = 60.0 / mean_cycle_length
        self.bpm = round(self.bpm)
        return self.bpm

    def display_audio_time_animation(self, speed=100, replay=False):
        if self.channels == 2:
            self.make_audio_one_channel()
        new_time_axis = []
        for i in range(len(self.time_axis)):
            if i & 1000 == 0:
                new_time_axis.append(self.time_axis[i])
        new_time_axis = np.array(new_time_axis)

        num_frames = (len(new_time_axis) / 10) - 1
        num_frames = int(num_frames)

        fig = plt.figure(figsize=[10, 5])
        ax = plt.axes(xlim=(-2.5, 2.5))
        ax.grid(True)
        audio_line = ax.plot(self.time_axis, self.audio, 'k-')
        current_time, = ax.plot([], [], color='steelblue')

        def init():
            current_time.set_data([], [])
            return

        def animate(index):
            #ax.set_xlim(new_time_axis[index] - 2.5, new_time_axis[index] + 2.5)
            #current_time.set_data([new_time_axis[index], new_time_axis[index]], [-10, 10])
            ax.set_xlim((index / 10) - 2.5, (index / 10) + 2.5)
            current_time.set_data([(index / 10), (index / 10)], [-10, 10])
            return current_time

        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=num_frames,
                                       interval=speed, repeat=replay)
        plt.show()
        plt.close(fig)
        return

    def butter_lowpass(self, cutoff=100, fs=44100, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='lowpass', analog=False)
        self.lpf_b = b
        self.lpf_a = a
        return

    def butter_highpass(self, cutoff=180, fs=44100, order=6):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='highpass', analog=False)
        self.hpf_b = b
        self.hpf_a = a
        return

    def filter_with_lpf(self):
        if self.lpf_b == None or self.lpf_a == None:
            self.butter_lowpass()

        self.lp_filtered_audio = filtfilt(self.lpf_b, self.lpf_a, self.audio)
        return

    def filter_with_hpf(self):
        if self.hpf_b == None or self.hpf_a == None:
            self.butter_highpass()

        self.hp_filtered_audio = filtfilt(self.hpf_b, self.hpf_a, self.audio)
        return





# Perhaps useless
def find_max_peak(audio, time_axis):
    """
    Get the time and index of the max peak
    :param audio: 1D numpy array of audio
    :param time_axis: 1D numpy array of time axis
    :return: max_index: int; time_at_max: float?
    """
    max_value = np.amax(audio)
    max_index = np.where(audio == max_value)[0][0]
    time_at_max = time_axis[max_index]
    return max_index, time_at_max


# Also perhaps useless
def remove_until_first_S1(audio, time_axis):
    """
    Look at first 5 seconds and remove anything before first max (S1)
    :param audio:
    :param time_axis:
    :return: new_audio: 1D numpy array; new_time_axis: 1D numpy array
    """
    five_sec_time_axis = time_axis[(time_axis < 5)]
    index_at_five_sec = five_sec_time_axis.size
    five_sec_audio = audio[0:index_at_five_sec]
    max_index, time_at_max = find_max_peak(five_sec_audio, five_sec_time_axis)
    new_audio = audio[max_index:-1]
    new_time_axis = time_axis[max_index:-1]
    new_time_axis = new_time_axis - time_at_max
    return new_audio, new_time_axis

def display_snippet_time(snippet, time_axis):

    # Plot amplitude vs time
    fig, ax = plt.subplots()
    ax.plot(time_axis, snippet, 'k-')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude (?)')
    ax.set_title('Audio vs Time', loc='left', variant='small-caps')
    ax.grid(True, 'both')
    fig.tight_layout()
    return

def display_snippet_frequency(snippet, fs):
    audio_frequency = abs(scipy.fft.fft(snippet))
    audio_freq_data = audio_frequency[range(len(audio_frequency) // 2)]
    max_amp = np.amax(audio_freq_data)
    audio_freq_data = audio_freq_data / max_amp

    # Convert to freqeuncy
    freq = fftpk.fftfreq(len(audio_frequency), (1.0 / fs))
    freq_axis = freq[range(len(audio_freq_data))]
    freq_axis = freq_axis[(freq_axis < 600)]  # the 300 is hardcoded and kinda random, should probs

    # Plot amplitude vs time
    fig, ax = plt.subplots()
    ax.plot(freq_axis, audio_freq_data[range(len(freq_axis))], 'k-')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude (?)')
    ax.set_title('Audio vs Frequency', loc='left', variant='small-caps')
    ax.grid(True, 'both')
    fig.tight_layout()
    return



if __name__ == "__main__":

    ##file_name = '../HeartSounds/14 Aortic, Normal S1 S2, Sitting, Bell.mp3'
    ##file_name = '../HeartSounds/12 Apex, S3 & Holo Sys Mur, LLD, Bell.mp3'
    #file_name = '../HeartSounds/01Normal.mp3'
    #file_name = '../HeartSounds/16 Aortic, Early Dias Mur, Sitting, Bell.mp3'
    file_name = '../HeartSounds/17 Aortic, Sys & Dias Mur, Sitting, Bell.mp3'


    """testResult = AuscultationResults(file_name)
    testResult.display_audio_time()
    testResult.display_audio_frequency()
    testResult.filter_with_lpf()
    testResult.filter_with_hpf()
    lub, dub = testResult.get_lub_and_dub_amplitudes()
    bpm = testResult.get_bpm()
    lub_length, dub_length = testResult.get_lub_and_dub_lengths()
    print(testResult.systolic_times.size, testResult.diastolic_times.size)
    sys_length, dias_length = testResult.get_systolic_and_diastolic_lengths()
    print('BPM: ', bpm)
    print('Lub: ', lub)
    print('Dub: ', dub)
    print('Lub length: ', lub_length)
    print('Dub length: ', dub_length)
    print('Systolic length: ', sys_length)
    print('Diastolic length: ', dias_length)

    # Printing the filtered data
    display_snippet_time(testResult.lp_filtered_audio, testResult.time_axis)
    display_snippet_time(testResult.hp_filtered_audio, testResult.time_axis)
    plt.show()

    # Okay she still very much in the works and kinds hurt to look at
    # but like she works!
    testResult.display_audio_time_animation()
    plt.show()

    print(testResult.maxs_df.head())
    print(testResult.time_axis.size)
    print(testResult.Fs)"""

    # Length of lub
    # Length of dub
    # Lub and dub amp ratio



    # Systole length
    # Diastole length

    """file_names = ['201102081321.wav',
                  '201102260502.wav',
                  '201103090635.wav',
                  '201103140132.wav',
                  '201103140822.wav',
                  '201103151912.wav',
                  '201103221214.wav',
                  '201104141251.wav',
                  '201105011626.wav',
                  '201105021654.wav',
                  '201105021804.wav',
                  '201105151450.wav',
                  '201106111136.wav',
                  '201106141148.wav',
                  '201106210943.wav',
                  '201106221418.wav',
                  '201106221450.wav',
                  '201108011112.wav',
                  '201108011114.wav',
                  '201108011115.wav',
                  '201108011118.wav']"""

    file_names = ['15 Aortic, Sys Mur & Absent S2, Sitting, Bell.mp3',
                  '16 Aortic, Early Dias Mur, Sitting, Bell.mp3',
                  '17 Aortic, Sys & Dias Mur, Sitting, Bell.mp3',
                  '18 Pulm, Single S2, Supine, Diaph.mp3',
                  '19 Pulm, Spilt S2 Persistent, Supine, Diaph.mp3',
                  '20 Pulm_Spilt_S2_Transient_Supine_Diaph.mp3',
                  '21 Pulm, Eject Sys Mur & Trans Split S2, Supine, Diaph.mp3',
                  '22 Pulm, Split S2 & Eject Sys Mur, Supine, Diaph.mp3',
                  '23 Pulm, Eject Sys Mur & Single S2 & Eject Click, Supine, Diaph.mp3']


    file_namee = []
    lub_length = []
    sys_length = []
    S1_and_sys_length = []

    dub_length = []
    dias_length = []
    S2_and_dias_length = []
    bpms = []

    sig_props = {'File Name': file_namee,
                 'Lub+Sys Length (S2-S1)': S1_and_sys_length,
                 'Dub+Dias Length (S1-S2)': S2_and_dias_length,
                 'BPM': bpms
                 }



    for fileName in file_names:
        directory = '../HeartSounds/{}'.format(fileName)
        testResult = AuscultationResults(directory)
        testResult.filter_with_lpf()

        testResult.get_lub_and_dub_amplitudes()
        testResult.get_bpm()
        testResult.get_lub_and_dub_lengths()
        testResult.get_systolic_and_diastolic_lengths()

        file_namee.append(fileName)
        lub_length.append(testResult.lub_length)
        dub_length.append(testResult.dub_length)
        sys_length.append(testResult.systolic_length)
        dias_length.append(testResult.diastolic_length)
        S1_and_sys_length.append(testResult.lub_length + testResult.systolic_length)
        S2_and_dias_length.append(testResult.dub_length + testResult.diastolic_length)
        bpms.append(testResult.bpm)
        print('Hi')

        ## Getting S1 and S2 times
        times = []
        cols = []

        for i in range(len(testResult.beg_sys_times)):
            times.append(testResult.beg_sys_times[i])
            times.append(testResult.beg_dias_times[i])
            cols.append('S1')
            cols.append('S2')

        ind_S1_and_S2_time_df = pd.DataFrame(times, index=cols)
        ind_S1_and_S2_time_df.transpose()
        ind_S1_and_S2_time_df.to_csv('../HeartSounds/MichiganCSVs/file-{}.csv'.format(fileName))




    sig_props_df = pd.DataFrame(sig_props)
    print(sig_props_df.head())
    sig_props_df.to_csv('../HeartSounds/michiganSoundsProcessedData.csv')




