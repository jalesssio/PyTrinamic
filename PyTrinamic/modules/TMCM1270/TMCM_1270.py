'''
Created on 03.12.2019

@author: JM
'''

from PyTrinamic.modules.tmcl_module import tmcl_module
from PyTrinamic.features.StallGuard2Module import StallGuard2Module
from PyTrinamic.features.LinearRampModule import LinearRampModule
from PyTrinamic.features.MotorControl import MotorControl

class TMCM_1270(tmcl_module, LinearRampModule, MotorControl, StallGuard2Module):

    class APs:
        TargetPosition                 = 0
        ActualPosition                 = 1
        TargetVelocity                 = 2
        ActualVelocity                 = 3
        MaxVelocity                    = 4
        MaxAcceleration                = 5
        MaxCurrent                     = 6
        StandbyCurrent                 = 7
        PositionReachedFlag            = 8
        HomeSwitch                     = 9
        RightEndstop                   = 10
        LeftEndstop                    = 11
        AutomaticRightStop             = 12
        AutomaticLeftStop              = 13
        swapSwitchInputs               = 14
        A1                             = 15
        V1                             = 16
        MaxDeceleration                = 17
        D1                             = 18
        StartVelocity                  = 19
        StopVelocity                   = 20
        RampWaitTime                   = 21
        THIGH                          = 22
        VDCMIN                         = 23
        rightSwitchPolarity            = 24
        leftSwitchPolarity             = 25
        softstop                       = 26
        HighSpeedChopperMode           = 27
        HighSpeedFullstepMode          = 28
        MeasuredSpeed                  = 29
        PowerDownRamp                  = 31
        RelativePositioningOptionCode  = 127
        MicrostepResolution            = 140
        ChopperBlankTime               = 162
        ConstantTOffMode               = 163
        DisableFastDecayComparator     = 164
        ChopperHysteresisEnd           = 165
        ChopperHysteresisStart         = 166
        TOff                           = 167
        SEIMIN                         = 168
        SECDS                          = 169
        SmartEnergyHysteresis          = 170
        SECUS                          = 171
        SmartEnergyHysteresisStart     = 172
        SG2FilterEnable                = 173
        SG2Threshold                   = 174
        ShortToGroundProtection        = 177
        VSense                         = 179
        SmartEnergyActualCurrent       = 180
        SmartEnergyStallVelocity       = 181
        SmartEnergyThresholdSpeed      = 182
        RandomTOffMode                 = 184
        ChopperSynchronization         = 185
        PWMThresholdSpeed              = 186
        PWMGrad                        = 187
        PWMAmplitude                   = 188
        PWMScale                       = 189
        pwmMode                        = 190
        PWMFrequency                   = 191
        PWMAutoscale                   = 192
        ReferenceSearchMode            = 193
        ReferenceSearchSpeed           = 194
        RefSwitchSpeed                 = 195
        RightLimitSwitchPosition       = 196
        LastReferencePosition          = 197
        encoderMode                    = 201
        MotorFullStepResolution        = 202
        pwmSymmetric                   = 203
        FreewheelingMode               = 204
        LoadValue                      = 206
        extendedErrorFlags             = 207
        DrvStatusFlags                 = 208
        EncoderPosition                = 209
        EncoderResolution              = 210
        max_EncoderDeviation           = 212
        PowerDownDelay                 = 214
        UnitMode                       = 255

    class ENUMs:
        pass

    class GPs:
        CANBitrate                    = 69
        CANSendId                     = 70
        CANReceiveId                  = 71
        CANSecondaryId                = 72
        autoStartMode                 = 77
        protectionMode                = 81
        eepromCoordinateStore         = 84
        zeroUserVariables             = 85
        applicationStatus             = 128
        programCounter                = 130
        lastTmclError                 = 131
        tickTimer                     = 132
        randomNumber                  = 133

    def __init__(self, connection, module_id=1):
        tmcl_module.__init__(self, connection, module_id)

        self.MOTORS = 1
        self.__default_motor = 0

    @staticmethod
    def getEdsFile():
        return __file__.replace("TMCM_1270.py", "TMCM_1270_V3.22.eds")

    def showChipInfo(self):
        print("The TMCM-1270 is a smart stepper motor driver module. The module is controlled via a CAN bus interface. Voltage supply: 6 - 24V")

    # Motion Control functions
    def rotate(self, axis, velocity):
        self.setTargetVelocity(axis, velocity)

    def stop(self, axis):
        self.rotate(0, axis)

    def moveTo(self, axis, position, velocity=None):
        if velocity:
            self.setMaxVelocity(axis, velocity)

        self.connection.move(0, axis, position, self.module_id)
        self.setTargetPosition(axis, position)

    def moveBy(self, axis, difference, velocity=None):
        position = difference + self.getActualPosition(axis)

        self.moveTo(axis, position, velocity)

        return position

    # Current control functions
    def setMotorRunCurrent(self, axis, current):
        self.setMaxCurrent(axis, current)

    def setMotorStandbyCurrent(self, axis, current):
        self.setAxisParameter(self.APs.StandbyCurrent, axis, current)

    def getMaxCurrent(self, axis):
        return self.axisParameter(self.APs.MaxCurrent, axis)

    def setMaxCurrent(self, axis, current):
        self.setAxisParameter(self.APs.MaxCurrent, axis, current)

    # Status functions
    def getStatusFlags(self, axis):
        return self.axisParameter(self.APs.TMC262ErrorFlags, axis)

    def getErrorFlags(self, axis):
        return self.axisParameter(self.APs.ExtendedErrorFlags, axis)

    def positionReached(self, axis):
        return self.axisParameter(self.APs.PositionReachedFlag, axis)

    # IO pin functions
    def analogInput(self, x):
        return self.connection.analogInput(x, self.module_id)

    def digitalInput(self, x):
        return self.connection.digitalInput(x, self.module_id)
