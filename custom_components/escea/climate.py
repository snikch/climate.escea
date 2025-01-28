"""Support for Escea fires."""
import logging
import escea
from datetime import timedelta
from typing import List, Optional

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction
)

from homeassistant.components.climate.const import (
    FAN_AUTO, FAN_ON,
    PRESET_NONE
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    UnitOfTemperature
)

import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

PRESET_FLAME_EFFECT = 'flame_effect'

OPERATION_LIST = [HVAC_MODE_HEAT, HVAC_MODE_OFF]
FAN_OPERATION_LIST = [FAN_ON, FAN_AUTO]
PRESET_LIST = [PRESET_NONE, PRESET_FLAME_EFFECT]


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    entities = []
    _LOGGER.debug("Looking for fires")
    fires = escea.fires(2)
    for fire in fires:
        _LOGGER.debug("Found fire %s at %s", fire.serial(), fire._ip)
        entities.append(EsceaFire(fire))
    async_add_entities(entities)
    return


class EsceaFire(ClimateEntity):
    """Representation of a Escea Fire."""

    def __init__(self, fire):
        """Initialize the fire."""
        self._fire = fire
        self._unique_id = "escea_{}".format(self._fire.serial())
        self.update()

    @property
    def supported_features(self) -> ClimateEntityFeature:
        """Return the list of all supported features using the ClimateEntityFeature enum."""
        return (
            ClimateEntityFeature.TARGET_TEMPERATURE |
            ClimateEntityFeature.FAN_MODE |
            ClimateEntityFeature.PRESET_MODE
        )

    @property
    def name(self):
        """Return the name of the fire."""
        return "Escea {}".format(self._fire.serial())
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID for this sensor."""
        return self._unique_id

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this fire uses."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._state['current_temp']

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._state['target_temp']

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    @property
    def hvac_action(self):
        """Return current HVAC action."""
        if self._state['on']:
            return HVACAction.HEATING

        return HVACAction.OFF

    @property
    def hvac_modes(self) -> List[str]:
        """Return the supported operations."""
        return OPERATION_LIST

    @property
    def hvac_mode(self):
        """Return current HVAC operation."""
        if self._state['on']:
            return HVACMode.HEAT

        return HVACMode.OFF

    def set_hvac_mode(self, hvac_mode):
        """Set the operation mode."""
        if hvac_mode == HVACMode.HEAT:
            self._fire.power_on()
        elif hvac_mode == HVACMode.OFF:
            self._fire.power_off()
        else:
            _LOGGER.error("Invalid operation mode provided %s", hvac_mode)
        self.update()

    @property
    def preset_modes(self) -> Optional[List[str]]:
        """Return a list of available preset modes."""
        return PRESET_LIST

    @property
    def preset_mode(self) -> Optional[str]:
        if self._state["flame_effect"]:
            return PRESET_FLAME_EFFECT
        return PRESET_NONE

    def set_preset_mode(self, preset_mode: Optional[str]) -> None:
        """Set a new preset mode.
        If preset_mode is None, then turn all presets off.
        """
        if preset_mode == PRESET_NONE:
            if self.preset_mode == PRESET_FLAME_EFFECT:
                self._fire.flame_effect_off()
        elif preset_mode == PRESET_FLAME_EFFECT:
            if not self.preset_mode == PRESET_FLAME_EFFECT:
                self._fire.flame_effect_on()
        else:
            _LOGGER.error("Invalid preset mode provided %s", preset_mode)

    @property
    def fan_mode(self):
        """Return the fan setting."""
        if self._state["fan_boost"]:
            return FAN_ON
        return FAN_AUTO

    @property
    def fan_modes(self) -> Optional[List[str]]:
        """Return a list of available fan modes."""
        return FAN_OPERATION_LIST

    def set_fan_mode(self, fan_mode):
        """Set new target temperature."""
        if fan_mode == FAN_ON:
            self._fire.fan_boost_on()
        else:
            self._fire.fan_boost_off()

    @property
    def is_aux_heat(self):
        """Return true if aux heater."""
        return self._state['fan_boost']

    def turn_aux_heat_on(self):
        """Turn auxiliary heater on, aka fan boost."""
        self._fire.fan_boost_on()

    def turn_aux_heat_off(self):
        """Turn auxiliary heater off, aka fan boost."""
        self._fire.fan_boost_off()

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        if temperature == self._state['target_temp']:
            return

        try:
            self._fire.set_temp(int(temperature))
        except escea.InvalidTemp:
            _LOGGER.error("Invalid temperature provided %s", temperature)

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return escea.MIN_TEMP

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return escea.MAX_TEMP

    def update(self):
        """Get the latest data."""
        self._state = self._fire.status().state
