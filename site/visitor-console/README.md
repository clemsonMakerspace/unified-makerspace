# Visitor Console Frontend

This app is the frontend for the makerspace visitor signin system.

## Requirements

- Node.js version 14 or greater

## Development

1. Run `npm install` to install all dependancies
2. To start the development server run `npm run start`
   - The site should now be accessable at http://localhost:3000/.

## Building and Dev Deployment

1. Run `npm install` to install all dependancies
2. To make a production build run `npm run build`
   - To make the frontend hit the desired api, set the environment variables mentioned below in a `.env` file
   - This will create a folder called `dist` with all of the static files ready to serve.
   - You can preview what the production deployment will look like by running `npm run preview` after building the app.
3. If you want to deploy the site using CDK: Copy the contents of the `dist` folder into `cdk/visit/console/Dev`
   - make sure to keep the `.gitkeep` in this folder, or you will have to ommit the removal of it from any commits

## Envrionment Variables

`VITE_API_ENDPOINT` (default: `https://api.cumaker.space`) - Will determine what api will be hit when making requests from the frontend. Note, there should not be a trailing slash as the routes will be appended to this endpoint with a prefixed slash. If you are deploying to your **Dev** stack, you should use the endpoint provided from the _SharedApiGateway_ that gets stood up.
