import { createReducer } from '../utils/redux'
import { CHANGE_UPLOAD_STATE, SELECT_SERVICE_PROVIDER } from '../constants/index'
import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'

const initialState = {
  app: {
    serviceProvider: 'HMIS',
    uploadState: '',
    jurisdiction: 'Your County',
  }
}

const app = createReducer(initialState, {
  [SELECT_SERVICE_PROVIDER]: (state, payload) => {
    return Object.assign({}, state, {
      serviceProvider: payload
    })
  },
  [CHANGE_UPLOAD_STATE]: (state, payload) => {
    return Object.assign({}, state, {
      uploadState: payload
    })
  }
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
