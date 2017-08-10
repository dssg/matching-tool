import App from './components/app'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import { render } from 'react-dom'
import { createStore, combineReducers } from 'redux'
import { Router, browserHistory } from 'react-router'
import { Provider } from 'react-redux'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'

import configureStore from './store/configureStore'
import { rootReducer, initialState } from './reducers'

const store = configureStore(initialState)

render((
  <Provider store={store}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </Provider>
), document.getElementById('app'));
