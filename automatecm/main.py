# main python file
#!/usr/bin/env python3
"""
automatecm - Command Automation Tool for Linux
Hybrid Python + Bash for optimal performance
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# distro detection:
def detect_distro() -> Tuple[str, str]:
    """Fast distro detection using /etc/os-release"""
    try:
        with open('/etc/os-release', 'r') as f:
            data = {}
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    data[key] = val.strip('"')

            distro_id = data.get('ID', '').lower()
            distro_like = data.get('ID_LIKE', '').lower()
            distro_name = data.get('PRETTY_NAME', 'Unknown Linux')

            # Fast family detection
            check = f"{distro_id} {distro_like}"
            if any(x in check for x in ['ubuntu', 'debian', 'mint', 'pop', 'kali']):
                return ('debian', distro_name)
            elif any(x in check for x in ['rhel', 'fedora', 'centos', 'rocky', 'alma']):
                return ('redhat', distro_name)
            elif any(x in check for x in ['arch', 'manjaro', 'endeavour']):
                return ('arch', distro_name)
            elif any(x in check for x in ['suse', 'opensuse']):
                return ('suse', distro_name)
            return ('unknown', distro_name)
    except:
        return ('unknown', 'Unknown Linux')


class DistroFamily(Enum):
    DEBIAN = "debian"
    REDHAT = "redhat"
    ARCH = "arch"
    SUSE = "suse"
    UNKNOWN = "unknown"


@dataclass
class Command:
    name: str
    description: str
    commands: Dict[str, str]
    requires_root: bool = False
    is_custom: bool = False
    alias: Optional[str] = None

    def get_cmd(self, family: str) -> Optional[str]:
        return self.commands.get(family)


class ConfigManager:
    """Fast JSON-based config management"""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "automatecm"
        self.config_file = self.config_dir / "custom_commands.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_custom(self) -> List[Command]:
        """Load custom commands"""
        if not self.config_file.exists():
            return []
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                return [Command(**cmd) for cmd in data]
        except:
            return []

    def save_custom(self, commands: List[Command]):
        """Save custom commands"""
        try:
            data = [asdict(cmd) for cmd in commands if cmd.is_custom]
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving: {e}")

    def add_custom(self, alias: str, name: str, desc: str, cmd: str, root: bool = False) -> bool:
        """Add custom command"""
        commands = self.load_custom()

        if any(c.alias == alias for c in commands):
            print(f"❌ Alias '{alias}' exists!")
            return False

        # Universal command for all distros
        new_cmd = Command(
            name=name,
            description=desc,
            commands={
                "debian": cmd, "redhat": cmd,
                "arch": cmd, "suse": cmd, "unknown": cmd
            },
            requires_root=root,
            is_custom=True,
            alias=alias
        )

        commands.append(new_cmd)
        self.save_custom(commands)
        return True

    def remove_custom(self, alias: str) -> bool:
        """Remove custom command"""
        commands = self.load_custom()
        filtered = [c for c in commands if c.alias != alias]

        if len(commands) == len(filtered):
            return False

        self.save_custom(filtered)
        return True


class CommandRegistry:
    """Registry with built-in + custom commands"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.commands = []
        self._register_builtin()
        self._load_custom()

    def _register_builtin(self):
        """Fast registration of built-in commands"""
        builtin = [
            ("System Update", "Update system packages", {
                "debian": "sudo apt update && sudo apt upgrade -y",
                "redhat": "sudo dnf update -y",
                "arch": "sudo pacman -Syu --noconfirm",
                "suse": "sudo zypper update -y"
            }, True),

            ("Clean Cache", "Clean package cache", {
                "debian": "sudo apt clean && sudo apt autoremove -y",
                "redhat": "sudo dnf clean all && sudo dnf autoremove -y",
                "arch": "sudo pacman -Sc --noconfirm",
                "suse": "sudo zypper clean -a"
            }, True),

            ("System Info", "Display system information", {
                "debian": "neofetch || (sudo apt install -y neofetch && neofetch)",
                "redhat": "neofetch || (sudo dnf install -y neofetch && neofetch)",
                "arch": "neofetch || (sudo pacman -S --noconfirm neofetch && neofetch)",
                "suse": "neofetch || (sudo zypper install -y neofetch && neofetch)"
            }, False),

            ("Disk Usage", "Analyze disk usage", {
                "debian": "df -h && echo '\n--- Top 10 Largest Directories ---' && sudo du -h / 2>/dev/null | sort -rh | head -10",
                "redhat": "df -h && echo '\n--- Top 10 Largest Directories ---' && sudo du -h / 2>/dev/null | sort -rh | head -10",
                "arch": "df -h && echo '\n--- Top 10 Largest Directories ---' && sudo du -h / 2>/dev/null | sort -rh | head -10",
                "suse": "df -h && echo '\n--- Top 10 Largest Directories ---' && sudo du -h / 2>/dev/null | sort -rh | head -10"
            }, False),

            ("Network Info", "Show network details", {
                "debian": "ip addr show && echo '\n--- Gateway ---' && ip route | grep default",
                "redhat": "ip addr show && echo '\n--- Gateway ---' && ip route | grep default",
                "arch": "ip addr show && echo '\n--- Gateway ---' && ip route | grep default",
                "suse": "ip addr show && echo '\n--- Gateway ---' && ip route | grep default"
            }, False),

            ("Running Services", "List active services", {
                "debian": "systemctl list-units --type=service --state=running",
                "redhat": "systemctl list-units --type=service --state=running",
                "arch": "systemctl list-units --type=service --state=running",
                "suse": "systemctl list-units --type=service --state=running"
            }, False),

            ("Memory Usage", "Display memory info", {
                "debian": "free -h && echo '\n--- Top 10 Memory Consumers ---' && ps aux --sort=-%mem | head -11",
                "redhat": "free -h && echo '\n--- Top 10 Memory Consumers ---' && ps aux --sort=-%mem | head -11",
                "arch": "free -h && echo '\n--- Top 10 Memory Consumers ---' && ps aux --sort=-%mem | head -11",
                "suse": "free -h && echo '\n--- Top 10 Memory Consumers ---' && ps aux --sort=-%mem | head -11"
            }, False),

            ("Failed Services", "Check failed services", {
                "debian": "systemctl --failed",
                "redhat": "systemctl --failed",
                "arch": "systemctl --failed",
                "suse": "systemctl --failed"
            }, False),

            ("System Logs", "View recent error logs", {
                "debian": "journalctl -p err -b --no-pager | tail -50",
                "redhat": "journalctl -p err -b --no-pager | tail -50",
                "arch": "journalctl -p err -b --no-pager | tail -50",
                "suse": "journalctl -p err -b --no-pager | tail -50"
            }, False),

            ("Security Updates", "Install security patches", {
                "debian": "sudo apt update && sudo unattended-upgrade -d",
                "redhat": "sudo dnf update --security -y",
                "arch": "sudo pacman -Syu --noconfirm",
                "suse": "sudo zypper patch -y"
            }, True),
        ]

        for name, desc, cmds, root in builtin:
            self.commands.append(Command(name, desc, cmds, root))

    def _load_custom(self):
        self.commands.extend(self.config.load_custom())

    def reload(self):
        self.commands = [c for c in self.commands if not c.is_custom]
        self._load_custom()

    def get(self, idx: int) -> Optional[Command]:
        return self.commands[idx] if 0 <= idx < len(self.commands) else None


