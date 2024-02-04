This was the first GUI app I built. My goal was to build an effective productivity timer with a twist. I didn't want anything too complex, just a snappy effective tool for timing your work.

Some of the maths for displaying the remaining time in user-legible format (HH:MM) caused me a bit of a headache. Also, packaging up the file in PyInstaller took quite a bit of trial and error. I am aware of an issue on certain Mac machines where the application file won't open with the following message: "LSOpenURLsWithRole() failed with error -10810 for the file /Applications/NWS.app."

Making the sound effects was good fun as was harvesting the Newton quotes. I also appreciated how simple it is to use events in Tkinter. Designing the look and feel, however simplistic, was an enjoyable process.

To ensure compatibility with other machines I am looking into code signing the app with an Apple developer account. The bundled .app file may not work on less up to date Mac machines or machines with a different version of Python than 3.10 installed. Lastly I haven't been able to get the .icns file to show up when the application is open in the dock. 