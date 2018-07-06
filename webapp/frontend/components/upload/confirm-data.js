import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import Reactable from 'reactable'
import { pickFile, resetEventType, resetUploadResponse, confirmUpload } from '../../actions'
import { connect } from 'react-redux'
import {red500} from 'material-ui/styles/colors'

function mapStateToProps(state) {
  return {
    selectedEventType: state.app.selectedEventType,
    exampleRows: state.app.uploadResponse.exampleRows,
    fieldOrder: state.app.uploadResponse.fieldOrder,
    numRows: state.app.uploadResponse.rowCount,
    uploadId: state.app.uploadResponse.uploadId,
    mergingIsLoading: state.app.mergingIsLoading,
    mergeProblem: state.app.mergeResults.status === 'error',
  }
}

function mapDispatchToProps(dispatch) {
  return {
    resetToStep0: () => {
      dispatch(resetUploadResponse())
      dispatch(resetEventType())
      dispatch(pickFile(''))
    },
    confirm: (uploadId) => {
      return () => {
        dispatch(confirmUpload(uploadId))
      }
    },
  }
}


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 },
  error: { color: red500 }
}

class ConfirmData extends React.Component {
  renderButtons() {
    return (
      <div>
        <p style={this.props.mergeProblem ? error : {}}>{this.props.mergeProblem ? 'There was a problem confirming the upload. Please try again.' : ''}</p>
        <RaisedButton
          onMouseUp={this.props.confirm(this.props.uploadId)}
          disabled={this.props.mergingIsLoading}
          style={styles.button}
          label="Confirm Upload"
        />
        <RaisedButton
          label="Cancel Upload"
          onClick={this.props.resetToStep0}
          style={styles.button}
        />
      </div>
    )
  }
  render() {
    return (
      <div style={styles.step}>
        <h2>Upload Confirmation</h2>
        <p>Your {this.props.selectedEventType.name} file was successfully validated. {this.props.numRows} valid rows were found.</p>
        <p>Verify that the first ten rows shown below uploaded in the way you expect. If you are satisfied then click 'Confirm Upload' below, or else click 'Cancel Upload' to try again.</p>
        {this.renderButtons()}
        <div>
          <Reactable.Table
            className="table"
            data={this.props.exampleRows}
            columns={this.props.fieldOrder} />
          {this.renderButtons()}
        </div>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(ConfirmData)
