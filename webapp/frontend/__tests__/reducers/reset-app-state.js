import resetAppState from '../../reducers/reset-app-state'

describe('resetAppState', () => {
  it('resets a state key in the app namespace to its initial value', () => {
    const stateKey = 'someKey.thing'

    const initialState = {
      app: {
        someKey: { thing: '' },
        otherKey: {}
      }
    }
    const currentState = {
      someKey: { thing: 'some file.csv' },
      otherKey: { a: 1 }
    }

    const afterState = {
      someKey: { thing: '' },
      otherKey: { a: 1 }
    }

    expect(resetAppState(currentState, stateKey, initialState)).toEqual(afterState)
  })
})

