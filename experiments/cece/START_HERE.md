# Start Cece's simulation on this Windows PC

This guide starts the **experimental** Cece setup: the robot and room in
Gazebo, the ESP32-C3 firmware and OLED in Wokwi, and a voice window that uses
the laptop microphone and speaker. AtBots connects the PC to OpenAI using the
ChatGPT sign-in you authorized. Leave the programs running while you use Cece.

The Gazebo gait moves the joints, but foot lift and landing are **not yet
verified**. Its movement is driven by the PC bridge; the simulated ESP32's
servo-driver outputs are not yet connected to the Gazebo joints. Laptop audio
is not a simulation of Cece's physical microphone or speaker. Do not use this
guide to power or program the physical robot.

## What is needed

On this PC, these items have already been set up:

- Windows, with **Ubuntu 24.04 in WSL 2**, ROS 2 Jazzy and Gazebo Harmonic.
- VS Code with the Wokwi extension and its license activated.
- The Cece repository and a compiled ESP32-C3 firmware binary.
- AtBots installed in the Cece Python environment and signed in to ChatGPT.
- A laptop microphone and speaker. Vosk and faster-whisper speech models are
  installed locally; spoken text uses faster-whisper in the steps below.
- An internet connection for OpenAI and Sydney weather.

The installed tools and speech models are **not stored in Git**. A fresh PC
needs those tools installed separately. The AtBots Windows keychain fix used
on this PC is documented in [the firmware notes](firmware/CeceBench/README.md).
Your ChatGPT account must separately authorize AtBots to use your plan.

