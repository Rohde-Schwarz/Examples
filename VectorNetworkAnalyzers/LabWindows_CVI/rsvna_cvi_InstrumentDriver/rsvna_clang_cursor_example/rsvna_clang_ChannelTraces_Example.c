
#include "rsvna.h"

#define STRING_LENGTH 4096  

#define checkErr(fCall) if (error = (fCall), error < 0) goto Error;

int main (void)
{
	ViString  resourceName = "TCPIP::localhost::INSTR";
	ViBoolean idQuery = VI_TRUE;
	ViBoolean resetDevice = VI_TRUE;
	ViStatus error = VI_SUCCESS;
	ViChar idResponse[STRING_LENGTH];
	ViSession io;
	ViChar  buffer[STRING_LENGTH];
	ViInt16 int16;
	ViReal64 cmpIn, cmpOut;
  
	printf ("Initializing instrument '%s' ... ", resourceName);
	checkErr(rsvna_init(resourceName, idQuery, resetDevice, &io));
	printf ("success.\n");

	printf ("Enabling remote display update ... ");
	checkErr(rsvna_ConfigureDisplayUpdate (io, VI_TRUE));
	printf ("success.\n");

	printf ("Reading instrument *IDN? string ... ");
	checkErr(rsvna_IDQueryResponse (io, STRING_LENGTH, idResponse));
	printf ("success.\n");
	printf ("Connected instrument: %s\n", idResponse);

	checkErr(rsvna_ConfigureAutoSystemErrQuery(io, VI_TRUE));
	checkErr(rsvna_ConfigureErrorChecking(io, VI_TRUE, VI_TRUE, VI_TRUE));
	checkErr(rsvna_ConfigureAcquisition(io, 1, RSVNA_VAL_SWEEP_ALL_CHAN, VI_FALSE, 1, RSVNA_VAL_SWEEP_ALL_CHAN));

	printf("Selftest ... ");
	checkErr(rsvna_self_test(io, &int16, buffer));
	printf("success. Result: %s\n", int16 == 0 ? "Passed" : "Failed");

	checkErr(rsvna_self_test(io, &int16, buffer));

	// Adding 2nd channel + 4 traces
	checkErr(rsvna_ChannelAdd(io, 2, "SecCh"));

	// Ch2 Trc1 S11 Smith
	checkErr(rsvna_TraceAdd(io, 2, "Ch2Trc1"));
	checkErr(rsvna_TraceAssignDiagramArea(io, 2, "Ch2Trc1"));
	checkErr(rsvna_TraceSelect(io, 2, "Ch2Trc1"));
	checkErr(rsvna_SelectSParameters(io, 2, "Ch2Trc1", 1, 1));
	checkErr(rsvna_ConfigureTraceFormat(io, 2, RSVNA_VAL_SMITH, 1001));

	// Ch2 Trc2 S12
	checkErr(rsvna_TraceAdd(io, 2, "Ch2Trc2"));
	checkErr(rsvna_SelectSParameters(io, 2, "Ch2Trc2", 1, 2));
	checkErr(rsvna_TraceAssignDiagramArea(io, 2, "Ch2Trc2"));

	// Ch2 Trc3 S21
	checkErr(rsvna_TraceAdd(io, 2, "Ch2Trc3"));
	checkErr(rsvna_SelectSParameters(io, 2, "Ch2Trc3", 2, 1));
	checkErr(rsvna_TraceAssignDiagramArea(io, 2, "Ch2Trc3"));

	// Ch2 Trc4 S22
	checkErr(rsvna_TraceAdd(io, 2, "Ch2Trc4"));
	checkErr(rsvna_SelectSParameters(io, 2, "Ch2Trc4", 2, 2));
	checkErr(rsvna_TraceAssignDiagramArea(io, 2, "Ch2Trc4"));

	checkErr(rsvna_GetCurrentDirectory(io, buffer));
	printf("Current directory for file operations: %s\n", buffer);

	// Store the instrument status
	printf("Storing the setup under the name 'Set.znx' ... ");
	checkErr(rsvna_RecallSetManager(io, RSVNA_VAL_RECALL_SET_SAVE, "Set.znx"));
	printf("success.\n");

	// Reset
	printf("Reset ... ");
	checkErr(rsvna_reset(io));
	printf("success.\n");
	
	// Recall
	printf("Recall the status 'Set.znx' ... ");
	checkErr(rsvna_RecallSetManager(io, RSVNA_VAL_RECALL_SET_OPEN, "Set.znx"));
	printf("success.\n");

	// Start sweep on Ch2, wait for it to finish
	printf("Sweeping channel 2 ... ");
	checkErr(rsvna_RestartSweep(io, 2, RSVNA_VAL_SWEEP_SINGLE_CHAN));
	printf("success.\n");

	printf("Exporting channel 2 (port 1) to 'Ch2TracesExport.s1p' ... ");
	checkErr(rsvna_TraceExportData(io, "Ch2Trc1", "Ch2TracesExport.s1p", RSVNA_VAL_UNFORMATTED, RSVNA_VAL_COMPLEX, RSVNA_VAL_POIN, RSVNA_VAL_SEM));
	printf("success.\n");

	printf("Exporting channel 2 to 'Ch2TracesExport.s2p' ... ");
	checkErr(rsvna_TraceExportData(io, "Ch2Trc1", "Ch2TracesExport.s2p", RSVNA_VAL_UNFORMATTED, RSVNA_VAL_COMPLEX, RSVNA_VAL_POIN, RSVNA_VAL_SEM));
	printf("success.\n");

	// Adding Ch3 with power sweep
	printf("Adding channel 3 with power sweep ... ");
	checkErr(rsvna_ChannelAdd(io, 3, "CompressionChannel"));
	checkErr(rsvna_TraceAdd(io, 3, "Ch3Trc1"));
	checkErr(rsvna_TraceAssignDiagramArea(io, 3, "Ch3Trc1"));
	checkErr(rsvna_TraceSelect(io, 3, "Ch3Trc1"));
	checkErr(rsvna_ConfigureSweepType(io, 3, RSVNA_VAL_SWEEP_POW));
	printf("success.\n");

	// Performing a sweep on the Channel3 only
	printf("Sweeping channel 3 ... ");
	checkErr(rsvna_RestartSweep(io, 3, RSVNA_VAL_SWEEP_SINGLE_CHAN));
	printf("success.\n");

	checkErr(rsvna_SetAttributeViReal64(io, "Channel3", RSVNA_ATTR_STATISTICAL_COMPRESSION_VALUE, 2.0));
	checkErr(rsvna_QueryTraceCompressionPoint(io, 1, &cmpIn, &cmpOut));
	printf("Compression points: cmpIn %0.4G, cmpOut %0.4G", cmpIn, cmpOut);

Error:
	(void)rsvna_close(io);

	if (error < VI_SUCCESS)
	{
	  rsvna_GetError(io, &error, STRING_LENGTH, buffer);
	  if (error != VI_SUCCESS)
	  {
		  printf("\n\nERROR OCCURED:\n%s", buffer);
	  }
	}
	else
	{
	  printf("\n\nFinished sucessfully");
	}

	printf("\nPress ENTER to continue...");
	(void)getchar();

	return error;
}

