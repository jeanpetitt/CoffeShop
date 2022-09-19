/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fullstack-udacity-ndg.us.auth0.com', 
    audience: 'coffeshop', 
    clientId: 'i15mgsT1JwHJ1pbnZGxG4Sxs1EYL1a0W',
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
