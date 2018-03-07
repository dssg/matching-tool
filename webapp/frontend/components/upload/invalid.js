import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import {List, ListItem} from 'material-ui/List'
import { resetUploadResponse, pickFile } from '../../actions'
import { connect } from 'react-redux'
import { clone, curry, flatten, map, mapObjIndexed, merge, slice, values } from 'ramda'
import {CSVLink} from 'react-csv'


function mapStateToProps(state) {
  return {
    eventType: state.app.eventType,
    errorReport: state.app.uploadResponse.errorReport,
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


const renderError = (error) => {
  return (
    <ListItem key={badRow.fieldName + badRow.message}>
      Field: {badRow.fieldName}
      Message: {badRow.message}
      # rows with error: {badRow.num_rows}
      row numbers with error: {badRow.row_numbers}
    </ListItem>
  )
}

class UploadInvalid extends React.Component {
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Failed</h2>
        <p>Your {this.props.eventType} file had {this.props.errorReport.length} types of errors</p>
        <p>Please fix the rows and re-upload. If possible, fix the fields at the source so future uploads work without error.</p>
        <RaisedButton
          style={styles.button}
          label="Try Again" 
          onMouseUp={this.props.retryUpload()}
        />
        <CSVLink filename="matchingToolErrorReport.csv" data={this.props.errors}>
          <RaisedButton style={styles.button} label="Download full error report" />
        </CSVLink>
        <List>
          {map(renderError, this.props.errorReport)}
        </List>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadInvalid)
