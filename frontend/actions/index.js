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
  UPDATE_DURATION
} from '../constants/index'
import { length } from 'ramda'
import { validJurisdictions } from '../utils/jurisdictions'

export function selectServiceProvider(serviceProvider) {
  return {
    type: SELECT_SERVICE_PROVIDER,
    payload: serviceProvider
  }
}

export function resetServiceProvider(serviceProvider) {
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
    'api/upload/jurisdictional_roles.json', {
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

export function getMatchingResults(data) {
  return {
    type: MATCHING_RESULTS,
    payload: data
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
