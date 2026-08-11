# PlayStation Wake-on-LAN Tool

A tiny Python utility that sends Wake-on-LAN (WoL) magic packets over UDP to wake various PlayStation consoles from
rest mode.

Unlike some existing tools, this does not require PSN connectivity or the PlayStation Second Screen pairing process
meaning `ps-wol.py` **works on both jailbroken and offline-only consoles**.

Authentication only requires a hexadecimal registration key which can be obtained by following a remote play pairing
process with tools like [Chiaki-Ng](https://github.com/streetpea/chiaki-ng)
or [Chiaki-Up](https://github.com/gameblabla/chiaki-up).

## Usage

For a PS4:

```bash
./ps-wol.py \
    --console ps4 \
    --host ps4.lan \
    --registkey 12345678
```

For a PS5:

```bash
./ps-wol.py \
    --console ps5 \
    --host ps5.lan \
    --registkey 12345678
```

Arguments:

```text
--console    ps4 or ps5
--host       Console hostname or IP address
--registkey  Chiaki Remote Play registration key
```

The script automatically selects the appropriate wakeup port and protocol version:

| Console | Destination | Protocol   |
|---------|------------:|------------|
| PS4     |     UDP 987 | `00020020` |
| PS5     |    UDP 9302 | `00030010` |

## Getting the Registration Key

The easiest way to obtain the key is to register the console once using Chiaki-Up/Chiaki-Ng and extract it from the
`.json`
configuration file `chiaki-up.json`:

```bash
cat chiaki-up.json | jq -r '.settings.registered_hosts[0].rp_regist_key' | base64 --decode
```

Adjust the array index if you have multiple consoles registered.

### Monitoring Power State

Similarly, you may also want to incorporate a power state check into your automation, which can be simply done by using
`netcat` and checking if a specific TCP port used by remote play is open.

For example: `nc -z -w 5 ps4.lan 9295` where a `0`/`1` response will indicate the system is on/off respectively.

### Credits
- [Chiaki](https://sr.ht/~thestr4ng3r/chiaki/) - pairing process, initiating wakeup packet
- [Wireshark](https://www.wireshark.org/) - wakeup packet analysis
