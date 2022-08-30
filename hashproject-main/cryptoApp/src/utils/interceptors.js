import axios from 'axios';

/**
 * Define interceptor to handle api resoponse and set header value
 */
const setupInterceptors = (store) => {
    axios.interceptors.request.use(function (config) {
        // config.headers["X-CMC_PRO_API_KEY"] = '7e49e5ac-b3e2-471f-8e6a-2fdeec271197';

        return config;
    }, (error) => {
        return Promise.reject(error);
    })
    axios.interceptors.response.use(response => {
        return response;
    }, (error) => {
        return Promise.reject(error);
    })
}
export default setupInterceptors

