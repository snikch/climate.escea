# Escea Home Assistant Custom Component

Adds support for Escea network fireplaces with auto discovery. Fan Boost is supported as the Fan Mode (Auto vs On).
Flame Effect is supported as a preset.

![Escea Fireplace in HA](https://github.com/snikch/climate.escea/blob/master/assets/screenshot.png)

## Installation

Ensure the `custom_components/escea` directory is copied, linked or mounted as `CONFIG_DIR/custom_components/escea` in
home assistant, and add `escea:` to your `configuration.yaml` to load the platform, and then add the escea platform to
your `climate` platform.

```yaml
escea:
climate:
  - platform: escea
```

## Supported Devices

This should support all network attached Escea fireplaces. It has been tested as working on:

- DX1500
