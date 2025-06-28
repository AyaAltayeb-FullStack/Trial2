from ocpp.routing import on
from ocpp.v16 import ChargePoint as CP, call_result, call
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus, RemoteStartStopStatus
import httpx
import datetime

DJANGO_API_BASE = "http://localhost:8000/api"

class ChargePointHandler(CP):
    def __init__(self, charger_id, websocket):
        super().__init__(charger_id, websocket)
        self.id = charger_id
        self.active_transaction_id = None
        self.logs = []

    def _now(self):
        return datetime.datetime.utcnow().isoformat()

    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, **kwargs):
        print(f"🚗 BootNotification from {self.id}")
        async with httpx.AsyncClient() as client:
            await client.post(f"{DJANGO_API_BASE}/chargers/", json={
                "charger_id": self.id,
                "model": charge_point_model,
                "vendor": "TestVendor"
            })

        return call_result.BootNotificationPayload(
            current_time=self._now(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on("Heartbeat")
    async def on_heartbeat(self):
        print(f"❤️ Heartbeat from {self.id}")
        return call_result.HeartbeatPayload(current_time=self._now())

    @on("Authorize")
    async def on_authorize(self, id_tag):
        print(f"✅ Authorize: {id_tag} from {self.id}")
        return call_result.AuthorizePayload(
            id_tag_info={"status": AuthorizationStatus.accepted}
        )

    @on("StartTransaction")
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        print(f"▶️ StartTransaction from {self.id} - {id_tag}")
        transaction_id = 100001  # In production, generate properly
        self.active_transaction_id = transaction_id

        async with httpx.AsyncClient() as client:
            await client.post(f"{DJANGO_API_BASE}/transactions/", json={
                "charger": self.id,
                "transaction_id": transaction_id,
                "id_tag": id_tag,
                "connector_id": connector_id,
                "meter_start": meter_start,
                "timestamp_start": timestamp
            })

        return call_result.StartTransactionPayload(
            transaction_id=transaction_id,
            id_tag_info={"status": AuthorizationStatus.accepted}
        )

    @on("StopTransaction")
    async def on_stop_transaction(self, transaction_id, meter_stop, timestamp, **kwargs):
        print(f"⏹ StopTransaction from {self.id} - {transaction_id}")
        async with httpx.AsyncClient() as client:
            await client.patch(f"{DJANGO_API_BASE}/transactions/{transaction_id}/", json={
                "meter_stop": meter_stop,
                "timestamp_stop": timestamp
            })

        return call_result.StopTransactionPayload(
            id_tag_info={"status": AuthorizationStatus.accepted}
        )
