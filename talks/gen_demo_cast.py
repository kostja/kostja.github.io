#!/usr/bin/env python3
"""Generate an asciicast v2 (.cast) file for the Picodata demo slide.

Produces a realistic terminal recording showing:
1. Cluster assembly: 3 nodes with replication factor 3
2. Admin socket: create user, grant DDL privilege
3. psql session: CREATE TABLE, INSERT, SELECT, system tables
"""

import json

OUTPATH = "/home/kostja/work/kostja.github.io/assets/img/talks/demo.cast"

# asciicast v2 header
header = {
    "version": 2,
    "width": 90,
    "height": 35,
    "timestamp": 1710000000,
    "title": "Picodata: bootstrap & SQL demo",
    "env": {"TERM": "xterm-256color", "SHELL": "/bin/bash"}
}

events = []
t = 0.0  # current timestamp

# ── ANSI color helpers ────────────────────────────────
BOLD = "\x1b[1m"
GREEN = "\x1b[1;32m"
BLUE = "\x1b[1;34m"
WHITE = "\x1b[1;37m"
CYAN = "\x1b[1;36m"
YELLOW = "\x1b[1;33m"
RESET = "\x1b[0m"


def pause(seconds):
    global t
    t += seconds


def type_cmd(cmd, char_delay=0.04):
    """Simulate typing a command character by character."""
    global t
    for ch in cmd:
        events.append([round(t, 4), "o", ch])
        t += char_delay
    pause(0.15)
    events.append([round(t, 4), "o", "\r\n"])
    pause(0.05)


def output(text):
    """Print output instantly (server response)."""
    global t
    for line in text.split("\n"):
        events.append([round(t, 4), "o", line + "\r\n"])
        t += 0.02


def comment(text):
    """Print a dim comment line."""
    global t
    events.append([round(t, 4), "o",
                   f"\x1b[2m# {text}\x1b[0m\r\n"])
    t += 0.02


def shell_prompt():
    """Show a bash prompt."""
    global t
    events.append([round(t, 4), "o", f"{GREEN}${RESET} "])


def psql_prompt(db="picodata"):
    """Show a psql prompt."""
    global t
    events.append([round(t, 4), "o", f"{db}=> "])


def admin_prompt():
    """Show the picodata admin prompt."""
    global t
    events.append([round(t, 4), "o", f"{CYAN}picodata>{RESET} "])


# ══════════════════════════════════════════════════════
# Part 1: Assemble a 3-node cluster
# ══════════════════════════════════════════════════════

output(f"{YELLOW}# Part 1: Assemble a 3-node cluster (RF=3){RESET}")
output("")
pause(1.0)

# ── Start first node (bootstraps the cluster) ────────
comment("First node bootstraps the cluster")
shell_prompt()
pause(0.3)
type_cmd("picodata run --data-dir /tmp/i1 --listen :3301 \\")
output("    --peer :3301 --init-replication-factor 3 &")
pause(0.5)
output(f"{GREEN}INFO{RESET}  listening on 0.0.0.0:3301")
output(f"{GREEN}INFO{RESET}  admin socket: /tmp/i1/admin.sock")
output(f"{GREEN}INFO{RESET}  cluster bootstrapped — 1 instance, 3000 buckets")
output("")
pause(0.8)

# ── Start second node ─────────────────────────────────
comment("Second and third nodes join via --peer")
shell_prompt()
pause(0.3)
type_cmd("picodata run --data-dir /tmp/i2 --listen :3302 --peer :3301 &")
pause(0.4)
output(f"{GREEN}INFO{RESET}  listening on 0.0.0.0:3302")
output(f"{GREEN}INFO{RESET}  joined cluster via 127.0.0.1:3301")
output("")
pause(0.6)

# ── Start third node ─────────────────────────────────
shell_prompt()
pause(0.3)
type_cmd("picodata run --data-dir /tmp/i3 --listen :3303 --peer :3301 &")
pause(0.4)
output(f"{GREEN}INFO{RESET}  listening on 0.0.0.0:3303")
output(f"{GREEN}INFO{RESET}  joined cluster via 127.0.0.1:3301")
output("")
pause(1.0)

