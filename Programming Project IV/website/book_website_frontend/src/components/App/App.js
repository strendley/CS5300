import React, {Component} from 'react';
import { 
    HashRouter,
    Route 
} from 'react-router-dom';


import Navigation from '../Navigation';
import Years from '../Years/Years';
import Add from '../Add/Add';
import HomePage from '../HomePage';
import PlayGround from '../PlayGround';
import Author from '../Author/Author'
class App extends  Component{
  constructor(props) {
    super(props);
    this.state = {}
  }

  render() {
    return (
  
      <HashRouter>
        <div>
          <Navigation />
          <hr />
          <Route exact path="/" render={() => <HomePage {...this.props} />}/>
          <Route path={'/home'} render={() => <HomePage {...this.props} />}/>
          <Route path={'/years'} render={() => <Years {...this.props}/>} />
          <Route path={'/add_book'} render={() => <Add {...this.props}/>} />
          <Route path={'/author'} render={() => <Author {...this.props}/>} />
          <Route path={'/playground'} render={() => <PlayGround {...this.props}/>} />
        </div>
      </HashRouter>

    );
  }
}  

export default App;