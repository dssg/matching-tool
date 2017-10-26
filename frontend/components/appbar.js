import AppBar from 'material-ui/AppBar'
import Tabs from 'material-ui/Tabs/Tabs'
import Tab from 'material-ui/Tabs/Tab'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router'
import { syncAvailableRoles } from '../actions'

import FlatButton from 'material-ui/FlatButton';
import IconButton from 'material-ui/IconButton';
import ActionHome from 'material-ui/svg-icons/action/home';

import { Toolbar, ToolbarGroup } from 'material-ui/Toolbar'
import { grey50 } from 'material-ui/styles/colors'

const styles = {
  appBar: {
    flexWrap: 'wrap',
  },
  tabs: {
    width: '50%'
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
        style={styles.appBar}
        showMenuIconButton={false}
      >
        <Tabs style={styles.tabs} value={this.props.location.pathname}>
          <Tab value="/" label="Home" containerElement={<Link to="/"/>} />
          <Tab value="/upload" label="Upload Data" containerElement={<Link to="/upload"/>} />
          <Tab value="/charts" label="Charts" containerElement={<Link to="/charts"/>} />
        </Tabs>
      <IconButton onClick={this.props.handleToggle}><ActionHome color={grey50} /></IconButton>
      </AppBar>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(MatchingAppBar)
