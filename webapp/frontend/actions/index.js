import {
  SELECT_SERVICE_PROVIDER,
  RESET_SERVICE_PROVIDER,
  SELECT_JURISDICTION,
  PICK_FILE,
  CHANGE_UPLOAD_STATE,
  SAVE_AVAILABLE_ROLES,
  SAVE_UPLOAD_RESPONSE,
  RESET_UPLOAD_RESPONSE,
  SAVE_MERGE_RESULTS,
  SET_ERROR_MESSAGE,
  MATCHING_RESULTS,
  UPDATE_CONTROLLED_DATE,
  UPDATE_DURATION,
  UPDATE_TABLE_DATA,
  UPDATE_SET_STATUS
} from '../constants/index'
import { length, filter } from 'ramda'
import { validJurisdictions } from '../utils/jurisdictions'

export function selectEventType(eventType) {
  return {
    type: SELECT_SERVICE_PROVIDER,
    payload: eventType
  }
}

export function resetEventType(eventType) {
  return {
    type: RESET_SERVICE_PROVIDER
  }
}

export function selectJurisdiction(jurisdiction) {
  return {
    type: SELECT_JURISDICTION,
    payload: jurisdiction
  }
}

export function pickFile(filename) {
  return {
    type: PICK_FILE,
    payload: filename
  }
}

export function changeUploadState(uploadState) {
  return {
    type: CHANGE_UPLOAD_STATE,
    payload: uploadState
  }
}

export function resetUploadState() {
  return {
    type: CHANGE_UPLOAD_STATE,
    payload: ''
  }
}

function fetchAvailableRoles() {
  return fetch(
    '/api/upload/jurisdictional_roles.json', {
      method: 'GET',
      dataType: 'json',
      credentials: 'include'
    }
  )
}

function saveAvailableRoles(results) {
  return {
    type: SAVE_AVAILABLE_ROLES,
    payload: results.results
  }
}

export function saveUploadResponse(response) {
  return {
    type: SAVE_UPLOAD_RESPONSE,
    payload: response
  }
}

export function resetUploadResponse() {
  return {
    type: RESET_UPLOAD_RESPONSE
  }
}

function errorMessage(error) {
  return {
    type: SET_ERROR_MESSAGE,
    payload: error
  }
}

export function syncAvailableRoles() {
  return function(dispatch) {
    return fetchAvailableRoles()
      .then((resp) => resp.json())
      .then((data) => {
        dispatch(saveAvailableRoles(data))
        const userJurisdictions = validJurisdictions(data.results)
        if(length(userJurisdictions) == 1) {
          dispatch(selectJurisdiction(userJurisdictions[0]))
        }
      })
  }
}


export function showMatchingResults(data) {
  return {
    type: MATCHING_RESULTS,
    payload: data.result
  }
}

export function getMatchingResults(d) {
  return function(dispatch) {
    return $.ajax({
      url: '/api/chart/get_full_json_for_view'+d,
      dataType: 'json',
      method: 'GET'
    })
    .then((data) => {
      return dispatch(showMatchingResults(data))
    })
  }
}

export function updateControlledDate(date) {
  return {
    type: UPDATE_CONTROLLED_DATE,
    payload: date
  }
}

export function updateDuration(data) {
  return {
    type: UPDATE_DURATION,
    payload: data
  }
}


function saveMergeResults(results) {
  return {
    type: SAVE_MERGE_RESULTS,
    payload: results
  }
}

export function confirmUpload(uploadId) {
  return function(dispatch) {
    return fetch('api/upload/merge_file?uploadId='+uploadId, { method: 'POST', credentials: 'include'})
        .then((resp) => resp.json())
        .then((data) => {
          dispatch(saveMergeResults(data))
        })
  }
}

export function updateTableData(data, section) {
  const isHmisAndBooking = n => n['hmis_id'].length != 0 && n['booking_id'].length != 0;
  const isHmis = n => n['hmis_id'].length != 0;
  const isBooking = n => n['booking_id'].length != 0;
  if (section.length == 2) {
    const newData = filter(isHmisAndBooking, data)
    return {
      type: UPDATE_TABLE_DATA,
      payload: newData
    }
  } else if (section[0] == "Jail") {
    const newData = filter(isBooking, data)
    return {
      type: UPDATE_TABLE_DATA,
      payload: newData
    }
  } else if (section[0] == "Homeless") {
    const newData = filter(isHmis, data)
    return {
      type: UPDATE_TABLE_DATA,
      payload: newData
    }
  } else {
    return {
      type: UPDATE_TABLE_DATA,
      payload: data
    }
  }
}

export function updateSetStatus(status) {
  if (status.length >= 2) {
    return {
      type: UPDATE_SET_STATUS,
      payload: "Intersection"
    }
  } else if (status[0] == "Jail") {
    return {
      type: UPDATE_SET_STATUS,
      payload: "Jail"
    }
  } else if (status[0] == "Homeless") {
    return {
      type: UPDATE_SET_STATUS,
      payload: "HMIS"
    }
  } else {
    return {
      type: UPDATE_SET_STATUS,
      payload: "All"
    }
  }

}
