import { lensPath, set, view } from 'ramda'
import { initialState } from './'

export default function resetAppState(state, payload, InitialState=initialState) {
  const lens = lensPath(payload.split('.'))
  const value = view(lens, InitialState.app)
  const newState = set(lens, value, state)
  return newState
}
