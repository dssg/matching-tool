import { createReducer } from '../utils/redux'
import {
  CHANGE_UPLOAD_STATE,
  SELECT_SERVICE_PROVIDER,
  SELECT_JURISDICTION,
  SAVE_AVAILABLE_ROLES,
  SAVE_UPLOAD_RESPONSE,
  SET_ERROR_MESSAGE,
  VENN_DIAGRAM_DATA,
  TABLE_DATA,
  JAIL_BAR_DATA,
  HOMELESS_BAR_DATA
} from '../constants/index'
import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'

const initialState = {
  app: {
    selectedServiceProvider: {
      name: '',
      slug: ''
    },
    uploadResponse: {
      status: '',
      exampleRows: [],
      rowCount: '',
      uploadId: ''
    },
    selectedJurisdiction: {
      name: '',
      slug: ''
    },
    availableJurisdictionalRoles: [],
    vennDiagramData: [ {sets: [''], size: null}],
    tableData: [],
    jailBarData: [],
    homelessBarData: [],
  }
}

const app = createReducer(initialState, {
  [SELECT_SERVICE_PROVIDER]: (state, payload) => {
    return Object.assign({}, state, {
      selectedServiceProvider: payload
    })
  },
  [SELECT_JURISDICTION]: (state, payload) => {
    console.log('selecting jurisdiction')
    console.log(payload)
    return Object.assign({}, state, {
      selectedJurisdiction: payload
    })
  },
  [CHANGE_UPLOAD_STATE]: (state, payload) => {
    return Object.assign({}, state, {
      uploadState: payload
    })
  },
  [SAVE_AVAILABLE_ROLES]: (state, payload) => {
    return Object.assign({}, state, {
      availableJurisdictionalRoles: payload
    })
  },
  [SAVE_UPLOAD_RESPONSE]: (state, payload) => {
    const newState = Object.assign({}, state, {
      uploadResponse: payload
    })
    return newState
  },
  [VENN_DIAGRAM_DATA]: (state, payload) => {
    return Object.assign({}, state, {
      vennDiagramData: payload
    })
  },
  [TABLE_DATA]: (state, payload) => {
    return Object.assign({}, state, {
      tableData: payload
    })
  },
  [JAIL_BAR_DATA]: (state, payload) => {
    return Object.assign({}, state, {
      jailBarData: payload
    })
  },
  [HOMELESS_BAR_DATA]: (state, payload) => {
    return Object.assign({}, state, {
      homelessBarData: payload
    })
  }
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
