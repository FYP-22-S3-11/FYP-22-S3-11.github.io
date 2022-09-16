import axios from "axios";

/**
 * Api call
 */
class HashService {
    getList = () => {
        let url = `${process.env.REACT_APP_API}/api/list`;
        return axios.get(url);
    };
}

const instance = new HashService();

export default instance;
