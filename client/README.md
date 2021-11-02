# video-timestamp-uploader

The is the frontend application containing a form with fields to select video files and define timestamps.

It is currently configured to POST data to the `client` application provided within this repository. This can be modified in the `sendVideo` function found in the `client/src/pages/Index.vue` file.

If changing the POST URL, please note that you may also need to update the response handling in the same `sendVideo` function. It currently attempts to access response data that may not be sent by the new address.

## Installation
```bash
yarn
```

## Usage

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```

### Lint the files
```bash
yarn run lint
```

### Build the app for production
```bash
quasar build
```

### Customize the configuration
See [Configuring quasar.conf.js](https://v2.quasar.dev/quasar-cli/quasar-conf-js).
