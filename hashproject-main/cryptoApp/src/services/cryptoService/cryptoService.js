import axios from "axios";

/**
 * Api call
 */
class CryptoService {
	getCryptoList = () => {
		let url = `${process.env.REACT_APP_API}/api/list`;
		return axios.get(url);
	};

	getCryptoDetail = (payload) => {
		let url = `${process.env.REACT_APP_API}/api/detail/${payload}`;
		return axios.get(url);
	};

	getAlgoList = () => {
		let url = `${process.env.REACT_APP_API}/api/algoList`;
		return axios.get(url);
	};

	getCoinList = (payload) => {
		let url = `${process.env.REACT_APP_API}/api/coinList/${payload}`;
		return axios.get(url);
	};
	
	getCoinDetail = (payload) => {
		let url = `${process.env.REACT_APP_API}/api/coinDetail/${payload.type}/${payload.name.replace(" ", "-").replace(".", "-")}`;
		return axios.get(url);
	};
}

const instance = new CryptoService();

export default instance;
