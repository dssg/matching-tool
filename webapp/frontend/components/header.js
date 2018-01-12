import Divider from 'material-ui/Divider'
import Drawer from 'material-ui/Drawer'
import Home from './home'
import MatchingAppBar from './appbar'
import MenuItem from 'material-ui/MenuItem'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import React from 'react'
import Results from './results'
import Upload from './upload'
import { Link } from 'react-router-dom'
import { Switch, Route } from 'react-router-dom'

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
    })
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
          <Link to='/results'><MenuItem primaryText='Results' onTouchTap={this.handleToggle} /></Link>
          <Divider />
          <Link to='/logout'><MenuItem value={'/logout'} primaryText='Logout' /></Link>
        </Drawer>
      </div>
    )
  }
}
export default Header
