# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order band-pass filter (BPF)
"""

import numpy as np

class BPF:
    def calculate_response_bpf(params, freq):

        # parameters
        for key in params:
            globals()[key] = params[key]

        # Calculate transfer function
        omega = 2*np.pi*freq
        frac1 = 1j * omega* R2 * C1
        frac2 = 1- omega**2 * R1 * R2 * C1* C2 + 1j * omega*(R1 * C1 + R2 * C2)
        transfer_function = -frac1/frac2

        # Calculate for amplitude response
        amplitude_response = np.abs(transfer_function)

        # Calculate for phase response
        phase_response = np.angle(transfer_function)*180/np.pi

        # Calculation Cutoff Frequency
        max_gain = np.max(amplitude_response)
        cutoff_gain = max_gain*np.sqrt(1/2)
        max_gain_index = np.argmax(amplitude_response)


        for i in range(max_gain_index, 0, -1):
            if amplitude_response[i] < cutoff_gain:
                lower_cutoff_freq = freq[i+1]
                break

        for i in range(max_gain_index, len(freq), 1):
            if amplitude_response[i] <cutoff_gain:
                upper_cutoff_freq = freq[i-1]
                break
        
        print(max_gain, lower_cutoff_freq, upper_cutoff_freq)

        return amplitude_response, phase_response, lower_cutoff_freq, upper_cutoff_freq