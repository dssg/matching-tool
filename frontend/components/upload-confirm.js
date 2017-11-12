import React from 'react'
import { selectServiceProvider, confirmUpload } from '../actions'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Dialog from 'material-ui/Dialog'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import { Redirect } from 'react-router'
import Upload from 'material-ui-upload/Upload'
import Reactable from 'reactable'


function mapStateToProps(state) {
  return {
    serviceProvider: state.app.serviceProvider,
    exampleRows: state.app.uploadResponse.exampleRows,
    numRows: state.app.uploadResponse.rowCount,
    uploadId: state.app.uploadResponse.uploadId,
    showModal: state.app.mergeResults.totalUniqueRows !== '',
    totalUniqueRows: state.app.mergeResults.totalUniqueRows,
    newUniqueRows: state.app.mergeResults.newUniqueRows
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
    confirm: (uploadId) => {
      return () => {
        dispatch(confirmUpload(uploadId))
      }
    }
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}

function renderModal(totalUniqueRows, newUniqueRows, redirectCallback) {
  const actions = [
    <RaisedButton
      label='Back to Home'
      primary={true}
      onClick={redirectCallback}
    />
  ]
  return <Dialog
    title="Upload Confirmed"
    actions={actions}
    modal={false}
    open={true}
    onRequestClose={redirectCallback}
  >
    Your upload has been confirmed. We found {totalUniqueRows} total unique rows in the upload file, and {newUniqueRows} that hadn't been uploaded before. Your data is now being sent to our matching service, and may take several hours to process. The matched results, when complete, will be available at the results page.
  </Dialog>
}

function homeRedirect() {
  return <Redirect push to="/" />
}

class UploadConfirmPage extends React.Component {
  state = {
    redirect: false
  }
  redirect = () => {
    this.setState({redirect: true})
  }
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Confirmation</h2>
        <p>Your {this.props.serviceProvider} file was successfully validated. {this.props.numRows} valid rows were found.</p>
        <p>Verify that the first ten rows shown below uploaded in the way you expect. If you are satisfied then click 'Confirm Upload' below, or else click 'Cancel Upload' to try again.</p>
        <Reactable.Table
          className="table"
          data={this.props.exampleRows} />
        <RaisedButton onMouseUp={this.props.confirm(this.props.uploadId)} style={styles.button} label="Confirm Upload" />
        <Link to='/upload'><RaisedButton style={styles.button} label="Cancel Upload" /></Link>
        {this.props.showModal ? renderModal(this.props.totalUniqueRows, this.props.newUniqueRows, this.redirect) : null} 
        {this.state.redirect ? homeRedirect() : null}
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadConfirmPage)
