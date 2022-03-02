# Visitor Console Frontend

This app is the frontend for the makerspace visitor signin system.

## Requirements

- Node.js version 14 or greater

## Development

1. Run `npm install` to install all dependancies
2. To start the development server run `npm run start`
   - The site should now be accessable at http://localhost:3000/.

## Building

1. Run `npm install` to install all dependancies
2. To make a production build run `npm run build`
   - This will create a folder called `dist` with all of the static files ready to serve.
   - You can preview what the production deployment will look like by running `npm run preview` after building the app.

## Envrionment Variables

`VITE_API_ENDPOINT` (default: `https://api.cumaker.space`) - Will determine what api will be hit when making requests from the frontend. Note, there should not be a trailing slash as the routes will be appended to this endpoint with a prefixed slash.
