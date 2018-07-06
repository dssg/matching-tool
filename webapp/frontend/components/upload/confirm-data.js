import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import Reactable from 'reactable'
import { pickFile, resetEventType, resetUploadResponse, confirmUpload } from '../../actions'
import { connect } from 'react-redux'

function mapStateToProps(state) {
  return {
    selectedEventType: state.app.selectedEventType,
    exampleRows: state.app.uploadResponse.exampleRows,
    fieldOrder: state.app.uploadResponse.fieldOrder,
    numRows: state.app.uploadResponse.rowCount,
    uploadId: state.app.uploadResponse.uploadId,
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
  step: { marginLeft: 75 }
}

class ConfirmData extends React.Component {
  renderButtons() {
    return (
      <div>
        <RaisedButton onMouseUp={this.props.confirm(this.props.uploadId)} style={styles.button} label="Confirm Upload" />
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
