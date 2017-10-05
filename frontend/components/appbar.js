import AppBar from 'material-ui/AppBar'
import Tabs from 'material-ui/Tabs/Tabs'
import Tab from 'material-ui/Tabs/Tab'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { browserHistory } from 'react-router'
import { syncAvailableRoles } from '../actions'

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
        onLeftIconButtonTouchTap={this.handleToggle}
      >
        <Tabs style={styles.tabs} value={this.props.location.pathname}>
          <Tab value="/" label="Home" containerElement={<Link to="/"/>} />
          <Tab value="/upload" label="Upload Data" containerElement={<Link to="/upload"/>} />
          <Tab value="/charts" label="Charts" containerElement={<Link to="/charts"/>} />
        </Tabs>
      </AppBar>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(MatchingAppBar)
