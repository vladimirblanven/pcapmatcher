import unittest
from scapy.all import wrpcap, Ether, IP, TCP
from tempfile import NamedTemporaryFile
import os
from pcapmatcher import read_pcap, find_matching_intervals, PacketInfo

class TestPcapUtil(unittest.TestCase):
    def create_test_pcap(self, packets):
        temp_pcap = NamedTemporaryFile(delete=False)
        temp_pcap.close()
        for packet in packets:
            packet.time = packet.time if hasattr(packet, 'time') else 0
            Ether()/IP()/TCP()
            wrpcap(temp_pcap.name, packet, append=True)
        return temp_pcap.name

    def test_read_pcap(self):
        packets = [Ether()/IP()/TCP(), Ether()/IP()/TCP()]
        pcap_file = self.create_test_pcap(packets)
        packets_read = read_pcap(pcap_file)
        self.assertEqual(len(packets_read), 2)
        os.remove(pcap_file)

    def test_find_matching_intervals(self):
        packets_a = [PacketInfo(0, Ether()/IP()/TCP(sport=12345)),
                     PacketInfo(1, Ether()/IP()/TCP(sport=12346)),
                     PacketInfo(2, Ether()/IP()/TCP(sport=12347))]
        packets_b = [PacketInfo(0, Ether()/IP()/TCP(sport=12345)),
                     PacketInfo(1, Ether()/IP()/TCP(sport=12346)),
                     PacketInfo(2, Ether()/IP()/TCP(sport=12347))]
        intervals = find_matching_intervals(packets_a, packets_b, 2)
        self.assertEqual(len(intervals), 1)
        self.assertEqual(intervals[0], (0, 0, 3))

if __name__ == '__main__':
    unittest.main()
