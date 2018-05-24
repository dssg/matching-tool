import setAppState from '../../reducers/set-app-state'

describe('setState', () => {
  it('sets the state for a current key', () => {
    const stateKey = 'filters'
    const value = [{ new: 1 }]

    const currentState = { filters: [{ old: 1 }] }

    const afterState = { filters: value }

    expect(setAppState(currentState, { stateKey, value })).toEqual(afterState)
  })

  it('handles nested keys using dot notation', () => {
    const stateKey = 'filters.tableData'
    const value = [{ new: 1 }]

    const currentState = {
      filters: {
        tableData: [{ old: 1 }]
      },
      other: { a: 1 }
    }

    const afterState = {
      filters: {
        tableData: value
      },
      other: { a: 1 }
    }

    expect(setAppState(currentState, { stateKey, value })).toEqual(afterState)
  })
})