class FastExecutor:
    """Fast command executor using bash subprocess"""

    def __init__(self, family: str):
        self.family = family

    def execute(self, cmd: Command) -> bool:
        """Execute command directly via bash"""
        command = cmd.get_cmd(self.family)

        if not command:
            print(f"❌ Not supported for {self.family}")
            return False

        print(f"\n{'=' * 60}")
        print(f"Executing: {cmd.name}")
        print(f"Description: {cmd.description}")
        if cmd.alias:
            print(f"Alias: {cmd.alias}")
        print(f"{'=' * 60}\n")

        if cmd.requires_root and os.geteuid() != 0:
            print("⚠️  Requires root privileges")

        try:
            # Direct bash execution for speed
            result = subprocess.run(
                command,
                shell=True,
                executable='/bin/bash'
            )

            if result.returncode == 0:
                print(f"\n✅ Completed successfully")
                return True
            else:
                print(f"\n⚠️  Exited with code {result.returncode}")
                return False
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False


class AutomateCM:
    """Main application - fast and lightweight"""

    def __init__(self):
        self.family, self.distro_name = detect_distro()
        self.config = ConfigManager()
        self.registry = CommandRegistry(self.config)
        self.executor = FastExecutor(self.family)

    def header(self):
        print(f"\n{'=' * 60}")
        print(f"  AutomateCM - Linux Command Automation")
        print(f"{'=' * 60}")
        print(f"Distribution: {self.distro_name}")
        print(f"Family: {self.family.upper()}")
        print(f"{'=' * 60}\n")

    def menu(self):
        print("\nCommands:\n")

        for i, cmd in enumerate(self.registry.commands):
            supported = cmd.get_cmd(self.family) is not None
            status = "✅" if supported else "❌"
            root = " [ROOT]" if cmd.requires_root else ""
            custom = " 🔧" if cmd.is_custom else ""
            alias_info = f" (alias: {cmd.alias})" if cmd.alias else ""

            print(f"{status} [{i + 1:2d}] {cmd.name}{root}{custom}{alias_info}")
            print(f"      {cmd.description}")

        print(f"\n [a] Add custom command")
        print(f" [d] Delete custom command")
        print(f" [l] List custom commands")
        print(f" [0] Exit")
        print(f"{'-' * 60}")

    def add_custom(self):
        print(f"\n{'=' * 60}")
        print("  Add Custom Command")
        print(f"{'=' * 60}\n")

        try:
            alias = input("Alias: ").strip()
            if not alias:
                print("❌ Empty alias")
                return

            name = input("Name: ").strip()
            desc = input("Description: ").strip()
            cmd = input("Command: ").strip()

            if not (name and desc and cmd):
                print("❌ All fields required")
                return

            root = input("Root? (y/N): ").strip().lower() == 'y'

            if self.config.add_custom(alias, name, desc, cmd, root):
                print(f"\n✅ Added '{alias}'!")
                self.registry.reload()
        except KeyboardInterrupt:
            print("\n⚠️  Cancelled")

    def delete_custom(self):
        customs = [c for c in self.registry.commands if c.is_custom]

        if not customs:
            print("\n❌ No custom commands")
            return

        print(f"\n{'=' * 60}")
        print("  Delete Custom Command")
        print(f"{'=' * 60}\n")

        for i, cmd in enumerate(customs):
            print(f"[{i + 1}] {cmd.alias} - {cmd.name}")

        try:
            choice = input("\nNumber (or 'c' to cancel): ").strip()
            if choice.lower() == 'c':
                return

            idx = int(choice) - 1
            if 0 <= idx < len(customs):
                alias = customs[idx].alias
                if input(f"Delete '{alias}'? (y/N): ").strip().lower() == 'y':
                    if self.config.remove_custom(alias):
                        print(f"\n✅ Deleted '{alias}'!")
                        self.registry.reload()
        except:
            print("❌ Invalid")

    def list_custom(self):
        customs = [c for c in self.registry.commands if c.is_custom]

        if not customs:
            print("\n📋 No custom commands")
            return

        print(f"\n{'=' * 60}")
        print("  Custom Commands")
        print(f"{'=' * 60}\n")

        for cmd in customs:
            print(f"🔧 {cmd.alias}")
            print(f"   Name: {cmd.name}")
            print(f"   Desc: {cmd.description}")
            print(f"   Cmd: {cmd.get_cmd(self.family)}")
            print(f"   Root: {'Yes' if cmd.requires_root else 'No'}\n")

    def run(self):
        self.header()

        if self.family == 'unknown':
            print("⚠️  Unknown distro - some commands may fail\n")

        while True:
            self.menu()

            try:
                choice = input("\nChoice: ").strip().lower()

                if choice == '0':
                    print("\n👋 Bye!\n")
                    break
                elif choice == 'a':
                    self.add_custom()
                    input("\nPress Enter...")
                elif choice == 'd':
                    self.delete_custom()
                    input("\nPress Enter...")
                elif choice == 'l':
                    self.list_custom()
                    input("\nPress Enter...")
                elif choice.isdigit():
                    idx = int(choice) - 1
                    cmd = self.registry.get(idx)

                    if not cmd:
                        print("❌ Invalid number")
                        continue

                    if input(f"\nExecute '{cmd.name}'? (y/N): ").strip().lower() == 'y':
                        self.executor.execute(cmd)
                        input("\nPress Enter...")
                else:
                    print("❌ Invalid option")

            except KeyboardInterrupt:
                print("\n\n👋 Bye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    try:
        app = AutomateCM()
        app.run()
    except Exception as e:
        print(f"Fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
