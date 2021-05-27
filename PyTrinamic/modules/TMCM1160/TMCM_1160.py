'''
Created on 09.04.2019

@author: ED, AH, LH
'''

from PyTrinamic.modules.tmcl_module import tmcl_module
from PyTrinamic.features.StallGuard2Module import StallGuard2Module
from PyTrinamic.features.LinearRampModule import LinearRampModule
from PyTrinamic.features.MotorControl import MotorControl

class TMCM_1160(tmcl_module, StallGuard2Module, LinearRampModule, MotorControl):

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
        referenceSwitchStatus          = 9
        RightEndstop                   = 10
        LeftEndstop                    = 11
        rightLimitSwitchDisable        = 12
        leftLimitSwitchDisable         = 13
        minimumSpeed                   = 130
        actualAcceleration             = 135
        RampMode                       = 138
        MicrostepResolution            = 140
        Ref_SwitchTolerance            = 141
        softStopFlag                   = 149
        EndSwitchPowerDown             = 150
        rampDivisor                    = 153
        PulseDivisor                   = 154
        Intpol                         = 160
        DoubleEdgeSteps                = 161
        ChopperBlankTime               = 162
        ConstantTOffMode               = 163
        DisableFastDecayComparator     = 164
        ChopperHysteresisEnd           = 165
        ChopperHysteresisStart         = 166
        TOff                           = 167
        SEIMIN                         = 168
        SECDS                          = 169
        smartEnergyHysteresis          = 170
        SECUS                          = 171
        smartEnergyHysteresisStart     = 172
        SG2FilterEnable                = 173
        SG2Threshold                   = 174
        slopeControlHighSide           = 175
        slopeControlLowSide            = 176
        ShortToGroundProtection        = 177
        ShortDetectionTime             = 178
        VSense                         = 179
        smartEnergyActualCurrent       = 180
        SmartEnergyStallVelocity       = 181
        smartEnergyThresholdSpeed      = 182
        smartEnergySlowRunCurrent      = 183
        RandomTOffMode                 = 184
        ReferenceSearchMode            = 193
        ReferenceSearchSpeed           = 194
        referenceSwitchSpeed           = 195
        referenceSwitchDistance        = 196
        lastReferenceSwitchPosition    = 197
        BoostCurrent                   = 200
        freewheelingDelay              = 204
        LoadValue                      = 206
        extendedErrorFlags             = 207
        DrvStatusFlags                 = 208
        EncoderPosition                = 209
        encoderPrescaler               = 210
        max_EncoderDeviation           = 212
        PowerDownDelay                 = 214
        absoluteResolverValue          = 215
        externalEncoderPosition        = 216
        externalEncoderPrescaler       = 217
        ExternalEncoderMax_Deviation   = 218
        Step_DirectionMode             = 254

    class ENUMs:
        pass

    class GPs:
        timer_0                        = 0
        timer_1                        = 1
        timer_2                        = 2
        stopLeft_0                     = 27
        stopRight_0                    = 28
        input_0                        = 39
        input_1                        = 40
        serialBaudRate                 = 65
        serialAddress                  = 66
        ASCIIMode                      = 67
        serialHeartbeat                = 68
        CANBitrate                     = 69
        CANSendId                      = 70
        CANReceiveId                   = 71
        telegramPauseTime              = 75
        serialHostAddress              = 76
        autoStartMode                  = 77
        limitSwitchPolarity            = 79
        protectionMode                 = 81
        CANHeartbeat                   = 82
        CANSecondaryAddress            = 83
        eepromCoordinateStore          = 84
        zeroUserVariables              = 85
        serialSecondaryAddress         = 87
        reverseShaftDirection          = 90
        applicationStatus              = 128
        downloadMode                   = 129
        programCounter                 = 130
        lastTmclError                  = 131
        tickTimer                      = 132
        randomNumber                   = 133

    def __init__(self, connection, module_id=1):
        tmcl_module.__init__(self, connection, module_id)

        self.MOTORS = 1
        self.__default_motor = 0

    @staticmethod
    def getEdsFile():
        return __file__.replace("TMCM_1160.py", "TMCM_1160_V3.20.eds")

    def showChipInfo(self):
        print("The TMCM-1160 is a single axis controller/driver module for 2-phase bipolar stepper motors with state of theart feature set. Voltage supply: 12 - 48V")

    # Motion Control functions
    def rotate(self, axis, velocity):
        self.setRampMode(axis, 2)

        self.setTargetVelocity(axis, velocity)

    def stop(self, axis):
        self.rotate(axis, 0)

    def moveTo(self, axis, position, velocity=None):
        if velocity:
            self.setMaxVelocity(axis, velocity)

        self.setTargetPosition(axis, position)

        self.setRampMode(axis, 0)

    def moveBy(self, axis, difference, velocity=None):
        position = difference + self.getActualPosition(axis)

        self.moveTo(axis, position, velocity)

        return position

    # Current control functions
    def getRampMode(self, axis):
        return self.axisParameter(self.APs.RampMode, axis)

    def setRampMode(self, axis, mode):
        return self.setAxisParameter(self.APs.RampMode, axis, mode)

    # Status functions
    def getStatusFlags(self, axis):
        return self.axisParameter(self.APs.DrvStatusFlags, axis)

    def getErrorFlags(self, axis):
        return self.axisParameter(self.APs.extendedErrorFlags, axis)

    def positionReached(self, axis):
        return self.axisParameter(self.APs.PositionReachedFlag, axis)

    # IO pin functions
    def analogInput(self, x):
        return self.connection.analogInput(x)

    def digitalInput(self, x):
        return self.connection.digitalInput(x)

    def showMotionConfiguration(self, axis):
        super().showMotionConfiguration(axis)
        print("\tRamp mode: " + ("position" if (self.getRampMode(axis) == 0) else "velocity"))
