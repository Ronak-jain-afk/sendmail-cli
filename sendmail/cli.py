#!/usr/bin/env python3

import argparse
import requests
import sys
from rich.console import Console

console = Console()

WEBHOOK_URL = "http://localhost:5678/webhook/sendmail"
API_KEY = "SENDMAIL_SECRET_9xA!23"

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

