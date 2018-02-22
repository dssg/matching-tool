import { createReducer } from '../utils/redux'
import {
  CHANGE_UPLOAD_STATE,
  RESET_SERVICE_PROVIDER,
  SELECT_SERVICE_PROVIDER,
  SELECT_JURISDICTION,
  PICK_FILE,
  SAVE_AVAILABLE_ROLES,
  SAVE_UPLOAD_RESPONSE,
  RESET_UPLOAD_RESPONSE,
  RESET_APP_STATE,
  SAVE_MERGE_RESULTS,
  SET_ERROR_MESSAGE,
  MATCHING_RESULTS,
  UPDATE_CONTROLLED_DATE,
  UPDATE_TABLE_DATA,
  UPDATE_SET_STATUS,
  VALIDATED_RESULT
} from '../constants/index'

import resetAppState from './reset-app-state'

import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import update from 'immutability-helper'


const initialState = {
  app: {
    selectedEventType: {
      name: '',
      slug: ''
    },
    filePicked: '',
    uploadResponse: {
      message: '',
      status: '',
      jobKey: '',
      exampleRows: [],
      fieldOrder: [],
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
        controlledDate: '',
        startDate: '',
        endDate: '',
        eventTypes: ['jail', 'hmis', 'intersection'],
        setStatus: 'All'
      },
      vennDiagramData: [{sets: [''], size: null}, {sets: [''], size: null}, {sets: [''], size: null}],
      filteredData: {
        tableData: [],
        jailDurationBarData: [],
        homelessDurationBarData: [],
        jailContactBarData: [],
        homelessContactBarData: []
      }
    }
  }
}

const app = createReducer(initialState, {
  [SELECT_SERVICE_PROVIDER]: (state, payload) => {
    return Object.assign({}, state, {
      selectedEventType: payload
    })
  },
  [RESET_SERVICE_PROVIDER]: (state) => {
    return Object.assign({}, state, {
      selectedEventType: {
        name: '',
        slug: '',
      }
    })
  },
  [SELECT_JURISDICTION]: (state, payload) => {
    return Object.assign({}, state, {
      selectedJurisdiction: payload
    })
  },
  [PICK_FILE]: (state, payload) => {
    return update(state, { filePicked: { $set: payload } })
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
  [RESET_UPLOAD_RESPONSE]: (state) => {
    return update(state, {
      uploadResponse: {$set: initialState.app.uploadResponse}
    })
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
  [SAVE_MERGE_RESULTS]: (state, payload) => {
    const newState = Object.assign({}, state, {
      mergeResults: {
        newUniqueRows: payload.new_unique_rows,
        totalUniqueRows: payload.total_unique_rows
      }
    })
    return newState
  },
  [RESET_APP_STATE]: resetAppState,
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
  [UPDATE_SET_STATUS]: (state, payload) => {
    const newState = update(state, {
      matchingResults: {
        filters: {
          setStatus: {$set: payload}
        }
      }
    })
    return newState
  },
  [VALIDATED_RESULT]: (state, payload) => {
    const newState = update(state, {
      uploadResponse: {$set: payload}
    })
    return newState
  },
})
const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
