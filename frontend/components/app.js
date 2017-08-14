import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Charts from './charts'
import Home from './home'
import Upload from './upload'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import AppBar from 'material-ui/AppBar'
import { Link } from 'react-router-dom'
import Tabs from 'material-ui/Tabs/Tabs'
import Tab from 'material-ui/Tabs/Tab'
import injectTapEventPlugin from 'react-tap-event-plugin'


const styles = {
  appBar: {
    flexWrap: 'wrap',
  },
  tabs: {
    width: '50%'
  }
}

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
    };
  }

  componentWillMount() {
    injectTapEventPlugin();
  }

  handleChange = (value) => {
    this.setState({
      value: value,
    });
  };
  render() {
    return (
      <MuiThemeProvider>
        <div>
          <AppBar title='Matching Tool' iconStyleLeft={{display: 'none'}} style={styles.appBar}>
            <Tabs style={styles.tabs} value={this.state.value} onChange={this.handleChange}>
              <Tab value={0} label="Home" containerElement={<Link to="/"/>} />
              <Tab value={1} label="Upload Data" containerElement={<Link to="/upload"/>}/>
              <Tab value={2} label="Charts" containerElement={<Link to="/charts"/>}/>
            </Tabs>
          </AppBar>
          <Switch>
            <Route exact path='/' component={Home}/>
            <Route path='/upload' component={Upload}/>
            <Route path='/charts' component={Charts}/>
          </Switch>
        </div>
      </MuiThemeProvider>
    )
  }
}
