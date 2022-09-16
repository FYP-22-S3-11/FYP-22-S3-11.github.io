import axios from "axios";

/**
 * Api call
 */
class CryptoService {
	
	getCoinDetail = (payload) => {
		console.log("payloadpayloadpayloadpasss", payload?.type)
		let url = `${process.env.REACT_APP_API}/api/coinDetail/${payload.type}/${payload.name}`;
		return axios.get(url);
	};
}

const instance = new CryptoService();

export default instance;
