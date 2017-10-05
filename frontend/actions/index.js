import {
  SELECT_SERVICE_PROVIDER,
  SELECT_JURISDICTION,
  CHANGE_UPLOAD_STATE,
  SAVE_AVAILABLE_ROLES,
  SAVE_UPLOAD_RESPONSE,
  SET_ERROR_MESSAGE,
  VENN_DIAGRAM_DATA,
  TABLE_DATA,
  BAR_DATA
} from '../constants/index'
import { length } from 'ramda'
import { validJurisdictions } from '../utils/jurisdictions'

export function selectServiceProvider(serviceProvider) {
  return {
    type: SELECT_SERVICE_PROVIDER,
    payload: serviceProvider
  }
}

export function selectJurisdiction(jurisdiction) {
  return {
    type: SELECT_JURISDICTION,
    payload: jurisdiction
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
    'jurisdictional_roles.json', {
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

export function getVennDiagramData(data) {
  return {
    type: VENN_DIAGRAM_DATA,
    payload: data
  }
}

export function getTableData(data) {
  return {
    type: TABLE_DATA,
    payload: data
  }
}

export function getBarData(data) {
  return {
    type: BAR_DATA,
    payload: data
  }
}
