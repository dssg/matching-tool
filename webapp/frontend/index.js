import App from './components/app'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import { AppContainer } from 'react-hot-loader'
import { render } from 'react-dom'
import { createStore, combineReducers } from 'redux'
import { Router, browserHistory } from 'react-router'
import { Provider } from 'react-redux'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'

import configureStore from './store/configureStore'
import { rootReducer, initialState } from './reducers'

const store = configureStore(initialState)
Raven.config('https://6ff53a7b40c940eb8917a6262c04bcc8@sentry.io/1191014').install()
//const history = syncHistoryWithStore(browserHistory, store)

render((
  <Provider store={store}>
    <BrowserRouter>
      <AppContainer>
        <App />
      </AppContainer>
    </BrowserRouter>
  </Provider>
), document.getElementById('app'));

if (module.hot) {
    module.hot.accept('./components/app', () => { render(App) })
}
