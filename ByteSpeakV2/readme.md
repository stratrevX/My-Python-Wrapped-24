**ByteSpeak 2**

ByteSpeak is a simple, lightweight CLI tool divided into two scripts that allows communication between devices.

**Server**
The server acts as host only, meaning that the server cannot prompt any text.
Features:
  - Key-Protection: It is prompted at the start if the request for a key (that you will set) must be made to every client that tries to connect to the server or not.
  - Port-Check: Once initialized, the server will check if the port is available or not; either way, you can choose whether to continue or not.
  - Handling: Each client = different thread, allowing multiple convos to happen simultaneously without lag.
  - Message Broadcasting: Once a client will prompt a text, the server will prompt it automatically making it visible to the other clients
  - OS Compatibility: The scripts follows OS instructions based on your OS automatically
  - User-Friendly: Provides clear and color-coded prompts, good aspect and easy to use.

**Client**
The client just establishes connection with server!

Features:
  - Interval - an interval between each prompt it's client-side based to avoid flooding, but tbh i don't like how i made it.
  - Os Compatibility: The client aswell follows instructions OS-Based if needed.
  - User-Friendly: The client aswell has a clear and color coded prompts.

**Be Aware**
Please Note that:
  - You are on your own: No protection is wrapped to the server/client script, meaning that any convo could be intercepted easily.
  - Few bugs: I'm not certain of the fully-functionality of these scripts and i do not intend to fix them soon since i'm working on another project.
  - External Conns: If you are trying to host a server, please check your Wifi Access Point's admin page and add a rule for port forwarding to your PC with the following port (443 or your choice).

**Modules to install**
 - colorama
 - requests
 - datetime
