import axios from 'axios';

/**
 * Define interceptor to handle api resoponse and set header value
 */
const setupInterceptors = (store) => {
    axios.interceptors.request.use(function (config) {

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

