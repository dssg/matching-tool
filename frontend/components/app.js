import React from 'react'
import { Switch, Route } from 'react-router-dom'
import Home from 'components/home'
import Upload from 'components/upload'


export default () => {
    return (
      <Switch>
        <Route exact path='/' component={Home}/>
        <Route path='/upload' component={Upload}/>
      </Switch>
    )
}
