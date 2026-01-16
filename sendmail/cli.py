#!/usr/bin/env python3
import os
import argparse
import requests
import sys
from rich.console import Console

console = Console()

config = load_config()

API_KEY = os.getenv("SENDMAIL_API_KEY") or config.get("API_KEY")
WEBHOOK_URL = os.getenv("SENDMAIL_WEBHOOK") or config.get("WEBHOOK_URL")

if not API_KEY:
    console.print("[bold red]ERROR: API key not set[/bold red]")
    sys.exit(1)

if not WEBHOOK_URL:
    console.print("[bold red]ERROR: Webhook URL not set[/bold red]")
    sys.exit(1)



def load_config():
    path = os.path.expanduser("~/.sendmailrc")
    config = {}

    if not os.path.exists(path):
        return config

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, val = line.split("=", 1)
            config[key.strip()] = val.strip()

    return config



def send_email(to, subject, message, is_html):
    payload = {
        "email": to,
        "subject": subject,
        "message": message,
        "html": is_html   
    }

    headers = {
        "x-api-key": API_KEY
    }

    try:
        r = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        return r.json()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Send email using n8n workflow"
    )

    parser.add_argument("email")
    parser.add_argument("subject")
    parser.add_argument("message")

    
    parser.add_argument(
        "--html",
        action="store_true",
        help="Send message as HTML email"
    )

    args = parser.parse_args()

    console.print("[cyan]📨 Sending email...[/cyan]")

    result = send_email(
        args.email,
        args.subject,
        args.message,
        args.html
    )

    if result.get("status") == "success":
        console.print(f"[bold green]✅ {result['message']}[/bold green]")
    else:
        console.print(f"[bold red]❌ {result['message']}[/bold red]")

if __name__ == "__main__":
    main()

