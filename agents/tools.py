from duckduckgo_search import DDGS
import random

def search_web(query: str, **kwargs) -> str:
    """
    Search the web for the given query using DuckDuckGo.
    """
    print(f"  [Tool] Searching web for: '{query}'")
    try:
        results = []
        with DDGS() as ddgs:
            # Get up to 3 results
            ddgs_gen = ddgs.text(query, max_results=3)
            if ddgs_gen:
                for r in ddgs_gen:
                    results.append(f"- {r['title']}: {r['body']}")
        
        if not results:
            return "(No live results found. Simulating data for demo stability.)"
            
        return "\n".join(results)
    except Exception as e:
        return f"Search failed: {e}"

def update_forecast(sku_id: str, new_forecast: int, **kwargs) -> str:
    """
    Update the forecast for a specific SKU.
    """
    print(f"  [Tool] Updating forecast for {sku_id} to {new_forecast}")
    return f"Forecast for {sku_id} updated to {new_forecast}."

def create_po(sku_id: str, quantity: int, **kwargs) -> str:
    """
    Create a Purchase Order (PO) for a specific SKU.
    """
    print(f"  [Tool] Creating PO for {sku_id}: {quantity} units")
    return f"PO created for {sku_id} with quantity {quantity}."

def transfer_inventory(sku_id: str, source_location: str, quantity: int, **kwargs) -> str:
    """
    Transfer inventory from a source location to the current SKU's location.
    """
    print(f"  [Tool] Transferring {quantity} units of {sku_id} from {source_location}")
    return f"Transfer of {quantity} units from {source_location} initiated."

def get_market_news(product_name: str, **kwargs) -> str:
    """
    Get simulated market news if real search fails or for demo purposes.
    """
    fallback_news = [
        f"Global shortage of components impacting {product_name} production.",
        f"Unexpected demand spike for {product_name} due to viral social media trend.",
        f"Competitor recall driving customers to {product_name}.",
    ]
    news = random.choice(fallback_news)
    print(f"  [Tool] Found simulated news: {news}")
    return news

def send_email(to_email: str, subject: str, body: str, **kwargs) -> str:
    """
    Send an email using SMTP credentials from environment variables.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os
    
    sender_email = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    
    if not sender_email or not password:
        return "Error: SMTP credentials (SMTP_EMAIL, SMTP_PASSWORD) not found in .env"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"  [Tool] Email sent to {to_email}")
        return f"Email successfully sent to {to_email}."
    except Exception as e:
        print(f"  [Tool] Failed to send email: {e}")
        return f"Failed to send email: {e}"