For another Windows PC, the main components are [WSL 2 with Ubuntu](https://learn.microsoft.com/windows/wsl/install),
[ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html) and
[Gazebo Harmonic with ROS](https://gazebosim.org/docs/harmonic/ros_installation/),
[VS Code and the Wokwi extension](https://docs.wokwi.com/vscode/getting-started),
Python 3.12, [AtBots](https://github.com/aetna000/atbots), and Arduino CLI
with the ESP32 core plus Adafruit SSD1327, GFX and BusIO libraries. The Python
environment needs `vosk`, `sounddevice`, `pyserial`, and `faster-whisper`.
The voice command below expects the Vosk `vosk-model-small-en-us-0.15` model
and the CTranslate2 `faster-whisper-base.en` model in the workspace's
`tools` folder. The first is listed on the [Vosk model page](https://alphacephei.com/vosk/models);
faster-whisper can download the second model into a local cache. The exact
paths and installed AtBots environment must then be adjusted to match that PC.

The paths below match this PC. If the repository has been moved, replace the
path in the commands with its new location. No API key or password should be
put in these commands or committed to the repository.

## 1. Start Gazebo and the room

Open **Windows PowerShell**, paste these lines, and press Enter:

```powershell
$ceceWorkspace = Join-Path $env:USERPROFILE 'OneDrive\Documents\ChatGPT\CeCe-the-robot\workspace'
$ceceRepo = Join-Path $ceceWorkspace 'xgoduck_project_repo'
Set-Location (Join-Path $ceceRepo 'experiments\cece\ros2_sim')
wsl -d Ubuntu -- bash -c 'source /opt/ros/jazzy/setup.bash && /usr/bin/python3 build_prototype_world.py && gz sim -r generated/starter_cece.sdf'
```

A **Gazebo Sim** window should open with Cece, a floor, walls and a blue box.
Use the mouse wheel to zoom in. Keep this PowerShell window open. The room is
a starter virtual room, not a reconstruction of your real room.

If Gazebo is already open with `cece_prototype` in the entity list, use that
instance instead of opening a second one.

## 2. Start the simulated ESP32 and OLED

1. Open VS Code. Choose **File → Open Folder** and open:

   ```text
   C:\Users\user\OneDrive\Documents\ChatGPT\CeCe-the-robot\workspace\xgoduck_project_repo\experiments\cece\firmware\CeceBench
   ```

2. Press **Ctrl+Shift+P**, type **Wokwi: Start Simulator**, and press Enter.
3. Keep the **Wokwi Simulator** tab open. You should see the ESP32, ultrasonic
   sensor, four servos, servo driver and square OLED.

If the simulator is already running in VS Code, reuse it. If Wokwi reports
that the firmware file is missing, build it once using the command in
[the firmware notes](firmware/CeceBench/README.md), then start Wokwi again.
The firmware binary is generated locally and is not included in Git.

## 3. Start the PC bridge

Open a **second Windows PowerShell window**, paste the following, and leave
the window open:

```powershell
$ceceWorkspace = Join-Path $env:USERPROFILE 'OneDrive\Documents\ChatGPT\CeCe-the-robot\workspace'
$ceceRepo = Join-Path $ceceWorkspace 'xgoduck_project_repo'
Set-Location (Join-Path $ceceRepo 'experiments\cece\firmware\CeceBench')
& (Join-Path $ceceWorkspace 'tools\atbots-env\Scripts\python.exe') pc_bridge/server.py --port 8768 --provider atbots --sim-motion
```

The window should say that the Cece bridge is on `127.0.0.1:8768`. The
`--sim-motion` option enables the experimental **Gazebo-only** gait. It
does not command physical servos.

If you see **address already in use**, the bridge may already be running.
Do not start a second bridge on that port. If AtBots needs sign-in again,
follow [its sign-in instructions](https://github.com/aetna000/atbots#account-sign-in)
in the installed AtBots environment and complete the browser consent yourself.

## 4. Start the voice window

Open a **third Windows PowerShell window**, paste these lines, and leave it
open:

```powershell
$ceceWorkspace = Join-Path $env:USERPROFILE 'OneDrive\Documents\ChatGPT\CeCe-the-robot\workspace'
$ceceRepo = Join-Path $ceceWorkspace 'xgoduck_project_repo'
$ceceTools = Join-Path $ceceWorkspace 'tools'
$whisperSnapshots = Join-Path $ceceTools 'whisper-models\models--Systran--faster-whisper-base.en\snapshots'
$whisperModel = (Get-ChildItem -LiteralPath $whisperSnapshots -Directory | Select-Object -First 1).FullName
Set-Location (Join-Path $ceceRepo 'experiments\cece\firmware\CeceBench')
& (Join-Path $ceceTools 'atbots-env\Scripts\python.exe') pc_bridge/laptop_voice.py --model (Join-Path $ceceTools 'vosk-model-small-en-us-0.15') --whisper-model $whisperModel
```

The **Cece - laptop voice prototype** window should open. Select your laptop's
microphone if it is not already selected. On this PC, **Microphone Array
(Conexant ISST Audio capture) (Windows WDM-KS)** was tested successfully.
Device numbers can change; use the name rather than relying on a number.

## 5. Talk to Cece

1. In the Cece voice window, click **Listen**.
2. Speak during the next five seconds, then wait for the answer.
3. Try **“What is the weather?”** Cece retrieves current Sydney weather,
   displays the reply on the Wokwi OLED and speaks through the laptop.
4. Try **“Move forward 20 steps.”** The PC bridge requests 20 alternating
   test half-steps in Gazebo. An unnumbered **“move forward”** continues until
   you say **“stop.”** The response means the request was launched; it does
   not certify that the robot completed a walk.

The voice window sends the text to the simulated ESP32 over Wokwi's serial
connection. The firmware then connects to `Wokwi-GUEST` and sends the request
over simulated Wi-Fi to the PC bridge. The bridge calls AtBots/OpenAI for
general questions, retrieves weather, or sends a simulation-only gait
request to Gazebo.

## If something does not work

- **Nothing is heard or recognized:** select the built-in microphone by name
  in the voice window and try again. A very low mic-level number can indicate
  a quiet or unavailable input. Check the laptop's microphone mute and Windows
  microphone access settings yourself.
- **No ESP32 response:** make sure the Wokwi Simulator tab is open and running.
  Its project enables RFC2217 on port 4000 for the voice window. Do not expose
  that unauthenticated port to untrusted networks.
- **Bridge error:** check that the second PowerShell window is still running,
  AtBots is signed in, and your ChatGPT account has granted plan usage.
- **No Gazebo movement:** check that Gazebo is running the generated Cece world
  and is playing, and that the bridge was started with `--sim-motion`.
- **Speech model not found:** the models are local files, not part of Git.
  Check the `tools\vosk-model-small-en-us-0.15` and
  `tools\whisper-models\models--Systran--faster-whisper-base.en\snapshots`
  folders inside the Cece workspace.

To finish, close the voice window, the Wokwi simulator tab and the Gazebo
window, then press **Ctrl+C** in the bridge and Gazebo PowerShell windows.
