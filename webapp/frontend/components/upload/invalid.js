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

function singleQuote(string) {
  return string.replace(/"/g, "'")
}

function formatWithSingleQuotes(error) {
    const newError = clone(error)
    newError.message = singleQuote(newError.message)
    newError.values = map(singleQuote, newError.values)
    return newError
}

const renderError = (error) => {
  return (
    <ListItem key={error.field_name + error.message}>
      Field: {error.field_name}<br />
      Message: {error.message}<br />
      # rows with this error: {error.num_rows}<br />
      distinct error values: {error.values.join(' | ')}
    </ListItem>
  )
}

class UploadInvalid extends React.Component {
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Failed</h2>
        <p>Your {this.props.eventType} file had {this.props.errorReport.length} columns with errors</p>
        <p>Please fix the rows and re-upload. If possible, fix the fields at the source so future uploads work without error.</p>
        <RaisedButton
          style={styles.button}
          label="Try Again" 
          onMouseUp={this.props.retryUpload()}
        />
        <CSVLink filename="matchingToolErrorReport.csv" data={slice(0, 1000, map(formatWithSingleQuotes, this.props.errorReport))}>
          <RaisedButton style={styles.button} label="Download full error report" />
        </CSVLink>
        <List>
          {map(renderError, map(formatWithSingleQuotes, this.props.errorReport))}
        </List>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadInvalid)
