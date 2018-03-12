import {formatWithSingleQuotes} from '../../../components/upload/invalid'

describe(formatWithSingleQuotes, () => {
  it('should format with single quotes', () => {
    const input = {
        field_name: 'field_name_1',
        message: 'message "1"',
        num_rows: 2,
        'values': ['value "1"', 'value "2"'],
        'row_numbers': [2, 3]
      }
    const expectedOutput = {
        field_name: 'field_name_1',
        message: 'message \'1\'',
        num_rows: 2,
        'values': ['value \'1\'', 'value \'2\''],
        'row_numbers': [2, 3]
      }
    expect(formatWithSingleQuotes(input)).toEqual(expectedOutput)
  })
})
