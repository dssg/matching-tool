import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'


function mapStateToProps(state) {
  return {
    totalUniqueRows: state.app.mergeResults.totalUniqueRows,
    newUniqueRows: state.app.mergeResults.newUniqueRows,
  }
}

function mapDispatchToProps(dispatch) {
  return {}
}


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}

class Done extends React.Component {
  render() {
    return (
      <div style={styles.step}>
        Your upload has been confirmed. We found {this.props.totalUniqueRows} total unique rows in the upload file, and {this.props.newUniqueRows} that hadn't been uploaded before. Your data is now being sent to our matching service, and may take several hours to process. The matched results, when complete, will be available at the results page.
        <Link to="/"><RaisedButton label="Back to Home" /></Link>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(Done)

