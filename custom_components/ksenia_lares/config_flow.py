import logging

import voluptuous as vol

from homeassistant.config_entries  import ConfigFlow, HANDLERS
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

@HANDLERS.register(DOMAIN)
class SimpleAlarmConfigFlow(ConfigFlow):

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}
        if user_input is not None:
            try:
                _LOGGER.debug("User input: %s", user_input)
                return self.async_create_entry(title="Simple Alarm", data=user_input)
            except Exception as e:
                _LOGGER.error("Errore durante la gestione del form: %s", str(e))
                errors["base"] = "unknown_error"
        data_schema = vol.Schema(
            {
                vol.Required("code"): str,
                vol.Required("ip"): str,
                vol.Required("port"): str,
                vol.Required("macAddr"): str,
                vol.Required("pinSuper"): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
