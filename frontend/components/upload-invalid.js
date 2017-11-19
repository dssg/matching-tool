import React from 'react'
import { resetUploadResponse, pickFile } from '../actions'
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
    errorRows: state.app.uploadResponse.exampleRows
  }
}

function mapDispatchToProps(dispatch) {
  return {
    retryUpload: () => {
      return () => {
        dispatch(resetUploadResponse())
        dispatch(pickFile(''))
      }
    },
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}


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

const renderIdField = (idFieldValue, idFieldName, idFieldObj) => {
  return (<p key={idFieldName}><b>{idFieldName}</b>: {idFieldValue}</p>)
}

const renderColumnError = (error) => {
  return (<p key={error.message}>{error.fieldName}: {error.message}</p>)
}

const renderBadRow = (badRow) => {
  return (
    <ListItem key={badRow.idFields.rowNumber}>
      {values(mapObjIndexed(renderIdField, badRow.idFields))}
      Invalid Fields:
      {map(renderColumnError, badRow.errors)}
    </ListItem>
  )
}

class UploadInvalidPage extends React.Component {


  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Failed</h2>
        <p>Your {this.props.serviceProvider} file had {this.props.errorRows.length} row(s) with errors.</p>
        <p>Please fix the rows and re-upload. If possible, fix the fields at the source so future uploads work without error.</p>
        <RaisedButton
          style={styles.button}
          label="Try Again" 
          onMouseUp={this.props.retryUpload()}
        />
        <List>
          {map(renderBadRow, this.props.errorRows)}
        </List>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadInvalidPage)
