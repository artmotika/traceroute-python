import sys
import argparse
import socket

PORT = 33434
TIMEOUT = 5
MESSAGE = "123"

def take_arguments():
    parser = argparse.ArgumentParser(
        prog='traceroute',
        description='Displaying possible routes (paths) and measuring transit delays of packets across an Internet Protocol (IP) network',
    )
    parser.add_argument('hostname', type=str, help='ip/domain to traceroute')
    parser.add_argument(
        '-ttl',
        default=55,
        help='Determine the count of intermediate routers being traversed towards the destination'
    )
    args = parser.parse_args()
    return {'hostname': args.hostname, 'ttl': args.ttl}


def traceroute():
    args = take_arguments()
    hostname = args.get('hostname')
    ttl = int(args.get('ttl'))

    dest_ip = socket.gethostbyname(hostname)
    print('Tracing the route to {0}'.format(dest_ip))

    # Prepare a socket to send UDP packets.
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receiver = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)

    receiver.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    receiver.settimeout(TIMEOUT)

    for i in range(1, ttl+1):
        sender.setsockopt(
            socket.IPPROTO_IP, socket.IP_TTL, i)

        # Attempt to send a UDP packet to the destination ip.
        sender.sendto(bytes(MESSAGE, 'utf-8'),
                              (dest_ip, PORT))

        try:
            _, addr = receiver.recvfrom(1500)
        except socket.error:
            addr = None

        if addr:
            sys.stdout.write("%d %s\n" % (i, addr[0]))
        else:
            sys.stdout.write("%d *\n" % i)
            continue

        if addr[0] == dest_ip:
            break

traceroute()
