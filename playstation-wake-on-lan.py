#!/usr/bin/env python3

import argparse
import socket


CONSOLE_CONFIG = {
    "ps4": {
        "port": 987,
        "protocol_version": "00020020",
    },
    "ps5": {
        "port": 9302,
        "protocol_version": "00030010",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Send a PlayStation Remote Play wakeup packet."
    )

    parser.add_argument(
        "--console",
        required=True,
        choices=CONSOLE_CONFIG.keys(),
        help="Console type: ps4 or ps5",
    )

    parser.add_argument(
        "--registkey",
        required=True,
        help="8-character Chiaki Remote Play registration key",
    )

    parser.add_argument(
        "--host",
        required=True,
        help="Destination hostname or IP address",
    )

    args = parser.parse_args()
    config = CONSOLE_CONFIG[args.console]

    try:
        user_credential = str(int(args.registkey, 16))
    except ValueError:
        parser.error("--registkey must be a valid hexadecimal value")

    payload = (
        "WAKEUP * HTTP/1.1\n"
        "client-type:vr\n"
        "auth-type:R\n"
        "model:w\n"
        "app-type:r\n"
        f"user-credential:{user_credential}\n"
        f"device-discovery-protocol-version:{config['protocol_version']}\n"
        "\n"
    ).encode("ascii")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", 9303))
        sock.sendto(payload, (args.host, config["port"]))


if __name__ == "__main__":
    main()
