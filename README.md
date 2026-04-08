# ProjektADS

A Python project demonstrating ADS (Automation Device Specification) communication with TwinCAT PLC using the pyads library.

## Description

This project provides examples of connecting to and communicating with a Beckhoff TwinCAT PLC system from a Linux machine. It includes:

- Basic connection and reading PLC variables
- Notification handling for integer values
- Notification handling for custom structures
- Handling notifications for two separate structures (left/right sensor data)

## Requirements

- Python 3.7+
- pyads library (Beckhoff ADS library for Python)
- TwinCAT PLC system accessible on the network

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ProjektADS
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv moje_ads
   source moje_ads/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install pyads
   ```

## Configuration

Before running the examples, configure the network settings in each script:

```python
PLC_IP = '192.168.1.52'        # IP address of your Windows machine running TwinCAT
PLC_NETID = '192.168.1.52.1.1' # NetID of your Windows machine
LINUX_NETID = '192.168.1.51.1.1'  # NetID for Linux machine (must be in same class as PLC)
```

### Network Setup

1. Ensure both Linux and Windows machines are on the same subnet
2. Configure TwinCAT to allow ADS communication
3. Add route from Linux to PLC using the configured NetIDs

## Usage

### Basic Connection (main.py)

Tests basic ADS connection and reads a PLC variable:

```bash
python main.py
```

### Integer Notifications (main_notifikacie_int.py)

Monitors changes to an integer variable in the PLC:

```bash
python main_notifikacie_int.py
```

### Structure Notifications (main_notifikacie_struct.py)

Handles notifications for custom PLC structures containing:
- id (INT)
- uhol (REAL/float)
- sirka (REAL/float)
- scan (BOOL)

```bash
python main_notifikacie_struct.py
```

### Dual Structure Notifications (main_notifikacie_2structs.py)

Monitors two separate structures (Lavy/Pravy - Left/Right) simultaneously:

```bash
python main_notifikacie_2structs.py
```

## PLC Variables

The examples expect the following variables in your TwinCAT project:

- `.cislo` - Integer variable
- `.ST_to_Jetson` - Custom structure (ST_to_Jetson)
- `.Lavy` - Left structure instance
- `.Pravy` - Right structure instance

## Troubleshooting

### Connection Issues

- Verify IP addresses and NetIDs are correct
- Ensure TwinCAT ADS port (801) is open and accessible
- Check firewall settings on both machines
- Confirm TwinCAT runtime is running

### Common Errors

- **ADS Error**: Check PLC state and variable names
- **Timeout**: Increase timeout values or check network latency
- **Route Error**: Verify NetID configuration and routing

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]