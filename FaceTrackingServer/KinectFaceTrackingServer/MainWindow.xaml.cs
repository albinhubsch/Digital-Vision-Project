// -----------------------------------------------------------------------
// <copyright file="MainWindow.xaml.cs" company="Microsoft">
//     Copyright (c) Microsoft Corporation.  All rights reserved.
// </copyright>
// -----------------------------------------------------------------------

//
namespace FaceTrackingBasics
{
    using System;
    using System.Windows;
    using System.Windows.Data;
    using System.Windows.Media;
    using System.Windows.Media.Imaging;
    using Microsoft.Kinect;
    using Microsoft.Kinect.Toolkit;
    using Microsoft.Kinect.Toolkit.FaceTracking;
    using System.Collections.Generic;
    using SimpleWebServer;
    using System.Net;
    using System.Diagnostics;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private static readonly int Bgr32BytesPerPixel = (PixelFormats.Bgr32.BitsPerPixel + 7) / 8;
        private readonly KinectSensorChooser sensorChooser = new KinectSensorChooser();
        //private WriteableBitmap colorImageWritableBitmap;
        //private ColorImageFormat currentColorImageFormat = ColorImageFormat.Undefined;
        private KinectSensor Kinect;
        private FaceTracker facetracker = null;
        private readonly Dictionary<int, FaceTracker> trackedSkeletons = new Dictionary<int, FaceTracker>();
        private byte[] colorImage;
        private short[] depthImage;
        private Skeleton[] skeletonData;
        private ColorImageFormat colorImageFormat = ColorImageFormat.Undefined;
        private DepthImageFormat depthImageFormat = DepthImageFormat.Undefined;
        private WebServer ws;
        public int[] Headpose;

        public MainWindow()
        {
            this.Headpose = new int[3];

            InitializeComponent();

            sensorChooser.KinectChanged += SensorChooserOnKinectChanged;

            sensorChooser.Start();

            this.ws = new WebServer("http://localhost:8080/test/");
            this.ws.Run();

        }

        private void SensorChooserOnKinectChanged(object sender, KinectChangedEventArgs kinectChangedEventArgs)
        {
            KinectSensor oldSensor = kinectChangedEventArgs.OldSensor;
            KinectSensor newSensor = kinectChangedEventArgs.NewSensor;

            if (oldSensor != null)
            {
                oldSensor.AllFramesReady -= KinectSensorOnAllFramesReady;
                oldSensor.ColorStream.Disable();
                oldSensor.DepthStream.Disable();
                oldSensor.DepthStream.Range = DepthRange.Default;
                oldSensor.SkeletonStream.Disable();
                oldSensor.SkeletonStream.EnableTrackingInNearRange = false;
                oldSensor.SkeletonStream.TrackingMode = SkeletonTrackingMode.Default;
            }

            if (newSensor != null)
            {

                try
                {
                    newSensor.ColorStream.Enable(ColorImageFormat.RgbResolution640x480Fps30);
                    newSensor.DepthStream.Enable(DepthImageFormat.Resolution320x240Fps30);
                    try
                    {
                        // This will throw on non Kinect For Windows devices.
                        newSensor.DepthStream.Range = DepthRange.Near;
                        newSensor.SkeletonStream.EnableTrackingInNearRange = true;
                    }
                    catch (InvalidOperationException)
                    {
                        newSensor.DepthStream.Range = DepthRange.Default;
                        newSensor.SkeletonStream.EnableTrackingInNearRange = false;
                    }

                    newSensor.SkeletonStream.TrackingMode = SkeletonTrackingMode.Seated;
                    newSensor.SkeletonStream.Enable();
                    newSensor.AllFramesReady += KinectSensorOnAllFramesReady;

                    this.Kinect = newSensor;
                }
                catch (InvalidOperationException)
                {
                    // This exception can be thrown when we are trying to
                    // enable streams on a device that has gone away.  This
                    // can occur, say, in app shutdown scenarios when the sensor
                    // goes away between the time it changed status and the
                    // time we get the sensor changed notification.
                    //
                    // Behavior here is to just eat the exception and assume
                    // another notification will come along if a sensor
                    // comes back.
                }
            }
        }

