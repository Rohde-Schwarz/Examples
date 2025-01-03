// rsmxo_ReadWaveformExample.cpp : This file contains the 'main' function. Program execution begins and ends there.
// C++ example on how to use the VXI Plug&Play Instrument drivers in C++.
// The example configures the MXO's Arbitrary generator, acquires a signal on Channel 1 and returns samples, plus 2 measurement results.

// Please connect the arbitrary generator 1 output to the channel 1 input.

// Prerequisites:
// - Install VISA, for example R&S VISA: https://www.rohde-schwarz.com/us/applications/r-s-visa-application-note_56280-148812.html
// - Install rsmxo VXIpnp driver 64-bit: https://www.rohde-schwarz.com/us/driver/mxo4/
//

#include <iostream>
#include "rsmxo.h"

using namespace std;

int main()
{
    ViSession io;
    ViStatus error;
    const string resourceName = "TCPIP::192.168.1.101::hislip0";
    char msg[4096];
    ViInt32 gen = RSMXO_VAL_GENERATOR1;
    ViInt32 channel = 1;
    ViInt32 meas1 = 1;
    ViInt32 meas2 = 2;

    // Initialization
    checkErr(rsmxo_init(const_cast<ViRsrc>(resourceName.c_str()), VI_FALSE, VI_FALSE, &io));
    checkErr(rsmxo_reset(io));
    checkErr(rsmxo_SetAttributeViBoolean(io, const_cast<ViString>(""), RSMXO_ATTR_REMOTE_DISPLAY_UPDATE_ENABLED, VI_TRUE)); // Update display in remote mode
    checkErr(rsmxo_SetCheckOption(io, VI_FALSE));
    checkErr(rsmxo_ConfigureAutoSystemErrQuery(io, VI_TRUE));
    


    // Setting up the MXO Generator
    checkErr(rsmxo_ConfigureGeneratorFunctionType(io, gen, RSMXO_VAL_GENERATOR_FUNCTION_TYPE_SINUSOID));
    checkErr(rsmxo_ConfigureGeneratorFrequency(io, gen, 1e3));
    checkErr(rsmxo_ConfigureGeneratorAmplitude(io, gen, 2.0));
    checkErr(rsmxo_EnableGenerator(io, gen, VI_TRUE));

    // Vertical Scale
    checkErr(rsmxo_ShowChannel(io, channel, VI_TRUE));
    checkErr(rsmxo_ConfigureVerticalScale(io, channel, 1.0)); // 1.0 Volts/div

    // Trigger
    checkErr(rsmxo_ConfigureTriggerMode(io, RSMXO_VAL_TRIGGER_MODE_AUTO));
    checkErr(rsmxo_ConfigureTriggerType(io, RSMXO_REPCAP_TRIGGEREVENT_TRIGA, RSMXO_VAL_TRIGGER_EDGE_EITHER));
    checkErr(rsmxo_ConfigureTriggerHoldoffTime(io, 0.001));

    // Timebase is set to 50us, to acquire 1kHz signal from the arb generator or the probe compensation output
    checkErr(rsmxo_ConfigureAcquisitionSampleRateSettings(io, RSMXO_VAL_ACQUISITION_SAMPLE_RATE_MODE_AUTO, 0, 1E6));
    checkErr(rsmxo_ConfigureHorizontalPosition(io, 0.0));
    checkErr(rsmxo_ConfigureHorizontalTimeScale(io, 500e-6));

    // Measurements configuration: Vpp and Frequency
    checkErr(rsmxo_ConfigureMeasurementSource(io, meas1, RSMXO_VAL_SOURCE_C1, RSMXO_VAL_SOURCE_NONE));
    checkErr(rsmxo_ConfigureMeasurementType(io, meas1, RSMXO_VAL_MEASUREMENT_TYPE_PEAK_DELTA));
    checkErr(rsmxo_EnableMeasurement(io, meas1, VI_TRUE));

    checkErr(rsmxo_ConfigureMeasurementSource(io, meas2, RSMXO_VAL_SOURCE_C1, RSMXO_VAL_SOURCE_NONE));
    checkErr(rsmxo_ConfigureMeasurementType(io, meas2, RSMXO_VAL_MEASUREMENT_TYPE_FREQUENCY));
    checkErr(rsmxo_EnableMeasurement(io, meas2, VI_TRUE));

    // Starting one acquisition and waiting for it to finish.
    checkErr(rsmxo_RunSingleAcquisition(io, 5000));

    // Fetch the waveform
    ViReal64 waveform[10000];
    ViInt32 points;
    checkErr(rsmxo_FetchChannelWaveform(io, channel, 10000, waveform, &points));
    std::cout << "Acquired waveform with " << points << " points\n";

    // Measurements queries
    ViReal64 res1, res2;
    checkErr(rsmxo_FetchMeasurementResultsStatistics(io, meas1, RSMXO_VAL_MEASUREMENT_STATISTICS_CURRENT, &res1));
    std::cout << "Waveform Measurement Vpp: " << res1 << " V\n";

    checkErr(rsmxo_FetchMeasurementResultsStatistics(io, meas2, RSMXO_VAL_MEASUREMENT_STATISTICS_CURRENT, &res2));
    std::cout << "Waveform Measurement Hz: " << res2 << " Hz";

Error:
    rsmxo_GetError(io, &error, 4096, msg);
    rsmxo_close(io);
    if (error < 0)
        std::cout << "\nError occurred:\n" << msg;

    std::cout << "\n\nPress any key to finish ...\n";
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu
