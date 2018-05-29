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
  SET_APP_STATE,
  SAVE_MERGE_RESULTS,
  SET_ERROR_MESSAGE,
  MATCHING_RESULTS,
  MATCHING_IS_LOADING,
  UPDATE_START_DATE,
  UPDATE_END_DATE,
  UPDATE_TABLE_SORT,
  NEXT_TABLE_PAGE,
  PREV_TABLE_PAGE,
  UPDATE_TABLE_DATA,
  UPDATE_SET_STATUS,
  VALIDATED_RESULT,
  FETCHING_RESULT,
  SHOW_JOBS,
  SHOW_HISTORY,
  TOGGLE_BAR_FLAG
} from '../constants/index'

import resetAppState from './reset-app-state'
import setAppState from './set-app-state'
import { nextTablePage, prevTablePage } from './update-table-page'

import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import update from 'immutability-helper'


const initialState = {
  app: {
    serverError: null,
    selectedEventType: {
      name: '',
      slug: ''
    },
    barFlag: false,
    filePicked: '',
    validationResponse: {
      message: '',
      status: '',
      jobKey: '',
    },
    allJobs: {
      current: [],
      q: []
    },
    history: [],
    uploadResponse: {
      status: '',
      isFetching: false,
      exampleRows: [],
      errorReport: [],
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
    matchingFilters: {
      startDate: '',
      endDate: '',
      limit: 11,
      offset: 0,
      orderColumn: 'matched_id',
      order: 'asc',
      eventTypes: ['jail', 'hmis', 'intersection'],
      setStatus: 'All'
    },
    matchingIsLoading: false,
    matchingResults: {
      vennDiagramData: [{sets: [''], size: null}, {sets: [''], size: null}, {sets: [''], size: null}],
      totalTableRows: null,
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
    const newState = update(state, {
      validationResponse: {$set: payload}
    })
    return newState
  },
  [RESET_UPLOAD_RESPONSE]: (state) => {
    return update(state, {
      uploadResponse: {$set: initialState.app.uploadResponse},
      validationResponse: {$set: initialState.app.validationResponse}
    })
  },
  [MATCHING_IS_LOADING]: (state, payload) => {
    const newState = update(state, {
      matchingIsLoading: {$set: payload}
    })
    return newState
  },
  [MATCHING_RESULTS]: (state, payload) => {
    return Object.assign({}, state, {
      matchingResults: payload
    })
  },
  [UPDATE_START_DATE]: (state, payload) => {
    const newState = update(state, {
      matchingFilters: {
        startDate: {$set: payload.startDate},
      }
    })
    return newState
  },
  [UPDATE_END_DATE]: (state, payload) => {
    const newState = update(state, {
      matchingFilters: {
        endDate: {$set: payload.endDate}
      }
    })
    return newState
  },
  [UPDATE_TABLE_SORT]: (state, payload) => {
    const newState = update(state, {
      matchingFilters: {
        orderColumn: {$set: payload.orderColumn},
        order: {$set: payload.order},
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
  [SET_APP_STATE]: setAppState,
  [NEXT_TABLE_PAGE]: nextTablePage,
  [PREV_TABLE_PAGE]: prevTablePage,
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
      matchingFilters: {
        setStatus: {$set: payload},
        offset: {$set: 0}

      }
    })
    return newState
  },
  [VALIDATED_RESULT]: (state, payload) => {
    const newState = update(state, {
      validationResponse: {
        message: {$set: payload.validation.message},
        status: {$set: payload.validation.status},
        jobKey: {$set: payload.validation.jobKey}
      },
      uploadResponse: {
        status: {$set: payload.upload_result.status},
        isFetching: {$set: false},
        exampleRows: {$set: payload.upload_result.exampleRows},
        errorReport: {$set: payload.upload_result.errorReport},
        fieldOrder: {$set: payload.upload_result.fieldOrder},
        rowCount: {$set: payload.upload_result.rowCount},
        uploadId: {$set: payload.upload_result.uploadId}
      }
    })
    return newState
  },
  [FETCHING_RESULT]: (state, payload) => {
    const newState = update(state, {
      validationResponse: {$set: payload.validation},
      uploadResponse: {
        isFetching: {$set: true}
      }
    })
    return newState
  },
  [SHOW_JOBS]: (state, payload) => {
    const newState = update(state, {
      allJobs: {$set: payload}
    })
    return newState
  },
  [SHOW_HISTORY]: (state, payload) => {
    const newState = update(state, {
      history: {$set: payload}
    })
    return newState
  },
  [SET_ERROR_MESSAGE]: (state, payload) => {
    const newState = update(state, {
      serverError: {$set: payload}
    })
    return newState
  },
  [TOGGLE_BAR_FLAG]: (state, payload) => {
    const newState = update(state, {
      barFlag: {$set: !state.barFlag}
    })
    return newState
  }
})

const rootReducer = combineReducers({
  routing: routerReducer,
  app,
})

export { rootReducer, initialState }
