import { createReducer } from '../utils/redux'
import { REPLACE_DATA, SELECT_SERVICE_PROVIDER } from '../constants/index'
import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'

const initialState = {
  app: {
    serviceProvider: 'HMIS'
  }
}

const app = createReducer(initialState, {
  [SELECT_SERVICE_PROVIDER]: (state, payload) => {
    console.log(state)
    console.log(payload)
    return Object.assign({}, state, {
      serviceProvider: payload
    })
  }
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
