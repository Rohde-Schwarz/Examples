// Preconditions:
// - Installed RsZnx driver 3.30.0 or newer
// - Installed R&S VISA 5.12.3 or newer

using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace rsznx_assigning_channels_example
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new rsznx_assigning_channels_example());
        }
    }
}
