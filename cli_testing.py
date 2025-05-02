# import argparse
# import json
# from testing import SmartPentester, DefensiveMechanisms  # Import original classes

# def run_scan(targets):
#     pentester = SmartPentester()
#     pentester.llm_enabled = True
#     pentester.timeout = 15  # Adjust if needed
    
#     for target in targets:
#         pentester.scan_endpoint(target)
    
#     pentester.generate_report()

# def view_report():
#     try:
#         with open("scan_report.json", "r") as f:
#             report = json.load(f)
#             print(json.dumps(report, indent=4))
#     except FileNotFoundError:
#         print("\n❌ No scan report found. Run a scan first.")

# def run_defensive():
#     defense = DefensiveMechanisms()
#     defense.generate_mitigation_report()

# def view_mitigation():
#     try:
#         with open("mitigation_report.json", "r") as f:
#             report = json.load(f)
#             print(json.dumps(report, indent=4))
#     except FileNotFoundError:
#         print("\n❌ No mitigation report found. Run defense module first.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Smart Pentester CLI")
#     parser.add_argument("command", choices=["scan", "view-report", "defense", "view-mitigation"],
#                         help="Command to execute")
#     parser.add_argument("--targets", nargs="*", help="Target URLs for scanning")
    
#     args = parser.parse_args()
    
#     if args.command == "scan":
#         if not args.targets:
#             print("\n❌ Please provide target URLs for scanning.")
#         else:
#             run_scan(args.targets)
#     elif args.command == "view-report":
#         view_report()
#     elif args.command == "defense":
#         run_defensive()
#     elif args.command == "view-mitigation":
#         view_mitigation()


#working 
# import argparse
# import json
# from testing import SmartPentester, DefensiveMechanisms

# def run_scan():
#     """Runs the security scan using predefined targets"""
#     pentester = SmartPentester()
#     pentester.llm_enabled = True  # Enable AI analysis
#     pentester.timeout = 15  # Set timeout

#     targets = [
#         "http://bwapp.hakhub.net/login.php",
#         "http://bwapp.hakhub.net/xss_get.php"
#     ]

#     for target in targets:
#         pentester.scan_endpoint(target)

#     pentester.generate_report()
#     print("\n✅ Scan completed. Report saved as scan_report.json")

# def view_report():
#     """Displays the scan report"""
#     try:
#         with open("scan_report.json", "r") as f:
#             report = json.load(f)
#         print(json.dumps(report, indent=4))
#     except FileNotFoundError:
#         print("\n❌ Scan report not found! Run the scan first.")

# def run_defense():
#     """Runs defensive mechanisms and generates mitigations"""
#     defense = DefensiveMechanisms()
#     defense.generate_mitigation_report()
#     print("\n✅ Mitigation report saved as mitigation_report.json")

# def view_mitigation():
#     """Displays the mitigation report"""
#     try:
#         with open("mitigation_report.json", "r") as f:
#             report = json.load(f)
#         print(json.dumps(report, indent=4))
#     except FileNotFoundError:
#         print("\n❌ Mitigation report not found! Run the defense first.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Mina-AI CLI for penetration testing and security analysis.")
#     parser.add_argument("command", choices=["scan", "view-report", "defense", "view-mitigation"], help="Select a function to run")
    
#     args = parser.parse_args()
    
#     if args.command == "scan":
#         run_scan()
#     elif args.command == "view-report":
#         view_report()
#     elif args.command == "defense":
#         run_defense()
#     elif args.command == "view-mitigation":
#         view_mitigation()

# working fine

# import json
# import argparse
# from rich.console import Console
# from rich.table import Table
# from testing import SmartPentester, DefensiveMechanisms

# console = Console()

# def run_scan():
#     """Runs the security scan using predefined targets"""
#     pentester = SmartPentester()
#     pentester.llm_enabled = True  # Enable AI analysis
#     pentester.timeout = 15  # Set timeout


# def view_scan_report():
#     try:
#         with open("scan_report.json", "r") as f:
#             findings = json.load(f)
#     except FileNotFoundError:
#         console.print("\n❌ [bold red]Scan report not found! Run a scan first.[/bold red]")
#         return

#     console.print("\n📄 [bold cyan]Scan Report[/bold cyan]\n" + "=" * 40)

#     for url, vulnerabilities in findings.items():
#         console.print(f"\n🔗 [bold yellow]Target:[/bold yellow] {url}")
#         for vuln, status in vulnerabilities.items():
#             console.print(f"  ✅ [bold green]{vuln}[/bold green]: {status}")

