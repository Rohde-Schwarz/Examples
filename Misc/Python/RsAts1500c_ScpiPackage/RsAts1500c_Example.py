"""
# GitHub examples repository path: not set yet

Created on 2023/02
Author: Customer Support / PJ
Version Number: 2
Date of last change: 2023/02/23
Requires: R&S ATC1500 with FW 1.5 or newer
- Installed RsAts1500c Python module (see https://pypi.org/project/RsAts1500c/)
- Installed VISA e.g. R&S Visa 5.12.x or newer
Description: Initiate Instrument, turn inner and outer axis to a defined value and back to 0 ° again,
             perform a stepped sweep on both axes and set the rotators back to 0 ° finally.

General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""


from RsAts1500c import *


# Define variables first, speed in °/s, positions / angles in °
InnerSpeed = 15  # Standard speed for inner axis - should not be changed
InnerStartPos = 0  # Inner rotator origin position
InAxRangeMin = -10  # Lowest position for the inner axis
InAxRangeMax = 10  # Highest position for the inner axis
InnerStepSize = 5  # Step size for an inner axis sweep
OuterSpeed = 45  # Standard speed for outer axis - should not be changed
OuterStartPos = 0  # Outer rotator origin position
OutAxRangeMin = -10  # Lowest position for the outer axis
OutAxRangeMax = 10  # Highest position for the outer axis
OuterStepSize = 5  # Step size for an outer axis sweep

ats = RsAts1500c('TCPIP::169.254.2.10::200::SOCKET')  # Open communication using the VISA identifier of the chamber


def preset():
    """Perform a preset and check chamber to be present after"""
    ats.utilities.preset()
    print(f"{ats.utilities.idn_string} is ready for use now")
    print()


def init():
    """Initialization of the chamber, moving all the positioners to 0° for placement of  DUTs"""
    ats.inner.set_speed(InnerSpeed)
    ats.outer.set_speed(OuterSpeed)

    ats.inner.set_target_value(InnerStartPos)
    ats.inner.start_movement()
    ats.utilities.wait_for_movements_finish()
    inner_pos = round(ats.inner.get_current_position(), 1)
    print(f'Inner axis now set to {inner_pos} °.')

    ats.outer.set_target_value(OuterStartPos)
    ats.outer.start_movement()
    ats.utilities.wait_for_movements_finish()
    outer_pos = round(ats.inner.get_current_position(), 1)
    print(f'Outer axis now set to {outer_pos} °.')

    ats.inner.start_referencing()
    print('Inner rotator has been referenced.')
    print('Chamber initialization process ended with success.')
    print()


def move():
    """Perform a fast move to a specified target angle"""
    ats.inner.set_target_value(InAxRangeMax)
    ats.inner.start_movement()
    ats.utilities.wait_for_movements_finish()
    inner_pos = round(ats.inner.get_current_position(), 1)
    print(f'After single movement the inner axis now is set to {inner_pos} °.')

    ats.outer.set_target_value(OutAxRangeMax)
    ats.outer.start_movement()
    ats.utilities.wait_for_movements_finish()
    outer_pos = round(ats.outer.get_current_position(), 1)
    print(f'After single movement the outer axis now is set to {outer_pos} °.')
    print()


def zero():
    """Perform a move back to the zero point"""
    print('Now set both rotators to 0 °.')
    ats.inner.set_target_value(0)
    ats.inner.start_movement()
    ats.utilities.wait_for_movements_finish()
    inner_pos = round(ats.inner.get_current_position(), 1)
    print(f'After moving the inner axis now is set back to {inner_pos} °.')

    ats.outer.set_target_value(0)
    ats.outer.start_movement()
    ats.utilities.wait_for_movements_finish()
    outer_pos = round(ats.outer.get_current_position(), 1)
    print(f'After moving the outer axis now is set back to {outer_pos} °.')
    print()


def in_min():
    """Perform a move to the lowest position for the inner axis"""
    ats.inner.set_target_value(InAxRangeMin)
    ats.inner.start_movement()
    ats.utilities.wait_for_movements_finish()


def out_min():
    """Perform a fast move to the lowest position for the outer axis"""
    ats.outer.set_target_value(OutAxRangeMin)
    ats.outer.start_movement()
    ats.utilities.wait_for_movements_finish()


def sweep():
    """Perform a sweep in predefined steps for both axes from each preset min and max position"""
    out_min()
    out_pos = OutAxRangeMin
    print("Outer Axis: ", round(ats.outer.get_current_position(), 1), "°, ")
    while out_pos < OutAxRangeMax:
        inner_sweep()
        next_pos = out_pos + OuterStepSize
        ats.outer.set_target_value(next_pos)
        ats.outer.start_movement()
        ats.utilities.wait_for_movements_finish()
        print("Outer Axis: ", round(ats.outer.get_current_position(), 1), "°, ")
        out_pos = next_pos
    inner_sweep()
    print()


def inner_sweep():
    """Sweep of the inner axis in predefined steps"""
    in_min()
    in_pos = InAxRangeMin
    print("Inner axis position update: ", round(ats.inner.get_current_position(), 1), "°, ",  end="")
    while in_pos < InAxRangeMax:
        new_pos = in_pos + InnerStepSize
        ats.inner.set_target_value(new_pos)
        ats.inner.start_movement()
        ats.utilities.wait_for_movements_finish()
        print(round(ats.inner.get_current_position(), 1), "°, ", end="")
        in_pos = new_pos
    print()


# Main program begins here
preset()
init()
move()
zero()
sweep()
zero()

print('Script is done now')
