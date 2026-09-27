"""Run on Pi from extracted bundle. Back up only affected files; preserve tasks/memory."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tomllib

SRC = Path(__file__).resolve().parent
HOME = Path.home() / ".openfang"
stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
backup = HOME / "backups" / ("obi-v1-" + stamp)
backup.mkdir(parents=True, exist_ok=True)
def put(source, destination):
    if destination.exists():
        saved = backup / destination.relative_to(HOME)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, saved)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

for folder, dest in [("skills", "skills"), ("workspace", "projects/obi"), ("agents", "agents"), ("bridge", "obi-bridge")]:
    for p in (SRC / folder).rglob("*"):
        if p.is_file():
            put(p, HOME / dest / p.relative_to(SRC / folder))
(HOME / "projects/obi/tasks").mkdir(exist_ok=True)

config = HOME / "config.toml"
if 'name = "obi_pc"' in config.read_text():
    shutil.copy2(config, backup / "config.toml")
    config.write_text(config.read_text().replace('name = "obi_pc"', 'name = "obipc"'))
parsed = tomllib.loads(config.read_text())
if not any(x.get("name") == "obipc" for x in parsed.get("mcp_servers", [])):
    shutil.copy2(config, backup / "config.toml")
    with config.open("a") as f:
        f.write(f'''\n[[mcp_servers]]
name = "obipc"
timeout_secs = 50
[mcp_servers.transport]
type = "stdio"
command = "/usr/bin/python3"
args = ["{HOME}/obi-bridge/pi_mcp.py"]
''')
tomllib.loads(config.read_text())

# Replace only generic scaffold instructions for this agent; preserve user memory.
state = HOME / "workspaces/obi-director"
for name, text in {
    "SOUL.md": "# Obi\nDirector de DoVi Games. Aplicá el system prompt y la skill obi-coordination.\n",
    "AGENTS.md": "# Operativa\nUsá las herramientas autorizadas. La coordinación vive en el workspace compartido; el código está en la PC. Conservá las decisiones del equipo.\n",
    "BOOTSTRAP.md": "# Inicio\nEl equipo y el proyecto ya están configurados. Atendé directamente el pedido actual.\n",
}.items():
    p = state / name
    if p.exists():
        dest = backup / p.relative_to(HOME)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
print(json.dumps({"backup": str(backup), "workspace": str(HOME / "projects/obi")}, indent=2))
