import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Charts from './charts'
import Home from './home'
import Upload from './upload'
import UploadSuccess from './upload-success'
import UploadInvalid from './upload-invalid'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import { Link } from 'react-router-dom'
import Drawer from 'material-ui/Drawer'
import MenuItem from 'material-ui/MenuItem'
import Divider from 'material-ui/Divider'
import MatchingAppBar from './appbar'

class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false
    };
  }

  handleToggle = () => {
    this.setState({
      open: !this.state.open
    });
  }
  render() {
    return (
      <div>
        <MatchingAppBar location={this.props.location} handleToggle={this.handleToggle} />
        <Drawer
          open={this.state.open}
          docked={false}
          onRequestChange={this.handleToggle}
          openSecondary={true}
        >
          <MenuItem primaryText='Welcome, Joe Walsh' />
          <Divider />
          <Link to='/'><MenuItem primaryText='Home' onTouchTap={this.handleToggle} /></Link>
          <Link to='/upload'><MenuItem primaryText='Upload' onTouchTap={this.handleToggle} /></Link>
          <Link to='/charts'><MenuItem primaryText='Charts' onTouchTap={this.handleToggle} /></Link>
          <Divider />
          <Link to='/logout'><MenuItem value={'/logout'} primaryText='Logout' /></Link>
        </Drawer>
      </div>
    )
  }
}
export default Header
