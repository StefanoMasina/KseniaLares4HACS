"""The KseniaIntegration integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import AlarmDataCoordinator  # Importa il coordinatore
from .websocket_client import SimpleAlarmWebSocketClient
from .websocket_super_user import WebsocketSuperUser

_PLATFORMS: list[Platform] = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Simple Alarm from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    print("ci sono")
    websocket_uri = (
        "wss://" + entry.data.get("ip") + ":" + entry.data.get("port") + "/KseniaWsock"
    )

    # Inizializza WebSocket e gestisci il login
    websocket_client = SimpleAlarmWebSocketClient(
        websocket_uri, entry.data.get("macAddr"), entry.data.get("code")
    )

    await websocket_client.connect()

    coordinator = AlarmDataCoordinator(hass, websocket_client)
    websocket_super_user = WebsocketSuperUser(
        websocket_uri,
        entry.data.get("macAddr"),
        entry.data.get("pinSuper"),
        coordinator,
        websocket_client,
    )

    await websocket_super_user.connectSuperUser()

    # Crea entità, servizi, ecc.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(
            entry, Platform.ALARM_CONTROL_PANEL
        )
    )
    hass.data[DOMAIN][entry.entry_id] = {DATA_COORDINATOR: coordinator}

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(
            entry,
            [
                Platform.ALARM_CONTROL_PANEL,
                Platform.SWITCH,
                Platform.BUTTON,
                Platform.BINARY_SENSOR,
            ],
        )
    )

    return True
