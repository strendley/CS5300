import React, { Component } from 'react'
import '../Years/Years.css';

export default class Years extends Component {

    constructor(props){
        super(props);
        this.state = {
            data : [],
            ishidden: {}
        };
    }

    componentDidMount(){
        fetch(
            'http://localhost:5000/years',
            {
                mode:'cors',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:5000'
                }
            }
        )
        .then(res => {res.json()
        .then(data => {
                this.setState({data:data.publish_year, isLoaded:true});
                console.log("state", this.state.data)
            });
        })
    }

    handleScroll = year => {
        var new_state = this.state.ishidden;
        if (this.state.ishidden[year] ===undefined){
            new_state[year] = true;
            this.setState({ishidden: new_state})
        }
        else{
            new_state[year] = !new_state[year];
            this.setState({ishidden: new_state})
        }
    }

    render() {
        const { data, ishidden } = this.state;
        var years = Object.keys(data)
        const books = years.map(year =>
            <div className="wrap-collapsible"> 
                <div for="collapsible" className="dropdown-toggle-split" onClick={() => this.handleScroll(year)} key={year}>{year}</div>
                {
                    ishidden[year] ===false || ishidden[year] ===undefined ?
                    <br/>
                    :
                    data[year].map(title => 
                        <div key={year}>
                            <h2 style={{color:'black'}}>{title}</h2> 
                        </div>)
                }
                <br/>
            </div>
        )

        /*var arr = [];
        Object.keys(data).forEach(function(publish_year){
            arr.push(data[publish_year]);
            console.log(publish_year)
            console.log(data[publish_year])
        });*/

        return (
            <div className="wrapper" >
                <div className="scroll-wrapper" 
                    style={{
                        width: '800px',
                        height: '900px',
                        marginTop: '40px'
                    }}
                >
                    {
                        books
                    }               
                </div>
            </div>
        );
    }
}
