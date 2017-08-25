import { SELECT_SERVICE_PROVIDER, CHANGE_UPLOAD_STATE } from '../constants/index'

export function selectServiceProvider(serviceProvider) {
  return {
    type: SELECT_SERVICE_PROVIDER,
    payload: serviceProvider
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
