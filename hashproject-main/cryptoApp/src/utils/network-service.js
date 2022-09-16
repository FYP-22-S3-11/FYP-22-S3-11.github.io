import axios from 'axios';
import { toast } from "react-toastify";

import { UNAUTH_USER, SHOW_LOADING, HIDE_LOADING } from './constants';

export default {
  setupInterceptors: (store) => {
    // axios.interceptors.response.use((response) => {
    //   console.log(response)
    //   return response.data
    // }, (error) => {
    //   if (error.response.status === 404 || error.response.status === 400 || error.response.status === 401 ) {
    //     toast.error(error.response.statusText);
    //   }
    //   if (error.response.status === 401) {
    //     store.dispatch({ type: UNAUTH_USER });
    //   }
    //   return Promise.reject(error.response.data);
    // })
    var requests = 0
    var requestsError = 0
    if(window.location.pathname !== '/') {
      requestsError = 0
    }
    axios.interceptors.request.use(function (config) {
      // spinning start to show
      store.dispatch({ type: SHOW_LOADING })
      requests++;
      return config
    }, function (error) {
      return Promise.reject(error);
    });

    axios.interceptors.response.use(function (response) {
      // spinning hide
      requests--;
      if (requests === 0) {
        store.dispatch({ type: HIDE_LOADING })
      }
      return response.data;
    }, function (error) {
      requests--;
      if (error.response.status === 404 || error.response.status === 400) {
        toast.error(error.response.statusText);
      }
      if (error.response.status === 401) {
        if(requestsError === 0 ) {
          toast.error(error.response.statusText); 
        } 
        requestsError = 1
        store.dispatch({ type: UNAUTH_USER });

      }
      return Promise.reject(error.response.data);
    });
  },
};