# ══════════════════════════════════════════════════════
# Part 2: Admin setup
# ══════════════════════════════════════════════════════

output(f"{YELLOW}# Part 2: Create a user via admin socket{RESET}")
output("")
pause(0.8)

shell_prompt()
pause(0.3)
type_cmd("picodata admin /tmp/i1/admin.sock")
pause(0.3)
output(f"Connected to admin console at {WHITE}/tmp/i1/admin.sock{RESET}")
output("")
pause(0.5)

# Create user
admin_prompt()
pause(0.3)
type_cmd("CREATE USER \"demo\" WITH PASSWORD 'DemoPass1';")
pause(0.2)
output(f"{GREEN}1{RESET}")
output("")
pause(0.4)

# Grant CREATE TABLE — the only privilege demo needs beyond what
# the public role already provides (read access to _pico_* tables)
comment("Grant DDL — read access to system tables is already public")
admin_prompt()
pause(0.3)
type_cmd("GRANT CREATE TABLE TO \"demo\";")
pause(0.2)
output(f"{GREEN}1{RESET}")
output("")
pause(0.5)

# Exit admin
admin_prompt()
pause(0.2)
type_cmd("\\q")
output("")
pause(0.5)

# ══════════════════════════════════════════════════════
# Part 3: SQL session via psql
# ══════════════════════════════════════════════════════

output(f"{YELLOW}# Part 3: SQL via standard psql{RESET}")
output("")
pause(0.8)

# ── Connect with psql ─────────────────────────────────
shell_prompt()
pause(0.3)
type_cmd("psql -h 127.0.0.1 -p 3301 -U demo")
pause(0.4)
output("Password for user demo: ********")
pause(0.3)
output("psql (17.4, server picodata 26.1)")
output("Type \"help\" for help.")
output("")
pause(0.5)

# ── Create table ──────────────────────────────────────
psql_prompt()
pause(0.4)
type_cmd("CREATE TABLE weather (")
output("    city TEXT NOT NULL,")
output("    temp DOUBLE PRECISION NOT NULL,")
output("    PRIMARY KEY (city)")
output(") USING MEMTX DISTRIBUTED BY (city);")
pause(0.3)
output("CREATE TABLE")
output("")
pause(0.8)

# ── Insert ────────────────────────────────────────────
psql_prompt()
pause(0.3)
type_cmd("INSERT INTO weather VALUES")
output("    ('Moscow', 15.2), ('Berlin', 18.7), ('Tokyo', 22.1);")
pause(0.3)
output("INSERT 0 3")
output("")
pause(0.8)

# ── Select ────────────────────────────────────────────
psql_prompt()
pause(0.3)
type_cmd("SELECT * FROM weather ORDER BY city;")
pause(0.2)
output("  city  | temp")
output("--------+------")
output(" Berlin | 18.7")
output(" Moscow | 15.2")
output(" Tokyo  | 22.1")
output("(3 rows)")
output("")
pause(1.2)

# ── System tables — cluster topology (3 instances) ───
psql_prompt()
pause(0.3)
type_cmd("SELECT name, replicaset_name, current_state, tier FROM _pico_instance;")
pause(0.2)
output("    name     | replicaset_name | current_state | tier")
output("-------------+-----------------+---------------+---------")
output(" default_1_1 | default_1       | Online        | default")
output(" default_1_2 | default_1       | Online        | default")
output(" default_1_3 | default_1       | Online        | default")
output("(3 rows)")
output("")
pause(1.2)

# ── System tables — tier config (RF=3) ────────────────
psql_prompt()
pause(0.3)
type_cmd("SELECT name, bucket_count, replication_factor FROM _pico_tier;")
pause(0.2)
output("  name   | bucket_count | replication_factor")
output("---------+--------------+--------------------")
output(" default |         3000 |                  3")
output("(1 row)")
output("")
pause(1.0)

# ── Final prompt ──────────────────────────────────────
psql_prompt()
pause(2.0)

# ── Write .cast file ─────────────────────────────────
with open(OUTPATH, "w") as f:
    f.write(json.dumps(header) + "\n")
    for ev in events:
        f.write(json.dumps(ev) + "\n")

print(f"Written {len(events)} events to {OUTPATH} ({t:.1f}s total)")
