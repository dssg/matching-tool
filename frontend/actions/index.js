import { REPLACE_DATA } from '../constants/index'

export function makeDataGood(message) {
  return {
    type: REPLACE_DATA,
    payload: {
      status: 'good',
      reason: message
    }
  }
}

export function makeDataBad(message) {
  console.log(message)
  return {
    type: REPLACE_DATA,
    payload: {
      status: 'bad',
      reason: message
    }
  }
}
