# pcapmatcher

pcapmatcher is a command-line utility written in Python for finding matching intervals of IP packets in two pcap files. The utility analyzes two pcap files and identifies intervals where packets match. It also provides information about the matching intervals, including the number of matching packets and the timestamps of the first matching packets in each file.

## Table of Contents

- [Description](#description)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Example](#example)
    - [Example Output](#example-output)
- [Code Structure](#code-structure)
  - [pcapmatcher.py](#pcapmatcherpy)
  - [tests.py](#testspy)
- [Testing](#testing)
- [Notes](#notes)
- [License](#license)

## Description

In the context of data transmission networks where there may be packet loss, delays, duplication, and reordering, pcapmatcher allows you to compare two pcap files and identify intervals with matching packets. The utility uses a "greedy" algorithm to find the largest possible intervals with matching packets.

## Project Structure

The project consists of two main files:

- `pcapmatcher.py` - The main utility that performs the analysis of pcap files.
- `tests.py` - Tests to ensure the correctness of the utility.
- `requirements.txt` - Lists the Python packages required for the project.

## Getting Started

### Prerequisites

- Python 3.6 

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/vladimirblanven/pcapmatcher.git
    cd pcapmatcher
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip3 install -r requirements.txt
    ```

### Usage

Run the utility with the following command:

```bash
python3 pcapmatcher.py <file_a> <file_b> [--min-match-length MIN_LENGTH] [--interval-numbers INTERVAL_NUMBERS]
```

<I>where</I>:
- `<file_a>` - Path to the first pcap file.
- `<file_b>` - Path to the second pcap file.
- `--min-match-length MIN_LENGTH` - Minimum number of consecutive matching packets required to form an interval (default is 3).
- `--interval-numbers INTERVAL_NUMBERS` - The interval number(s) to display information about. You can specify multiple numbers (default is 1).


#### Example:

```bash
python3 pcapmatcher.py file1.pcap file2.pcap --min-match-length 4 --interval-numbers 1 2
```

#### Example Output:

```yaml
Total matching intervals: 2
Interval 1:
  Number of matching packets: 5
  First matching packet in file1.pcap: Packet #10, Timestamp: 1609459200.123456
  First matching packet in file2.pcap: Packet #15, Timestamp: 1609459200.654321
Interval 2:
  Number of matching packets: 3
  First matching packet in file1.pcap: Packet #25, Timestamp: 1609459300.123456
  First matching packet in file2.pcap: Packet #30, Timestamp: 1609459300.654321
```

## Code Structure

### pcapmatcher.py
- `read_pcap(file)` - Function to read a pcap file and extract packets.
- `find_matching_intervals(packets_a, packets_b, min_match_length)` - Function to find matching intervals.
- `print_interval_info(intervals, packets_a, packets_b, interval_numbers, file_a_name, file_b_name)` - Function to print information about matching intervals.
- `main()` - Main function for argument parsing and executing the analysis.
### tests.py
- `create_test_pcap(packets)` - Helper function to create a temporary pcap file with given packets.
- `test_read_pcap()` - Test for the pcap file reading function.
- `test_find_matching_intervals()` - Test for the matching intervals finding function.

## Testing

To ensure the functionality of pcapmatcher, you can run the tests using unittest. This will validate that the utility correctly reads pcap files and finds matching intervals.

1. Run the tests with the following command:

```bash
python3 -m unittest tests.py
```
<I>This command will discover and execute all tests defined in the tests.py file.</I>

2. See test results:

If all tests pass, you should see output indicating that all tests were successful. If any tests fail, the output will provide information about which tests did not pass and why.

## Notes

The utility assumes that both pcap files contain IP packets and that the packets in the files may be in any order.
The maximum supported size for a pcap file is 10 MB.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
