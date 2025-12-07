from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class LogEntry:
    agent: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    level: str = "INFO"

@dataclass
class AgentState:
    sku_id: str
    product_name: str
    current_stock: int
    forecast: int
    sales_trend: int
    lead_time: int
    location: str
    on_order: int = 0 # New field
    
    # Analysis Results
    status: str = "Unknown"
    risk_type: Optional[str] = None
    new_forecast: Optional[int] = None
    root_cause: Optional[str] = None
    inventory_action: Optional[str] = None
    procurement_action: Optional[str] = None
    final_summary: Optional[str] = None
    
    # Logs
    logs: List[LogEntry] = field(default_factory=list)
    
    def add_log(self, agent: str, message: str, level: str = "INFO"):
        self.logs.append(LogEntry(agent=agent, message=message, level=level))
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sku_data": {
                "SKU_ID": self.sku_id,
                "Product_Name": self.product_name,
                "Current_Stock": self.current_stock,
                "Forecast": self.forecast,
                "Sales_Trend_Last_30_Days": self.sales_trend,
                "Supplier_Lead_Time": self.lead_time,
                "Location": self.location,
                "On_Order": self.on_order
            },
            "status": self.status,
            "risk_type": self.risk_type,
            "new_forecast": self.new_forecast,
            "root_cause": self.root_cause,
            "inventory_action": self.inventory_action,
            "procurement_action": self.procurement_action,
            "final_summary": self.final_summary,
            "logs": [f"[{log.agent}] {log.message}" for log in self.logs]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentState':
        return cls(
            sku_id=data["SKU_ID"],
            product_name=data["Product_Name"],
            current_stock=int(data["Current_Stock"]),
            forecast=int(data["Forecast"]),
            sales_trend=int(data["Sales_Trend_Last_30_Days"]),
            lead_time=int(data["Supplier_Lead_Time"]),
            location=data["Location"],
            on_order=int(data.get("On_Order", 0))
        )
