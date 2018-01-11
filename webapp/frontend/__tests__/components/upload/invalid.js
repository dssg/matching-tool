import {flattenErrorRows} from '../../../components/upload/invalid'


describe('flattenErrorRows', () => {
  it('should flatten error rows', () => {
    const input = [
      {
        errors: [{ fieldName: 'field_name_1', message: 'message 1' }],
        idFields: {myId: 1, myOtherId: 2}
      },
      {
        errors: [
          { fieldName: 'field_name_1', message: 'message "1"' }, 
          { fieldName: 'field_name_2', message: 'message 2' }, 
        ],
        idFields: {myId: 2, myOtherId: 3}
      }
    ]
    const expectedOutput = [
      {fieldName: 'field_name_1', message: 'message 1', myId: 1, myOtherId: 2},
      {fieldName: 'field_name_1', message: "message '1'", myId: 2, myOtherId: 3},
      {fieldName: 'field_name_2', message: 'message 2', myId: 2, myOtherId: 3},
    ]
    expect(flattenErrorRows(input)).toEqual(expectedOutput)
  })
})
