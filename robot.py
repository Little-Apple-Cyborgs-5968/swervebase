#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import wpimath
import wpilib.drive
import wpimath.filter
import wpimath.controller
import phoenix6
import time


class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        """Robot initialization function"""
        self.joystick = wpilib.XboxController(0)
        # self.swerve = drivetrain.Drivetrain()

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

    def autonomousPeriodic(self) -> None:
        self.driveWithJoystick(False)
        # self.swerve.updateOdometry()
        print("auto periodic")

    def teleopInit(self) -> None:
        print("init")
        self.talonfx = phoenix6.hardware.TalonFX(2)
        self.timer = wpilib.Timer()
        self.timer.start()
        self.control = phoenix6.controls.DutyCycleOut(0)
        

    def teleopPeriodic(self):
        """Every 100ms, print the status of the StatusSignal"""
        self.talonfx.set_control(self.control.with_output(self.joystick.getLeftY()))
        if self.timer.hasElapsed(0.1):
            self.timer.reset()
            # get_position automatically calls refresh(), no need to manually refresh.
            #
            # StatusSignals also implement the str dunder to provide a useful print of the signal
            pos = self.talonfx.get_position()
            print(f"Positions is {str(pos)} with {pos.timestamp.get_latency()} seconds of latency")

            # Get the velocity StatusSignal
            vel = self.talonfx.get_velocity()
            # This time wait for the signal to reduce latency
            vel.wait_for_update(0.1)
            print(f"Velocity is {vel} with {vel.timestamp.get_latency()} seconds of latency")

            print("")



    def driveWithJoystick(self, fieldRelative: bool) -> None:
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        xSpeed = (
            -self.xspeedLimiter.calculate(
                wpimath.applyDeadband(self.joystick.getLeftY(), 0.02)
            )
            * drivetrain.kMaxSpeed
        )

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        ySpeed = (
            -self.yspeedLimiter.calculate(
                wpimath.applyDeadband(self.joystick.getLeftX(), 0.02)
            )
            * drivetrain.kMaxSpeed
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rotLimiter.calculate(
                wpimath.applyDeadband(self.joystick.getRightX(), 0.02)
            )
            * drivetrain.kMaxSpeed
        )

        # self.swerve.drive(xSpeed, ySpeed, rot, fieldRelative, self.getPeriod())
        print(f"Variables: {xSpeed}, {ySpeed}, {rot}, {fieldRelative}, {self.getPeriod()}")