import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Results from './results'
import Home from './home'
import Upload from './upload'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEventPlugin from 'react-tap-event-plugin'
import getMuiTheme from 'material-ui/styles/getMuiTheme';

const muiTheme = getMuiTheme({
  appBar: {
    height: 48,
  },
})

class App extends React.Component {
  componentWillMount() {
    injectTapEventPlugin();
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/upload' component={Upload} />
          <Route path='/results' component={Results} />
        </Switch>
      </MuiThemeProvider>
    )
  }
}
export default App
