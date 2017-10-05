import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Charts from './charts'
import Home from './home'
import Upload from './upload'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEventPlugin from 'react-tap-event-plugin'


class App extends React.Component {
  componentWillMount() {
    injectTapEventPlugin();
  }

  render() {
    return (
      <MuiThemeProvider>
        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/upload' component={Upload} />
          <Route path='/charts' component={Charts} />
        </Switch>
      </MuiThemeProvider>
    )
  }
}
export default App