# def view_mitigation_report():
#     try:
#         with open("mitigation_report.json", "r") as f:
#             mitigations = json.load(f)
#     except FileNotFoundError:
#         console.print("\n❌ [bold red]Mitigation report not found! Run defense first.[/bold red]")
#         return

#     console.print("\n🛡️  [bold cyan]Mitigation Report[/bold cyan]\n" + "=" * 40)

#     for url, solutions in mitigations.items():
#         console.print(f"\n🔗 [bold yellow]Target:[/bold yellow] {url}")
#         for vuln, fix in solutions.items():
#             console.print(f"  🔹 [bold blue]{vuln}[/bold blue]: {fix}")

# def run_defense():
#     """Runs defensive mechanisms and generates mitigations"""
#     defense = DefensiveMechanisms()
#     defense.generate_mitigation_report()
#     print("\n✅ Mitigation report saved as mitigation_report.json")


#     targets = [
#         "http://bwapp.hakhub.net/login.php",
#         "http://bwapp.hakhub.net/xss_get.php"
#     ]

#     for target in targets:
#         SmartPentester.scan_endpoint(target)

#     SmartPentester.generate_report()
#     print("\n✅ Scan completed. Report saved as scan_report.json")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="CLI for Smart Pentester")
#     parser.add_argument("action", choices=["scan", "view-report", "defense", "view-mitigation"], help="Choose an action")

#     args = parser.parse_args()

#     if args.command == "scan":
#         run_scan()

#     elif args.command == "defense":
#         run_defense()

#     if args.action == "view-report":
#         view_scan_report()

#     elif args.action == "view-mitigation":
#         view_mitigation_report()

# import json
# import time
# import curses
# import os

# class PentestCLI:
#     def __init__(self):
#         self.options = ["Start Scan", "View Scan Report", "View Mitigation Report", "Exit"]
#         self.selected = 0
    
#     def run_scan(self, stdscr):
#         stdscr.clear()
#         stdscr.addstr(2, 2, "🔍 Running security scan...")
#         stdscr.refresh()
#         time.sleep(2)
#         os.system("python testing.py")  # Run scanning script
#         stdscr.addstr(4, 2, "✅ Scan completed! Report saved.")
#         stdscr.addstr(6, 2, "Press any key to return to menu...")
#         stdscr.refresh()
#         stdscr.getch()
    
#     def view_report(self, stdscr, filename, title):
#         stdscr.clear()
#         stdscr.addstr(2, 2, f"📄 {title}:")
        
#         try:
#             with open(filename, "r") as f:
#                 report = json.load(f)
#                 y = 4
#                 for url, issues in report.items():
#                     stdscr.addstr(y, 2, f"🔗 {url}", curses.A_BOLD)
#                     y += 1
#                     for vuln, status in issues.items():
#                         stdscr.addstr(y, 4, f"⚠️ {vuln}: {status}")
#                         y += 1
#                     y += 1
#         except FileNotFoundError:
#             stdscr.addstr(4, 2, "❌ Report not found! Run a scan first.")
        
#         stdscr.addstr(y + 2, 2, "Press any key to return to menu...")
#         stdscr.refresh()
#         stdscr.getch()
    
#     def main_menu(self, stdscr):
#         curses.curs_set(0)
#         while True:
#             stdscr.clear()
#             stdscr.addstr(2, 2, "🔐 Penetration Testing Assistant", curses.A_BOLD)
#             for i, option in enumerate(self.options):
#                 if i == self.selected:
#                     stdscr.addstr(4 + i, 4, f"> {option} <", curses.A_REVERSE)
#                 else:
#                     stdscr.addstr(4 + i, 4, option)
            
#             key = stdscr.getch()
#             if key == curses.KEY_UP and self.selected > 0:
#                 self.selected -= 1
#             elif key == curses.KEY_DOWN and self.selected < len(self.options) - 1:
#                 self.selected += 1
#             elif key == 10:  # Enter key
#                 if self.selected == 0:
#                     self.run_scan(stdscr)
#                 elif self.selected == 1:
#                     self.view_report(stdscr, "scan_report.json", "Scan Report")
#                 elif self.selected == 2:
#                     self.view_report(stdscr, "mitigation_report.json", "Mitigation Report")
#                 elif self.selected == 3:
#                     break  # Exit CLI

