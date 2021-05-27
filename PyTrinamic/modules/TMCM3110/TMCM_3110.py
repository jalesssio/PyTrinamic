'''
Created on 05.06.2020

@author: JM
'''

from PyTrinamic.modules.tmcl_module import tmcl_module
from PyTrinamic.features.StallGuard2Module import StallGuard2Module
from PyTrinamic.features.LinearRampModule import LinearRampModule
from PyTrinamic.features.MotorControl import MotorControl

class TMCM_3110(tmcl_module, StallGuard2Module, LinearRampModule, MotorControl):

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
        ReferenceSwitchStatus          = 9
        RightEndstop                   = 10
        LeftEndstop                    = 11
        RightLimitSwitchDisable        = 12
        LeftLimitSwitchDisable         = 13
        MinimumSpeed                   = 130
        ActualAcceleration             = 135
        RampMode                       = 138
        MicrostepResolution            = 140
        ReferenceSwitchTolerance       = 141
        SoftStopFlag                   = 149
        EndSwitchPowerDown             = 150
        RampDivisor                    = 153
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
        SlopeControlHighSide           = 175
        SlopeControlLowSide            = 176
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
        ReferenceSwitchSpeed           = 195
        ReferenceSwitchDistance        = 196
        LastReferenceSwitchPosition    = 197
        BoostCurrent                   = 200
        EncoderMode                    = 201
        FreewheelingDelay              = 204
        LoadValue                      = 206
        ExtendedErrorFlags             = 207
        DrvStatusFlags                 = 208
        EncoderPosition                = 209
        EncoderPrescaler               = 210
        MaxEncoderDeviation            = 212
        GroupIndex                     = 213
        PowerDownDelay                 = 214
        StepDirectionMode              = 254

    class ENUMs:
        pass

    class GPs:
        pass

    def __init__(self, connection, module_id=1):
        tmcl_module.__init__(self, connection, module_id)

        self.MOTORS = 3
        self.__default_motor = 0

    @staticmethod
    def getEdsFile():
        return __file__.replace("TMCM_3110.py", "TMCM_3110_V.320.eds")

    def showChipInfo(self):
        print("The TMCM-3110 is a 3-Axis Stepper Controller / Driver. Voltage supply: 12 - 48V")

    # Motion Control functions
    def rotate(self, axis, velocity):
        self.setRampMode(axis, 2)

        self.setAxisParameter(self.APs.TargetVelocity, axis, velocity)

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
        return self.axisParameter(self.APs.ExtendedErrorFlags, axis)

    def positionReached(self, axis):
        return self.axisParameter(self.APs.PositionReachedFlag, axis)

    # IO pin functions
    def analogInput(self, x):
        return self.connection.analogInput(x, self.module_id)

    def digitalInput(self, x):
        return self.connection.digitalInput(x, self.module_id)

    def showMotionConfiguration(self, axis):
        super().showMotionConfiguration(axis)
        print("\tRamp mode: " + ("position" if (self.getRampMode(axis) == 0) else "velocity"))
