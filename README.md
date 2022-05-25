[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

# Escea Home Assistant Custom Component

Adds support for Escea network fireplaces with auto discovery. Fan Boost is supported as the Fan Mode (Auto vs On).
Flame Effect is supported as a preset.

![Escea Fireplace in HA](https://github.com/snikch/climate.escea/blob/master/assets/screenshot.png)![](https://github.com/snikch/climate.escea/blob/master/assets/icon.png)

## Installation

1. Download via HACS or copy the `custom_components/escea` directory into the `CONFIG_DIR/custom_components/escea` directory in
home assistant
2. Add `- platform: escea` to your `climate` config in `configuration.yaml` to load the platform.

```yaml
climate:
  - platform: escea
```

## Supported Devices

This should support all network attached Escea fireplaces. It has been tested as working on:

- DX1500
- DX1000
- DS1400
- DF700

![](https://github.com/snikch/climate.escea/blob/master/assets/logo.png)
