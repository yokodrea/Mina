
import json
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt, IntPrompt, Confirm
from testing import SmartPentester, DefensiveMechanisms

console = Console()

# Default configuration
DEFAULT_TARGETS = [
    "http://bwapp.hakhub.net/login.php",
    "http://bwapp.hakhub.net/xss_get.php"
]

def show_banner():
    console.print("\n[bold blue]▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄[/bold blue]")
    console.print("[bold blue]█[/bold blue] [bold white]SMART PENTESTER CLI - AI SECURITY SCANNER[/bold white] [bold blue]█[/bold blue]")
    console.print("[bold blue]▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀[/bold blue]\n")

def show_menu():
    console.print("[bold]Main Menu:[/bold]")
    console.print("1. 🚀 Run Security Scan")
    console.print("2. 🛡️ Generate Defense Strategies")
    console.print("3. 📊 View Scan Report")
    console.print("4. 📝 View Mitigation Report")
    console.print("5. 🚪 Exit\n")

def run_interactive_scan():
    """Interactive scan configuration"""
    console.print("\n[bold cyan]⚙️ Scan Configuration[/bold cyan]")
    
    # Target selection
    targets = Prompt.ask(
        "[bold]Enter target URLs[/bold] (space separated, blank for defaults)",
        default=" ".join(DEFAULT_TARGETS))
    targets = targets.split()
    
    # Timeout setting
    timeout = IntPrompt.ask(
        "[bold]Enter timeout (seconds)[/bold]",
        default=15)
    
    # AI toggle
    use_ai = Confirm.ask(
        "[bold]Enable AI analysis?[/bold]",
        default=True)
    
    run_scan(targets=targets, timeout=timeout, ai_enabled=use_ai)

def run_scan(targets=None, timeout=15, ai_enabled=True):
    """Run security scan with progress tracking"""
    pentester = SmartPentester()
    pentester.llm_enabled = ai_enabled
    pentester.timeout = timeout

    targets = targets or DEFAULT_TARGETS
    
    console.print("\n🔍 [bold cyan]Starting Security Scan[/bold cyan]")
    console.print(f"📌 Targets: {', '.join(targets)}")
    console.print(f"⚙️ Settings: AI Analysis {'[green]Enabled[/green]' if ai_enabled else '[red]Disabled[/red]'}, Timeout: {timeout}s\n")

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
    table.add_column("Target", style="cyan", no_wrap=True)
    table.add_column("Vulnerability", style="green")
    table.add_column("Status", style="yellow")

    for url, vulnerabilities in findings.items():
        for vuln, status in vulnerabilities.items():
            status_icon = "✅" if "Vulnerable" in status else "❌"
            status_color = "green" if "Vulnerable" in status else "red"
            table.add_row(url, vuln, f"[{status_color}]{status_icon} {status}[/{status_color}]")

    console.print(table)
    console.print("\nPress Enter to continue...", end="")
    input()

def run_defense():
    """Generate mitigation strategies with confirmation"""
    if Confirm.ask("\n🛡️ [bold]Generate defense recommendations?[/bold]", default=True):
        defense = DefensiveMechanisms()
        defense.generate_mitigation_report()
        console.print("\n✅ [bold green]Mitigation report saved to mitigation_report.json[/bold green]")
    else:
        console.print("\n🚫 [yellow]Operation cancelled[/yellow]")

def view_mitigation_report():
    """Display mitigation suggestions with pagination"""
    try:
        with open("mitigation_report.json", "r") as f:
            mitigations = json.load(f)
    except FileNotFoundError:
        console.print("\n❌ [bold red]Error: Mitigation report not found! Run defense first.[/bold red]")
        return

    console.print("\n🛡️ [bold cyan]Mitigation Report[/bold cyan]")
    
    for url, solutions in mitigations.items():
        console.print(f"\n🔗 [bold yellow]Target:[/bold yellow] {url}")
        for vuln, fix in solutions.items():
            console.print(f"  🔹 [bold blue]{vuln}[/bold blue]")
            console.print(f"  📝 {fix}\n")
    
    console.print("\nPress Enter to continue...", end="")
    input()

def interactive_mode():
    """Run the interactive menu system"""
    while True:
        show_banner()
        show_menu()
        
        choice = Prompt.ask(
            "[bold]Select an option[/bold] (1-5)",
            choices=["1", "2", "3", "4", "5"],
            show_choices=False)
        
        if choice == "1":
            run_interactive_scan()
        elif choice == "2":
            run_defense()
        elif choice == "3":
            view_scan_report()
        elif choice == "4":
            view_mitigation_report()
        elif choice == "5":
            console.print("\n👋 [bold green]Goodbye![/bold green]")
            break

def cli_mode():
    """Run in traditional CLI mode"""
    parser = argparse.ArgumentParser(
        description="Smart Pentester CLI - AI-Powered Security Scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Run security scan')
    scan_parser.add_argument('--targets', nargs='+', default=DEFAULT_TARGETS, help='URLs to scan')
    scan_parser.add_argument('--timeout', type=int, default=15, help='Request timeout in seconds')
    scan_parser.add_argument('--no-ai', action='store_true', help='Disable AI analysis')

    # Report commands
    subparsers.add_parser('report', help='View scan report')
    subparsers.add_parser('defense', help='Generate mitigation strategies')
    subparsers.add_parser('mitigation', help='View mitigation report')

    args = parser.parse_args()

    try:
        if args.command == 'scan':
            run_scan(targets=args.targets, timeout=args.timeout, ai_enabled=not args.no_ai)
        elif args.command == 'report':
            view_scan_report()
        elif args.command == 'defense':
            run_defense()
        elif args.command == 'mitigation':
            view_mitigation_report()

    except Exception as e:
        console.print(f"\n❌ [bold red]Error: {str(e)}[/bold red]")

if __name__ == "__main__":
    # Detect if running without arguments (interactive mode)
    import sys
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        cli_mode()