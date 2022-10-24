import axios from "axios";

/**
 * Api call
 */
class DominanceService {    
	checkDominance = (payload) => {
		var formData = new FormData();
		for(var i=0;i<payload.length;i++) {
			formData.append("file", payload[i]);
		}		

        // let baseURL = 'http://127.0.0.1:8000';
		// let url = `${baseURL}/api/check-file/`;
		let url = `${process.env.REACT_APP_API}/api/check-file/`;
		return axios.post(url, formData, {
			headers: {
			  'Content-Type': 'multipart/form-data'
			}
		})
	};
}

const instance = new DominanceService();

export default instance;
