import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import {List, ListItem} from 'material-ui/List'
import { resetUploadResponse, pickFile } from '../../actions'
import { connect } from 'react-redux'
import { map, mapObjIndexed, values } from 'ramda'


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

class UploadInvalid extends React.Component {


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
export default connect(mapStateToProps, mapDispatchToProps)(UploadInvalid)
