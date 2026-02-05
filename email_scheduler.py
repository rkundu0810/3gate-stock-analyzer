"""
Daily Stock Analysis Scheduler with Email Notifications
Runs at 9:30 AM IST daily and sends analysis report via email

Based on Zerodha Varsity Technical Analysis Framework
"""

import schedule
import time
from datetime import datetime
import subprocess
import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'scheduler.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from stock_analyzer import ZerodhaAnalyzer


class EmailConfig:
    """Email configuration handler"""

    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "email_config.json")
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Load email configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self, config: dict):
        """Save email configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        required = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password', 'recipient_email']
        return all(self.config.get(k) and self.config.get(k) != f"your_{k.split('_')[-1]}" for k in required[:4])


class EmailSender:
    """Email sender using SMTP"""

    def __init__(self, config: EmailConfig):
        self.config = config.config

    def format_html_report(self, text_report: str, summary_data: list) -> str:
        """Convert text report to HTML email format"""

        # Extract BUY recommendations
        buy_stocks = [s for s in summary_data if s.get('verdict') == 'BUY']
        wait_stocks = [s for s in summary_data if s.get('verdict') == 'WAIT']
        skip_stocks = [s for s in summary_data if s.get('verdict') == 'SKIP']

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a237e; border-bottom: 3px solid #3f51b5; padding-bottom: 10px; }}
        h2 {{ color: #303f9f; margin-top: 30px; }}
        .summary-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .summary-table th {{ background: #3f51b5; color: white; padding: 12px; text-align: left; }}
        .summary-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .summary-table tr:hover {{ background: #f5f5f5; }}
        .buy {{ color: #2e7d32; font-weight: bold; }}
        .wait {{ color: #f57c00; font-weight: bold; }}
        .skip {{ color: #c62828; font-weight: bold; }}
        .recommendation-box {{ padding: 15px; border-radius: 8px; margin: 15px 0; }}
        .buy-box {{ background: #e8f5e9; border-left: 4px solid #2e7d32; }}
        .wait-box {{ background: #fff3e0; border-left: 4px solid #f57c00; }}
        .checklist {{ background: #fafafa; padding: 15px; border-radius: 5px; font-family: monospace; }}
        .pass {{ color: #2e7d32; }}
        .fail {{ color: #c62828; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
        .highlight {{ background: #fff9c4; padding: 2px 5px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Daily Stock Analysis Report</h1>
        <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        <p><strong>Framework:</strong> Zerodha Varsity Technical Analysis</p>

        <h2>Quick Summary</h2>
        <table class="summary-table">
            <tr>
                <th>Symbol</th>
                <th>Price</th>
                <th>RSI</th>
                <th>Score</th>
                <th>Verdict</th>
                <th>Confidence</th>
            </tr>
"""

        for stock in summary_data:
            verdict_class = stock.get('verdict', 'skip').lower()
            html += f"""
            <tr>
                <td><strong>{stock.get('symbol', 'N/A')}</strong></td>
                <td>{stock.get('price', 'N/A')}</td>
                <td>{stock.get('rsi', 'N/A')}</td>
                <td>{stock.get('score', 'N/A')}</td>
                <td class="{verdict_class}">{stock.get('verdict', 'N/A')}</td>
                <td>{stock.get('confidence', 'N/A')}</td>
            </tr>
"""

        html += """
        </table>
"""

        # BUY Recommendations
        if buy_stocks:
            html += """
        <h2>BUY Recommendations</h2>
"""
            for stock in buy_stocks:
                html += f"""
        <div class="recommendation-box buy-box">
            <strong class="buy">{stock.get('symbol')}</strong> @ {stock.get('price')}
            <br>Confidence: {stock.get('confidence')} | Checklist Score: {stock.get('score')}
        </div>
"""

        # WAIT Watchlist
        if wait_stocks:
            html += """
        <h2>Watchlist (WAIT)</h2>
"""
            for stock in wait_stocks:
                html += f"""
        <div class="recommendation-box wait-box">
            <strong class="wait">{stock.get('symbol')}</strong> @ {stock.get('price')}
            <br>Score: {stock.get('score')} - Monitor for entry opportunity
        </div>
"""

        # Key Principles Reminder
        html += """
        <h2>7-Point Zerodha Checklist</h2>
        <div class="checklist">
            <ol>
                <li>Recognizable candlestick pattern identified</li>
                <li>Prior trend supports the pattern</li>
                <li>S&R within 4% of stoploss</li>
                <li>Volume ≥ 10-day average</li>
                <li>Risk-Reward Ratio ≥ 1.5:1</li>
                <li>RSI/MACD indicator confirmation</li>
                <li>Dow Theory trend alignment</li>
            </ol>
        </div>

        <h2>Key Principles</h2>
        <ul>
            <li><span class="highlight">Buy strength, sell weakness</span></li>
            <li><span class="highlight">Prior trend must exist for pattern validity</span></li>
            <li><span class="highlight">S&R must be within 4% of stoploss</span></li>
            <li><span class="highlight">Volume must confirm the move</span></li>
            <li><span class="highlight">Minimum RRR of 1.5:1</span></li>
            <li><span class="highlight">Deciding not to trade is itself a trading decision</span></li>
        </ul>

        <div class="footer">
            <p>This report is generated automatically based on Zerodha Varsity Technical Analysis Framework.</p>
            <p>Always perform your own due diligence before making trading decisions.</p>
            <p><em>Generated by Stock Analysis Scheduler</em></p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def send_email(self, subject: str, text_body: str, html_body: str = None, attachment_path: str = None) -> bool:
        """Send email with report"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            msg['Subject'] = f"{self.config.get('email_subject_prefix', '')} {subject}"

            # Attach text version
            msg.attach(MIMEText(text_body, 'plain'))

            # Attach HTML version if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))

            # Attach file if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                msg.attach(part)

            # Connect and send
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            if self.config.get('use_tls', True):
                server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully to {self.config['recipient_email']}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


