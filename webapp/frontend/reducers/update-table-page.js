import update from 'immutability-helper'


export function nextTablePage(state, payload) {
  const newState = update(state, {
    matchingFilters: {
      offset: {$set: Number(state.matchingFilters.limit) + Number(state.matchingFilters.offset)}
    }
  })
  return newState
}



export function prevTablePage(state, payload) {
  const newState = update(state, {
    matchingFilters: {
      offset: {$set: Number(state.matchingFilters.offset) - Number(state.matchingFilters.limit)}
    }
  })
  return newState
}
