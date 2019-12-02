import React, { Component } from 'react';
import logo from '../../imgs/book_logo.png';
import Body from './Body';
import './HomePage.css';

class HomePage extends Component {
    constructor(props){
        super(props);

        this.state ={
            data: []
        }

        this.wiki = this.wiki.bind(this);
    }

    wiki(element){
        window.open('https://en.wikipedia.org/wiki/'+ element.target.getAttribute("value").split(" ").slice(0,2).reverse().join("_"));
    }
    componentDidMount(){
        fetch(
            'http://localhost:5000/book_editions', 
            {
                mode:'cors',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:5000'
                }
            }
        )
        .then(res => {
            res.json().then(data => {
                this.setState({data:data});
            });
        })
        
    }

    render(){

        return (
            <div >
                {/* <MainHeader/> */}
                <div className="HomePage-body HomePage">
                <img src={logo} className="HomePage-logo" alt="logo" />
                    <Body ></Body>

                </div>
            </div>
        );
    }
}

export default HomePage;