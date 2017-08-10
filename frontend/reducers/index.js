import { createReducer } from '../utils/redux'
import { REPLACE_DATA } from '../constants/index'
import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'

const initialState = {
  app: {
    data: {
      status: 'unknown',
      reason: 'because you have not clicked a button'
    }
  }
}

const app = createReducer(initialState, {
  [REPLACE_DATA]: (state, payload) =>
    Object.assign({}, state, {
      data: payload
    })
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
