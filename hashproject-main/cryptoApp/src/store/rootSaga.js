import { all } from "redux-saga/effects";
import { getUserLoginSaga } from "./AuthStore/saga";
import { userSaga } from './ServiceStore/saga';
import { userDetailSaga } from './UserStore/saga';

export default function* rootSaga() {
  yield all([getUserLoginSaga(), userSaga(), userDetailSaga()]);
}
