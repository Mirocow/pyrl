#!/usr/bin/env python3
"""
Pyrl Test Runner - Run examples and generate test reports.

Usage:
    python run_tests.py                     - Run all tests
    python run_tests.py --debug             - Show detailed error info
    python run_tests.py --timeout 60        - Set timeout per test
    python run_tests.py -o report.md        - Custom output path
"""
import os
import sys
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_config

# --- ANSI Color Codes (matching pyrl_cli.py style) ---
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# --- Data Structures ---

@dataclass
class TestResult:
    filename: str
    category: str
    success: bool
    execution_time: float
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    error_line: Optional[int] = None
    stderr: Optional[str] = None
    stdout: Optional[str] = None  # Добавлено для отладки

@dataclass
class TestReport:
    timestamp: str
    total_files: int
    passed: int
    failed: int
    timeout: int
    results: List[TestResult] = field(default_factory=list)
    category_stats: Dict[str, Dict[str, int]] = field(default_factory=dict)
    error_summary: Dict[str, List[str]] = field(default_factory=dict)

# --- Helper Functions (matching pyrl_cli.py style) ---

def format_error_type(error_type: str) -> str:
    """Format error type with spaces (e.g., 'PyrlRuntimeError' -> 'PYRL RUNTIME ERROR')."""
    formatted = re.sub(r'(?<!^)(?=[A-Z])', ' ', error_type)
    return formatted.upper()

