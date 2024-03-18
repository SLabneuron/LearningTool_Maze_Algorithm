# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order high-pass filter (HPF)
"""

import numpy as np

class HPF:
    def calculate_response_hpf(params, freq):

        # parameters
        for key in params:
            globals()[key] = params[key]

        # Calculate transfer function
        omega = 2*np.pi*freq
        frac1 = 1j * omega * R2 * C1
        frac2 = 1 + 1j  * omega * R1 * C1
        transfer_function = -frac1/frac2

        # Calculate for amplitude response
        amplitude_response = np.abs(transfer_function)

        # Calculate for phase response
        phase_response = np.angle(transfer_function)*180/np.pi

        max_gain = np.max(amplitude_response)
        cutoff_gain = max_gain*np.sqrt(1/2)
        cutoff_freq_index = np.argmin(np.abs(amplitude_response - cutoff_gain))
        cutoff_freq = freq[cutoff_freq_index]

        return amplitude_response, phase_response, cutoff_freq