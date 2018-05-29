import { lensPath, set } from 'ramda'

export default function setState(state, { stateKey, value }) {
  const lens = lensPath(stateKey.split('.'))

  return set(lens, value, state)
}