# if __name__ == "__main__":
#     curses.wrapper(PentestCLI().main_menu)

import json
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import track
from testing import SmartPentester, DefensiveMechanisms

console = Console()

# Default configuration
DEFAULT_TARGETS = [
    "http://bwapp.hakhub.net/login.php",
    "http://bwapp.hakhub.net/xss_get.php"
]

def run_scan(targets=None, timeout=15, ai_enabled=True):
    """
    Run security scan on specified targets
    Args:
        targets (list): URLs to scan (uses DEFAULT_TARGETS if None)
        timeout (int): Request timeout in seconds
        ai_enabled (bool): Enable AI analysis
    """
    pentester = SmartPentester()
    pentester.llm_enabled = ai_enabled
    pentester.timeout = timeout

    targets = targets or DEFAULT_TARGETS
    
    console.print("\n🔍 [bold cyan]Starting Security Scan[/bold cyan]")
    console.print(f"📌 Targets: {', '.join(targets)}")
    console.print(f"⚙️  Settings: AI Analysis {'Enabled' if ai_enabled else 'Disabled'}, Timeout: {timeout}s\n")

    for target in track(targets, description="Scanning..."):
        pentester.scan_endpoint(target)

    pentester.generate_report()
    console.print("\n✅ [bold green]Scan completed! Report saved to scan_report.json[/bold green]")

def view_scan_report():
    """Display scan results in a formatted table"""
    try:
        with open("scan_report.json", "r") as f:
            findings = json.load(f)
    except FileNotFoundError:
        console.print("\n❌ [bold red]Error: Scan report not found! Run a scan first.[/bold red]")
        return

    table = Table(title="\n📄 Scan Report", show_header=True, header_style="bold magenta")
    table.add_column("Target", style="cyan")
    table.add_column("Vulnerability", style="green")
    table.add_column("Status", style="yellow")

    for url, vulnerabilities in findings.items():
        for vuln, status in vulnerabilities.items():
            status_icon = "✅" if "Vulnerable" in status else "❌"
            table.add_row(url, vuln, f"{status_icon} {status}")

    console.print(table)

def run_defense():
    """Generate mitigation strategies for found vulnerabilities"""
    console.print("\n🛡️  [bold cyan]Generating Defense Recommendations[/bold cyan]")
    
    defense = DefensiveMechanisms()
    defense.generate_mitigation_report()
    
    console.print("\n✅ [bold green]Mitigation report saved to mitigation_report.json[/bold green]")

def view_mitigation_report():
    """Display mitigation suggestions in a formatted view"""
    try:
        with open("mitigation_report.json", "r") as f:
            mitigations = json.load(f)
    except FileNotFoundError:
        console.print("\n❌ [bold red]Error: Mitigation report not found! Run defense first.[/bold red]")
        return

    console.print("\n🛡️  [bold cyan]Mitigation Report[/bold cyan]")
    
    for url, solutions in mitigations.items():
        console.print(f"\n🔗 [bold yellow]Target:[/bold yellow] {url}")
        for vuln, fix in solutions.items():
            console.print(f"  🔹 [bold blue]{vuln}[/bold blue]")
            console.print(f"  📝 {fix}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Smart Pentester CLI - AI-Powered Security Scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Run security scan')
    scan_parser.add_argument(
        '--targets', 
        nargs='+', 
        default=DEFAULT_TARGETS,
        help='URLs to scan (space separated)'
    )
    scan_parser.add_argument(
        '--timeout', 
        type=int, 
        default=15,
        help='Request timeout in seconds'
    )
    scan_parser.add_argument(
        '--no-ai', 
        action='store_true',
        help='Disable AI analysis (rule-based only)'
    )

    # Report command
    subparsers.add_parser('report', help='View scan report')

    # Defense command
    subparsers.add_parser('defense', help='Generate mitigation strategies')

    # Mitigation command
    subparsers.add_parser('mitigation', help='View mitigation report')

    args = parser.parse_args()

    try:
        if args.command == 'scan':
            run_scan(
                targets=args.targets,
                timeout=args.timeout,
                ai_enabled=not args.no_ai
            )
        elif args.command == 'report':
            view_scan_report()
        elif args.command == 'defense':
            run_defense()
        elif args.command == 'mitigation':
            view_mitigation_report()

    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")
        if isinstance(e, KeyboardInterrupt):
            console.print("Operation cancelled by user")

if __name__ == "__main__":
    main()
