import networkx as nx
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.access_log import AccessLog
from app.models.beneficiary import Beneficiary
from app.models.permission import Permission


class GraphEngine:
    def __init__(self, db: Session):
        self.db = db
        self.graph = nx.DiGraph()

    def build_full_graph(self):
        self.graph.clear()

        # Add transactions as edges between accounts
        transactions = self.db.query(Transaction).all()
        for tx in transactions:
            self.graph.add_edge(
                tx.source_account_id,
                tx.destination_account_id,
                type="TRANSFER",
                transaction_id=tx.id,
                amount=tx.amount,
                timestamp=tx.timestamp.isoformat()
            )

        # Add employee access edges
        access_logs = self.db.query(AccessLog).all()
        for log in access_logs:
            if log.customer_id:
                self.graph.add_edge(log.employee_id, log.customer_id, type="ACCESSED",
                                    timestamp=log.timestamp.isoformat())
            if log.account_id:
                self.graph.add_edge(log.employee_id, log.account_id, type="ACCESSED_ACCOUNT",
                                    timestamp=log.timestamp.isoformat())

        # Add beneficiary creation edges
        beneficiaries = self.db.query(Beneficiary).all()
        for b in beneficiaries:
            if b.created_by_employee_id:
                self.graph.add_edge(b.created_by_employee_id, b.account_id, type="CREATED_BENEFICIARY",
                                    beneficiary_id=b.id)

        return self.graph

    def detect_cycles(self, min_length=3, max_length=6):
        self.build_full_graph()
        try:
            simple_cycles = list(nx.simple_cycles(self.graph))
            filtered_cycles = [c for c in simple_cycles if min_length <= len(c) <= max_length]
            return filtered_cycles
        except Exception:
            return []

    def get_frontend_payload(self, focus_id: str = None):
        self.build_full_graph()
        nodes = []
        edges = []

        subgraph = self.graph
        if focus_id and focus_id in self.graph:
            # Extract local neighborhood radius 2
            neighbors = nx.ego_graph(self.graph.to_undirected(), focus_id, radius=2).nodes()
            subgraph = self.graph.subgraph(neighbors)

        for node in subgraph.nodes():
            node_type = "account"
            if node.startswith("EMP") or len(node) > 20:  # heuristic or check entity prefix
                node_type = "entity"
            nodes.append({"id": node, "type": node_type, "label": node[:8]})

        for u, v, data in subgraph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "type": data.get("type", "EDGE"),
                "amount": data.get("amount", 0),
                "transaction_id": data.get("transaction_id")
            })

        return {"nodes": nodes, "edges": edges}