        /// <summary>
        /// Window Closed Event. Handles the event if the window is closed
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void WindowClosed(object sender, EventArgs e)
        {
            sensorChooser.Stop();
            this.ws.Stop();
        }

        /// <summary>
        /// When all frames ready trigger this function and do all facetracking.
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void KinectSensorOnAllFramesReady(object sender, AllFramesReadyEventArgs e)
        {

            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();

            ColorImageFrame colorImageFrame = null;
            DepthImageFrame depthImageFrame = null;
            SkeletonFrame skeletonFrame = null;

            try
            {
                colorImageFrame = e.OpenColorImageFrame();
                depthImageFrame = e.OpenDepthImageFrame();
                skeletonFrame = e.OpenSkeletonFrame();

                if (colorImageFrame == null || depthImageFrame == null || skeletonFrame == null)
                {
                    return;
                }

                // Check for image format changes.  The FaceTracker doesn't
                // deal with that so we need to reset.
                if (this.depthImageFormat != depthImageFrame.Format)
                {
                    this.depthImage = null;
                    this.depthImageFormat = depthImageFrame.Format;
                }

                if (this.colorImageFormat != colorImageFrame.Format)
                {
                    this.colorImage = null;
                    this.colorImageFormat = colorImageFrame.Format;
                }

                // Create any buffers to store copies of the data we work with
                if (this.depthImage == null)
                {
                    this.depthImage = new short[depthImageFrame.PixelDataLength];
                }

                if (this.colorImage == null)
                {
                    this.colorImage = new byte[colorImageFrame.PixelDataLength];
                }

                // Get the skeleton information
                if (this.skeletonData == null || this.skeletonData.Length != skeletonFrame.SkeletonArrayLength)
                {
                    this.skeletonData = new Skeleton[skeletonFrame.SkeletonArrayLength];
                }

                colorImageFrame.CopyPixelDataTo(this.colorImage);
                depthImageFrame.CopyPixelDataTo(this.depthImage);
                skeletonFrame.CopySkeletonDataTo(this.skeletonData);

                // Fix this loop, its not really very usefull. Brute force solution
                foreach (Skeleton skeleton in this.skeletonData)
                {
                    try
                    {

                        // Create a face tracker
                        if (this.facetracker == null)
                        {
                            this.facetracker = new FaceTracker(this.Kinect);
                        }

                        // Start the face tracker
                        FaceTrackFrame faceFrame = this.facetracker.Track(
                                                            this.Kinect.ColorStream.Format, this.colorImage,
                                                            this.Kinect.DepthStream.Format, this.depthImage,
                                                            skeleton);

                        // If tracked succesfully update values to server
                        if (faceFrame.TrackSuccessful)
                        {
                            // Head Pose Angles http://msdn.microsoft.com/en-us/library/jj130970#k4w_face_head_pose_angles
                            // X - Pitch
                            // Y - Yaw
                            // Z - Roll

                            // Prepare and format head pose
                            Vector3DF faceRotation = faceFrame.Rotation;
                            string pose = string.Format("X:{0:+00;-00},Y:{1:+00;-00},Z:{2:+00;-00}", faceRotation.X, faceRotation.Y, faceRotation.Z);

                            // Set new head pose in webserver
                            this.ws.setHeadpose(pose);
                        }
                    }
                    catch (Exception ef)
                    {
                        Console.WriteLine("{0} Exception caught.", ef);
                    }
                }

            }

            //Finally dispose everything
            finally
            {
                if (colorImageFrame != null)
                {
                    colorImageFrame.Dispose();
                }

                if (depthImageFrame != null)
                {
                    depthImageFrame.Dispose();
                }

                if (skeletonFrame != null)
                {
                    skeletonFrame.Dispose();
                }
            }

            // Stop timing
            stopwatch.Stop();

            // Write result
            //Console.WriteLine("Time elapsed: {0}", stopwatch.Elapsed);

        }

    }
}
