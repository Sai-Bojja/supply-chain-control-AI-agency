from .base_agent import Agent
from .tools import send_email

def email_instructions(context_variables):
    summary = context_variables.get("summary", "No summary provided.")
    logs = context_variables.get("logs", [])
    recipient = context_variables.get("user_email", "unknown@example.com")
    
    return f"""You are an Email Reporting Agent.
Your job is to send a professional supply chain status report to the user.

1. Format a clear email body based on the 'summary' and key insights from the 'logs'.
2. Use a subject line like: "Supply Chain Alert: [Product Name] - [Status]".
3. Use the 'send_email' tool to send the report to: {recipient}.
4. Confirm to the user that the email has been sent.

Context:
- Summary: {summary}
- Recipient: {recipient}
"""

email_agent = Agent(
    name="Email Agent",
    model="gpt-4o",
    instructions=email_instructions,
    tools=[send_email]
)
