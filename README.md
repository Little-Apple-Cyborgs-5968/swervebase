### TODO

- Consider setting up the PDM package manager.
- Implement a custom dashboard. (FOR PID TWEAKING)
- work on simulation (physics.py)
- make sure the swerve code works with our modules (MK4i Swerve Module kraken x60 motor shaft) check both chassis.py (from team 4774) and swervermodule.py (official example)

### Code Structure (TODO: Convert to this)

The project uses RobotPy's Magicbot framework:

- `robot.py`: Entry point that maps driver inputs to high-level robot actions.
- `components/`: Abstracts hardware into robot actions.
- `controllers/`: Automates robot actions, primarily using state machines.
- `autonomous/`: Manages robot behavior during the autonomous period.
- `ids.py`: Contains CAN IDs, PH channels, and other port numbers.
