import React from 'react'
import { Switch, Route } from 'react-router-dom'
import { connect } from 'react-redux'
import Charts from './charts'
import Home from './home'
import Upload from './upload'
import UploadSuccess from './upload-success'
import UploadInvalid from './upload-invalid'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import AppBar from 'material-ui/AppBar'
import { Link } from 'react-router-dom'
import Tabs from 'material-ui/Tabs/Tabs'
import Tab from 'material-ui/Tabs/Tab'
import Drawer from 'material-ui/Drawer'
import MenuItem from 'material-ui/MenuItem'
import Divider from 'material-ui/Divider'
import injectTapEventPlugin from 'react-tap-event-plugin'


const styles = {
  appBar: {
    flexWrap: 'wrap',
  },
  tabs: {
    width: '50%'
  }
}

function mapStateToProps(state) {
  return {
    title: 'Matching Tool - ' + state.app.jurisdiction
  }
}

function mapDispatchToProps(dispatch) {
  return {
    resetUploadState: () => {
      return () => {
        dispatch(resetUploadState())
      }
    }
  }
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
      open: false
    };
  }

  componentWillMount() {
    injectTapEventPlugin();
  }

  handleChange = (value) => {
    this.setState({
      value: value,
    });
  }

  handleToggle = () => {
    this.setState({
      open: !this.state.open
    });
  }
  render() {
    return (
      <MuiThemeProvider>
        <div>
          <AppBar
            title={this.props.title}
            style={styles.appBar}
            onLeftIconButtonTouchTap={this.handleToggle}
          >
            <Tabs style={styles.tabs} value={this.state.value} onChange={this.handleChange}>
              <Tab value={0} label="Home" containerElement={<Link to="/"/>} />
              <Tab value={1} label="Upload Data" containerElement={<Link to="/upload"/>} />
              <Tab value={2} label="Charts" containerElement={<Link to="/charts"/>} />
            </Tabs>
          </AppBar>
          <Drawer
            open={this.state.open}
            docked={false}
            onRequestChange={this.handleToggle}
          >
            <MenuItem primaryText='Welcome, Joe Walsh' />
            <Divider />
            <Link to='/'><MenuItem primaryText='Home' onTouchTap={this.handleToggle} /></Link>
            <Link to='/upload'><MenuItem primaryText='Upload' onTouchTap={this.handleToggle} /></Link>
            <Link to='/charts'><MenuItem primaryText='Charts' onTouchTap={this.handleToggle} /></Link>
            <Divider />
            <Link to='/logout'><MenuItem value={'/logout'} primaryText='Logout' /></Link>
          </Drawer>
          <Switch>
            <Route exact path='/' component={Home} />
            <Route path='/upload' component={Upload} />
            <Route path='/charts' component={Charts} />
          </Switch>
        </div>
      </MuiThemeProvider>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(App)
