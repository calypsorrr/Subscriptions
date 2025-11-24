import re
from typing import List, Dict
from datetime import datetime, timedelta

class EmailParser:
    """
    Parser to discover subscriptions from email content.
    This is a basic implementation that can be extended with actual email API integration.
    """
    
    # Common subscription-related keywords
    SUBSCRIPTION_KEYWORDS = [
        "subscription", "renewal", "billing", "payment", "invoice",
        "recurring", "auto-renew", "membership", "premium"
    ]
    
    # Common subscription companies and their patterns
    COMPANY_PATTERNS = {
        "Netflix": [r"netflix", r"nflx"],
        "Spotify": [r"spotify"],
        "Amazon Prime": [r"amazon.*prime", r"prime.*video"],
        "Disney+": [r"disney", r"disneyplus"],
        "Hulu": [r"hulu"],
        "Apple": [r"apple.*music", r"apple.*tv", r"icloud"],
        "Microsoft": [r"microsoft.*365", r"office.*365", r"xbox"],
        "Adobe": [r"adobe", r"creative.*cloud"],
        "YouTube Premium": [r"youtube.*premium", r"youtube.*red"],
        "Dropbox": [r"dropbox"],
        "GitHub": [r"github"],
        "LinkedIn": [r"linkedin.*premium"],
        "Patreon": [r"patreon"],
        "Twitch": [r"twitch.*prime"],
    }
    
    def extract_price(self, text: str) -> tuple:
        """Extract price from text, returns (amount, currency)"""
        # Pattern for prices like $9.99, €10.00, £5.99, 9.99 USD
        price_patterns = [
            r'\$(\d+\.?\d*)',  # $9.99
            r'€(\d+\.?\d*)',   # €10.00
            r'£(\d+\.?\d*)',   # £5.99
            r'(\d+\.?\d*)\s*(USD|EUR|GBP|CAD|AUD)',  # 9.99 USD
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = float(match.group(1))
                currency = match.group(2) if len(match.groups()) > 1 else self._detect_currency(pattern)
                return amount, currency
        
        return 0.0, "USD"
    
    def _detect_currency(self, pattern: str) -> str:
        """Detect currency from pattern"""
        if '$' in pattern:
            return "USD"
        elif '€' in pattern:
            return "EUR"
        elif '£' in pattern:
            return "GBP"
        return "USD"
    
    def detect_billing_cycle(self, text: str) -> str:
        """Detect billing cycle from text"""
        text_lower = text.lower()
        if any(word in text_lower for word in ["yearly", "annual", "per year", "annually"]):
            return "yearly"
        elif any(word in text_lower for word in ["quarterly", "per quarter", "3 months"]):
            return "quarterly"
        elif any(word in text_lower for word in ["monthly", "per month"]):
            return "monthly"
        return "monthly"
    
    def parse_email_content(self, subject: str, body: str, sender: str) -> Dict:
        """Parse email to extract subscription information"""
        full_text = f"{subject} {body}".lower()
        
        # Detect company
        company = None
        for comp_name, patterns in self.COMPANY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, full_text, re.IGNORECASE):
                    company = comp_name
                    break
            if company:
                break
        
        # If no known company found, try to extract from sender
        if not company:
            # Extract domain from email
            if '@' in sender:
                domain = sender.split('@')[1].split('.')[0]
                company = domain.capitalize()
        
        # Extract price
        amount, currency = self.extract_price(f"{subject} {body}")
        
        # Detect billing cycle
        billing_cycle = self.detect_billing_cycle(f"{subject} {body}")
        
        # Calculate monthly/yearly costs
        monthly_cost = 0.0
        yearly_cost = 0.0
        
        if billing_cycle == "monthly":
            monthly_cost = amount
            yearly_cost = amount * 12
        elif billing_cycle == "yearly":
            yearly_cost = amount
            monthly_cost = amount / 12
        elif billing_cycle == "quarterly":
            monthly_cost = amount / 3
            yearly_cost = amount * 4
        
        return {
            "company": company or "Unknown",
            "email": sender,
            "monthly_cost": round(monthly_cost, 2),
            "yearly_cost": round(yearly_cost, 2),
            "currency": currency,
            "billing_cycle": billing_cycle,
            "status": "active"
        }
    
    def discover_subscriptions(self) -> List[Dict]:
        """
        Discover subscriptions from emails.
        This is a mock implementation. In production, you would:
        1. Connect to Gmail/Outlook API
        2. Search for subscription-related emails
        3. Parse each email
        4. Return discovered subscriptions
        """
        # Mock data for demonstration
        # In production, replace this with actual email API calls
        mock_emails = [
            {
                "subject": "Your Netflix subscription - $15.99/month",
                "body": "Thank you for your Netflix subscription. Your next billing date is...",
                "sender": "netflix@netflix.com"
            },
            {
                "subject": "Spotify Premium - $9.99 monthly payment",
                "body": "Your Spotify Premium subscription has been renewed.",
                "sender": "noreply@spotify.com"
            },
            {
                "subject": "Amazon Prime Membership - $139/year",
                "body": "Your Amazon Prime annual membership renewal.",
                "sender": "auto-confirm@amazon.com"
            }
        ]
        
        discovered = []
        for email in mock_emails:
            parsed = self.parse_email_content(
                email["subject"],
                email["body"],
                email["sender"]
            )
            discovered.append(parsed)
        
        return discovered
    
    def connect_gmail(self, credentials_path: str = None):
        """
        Connect to Gmail API for actual email parsing.
        This would require Google API credentials.
        """
        # TODO: Implement Gmail API integration
        pass
    
    def connect_outlook(self, credentials_path: str = None):
        """
        Connect to Outlook/Microsoft Graph API for email parsing.
        This would require Microsoft API credentials.
        """
        # TODO: Implement Outlook API integration
        pass

