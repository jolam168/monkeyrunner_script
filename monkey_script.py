from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import sys
import os

password = "9119"
package = 'com.android.example'
activity = 'com.android.example.MainActivity'
runComponent = package + '/' + activity


device = MonkeyRunner.waitForConnection()

if not device:
    print("no devices")
    sys.exit(1)

# device.installPackage('myproject/bin/MyApplication.apk')

def get_devices():
    connected_devices = os.popen('adb devices').read().strip().split('\n')[1:]
    devices = []
    for deviceId in connected_devices:
        # get device name
        deviceName = deviceId.split('\t')[0]
        print('deviceName: ' + deviceName)

        # get connection of device
        device = MonkeyRunner.waitForConnection(10.0, deviceName)
        devices.append(device)

def press_password(device, password):
    for c in password:
        device.press("KEYCODE_" + c)
        MonkeyRunner.sleep(1)

    device.press('KEYCODE_ENTER')
    MonkeyRunner.sleep(2)


def setup():
    device.press('KEYCODE_POWER', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(3)
    device.wake()

    MonkeyRunner.sleep(1)
    device.press("KEYCODE_BACK")
    MonkeyRunner.sleep(2)

    device.drag((300, 1300), (300, 150), 0.5, 10)
    MonkeyRunner.sleep(2)

    press_password(device, password)


def snapshot_main_page():
    MonkeyRunner.sleep(4)
    device.drag((300, 1300), (300, 150), 0.5, 10)  # scroll down
    MonkeyRunner.sleep(1)
    newimage = device.takeSnapshot()
    subimage = newimage.getSubImage((30, 1386, 360, 360))
    subimage.writeToFile('snapshot.png')


def main():
    setup()
    device.startActivity(component=runComponent)
    snapshot_main_page()


main()

if __name__ == "__main__":
    main()
