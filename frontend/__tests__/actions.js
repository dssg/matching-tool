import * as actions from '../actions'
import * as constants from '../constants'
import configureMockStore from 'redux-mock-store'
import fetchMock from 'fetch-mock'
import thunk from 'redux-thunk'
import fs from 'fs'


describe('actions', () => {
  it('should create an action to select a service provider', () => {
    const payload = 'hmis'
    const expectedAction = {
      type: constants.SELECT_SERVICE_PROVIDER,
      payload
    }
    expect(actions.selectServiceProvider(payload)).toEqual(expectedAction)
  })
})


const middlewares = [thunk]
const mockStore = configureMockStore(middlewares)

function endpointJSON(user, endpoint) {
  var fname = '../endpoint_examples/' + user + '/' + endpoint
  return JSON.parse(fs.readFileSync(fname))
}

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