def get_stocks_from_file() -> list:
    """Read stock list from watchlist file. Strips inline comments after #."""
    watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")
    if os.path.exists(watchlist_path):
        stocks = []
        with open(watchlist_path, 'r') as f:
            for line in f:
                line = line.split('#')[0].strip()  # Strip inline comments
                if line:
                    stocks.append(line)
        return stocks
    return []


def run_daily_analysis_with_email():
    """Run the daily analysis and send email report"""
    logger.info("=" * 60)
    logger.info(f"DAILY STOCK ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # Get stocks from watchlist
    stocks = get_stocks_from_file()

    if not stocks:
        logger.warning("No stocks in watchlist. Skipping analysis.")
        return

    logger.info(f"Analyzing {len(stocks)} stocks: {', '.join(stocks[:5])}{'...' if len(stocks) > 5 else ''}")

    # Run analysis
    analyzer = ZerodhaAnalyzer()

    # Collect summary data for email formatting
    summary_data = []
    all_reports = []

    for symbol in stocks:
        analysis = analyzer.analyze_stock(symbol.strip())
        if analysis:
            report = analyzer.format_report(analysis)
            all_reports.append(report)
            summary_data.append({
                'symbol': analysis['symbol'],
                'price': analysis['moving_averages']['current_price'],
                'rsi': analysis['rsi'],
                'verdict': analysis['verdict']['verdict'],
                'confidence': analysis['verdict']['confidence'],
                'score': f"{analysis['checklist_result']['score']}/7"
            })

    if not summary_data:
        logger.warning("No analysis results generated.")
        return

    # Generate text report
    text_report = analyzer.run_analysis(stocks)

    # Send email
    email_config = EmailConfig()

    if email_config.is_configured():
        sender = EmailSender(email_config)

        # Create HTML report
        html_report = sender.format_html_report(text_report, summary_data)

        # Get report file path
        report_filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        report_path = os.path.join(analyzer.results_dir, report_filename)

        # Count recommendations
        buy_count = len([s for s in summary_data if s['verdict'] == 'BUY'])
        wait_count = len([s for s in summary_data if s['verdict'] == 'WAIT'])

        subject = f"Daily Report - {buy_count} BUY, {wait_count} WAIT - {datetime.now().strftime('%d %b %Y')}"

        success = sender.send_email(
            subject=subject,
            text_body=text_report,
            html_body=html_report,
            attachment_path=report_path
        )

        if success:
            logger.info("Email report sent successfully!")
        else:
            logger.error("Failed to send email report.")
    else:
        logger.warning("Email not configured. Report saved to file only.")
        logger.info(f"Configure email in: {email_config.config_path}")

    # Windows notification
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        buy_count = len([s for s in summary_data if s['verdict'] == 'BUY'])
        toaster.show_toast(
            "Stock Analysis Complete",
            f"{len(stocks)} stocks analyzed. {buy_count} BUY signals.",
            duration=10
        )
    except ImportError:
        pass

    logger.info("Analysis complete!")
    return text_report


def run_scheduler():
    """Run the scheduler - analysis at 9:30 AM daily"""
    logger.info("=" * 60)
    logger.info(" STOCK ANALYSIS SCHEDULER - EMAIL ENABLED")
    logger.info("=" * 60)
    logger.info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    logger.info("Analysis scheduled for 9:30 AM daily")
    logger.info("Press Ctrl+C to stop\n")

    # Schedule daily at 9:30 AM
    schedule.every().day.at("09:30").do(run_daily_analysis_with_email)

    # Optional: Additional market timing alerts
    schedule.every().day.at("09:15").do(lambda: logger.info("Indian market opened!"))
    schedule.every().day.at("19:00").do(lambda: logger.info("US pre-market starting!"))

    while True:
        schedule.run_pending()
        time.sleep(60)


def setup_email():
    """Interactive email setup"""
    print("\n" + "=" * 60)
    print(" EMAIL CONFIGURATION")
    print("=" * 60)

    config = EmailConfig()

    print("\nCurrent configuration:")
    if config.config:
        for key, value in config.config.items():
            if 'password' in key.lower():
                print(f"  {key}: {'*' * 8}")
            else:
                print(f"  {key}: {value}")
    else:
        print("  No configuration found.")

    print("\nEmail Setup Options:")
    print("  1. Gmail (recommended)")
    print("  2. Outlook/Hotmail")
    print("  3. Custom SMTP")
    print("  4. Skip email setup")

    choice = input("\nSelect option (1-4): ").strip()

    if choice == '4':
        print("Skipping email setup.")
        return

    new_config = {}

    if choice == '1':
        new_config['smtp_server'] = 'smtp.gmail.com'
        new_config['smtp_port'] = 587
        print("\nFor Gmail, you need an App Password:")
        print("  1. Go to Google Account > Security")
        print("  2. Enable 2-Factor Authentication")
        print("  3. Generate App Password for 'Mail'")
        print("  4. Use that 16-character password below")
    elif choice == '2':
        new_config['smtp_server'] = 'smtp.office365.com'
        new_config['smtp_port'] = 587
    else:
        new_config['smtp_server'] = input("SMTP Server: ").strip()
        new_config['smtp_port'] = int(input("SMTP Port (587): ").strip() or "587")

    new_config['sender_email'] = input("\nYour email address: ").strip()
    new_config['sender_password'] = input("App password: ").strip()
    new_config['recipient_email'] = input("Recipient email (press Enter for same): ").strip()

    if not new_config['recipient_email']:
        new_config['recipient_email'] = new_config['sender_email']

    new_config['use_tls'] = True
    new_config['email_subject_prefix'] = "[Stock Analysis]"

    # Test connection
    print("\nTesting email connection...")
    try:
        server = smtplib.SMTP(new_config['smtp_server'], new_config['smtp_port'])
        server.starttls()
        server.login(new_config['sender_email'], new_config['sender_password'])
        server.quit()
        print("Connection successful!")

        # Send test email
        send_test = input("Send test email? (y/n): ").strip().lower()
        if send_test == 'y':
            config.save_config(new_config)
            sender = EmailSender(config)
            sender.send_email(
                subject="Test - Stock Analysis Scheduler",
                text_body="This is a test email from Stock Analysis Scheduler.\n\nIf you received this, your email configuration is working correctly!",
                html_body="<h2>Test Email</h2><p>This is a test email from Stock Analysis Scheduler.</p><p>If you received this, your email configuration is working correctly!</p>"
            )
            print("Test email sent!")
        else:
            config.save_config(new_config)

        print("\nEmail configuration saved!")

    except Exception as e:
        print(f"\nConnection failed: {e}")
        save_anyway = input("Save configuration anyway? (y/n): ").strip().lower()
        if save_anyway == 'y':
            config.save_config(new_config)


def setup_windows_task():
    """Setup Windows Task Scheduler for 9:30 AM daily"""
    print("\n" + "=" * 60)
    print(" WINDOWS TASK SCHEDULER SETUP")
    print("=" * 60)

    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    working_dir = os.path.dirname(script_path)

    # Create batch file
    batch_path = os.path.join(working_dir, "run_email_analysis.bat")
    batch_content = f'''@echo off
cd /d "{working_dir}"
"{python_path}" "{script_path}" --run-now
'''

    with open(batch_path, 'w') as f:
        f.write(batch_content)

    print(f"\nCreated batch file: {batch_path}")

    # PowerShell command
    print("\nTo create scheduled task, run PowerShell as Administrator:")
    print("-" * 60)
    print(f'''
$action = New-ScheduledTaskAction -Execute "{batch_path}"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:30AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "DailyStockAnalysisEmail" -Action $action -Trigger $trigger -Settings $settings -Description "Daily stock analysis at 9:30 AM with email report"
''')
    print("-" * 60)

    # schtasks command
    print("\nOr use this CMD command (as Administrator):")
    cmd = f'schtasks /create /tn "DailyStockAnalysisEmail" /tr "{batch_path}" /sc daily /st 09:30 /f'
    print(f"\n{cmd}")

    create_now = input("\nCreate task now? (y/n): ").strip().lower()
    if create_now == 'y':
        try:
            result = subprocess.run(
                ['schtasks', '/create', '/tn', 'DailyStockAnalysisEmail',
                 '/tr', batch_path, '/sc', 'daily', '/st', '09:30', '/f'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("\nTask created successfully!")
                print("Analysis with email will run daily at 9:30 AM")
            else:
                print(f"\nFailed: {result.stderr}")
                print("Try running as Administrator")
        except Exception as e:
            print(f"\nError: {e}")
            print("Please run the command manually as Administrator")


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print(" STOCK ANALYSIS SCHEDULER - EMAIL EDITION")
    print(" Zerodha Varsity Technical Analysis Framework")
    print("=" * 60)

    print("\nOptions:")
    print("  1. Run analysis NOW (with email)")
    print("  2. Start background scheduler (9:30 AM daily)")
    print("  3. Setup Windows Task Scheduler")
    print("  4. Configure email settings")
    print("  5. Edit watchlist")
    print("  6. Test email")
    print("  7. Quit")

    choice = input("\nEnter choice (1-7): ").strip()

    if choice == '1':
        run_daily_analysis_with_email()

    elif choice == '2':
        run_scheduler()

    elif choice == '3':
        setup_windows_task()

    elif choice == '4':
        setup_email()

    elif choice == '5':
        edit_watchlist()

    elif choice == '6':
        test_email()

    elif choice == '7':
        print("Goodbye!")
        sys.exit(0)

    else:
        print("Invalid choice")


def edit_watchlist():
    """Edit the watchlist file"""
    watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")

    print("\n" + "=" * 60)
    print(" WATCHLIST EDITOR")
    print("=" * 60)

    if os.path.exists(watchlist_path):
        with open(watchlist_path, 'r') as f:
            current = f.read()
        print("\nCurrent watchlist:")
        print(current)

    stocks = get_stocks_from_file()

    print("\nOptions: add SYMBOL | remove SYMBOL | clear | list | done")

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd == 'done':
            break
        elif cmd.startswith('add '):
            symbol = cmd[4:].strip().upper()
            if symbol and symbol not in stocks:
                stocks.append(symbol)
                print(f"Added {symbol}")
        elif cmd.startswith('remove '):
            symbol = cmd[7:].strip().upper()
            if symbol in stocks:
                stocks.remove(symbol)
                print(f"Removed {symbol}")
        elif cmd == 'clear':
            stocks = []
            print("Cleared watchlist")
        elif cmd == 'list':
            print(f"Current: {', '.join(stocks)}")

    with open(watchlist_path, 'w') as f:
        f.write("# Stock Watchlist - One symbol per line\n")
        f.write("# Examples: RELIANCE.NS, TCS.NS, AAPL, MSFT\n\n")
        for s in stocks:
            f.write(f"{s}\n")

    print(f"\nSaved {len(stocks)} stocks to watchlist")


def test_email():
    """Send a test email"""
    print("\n" + "=" * 60)
    print(" TEST EMAIL")
    print("=" * 60)

    config = EmailConfig()

    if not config.is_configured():
        print("\nEmail not configured. Run option 4 first to setup email.")
        return

    print("\nSending test email...")
    sender = EmailSender(config)

    success = sender.send_email(
        subject=f"Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        text_body="This is a test email from Stock Analysis Scheduler.\n\nIf you received this, your configuration is working!",
        html_body="""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #1a237e;">Test Email</h2>
            <p>This is a test email from <strong>Stock Analysis Scheduler</strong>.</p>
            <p style="color: #2e7d32;">If you received this, your email configuration is working correctly!</p>
            <hr>
            <p style="color: #666; font-size: 12px;">Zerodha Varsity Technical Analysis Framework</p>
        </body>
        </html>
        """
    )

    if success:
        print("Test email sent successfully!")
    else:
        print("Failed to send test email. Check your configuration.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--run-now':
            run_daily_analysis_with_email()
        elif sys.argv[1] == '--scheduler':
            run_scheduler()
    else:
        main()
