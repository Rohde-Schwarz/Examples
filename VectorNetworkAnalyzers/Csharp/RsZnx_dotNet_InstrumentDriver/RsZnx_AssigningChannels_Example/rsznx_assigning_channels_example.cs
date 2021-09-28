using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using RohdeSchwarz.RsZnx;

namespace rsznx_assigning_channels_example
{
    public partial class rsznx_assigning_channels_example : Form
    {
        //private rsznx m_instrument = null;

        public rsznx_assigning_channels_example()
        {
            InitializeComponent();
        }

        private void ExitButton_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void StartButton_Click(object sender, EventArgs e)
        {
            String buffer = String.Empty;
            
            RsZnx driver;
            using (driver = new RsZnx(ResourceDescriptor.Text, IDQuery.Checked, ResetDevice.Checked))
            {

                try
                {
                    UseWaitCursor = true;
                    System.Windows.Forms.Cursor.Current = Cursors.WaitCursor;

                    TraceCatalog.Text = "";

                    /* reset instrument */
                    if (ResetDevice.Checked)
                        driver.System.Reset();

                    /* switch device display on/off */
                    driver.GeneralSettings.DisplayUpdateEnabled = DisplayUpdate.On;

                    /* Add a new channel if it doesn't exist */
                    driver.Channel.AddChannel(Convert.ToInt32(Channel.Value), "");

                    var channelRc = $"CH{Channel.Value}";

                    /* Create a new trace */
                    driver.Channel.Channels[channelRc].Meas.SParameters.SelectSParameters(TraceName.Text, Convert.ToInt32(SOutPort.Value), Convert.ToInt32(SInPort.Value));

                    /* Select active trace */
                    driver.Channel.Channels[channelRc].Trace.Select = TraceName.Text;

                    /* Change the format for trace */
                    driver.Channel.Channels[channelRc].Format.TraceFormat = (TraceFormat)TraceFormat.SelectedIndex;
                    
                    driver.Channel.Channels[channelRc].Format.GroupDelayAperturePoints = 10;

                    /* Display the trace in the display area */
                    driver.Channel.Channels[channelRc].Trace.AssignTraceDiagramArea(TraceName.Text, Convert.ToInt32(Window.Value));

                    /* List the traces, assigned to a certain Channel */
                    buffer = driver.Channel.Channels[channelRc].Trace.ChannelCatalog;
                    
                    /* Show trace list in front panel textbox */
                    TraceCatalog.Text = buffer.ToString();

                    MessageBox.Show("You should be able to see the added trace on the instrument now. Press OK to continue.", "Vector Network Analyzer Example");

                    /* Find the number for the trace */
                    TraceDiagramNumber traceDiagramNumber = driver.Channel.Channels[String.Format("CH{0}", Channel.Value)].Trace.DiagramNumber(TraceName.Text);

                    /* Remove the trace from the diagram area */
                    driver.Channel.Channels[channelRc].Trace.UnassignTraceDiagramArea(Convert.ToInt32(Window.Value), traceDiagramNumber.diagramNumber);

                    /* Delete a trace with a specified trace name and channel. */
                    driver.Channel.Channels[channelRc].Trace.Delete = TraceName.Text;
                }
                //driver IO error
                catch (Ivi.Driver.IOException ex)
                {
                    MessageBox.Show("Driver error occured: " + ex.Message);
                }

                //driver function is not supported by this sensor
                catch (Ivi.Driver.OperationNotSupportedException ex)
                {
                    MessageBox.Show("Instrument doesn't support the function: " + ex.Message);
                }

                //when a task takes longer than the defined timeout
                catch (Ivi.Driver.MaxTimeExceededException ex)
                {
                    MessageBox.Show("Operation took longer than the maximum defined time: " + ex.Message);
                }

                //if the instrument returns an error in the error queue
                catch (Ivi.Driver.InstrumentStatusException ex)
                {
                    MessageBox.Show("Instrument system error occured: " + ex.Message);
                }

                //if the instrument returns an error in the error queue
                catch (Ivi.Driver.SelectorNameException ex)
                {
                    MessageBox.Show("Invalid selector name used: " + ex.Message);
                }

                finally
                {
                    System.Windows.Forms.Cursor.Current = Cursors.Default;
                    UseWaitCursor = false;
                }
            }
        }

        private void rsznx_assigning_channels_example_Load(object sender, EventArgs e)
        {
            TraceFormat.SelectedIndex = 2;
        }

        private void Label2_Click(object sender, EventArgs e)
        {

        }
    }
}
