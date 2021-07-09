namespace rsznx_assigning_channels_example
{
    partial class rsznx_assigning_channels_example
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(rsznx_assigning_channels_example));
            this.Label2 = new System.Windows.Forms.Label();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.DisplayEnable = new System.Windows.Forms.CheckBox();
            this.ResourceDescriptor = new System.Windows.Forms.TextBox();
            this.ResetDevice = new System.Windows.Forms.CheckBox();
            this.IDQuery = new System.Windows.Forms.CheckBox();
            this.Label1 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.label8 = new System.Windows.Forms.Label();
            this.TraceFormat = new System.Windows.Forms.ComboBox();
            this.label7 = new System.Windows.Forms.Label();
            this.Window = new System.Windows.Forms.NumericUpDown();
            this.label6 = new System.Windows.Forms.Label();
            this.SInPort = new System.Windows.Forms.NumericUpDown();
            this.label5 = new System.Windows.Forms.Label();
            this.SOutPort = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.TraceName = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.Channel = new System.Windows.Forms.NumericUpDown();
            this.StartButton = new System.Windows.Forms.Button();
            this.TraceCatalog = new System.Windows.Forms.TextBox();
            this.label9 = new System.Windows.Forms.Label();
            this.ExitButton = new System.Windows.Forms.Button();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Window)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.SInPort)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.SOutPort)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.Channel)).BeginInit();
            this.SuspendLayout();
            // 
            // Label2
            // 
            this.Label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.Label2.ForeColor = System.Drawing.Color.SteelBlue;
            this.Label2.Location = new System.Drawing.Point(12, 9);
            this.Label2.Name = "Label2";
            this.Label2.Size = new System.Drawing.Size(544, 48);
            this.Label2.TabIndex = 89;
            this.Label2.Text = "Rohde && Schwarz ZNx Vector Network Analyzer\r\nAssigning Channels Traces And Diagr" +
    "ams Example";
            this.Label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            this.Label2.Click += new System.EventHandler(this.Label2_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.DisplayEnable);
            this.groupBox1.Controls.Add(this.ResourceDescriptor);
            this.groupBox1.Controls.Add(this.ResetDevice);
            this.groupBox1.Controls.Add(this.IDQuery);
            this.groupBox1.Controls.Add(this.Label1);
            this.groupBox1.Location = new System.Drawing.Point(9, 66);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(550, 70);
            this.groupBox1.TabIndex = 94;
            this.groupBox1.TabStop = false;
            // 
            // DisplayEnable
            // 
            this.DisplayEnable.Checked = true;
            this.DisplayEnable.CheckState = System.Windows.Forms.CheckState.Checked;
            this.DisplayEnable.Location = new System.Drawing.Point(451, 31);
            this.DisplayEnable.Name = "DisplayEnable";
            this.DisplayEnable.Size = new System.Drawing.Size(96, 18);
            this.DisplayEnable.TabIndex = 4;
            this.DisplayEnable.Text = "Display Enable";
            // 
            // ResourceDescriptor
            // 
            this.ResourceDescriptor.Location = new System.Drawing.Point(5, 31);
            this.ResourceDescriptor.Name = "ResourceDescriptor";
            this.ResourceDescriptor.Size = new System.Drawing.Size(180, 20);
            this.ResourceDescriptor.TabIndex = 1;
            this.ResourceDescriptor.Text = "GPIB::20::INSTR";
            // 
            // ResetDevice
            // 
            this.ResetDevice.Checked = true;
            this.ResetDevice.CheckState = System.Windows.Forms.CheckState.Checked;
            this.ResetDevice.Location = new System.Drawing.Point(277, 31);
            this.ResetDevice.Name = "ResetDevice";
            this.ResetDevice.Size = new System.Drawing.Size(96, 18);
            this.ResetDevice.TabIndex = 3;
            this.ResetDevice.Text = "Reset Device";
            // 
            // IDQuery
            // 
            this.IDQuery.Checked = true;
            this.IDQuery.CheckState = System.Windows.Forms.CheckState.Checked;
            this.IDQuery.Location = new System.Drawing.Point(199, 31);
            this.IDQuery.Name = "IDQuery";
            this.IDQuery.Size = new System.Drawing.Size(72, 18);
            this.IDQuery.TabIndex = 2;
            this.IDQuery.Text = "ID Query";
            // 
            // Label1
            // 
            this.Label1.Location = new System.Drawing.Point(6, 12);
            this.Label1.Name = "Label1";
            this.Label1.Size = new System.Drawing.Size(120, 16);
            this.Label1.TabIndex = 40;
            this.Label1.Text = "Resource Descriptor";
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.label8);
            this.groupBox2.Controls.Add(this.TraceFormat);
            this.groupBox2.Controls.Add(this.label7);
            this.groupBox2.Controls.Add(this.Window);
            this.groupBox2.Controls.Add(this.label6);
            this.groupBox2.Controls.Add(this.SInPort);
            this.groupBox2.Controls.Add(this.label5);
            this.groupBox2.Controls.Add(this.SOutPort);
            this.groupBox2.Controls.Add(this.label4);
            this.groupBox2.Controls.Add(this.TraceName);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.Channel);
            this.groupBox2.Location = new System.Drawing.Point(9, 142);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(550, 133);
            this.groupBox2.TabIndex = 95;
            this.groupBox2.TabStop = false;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(148, 70);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(70, 13);
            this.label8.TabIndex = 11;
            this.label8.Text = "Trace Format";
            // 
            // TraceFormat
            // 
            this.TraceFormat.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.TraceFormat.FormattingEnabled = true;
            this.TraceFormat.Items.AddRange(new object[] {
            "dB Mag",
            "Phase",
            "Smith",
            "Polar",
            "Delay",
            "SWR",
            "Lin Mag",
            "Real",
            "Imag",
            "Inverted Smith",
            "Unwrapped Phase"});
            this.TraceFormat.Location = new System.Drawing.Point(151, 86);
            this.TraceFormat.Name = "TraceFormat";
            this.TraceFormat.Size = new System.Drawing.Size(121, 21);
            this.TraceFormat.TabIndex = 10;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(6, 70);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(46, 13);
            this.label7.TabIndex = 9;
            this.label7.Text = "Window";
            // 
            // Window
            // 
            this.Window.Location = new System.Drawing.Point(5, 86);
            this.Window.Maximum = new decimal(new int[] {
            99999,
            0,
            0,
            0});
            this.Window.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.Window.Name = "Window";
            this.Window.Size = new System.Drawing.Size(120, 20);
            this.Window.TabIndex = 9;
            this.Window.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.Window.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(421, 16);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(48, 13);
            this.label6.TabIndex = 7;
            this.label6.Text = "S In Port";
            // 
            // SInPort
            // 
            this.SInPort.Location = new System.Drawing.Point(423, 33);
            this.SInPort.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.SInPort.Name = "SInPort";
            this.SInPort.Size = new System.Drawing.Size(120, 20);
            this.SInPort.TabIndex = 8;
            this.SInPort.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.SInPort.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(274, 17);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(56, 13);
            this.label5.TabIndex = 5;
            this.label5.Text = "S Out Port";
            // 
            // SOutPort
            // 
            this.SOutPort.Location = new System.Drawing.Point(277, 33);
            this.SOutPort.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.SOutPort.Name = "SOutPort";
            this.SOutPort.Size = new System.Drawing.Size(120, 20);
            this.SOutPort.TabIndex = 7;
            this.SOutPort.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.SOutPort.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(148, 16);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(66, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "Trace Name";
            // 
            // TraceName
            // 
            this.TraceName.Location = new System.Drawing.Point(151, 33);
            this.TraceName.Name = "TraceName";
            this.TraceName.Size = new System.Drawing.Size(100, 20);
            this.TraceName.TabIndex = 6;
            this.TraceName.Text = "TrcDisp";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(6, 16);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(46, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "Channel";
            // 
            // Channel
            // 
            this.Channel.Location = new System.Drawing.Point(5, 33);
            this.Channel.Maximum = new decimal(new int[] {
            99999,
            0,
            0,
            0});
            this.Channel.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.Channel.Name = "Channel";
            this.Channel.Size = new System.Drawing.Size(120, 20);
            this.Channel.TabIndex = 5;
            this.Channel.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.Channel.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // StartButton
            // 
            this.StartButton.Location = new System.Drawing.Point(9, 394);
            this.StartButton.Name = "StartButton";
            this.StartButton.Size = new System.Drawing.Size(75, 23);
            this.StartButton.TabIndex = 0;
            this.StartButton.Text = "Start";
            this.StartButton.UseVisualStyleBackColor = true;
            this.StartButton.Click += new System.EventHandler(this.StartButton_Click);
            // 
            // TraceCatalog
            // 
            this.TraceCatalog.Location = new System.Drawing.Point(9, 303);
            this.TraceCatalog.Multiline = true;
            this.TraceCatalog.Name = "TraceCatalog";
            this.TraceCatalog.Size = new System.Drawing.Size(550, 72);
            this.TraceCatalog.TabIndex = 12;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(11, 287);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(74, 13);
            this.label9.TabIndex = 1;
            this.label9.Text = "Trace Catalog";
            // 
            // ExitButton
            // 
            this.ExitButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.ExitButton.Location = new System.Drawing.Point(477, 394);
            this.ExitButton.Name = "ExitButton";
            this.ExitButton.Size = new System.Drawing.Size(75, 23);
            this.ExitButton.TabIndex = 11;
            this.ExitButton.Text = "Exit";
            this.ExitButton.UseVisualStyleBackColor = true;
            this.ExitButton.Click += new System.EventHandler(this.ExitButton_Click);
            // 
            // rsznx_assigning_channels_example
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(568, 429);
            this.Controls.Add(this.ExitButton);
            this.Controls.Add(this.label9);
            this.Controls.Add(this.StartButton);
            this.Controls.Add(this.TraceCatalog);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.Label2);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "rsznx_assigning_channels_example";
            this.Text = "rsznx Assigning Channels Traces Diagrams Example";
            this.Load += new System.EventHandler(this.rsznx_assigning_channels_example_Load);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.Window)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.SInPort)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.SOutPort)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.Channel)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        internal System.Windows.Forms.Label Label2;
        private System.Windows.Forms.GroupBox groupBox1;
        internal System.Windows.Forms.CheckBox DisplayEnable;
        internal System.Windows.Forms.TextBox ResourceDescriptor;
        internal System.Windows.Forms.CheckBox ResetDevice;
        internal System.Windows.Forms.CheckBox IDQuery;
        internal System.Windows.Forms.Label Label1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.NumericUpDown SInPort;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown SOutPort;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox TraceName;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown Channel;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.ComboBox TraceFormat;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.NumericUpDown Window;
        private System.Windows.Forms.Button StartButton;
        private System.Windows.Forms.TextBox TraceCatalog;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Button ExitButton;
    }
}