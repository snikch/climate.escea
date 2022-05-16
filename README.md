# Escea Home Assistant Custom Component

Adds support for Escea network fireplaces with auto discovery. Fan Boost is supported as the Fan Mode (Auto vs On).
Flame Effect is supported as a preset.

![Escea Fireplace in HA](https://github.com/snikch/climate.escea/blob/master/assets/screenshot.png)

## Installation

Ensure the `custom_components/escea` directory is copied, linked or mounted as `CONFIG_DIR/custom_components/escea` in
home assistant, and add `- platform: escea` to your `climate` config in `configuration.yaml` to load the platform.

```yaml
climate:
  - platform: escea
```

## Supported Devices

This should support all network attached Escea fireplaces. It has been tested as working on:

- DX1500
- DX1000
- DS1400
