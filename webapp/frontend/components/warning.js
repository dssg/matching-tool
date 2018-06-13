import React from 'react'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import RaisedButton from 'material-ui/RaisedButton'

export default class WarningPopup extends React.Component {
  constructor(props) {
      super(props);
  }

  render() {
      const actions = [
        <FlatButton
          label="OK"
          primary={true}
          onClick={this.props.handleClose} />
      ]

      return (
        <div>
          <Dialog
            title="Date Error"
            actions={actions}
            modal={false}
            open={this.props.open}
            onRequestClose={this.props.handleClose}
          >
          End Date should not be earlier than Start Date!
          </Dialog>
        </div>
      )
  }
}
