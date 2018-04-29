add_library('serial')
from processing.serial import Serial

class MBHandler:
    """A class for handling micro:bit serial communication."""
    
    def __init__(self):
        """Initialise the micro:bit, would be good to find it automatically."""
        portName = Serial.list()[len(Serial.list()) - 1]
        port = Serial(this,portName,115200)
        port.bufferUntil(10)
        self.port = port
        self.state = {'a': False, 'b': False}
        self.data = {
                     'name': u'None',
                     'accelerometer': PVector(0,0,-64),
                     'button_a': {
                          'pressed': False,
                          'down': False,
                          'up': False
                          },
                     'button_b': {
                          'pressed': False,
                          'down': False,
                          'up': False
                        }
                        }
    
    def action(self):
        pass
    
    def addEvent(self,evt):
        if evt == self.port:
            self.processEvent(evt.readString())

    def processEvent(self,data):
        if data == 'None':
            return
        try:
            v = int(data.split(':')[0],16)
        except:
            return
        b = (v & 1 == 1)
        v >>= 1
        a = (v & 1 == 1)
        v >>= 1
        z = v & 255
        v >>= 8
        y = v & 255
        v >>= 8
        x = v & 255
        if x > 127:
            x -= 256
        if y > 127:
            y -= 256
        if z > 127:
            z -= 256
        #x *= -1
        y *= -1
        name = data.split(':')[1].rstrip()
        self.data["name"] = name
        self.data["accelerometer"].x = x
        self.data["accelerometer"].y = y
        self.data["accelerometer"].z = z
        self.data["button_a"] = {
                                 'pressed': a,
                                 'down': a and not self.state['a'],
                                 'up': not a and self.state['a']
                          }
        self.data["button_b"] = {
                          'pressed': b,
                          'down': b and not self.state['b'],
                          'up': not b and self.state['b']
                          }
        self.state['a'] = a
        self.state['b'] = b
        self.action()
        return True
