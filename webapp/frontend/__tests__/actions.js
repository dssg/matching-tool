import * as actions from '../actions'
import * as constants from '../constants'
import configureMockStore from 'redux-mock-store'
import fetchMock from 'fetch-mock'
import thunk from 'redux-thunk'
import endpointJSON from './utils'
import fs from 'fs'


describe('actions', () => {
  it('should create an action to select a event type', () => {
    const payload = 'hmis'
    const expectedAction = {
      type: constants.SELECT_SERVICE_PROVIDER,
      payload
    }
    expect(actions.selectEventType(payload)).toEqual(expectedAction)
  })
})


const middlewares = [thunk]
const mockStore = configureMockStore(middlewares)

describe('syncRoleAction', () => {
  it('should create actions to fetch and save available roles from the server', () => {
    const mockReturnJSON = endpointJSON('hmis_only', 'jurisdictional_roles.json')
    fetchMock.getOnce(
      '/api/upload/jurisdictional_roles.json',
      {
        body: mockReturnJSON,
        headers: { 'content-type': 'application/json' }
      }
    )
    const expectedActions = [
      { type: constants.SAVE_AVAILABLE_ROLES, payload: mockReturnJSON.results },
      { type: constants.SELECT_JURISDICTION, payload: { slug: 'your_county', name: 'Your County' } }
    ]
    const store = mockStore({availableRoles: []})
    return store.dispatch(actions.syncAvailableRoles()).then(() => {
      expect(store.getActions()).toEqual(expectedActions)
    })
  })
})


describe('confirmUpload', () => {
  it('should tell the server to merge the file and then save the results locally', () => {
    fetchMock.postOnce(
      'api/upload/merge_file?uploadId=123',
      {
        body: { totalUniqueRows: 5, newUniqueRows: 4 } ,
        headers: { 'content-type': 'application/json' }
      }
    )
    const expectedActions = [
      { type: constants.SAVE_MERGE_RESULTS, payload: { totalUniqueRows: 5, newUniqueRows: 4 } }
    ]
    const store = mockStore({mergeResults: {}})
    return store.dispatch(actions.confirmUpload('123')).then(() => {
      expect(store.getActions()).toEqual(expectedActions)
    })
  })
})


describe('getMatchingResults', () => {
  it('should query and get the matched result based on the start and end time', () => {
    const mockReturnJSON = JSON.parse(fs.readFileSync('../sample_data/results_input/results_12012017_01012018_page1.json'))
    const urlParams = 'startDate=2017-12-01&endDate=2018-01-01&jurisdiction=test_jurisdiction&limit=3&offset=0'
    fetchMock.getOnce(
      'api/chart/get_schema?' + urlParams,
      {
        body: mockReturnJSON,
        headers: { 'content-type': 'application/json' }
      }
    )
    const expectedActions = [
      { type: constants.MATCHING_IS_LOADING, payload: true },
      { type: constants.MATCHING_RESULTS, payload: mockReturnJSON.results },
      { type: constants.MATCHING_IS_LOADING, payload: false },
    ]
    const store = mockStore({matchingResults: {}})
    return store.dispatch(actions.getMatchingResults(urlParams)).then(() => {
      expect(store.getActions()).toEqual(expectedActions)
    })
  })
})
