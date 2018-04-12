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
      </div>
    )
  }
}
export default Header
