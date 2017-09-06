import React from 'react'
import { changeUploadState } from '../actions'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'
import { Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn } from 'material-ui/Table'
import { map, mapObjIndexed, addIndex, values, keys } from 'ramda'
import { List, ListItem } from 'material-ui/List'


function mapStateToProps(state) {
  return {
    serviceProvider: state.app.serviceProvider,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    retryUpload: () => {
      return () => {
        dispatch(changeUploadState(''))
      }
    },
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}

const invalidRows = [
  {
    'Internal Person ID': "A023918475",
    'Internal Event ID': "248457",
    'Row #': 4,
    'Birthdate': "1972-01-01",
    'SSN': "123-45-6789",
    'DMV Number': "S123-4567-7890",
    'DMV State': "IL",
    'Additional State or Federal ID': "C1293048",
    'Name of Additional State or Federal ID': "Canadian Social Insurance Number",
    'Race/Ethnicity': "B",
    'Ethnicity': null,
    'Sex/Gender': "F",
    'Veteran Status': 0,
    'Disabling Condition': 1,
    'Project Start Date': "2015-01-25",
    'Project Exit Date': "2015-01-26",
    'Program Name': "Safe Haven Shelter",
    'Program Type': "Emergency Shelter",
    'Federal Program': "RHSP",
    'Destination': 8,
    'Household ID': 243859,
    'Relationship to Head of Household': 1,
    'Housing Move-in Date': "2015-02-01",
    'Living Situation: Type of Residence': 12,
    'Living Situation: Length of Stay': 34,
    'Living Situation: Date Homelessness Started': "2014-12-01",
    'Living Situation: Number of Times on Street': 1,
    'Living Situation: Number of Months Homeless': 1
  },
]

const header = keys(invalidRows[0])

const renderRowColumn = (value, index) => {
  return (<TableRowColumn key={index}>{value}</TableRowColumn>)
}

const renderRow = (row, index) => {
  const cols = addIndex(map)(renderRowColumn, values(row))
  return (<TableRow key={index}>{cols}</TableRow>)
}

const renderRows = (rows) => {
  return addIndex(map)(renderRow, rows)
}

class UploadInvalidPage extends React.Component {
  renderHeaderColumn(column) {
    return (<TableHeaderColumn key={column}>{column}</TableHeaderColumn>)
  }

  renderHeader() {
    return map(this.renderHeaderColumn, header)
  }

  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Failed</h2>
        <p>Your {this.props.serviceProvider} file had 2 rows with errors.</p>
        <p>Please fix the rows and re-upload. If possible, fix the fields at the source so future uploads work without error.</p>
        <RaisedButton
          style={styles.button}
          label="Try Again" 
          onMouseUp={this.props.retryUpload()}
        />
        <List>
          <ListItem>
            <p><b>Row #</b>: 4</p>
            <p><b>Internal Person ID</b>: 1234567</p>
            <p><b>Internal Event ID</b>: 4567788</p>
            Invalid Fields:
            <p>Date of Birth - '20116' is not a valid date</p>
          </ListItem>
          <ListItem>
            <p><b>Row #</b>: 26</p>
            <p><b>Internal Person ID</b>: 364723</p>
            <p><b>Internal Event ID</b>: 939383939</p>
            Invalid Fields:
            <p>Living Situation: Length of Stay - 'No' is not a valid number</p>
          </ListItem>
        </List>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadInvalidPage)