def print_debug_error(error_type: str, error: Exception, stderr: Optional[str] = None, stdout: Optional[str] = None, debug: bool = False) -> None:
    """Print detailed debug information for ANY error (matching pyrl_cli.py style)."""
    if debug:
        import traceback
        print(f"\n{Colors.RED}{'='*60}{Colors.RESET}", file=sys.stderr)
        print(f"{Colors.RED}{format_error_type(error_type)}{Colors.RESET}", file=sys.stderr)
        print(f"{Colors.RED}{'='*60}{Colors.RESET}", file=sys.stderr)
        print(f"{Colors.YELLOW}Message:{Colors.RESET} {error}", file=sys.stderr)
        print(f"{Colors.YELLOW}Type:{Colors.RESET} {type(error).__name__}", file=sys.stderr)
        if hasattr(error, '__traceback__') and error.__traceback__:
            print(f"{Colors.YELLOW}Traceback:{Colors.RESET}", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        if stderr:
            print(f"{Colors.YELLOW}Stderr:{Colors.RESET}", file=sys.stderr)
            for line in stderr.split('\n')[:30]:
                print(f"  {Colors.GRAY}{line}{Colors.RESET}", file=sys.stderr)
        if stdout:
            print(f"{Colors.YELLOW}Stdout:{Colors.RESET}", file=sys.stderr)
            for line in stdout.split('\n')[:10]:
                print(f"  {Colors.GRAY}{line}{Colors.RESET}", file=sys.stderr)
        print(f"{Colors.RED}{'='*60}{Colors.RESET}\n", file=sys.stderr)

# --- Runner Class ---

class PyrlTestRunner:
    def __init__(self, examples_dir: Path, cli_path: Path, timeout: int = 30, debug: bool = False):
        self.examples_dir = examples_dir
        self.cli_path = cli_path
        self.timeout = timeout
        self.debug = debug
        self.results: List[TestResult] = []

    def run_file(self, filepath: Path) -> TestResult:
        """Execute a single .pyrl file and capture results."""
        start_time = datetime.now()
        category = filepath.parent.name if filepath.parent != self.examples_dir else "root"
        filename = filepath.name

        try:
            cmd = ['python', str(self.cli_path), str(filepath)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=str(self.cli_path.parent)
            )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            if result.returncode == 0:
                return TestResult(
                    filename=filename,
                    category=category,
                    success=True,
                    execution_time=duration,
                    stdout=result.stdout,
                    stderr=result.stderr
                )
            else:
                return TestResult(
                    filename=filename,
                    category=category,
                    success=False,
                    execution_time=duration,
                    error_type="PyrlRuntimeError",
                    error_message=result.stderr.strip().split('\n')[-1] if result.stderr else "Unknown error",
                    stderr=result.stderr,
                    stdout=result.stdout
                )

        except subprocess.TimeoutExpired as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            return TestResult(
                filename=filename,
                category=category,
                success=False,
                execution_time=duration,
                error_type="TimeoutError",
                error_message=f"Execution exceeded {self.timeout}s",
                stderr=e.stderr if isinstance(e.stderr, str) else str(e.stderr) if e.stderr else None,
                stdout=e.stdout if isinstance(e.stdout, str) else str(e.stdout) if e.stdout else None
            )
        except FileNotFoundError as e:
            # Частая ошибка: python или pyrl_cli.py не найдены
            return TestResult(
                filename=filename,
                category=category,
                success=False,
                execution_time=0,
                error_type="FileNotFoundError",
                error_message=str(e),
                stderr=str(e)
            )
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            return TestResult(
                filename=filename,
                category=category,
                success=False,
                execution_time=duration,
                error_type=type(e).__name__,
                error_message=str(e),
                stderr=str(e)
            )

    def run_all(self) -> None:
        """Run all tests in the examples directory."""
        pyrl_files = sorted(self.examples_dir.glob("*.pyrl"))

        if not pyrl_files:
            print(f"{Colors.RED}No .pyrl files found{Colors.RESET}")
            return

        print(f"Found {Colors.CYAN}{len(pyrl_files)}{Colors.RESET} Pyrl files to run\n")

        for i, filepath in enumerate(pyrl_files, 1):
            print(f"[{i}/{len(pyrl_files)}] Running {Colors.BLUE}{filepath.name}{Colors.RESET}...", end=" ", flush=True)

            result = self.run_file(filepath)
            self.results.append(result)

            # Вывод статуса с цветами
            if result.success:
                print(f"{Colors.GREEN}✅ PASS{Colors.RESET} ({result.execution_time:.2f}s)", flush=True)
            else:
                print(f"{Colors.RED}❌ FAIL{Colors.RESET} ({result.execution_time:.2f}s)", flush=True)

                # В режиме отладки показываем полную информацию
                if self.debug:
                    print_debug_error(
                        result.error_type or "UnknownError",
                        Exception(result.error_message or "No message"),
                        stderr=result.stderr,
                        stdout=result.stdout,
                        debug=True
                    )
                else:
                    # В обычном режиме — краткая информация в стиле pyrl_cli
                    error_formatted = format_error_type(result.error_type or "Error")
                    print(f"   {Colors.RED}└─ {error_formatted}{Colors.RESET}: {result.error_message}", file=sys.stderr)

        print(f"\n{Colors.GRAY}All tests completed.{Colors.RESET}")

    def generate_report(self) -> TestReport:
        """Aggregate results into a report object."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        timeout = sum(1 for r in self.results if r.error_type == "TimeoutError")

        category_stats: Dict[str, Dict[str, int]] = {}
        for r in self.results:
            if r.category not in category_stats:
                category_stats[r.category] = {"total": 0, "passed": 0, "failed": 0}
            category_stats[r.category]["total"] += 1
            if r.success:
                category_stats[r.category]["passed"] += 1
            else:
                category_stats[r.category]["failed"] += 1

        error_summary: Dict[str, List[str]] = {}
        for r in self.results:
            if not r.success and r.error_type:
                if r.error_type not in error_summary:
                    error_summary[r.error_type] = []
                error_summary[r.error_type].append(r.filename)

        return TestReport(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_files=total,
            passed=passed,
            failed=failed,
            timeout=timeout,
            results=self.results,
            category_stats=category_stats,
            error_summary=error_summary
        )

    def save_markdown_report(self, output_path: Path):
        """Save report as Markdown file."""
        report = self.generate_report()
        report_dict = asdict(report)

        lines = [
            "# Pyrl Examples Test Report",
            "",
            f"**Generated:** {report.timestamp}",
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Total | {report.total_files} |",
            f"| Passed | {report.passed} |",
            f"| Failed | {report.failed} |",
            f"| Timeout | {report.timeout} |",
        ]

        if report.total_files > 0:
            rate = report.passed / report.total_files * 100
            lines.append(f"| Success Rate | {rate:.1f}% |")
        else:
            lines.append("| Success Rate | 0.0% |")

        lines.extend([
            "",
            "## Category Breakdown",
            "",
            "| Category | Total | Passed | Failed | Rate |",
            "|----------|-------|--------|--------|------|",
        ])

        for cat, stats in sorted(report_dict['category_stats'].items()):
            rate = stats["passed"] / stats["total"] * 100 if stats["total"] > 0 else 0
            lines.append(f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} | {rate:.1f}% |")

        # Failed examples
        failed_results = [r for r in report_dict['results'] if not r['success']]
        if failed_results:
            lines.extend([
                "",
                "## Failed Examples",
                "",
            ])

            for r in failed_results:
                error_formatted = format_error_type(r.get('error_type', 'Error'))
                lines.extend([
                    f"### {r['filename']}",
                    "",
                    f"- **Category:** {r['category']}",
                    f"- **Error Type:** {error_formatted}",
                    f"- **Error Message:** {r.get('error_message', 'N/A')}",
                    f"- **Line:** {r.get('error_line', 'N/A')}",
                    f"- **Execution Time:** {r['execution_time']:.2f}s",
                ])

                if r.get('stderr'):
                    stderr_content = r['stderr'][:500] + ("..." if len(r['stderr']) > 500 else "")
                    lines.extend([
                        "",
                        "**Stderr:**",
                        "```text",
                        stderr_content,
                        "```",
                    ])

                lines.append("")

        # Error summary
        if report_dict['error_summary']:
            lines.extend([
                "",
                "## Error Types",
                "",
            ])

            for error_type, files in sorted(report_dict['error_summary'].items(), key=lambda x: -len(x[1])):
                error_formatted = format_error_type(error_type)
                lines.append(f"### {error_formatted} ({len(files)} occurrences)")
                lines.append("")
                for f in files:
                    lines.append(f"- {f}")
                lines.append("")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"\n{Colors.CYAN}📄 Markdown report saved to:{Colors.RESET} {output_path}")

# --- Main Entry Point ---

def main():
    parser = argparse.ArgumentParser(
        description='Pyrl Test Runner - Run examples and generate reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                     Run all tests
    python run_tests.py --debug             Show detailed error info
    python run_tests.py --timeout 60        Set 60s timeout per test
    python run_tests.py -o report.md        Save report to custom path
    python run_tests.py --cli ./pyrl_cli.py Use custom CLI path
"""
    )
    parser.add_argument("--output", "-o", type=str, default="test_report.md", help="Path to save the Markdown report")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Timeout per test in seconds")
    parser.add_argument("--cli", type=str, default=None, help="Path to pyrl_cli.py (auto-detected if not specified)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode (show full traceback)")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")
    args = parser.parse_args()

    config = get_config()
    examples_dir = config.examples_dir

    # Auto-detect pyrl_cli.py location
    if args.cli:
        cli_path = Path(args.cli)
    else:
        project_root = Path(__file__).parent.parent
        cli_path = project_root / "pyrl_cli.py"

        if not cli_path.exists():
            cli_path = Path(__file__).parent / "pyrl_cli.py"

    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}Pyrl Examples Run Test{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print()
    print(f"Examples directory: {Colors.BLUE}{examples_dir}{Colors.RESET}")
    print(f"CLI path: {Colors.BLUE}{cli_path}{Colors.RESET}")
    print(f"Debug mode: {Colors.GREEN}ON{Colors.RESET}" if args.debug else f"Debug mode: {Colors.GRAY}OFF{Colors.RESET}")
    print()

    if not examples_dir.exists():
        print(f"{Colors.RED}Error: Directory {examples_dir} not found{Colors.RESET}", file=sys.stderr)
        return 1

    if not cli_path.exists():
        print(f"{Colors.RED}Error: CLI file {cli_path} not found{Colors.RESET}", file=sys.stderr)
        print(f"{Colors.GRAY}Use --cli to specify the path to pyrl_cli.py{Colors.RESET}", file=sys.stderr)
        return 1

    # Проверка: можем ли мы запустить CLI вручную?
    if args.debug:
        print(f"{Colors.GRAY}Testing CLI execution...{Colors.RESET}", file=sys.stderr)
        test_cmd = [sys.executable, str(cli_path.resolve()), "--help"]
        try:
            test_run = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            if test_run.returncode == 0:
                print(f"{Colors.GREEN}✓ CLI is executable{Colors.RESET}", file=sys.stderr)
            else:
                print(f"{Colors.YELLOW}⚠ CLI returned non-zero: {test_run.returncode}{Colors.RESET}", file=sys.stderr)
                print(f"{Colors.GRAY}Stderr: {test_run.stderr[:200]}{Colors.RESET}", file=sys.stderr)
        except Exception as e:
            print(f"{Colors.RED}✗ Failed to test CLI: {e}{Colors.RESET}", file=sys.stderr)
        print()
    runner = PyrlTestRunner(examples_dir, cli_path, timeout=args.timeout, debug=args.debug)

    if args.dry_run:
        print(f"{Colors.GRAY}Dry run - would execute:{Colors.RESET}")
        for filepath in sorted(examples_dir.glob("*.pyrl"))[:3]:
            cmd = [sys.executable, str(cli_path.resolve()), str(filepath.resolve())]
            print(f"  {' '.join(cmd)}")
        return 0
    # Run all tests
    runner.run_all()

    # Generate and save report
    output_path = Path(args.output)
    runner.save_markdown_report(output_path)

    # Return exit code based on test results
    report = runner.generate_report()
    if report.failed > 0:
        print(f"\n{Colors.YELLOW}⚠️  {report.failed} test(s) failed{Colors.RESET}")
        # Подсказка: запустите с --debug для деталей
        if not args.debug:
            print(f"{Colors.GRAY}Tip: Run with --debug to see detailed error information{Colors.RESET}")
        return 1
    else:
        print(f"\n{Colors.GREEN}✅ All {report.passed} test(s) passed{Colors.RESET}")
        return 0

if __name__ == '__main__':
    sys.exit(main())