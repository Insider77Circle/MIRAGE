import asyncio
import functools
from collections import deque
from datetime import datetime

# --- RICH TUI LIBRARIES ---
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text
from rich import box

# --- CORE LOGIC ---
from mirage_core import (
    Fabricator, MirageAI, handle_client,
    DIFFICULTY, ACTIVE_PORTS, WORLD_CONTEXT
)

# ==========================================
#   UI CONFIG & STATE
# ==========================================
# UI Theme Colors
C_CB = "bright_cyan"
C_GN = "bright_green"
C_RD = "bright_red"
C_MG = "bright_magenta"
C_TXT = "white"
C_DIM = "grey50"

# UI STATE BUFFERS
log_buffer = deque(maxlen=20)
connection_history = deque(maxlen=5)
system_status = {"cpu": 12, "mem": 45, "threat": "LOW"}

# ==========================================
#   TUI EVENT HANDLER
# ==========================================
async def tui_event_handler(event):
    """Processes events from the core and updates TUI state buffers."""
    event_type = event.get("type")
    
    if event_type == "connection":
        connection_history.appendleft((event["time"], event["ip"], event["port"]))
        log_buffer.append(f"[{C_GN}]→ Incoming connection from {event['ip']} on port {event['port']}[/{C_GN}]")
    
    elif event_type == "status_update":
        system_status["cpu"] = min(99, max(10, system_status["cpu"] + event["cpu_delta"]))
        system_status["mem"] = min(99, max(10, system_status["mem"] + event["mem_delta"]))
        
    elif event_type == "ai_log":
        log_buffer.append(f"[{C_CB}][AI THOUGHT][/{C_CB}] {event['message']}")
        
    elif event_type == "threat_update":
        system_status["threat"] = event["level"]
        
    elif event_type == "error":
        log_buffer.append(f"[{C_RD}][ERROR][/{C_RD}] {event['message']}")

    elif event_type == "fab":
        log_buffer.append(f"[{C_MG}][FABRICATOR][/{C_MG}] {event['message']}")


# ==========================================
#   TUI LAYOUT COMPONENTS
# ==========================================
def make_layout() -> Layout:
    # ... (Same as original)
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="body", ratio=2),
    )
    layout["body"].split_column(
        Layout(name="gauges", size=8),
        Layout(name="middle_section", ratio=1),
        Layout(name="bottom_log", size=12),
    )
    layout["middle_section"].split_row(
        Layout(name="history", ratio=1),
        Layout(name="active_tasks", ratio=1),
    )
    return layout

def get_header():
    # ... (Same as original)
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="right", ratio=1)
    grid.add_row(
        Text(" MIRAGE V3 // CYBERPUNK PROTOCOL", style=f"bold italic {C_CB}"),
        Text(f" TARGET: {WORLD_CONTEXT['network']['hostname']} ", style=f"bold {C_MG}"),
        Text(datetime.now().strftime("%H:%M:%S UTC "), style=C_DIM),
    )
    return Panel(grid, style=f"{C_CB} on black", box=box.HEAVY_EDGE)

def get_sidebar():
    # ... (Same as original)
    table = Table(show_header=False, box=None, expand=True)
    table.add_column("Icon", style=C_MG, width=2)
    table.add_column("Label", style=C_TXT)
    
    menu_items = [
        ("◈", "Dashboard"), ("▣", "Network Map"), ("▤", "Asset Browser"),
        ("▥", "Web App Config"), ("▦", "Burp Suite Logs"), ("!", f"Diff: {DIFFICULTY}")
    ]
    for icon, label in menu_items:
        table.add_row(icon, label)
        table.add_row("", "") # Spacer

    return Panel(Align.center(table, vertical="top"), title="[bold]NAVIGATION[/bold]", border_style=C_CB, box=box.ROUNDED)

def get_gauges():
    # ... (Same as original)
    def make_gauge_panel(title, value, color):
        pg = Progress(
            TextColumn("[bold]{task.fields[val_label]}", justify="right"),
            BarColumn(bar_width=None, style=f"dim {color}", complete_style=color, finished_style=color),
            expand=True
        )
        task_id = pg.add_task("", total=100, val_label=f"{value}%" if isinstance(value, int) else value)
        if isinstance(value, int):
            pg.update(task_id, completed=value)
        return Panel(pg, title=f"[{C_TXT}]{title}[/]", border_style=color)

    gauge_layout = Table.grid(expand=True, padding=1)
    gauge_layout.add_column(ratio=1)
    gauge_layout.add_column(ratio=1)
    gauge_layout.add_column(ratio=1)
    
    threat_color = C_RD if system_status["threat"] == "HIGH" else C_MG if system_status["threat"] == "MEDIUM" else C_GN
    gauge_layout.add_row(
        make_gauge_panel("CPU LOAD", system_status["cpu"], C_GN),
        make_gauge_panel("MEMORY USAGE", system_status["mem"], C_CB),
        make_gauge_panel("THREAT LEVEL", system_status["threat"], threat_color),
    )
    return gauge_layout

def get_history_table():
    # ... (Same as original)
    table = Table(expand=True, border_style="dim grey30", box=box.SIMPLE_HEAD)
    table.add_column("Time", style=C_DIM)
    table.add_column("Source IP", style=C_CB)
    table.add_column("Port", style=C_MG, justify="right")

    for time_str, ip, port in connection_history:
        table.add_row(time_str, ip, str(port))
        
    return Panel(table, title="[bold]CONNECTION HISTORY[/bold]", border_style=C_CB)

def get_log_window():
    # ... (Same as original)
    text = Text()
    for line in log_buffer:
        text.append(line + "\n")
    
    return Panel(Align.left(text, vertical="bottom"), title="[bold]AI KERNEL LOG / CHAT[/bold]", border_style=C_MG, box=box.HEAVY)


# ==========================================
#   MAIN TUI APP LOOP
# ==========================================
async def main_loop():
    # 1. Initialize Core Components, passing the TUI handler to them
    tui_logger = lambda event: asyncio.create_task(tui_event_handler(event))
    fab = Fabricator(logger=tui_logger)
    ai_engine = MirageAI(logger=tui_logger)
    
    # Run asset generation
    fab.run()
    
    # 2. Start Honeypot Listeners
    servers = []
    log_buffer.append(f"[{C_MG}]Starting TUI and listeners on ports: {ACTIVE_PORTS}[/{C_MG}]")
    for port in ACTIVE_PORTS:
        try:
            # The core handle_client is now passed the AI engine and the TUI event handler
            handler = functools.partial(handle_client, ai_engine=ai_engine, event_callback=tui_event_handler)
            server = await asyncio.start_server(handler, '0.0.0.0', port)
            servers.append(server)
        except PermissionError:
             log_buffer.append(f"[{C_RD}]ERROR: Failed to bind Port {port}. Run with sudo.[/{C_RD}]")

    if not servers:
        print("Failed to start any servers. Exiting.")
        return

    # 3. Run the TUI
    layout = make_layout()
    with Live(layout, refresh_per_second=4, screen=True) as live:
        while True:
            layout["header"].update(get_header())
            layout["sidebar"].update(get_sidebar())
            layout["gauges"].update(get_gauges())
            layout["history"].update(get_history_table())
            layout["active_tasks"].update(Panel(Align.center(Text("Burp Suite Module: ACTIVE\nWeb Traffic Intercept: ON", style=C_GN)), title="MODULE STATUS", border_style=C_GN))
            layout["bottom_log"].update(get_log_window())
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nMirage V3 TUI Shutdown initiated...")
