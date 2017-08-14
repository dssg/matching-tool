import { SELECT_SERVICE_PROVIDER } from '../constants/index'

export function selectServiceProvider(serviceProvider) {
  console.log('in action creator')
  return {
    type: SELECT_SERVICE_PROVIDER,
    payload: serviceProvider
  }
}
