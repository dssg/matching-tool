import ActionHome from 'material-ui/svg-icons/action/home';
import AppBar from 'material-ui/AppBar'
import FlatButton from 'material-ui/FlatButton';
import IconButton from 'material-ui/IconButton';
import Tab from 'material-ui/Tabs/Tab'
import Tabs from 'material-ui/Tabs/Tabs'
import React from 'react'
import { Link } from 'react-router-dom'
import { browserHistory } from 'react-router'
import { connect } from 'react-redux'
import { grey50 } from 'material-ui/styles/colors'
import { syncAvailableRoles } from '../actions'

const styles = {
  appBar: {
    flexWrap: 'wrap',
  },
  tabs: {
    width: '50%'
  },
  titleStyle: {
    'fontSize': 20,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    syncAvailableRoles: () => {
      dispatch(syncAvailableRoles())
    }
  }
}

function mapStateToProps(state, ownProps) {
  return {
    loc: ownProps.params,
    title: 'Matching Tool - ' + state.app.selectedJurisdiction.name,
    router: state.routing
  }
}


class MatchingAppBar extends React.Component {
  handleChange = (value) => {
    this.setState({
      value: value,
    });
  }

  componentDidMount() {
    this.props.syncAvailableRoles()
  }

  render() {
    return (
      <AppBar
        title={this.props.title}
        titleStyle={styles.titleStyle}
        style={styles.appBar}
        showMenuIconButton={false}
      >
        <Tabs style={styles.tabs} value={this.props.location.pathname}>
          <Tab value="/" label="Home" containerElement={<Link to="/"/>} />
          <Tab value="/upload" label="Upload Data" containerElement={<Link to="/upload"/>} />
          <Tab value="/results" label="Results" containerElement={<Link to="/results"/>} />
        </Tabs>
      <IconButton onClick={this.props.handleToggle}><ActionHome color={grey50} /></IconButton>
      </AppBar>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(MatchingAppBar)
