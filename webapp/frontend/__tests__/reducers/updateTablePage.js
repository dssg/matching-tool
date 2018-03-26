import { nextTablePage, prevTablePage } from '../../reducers/update-table-page'

describe('update-table-page', () => {
  it('converts next and previous actions to offsets based on limit', () => {
    const currentState = {
      matchingFilters: {
        limit: 10,
        offset: 20
      }
    }

    expect(nextTablePage(currentState).matchingFilters.offset).toEqual(30)
    expect(nextTablePage(nextTablePage(currentState)).matchingFilters.offset).toEqual(40)
    expect(prevTablePage(nextTablePage(currentState)).matchingFilters.offset).toEqual(currentState.matchingFilters.offset)
  })
})

