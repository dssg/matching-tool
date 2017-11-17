import { createReducer } from '../utils/redux'
import {
  CHANGE_UPLOAD_STATE,
  SELECT_SERVICE_PROVIDER,
  SELECT_JURISDICTION,
  SAVE_AVAILABLE_ROLES,
  SAVE_UPLOAD_RESPONSE,
  SAVE_MERGE_RESULTS,
  SET_ERROR_MESSAGE,
  MATCHING_RESULTS,
  UPDATE_CONTROLLED_DATE,
  UPDATE_DURATION,
  UPDATE_TABLE_DATA
} from '../constants/index'
import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import update from 'immutability-helper'

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
    mergeResults: {
      totalUniqueRows: '',
      newUniqueRows: '',
    },
    selectedJurisdiction: {
      name: '',
      slug: ''
    },
    availableJurisdictionalRoles: [],
    matchingResults: {
      filters: {
        controlledDate: '2017-10-31',
        duration: '1 month',
        startDate: '2016-11-18',
        endDate: '2017-11-18',
        serviceProviders: ['jail', 'hmis', 'intersection']
      },
      vennDiagramData: [{sets: [''], size: null}, {sets: [''], size: null}, {sets: [''], size: null}],
      filteredData: {
        tableData: [],
        jailBarData: [],
        homelessBarData: [],
      }
    }
  }
}

const app = createReducer(initialState, {
  [SELECT_SERVICE_PROVIDER]: (state, payload) => {
    return Object.assign({}, state, {
      selectedServiceProvider: payload
    })
  },
  [SELECT_JURISDICTION]: (state, payload) => {
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
  [MATCHING_RESULTS]: (state, payload) => {
    return Object.assign({}, state, {
      matchingResults: payload
    })
  },
  [UPDATE_CONTROLLED_DATE]: (state, payload) => {
    const newState = update(state, {
      matchingResults: {
        filters: {
          controlledDate: {$set: payload}
        }
      }
    })
    return newState
  },
  [UPDATE_DURATION]: (state, payload) => {
    const newState = update(state, {
      matchingResults: {
        filters: {
          duration: {$set: payload}
        }
      }
    })
    return newState
  },
  [SAVE_MERGE_RESULTS]: (state, payload) => {
    const newState = Object.assign({}, state, {
      mergeResults: {
        newUniqueRows: payload.new_unique_rows,
        totalUniqueRows: payload.total_unique_rows
      }
    })
    return newState
  },
  [UPDATE_TABLE_DATA]: (state, payload) => {
    const newState = update(state, {
      matchingResults: {
        filteredData: {
          tableData: {$set: payload}
        }
      }
    })
    return newState
  },
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
