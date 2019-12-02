import React, { Component } from 'react'
import {Form, Button} from 'react-bootstrap'
import {Typeahead} from 'react-bootstrap-typeahead';
import '../Author/Author.css'
import book from '../../imgs/book.png'

export default class Author extends Component{

    constructor(props){
        super(props);
        this.state = {
            data : [],
            author: 'Dickens Charles',
            image: '', 
            authors: [],
            selected: ''
        };
    }

    componentDidMount(){
        this.getData('Dickens Charles');
        this.getAuthors();
    }
    getAuthors = () => {
        fetch(
            `http://localhost:5000/author`,
            {
                mode:'cors',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:5000'
                }
            }
        )
        .then(res=>{
            res.json()
        .then(data=>{
                var elements = []
                data.forEach(element => {
                    elements.push(element.author)
                });
                if(data === 'ERROR')
                    this.setState({authors:[]})
                else
                    this.setState({authors:elements, isLoaded:true});
            });
        })
    }
    onChange = e => {
        this.setState({selected:e[0]})
    }
    getData = author => {
        this.setState({author})
        fetch(
            `http://localhost:5000/book_editions?author=${author}`,
            {
                mode:'cors',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:5000'
                }
            }
        )
        .then(res=>{
            res.json()
        .then(data=>{
                if(data === 'ERROR'){
                    this.setState({data:[]})
                }
                else
                    this.setState({data:data, isLoaded:true});
            });
        })

        var author_query = `http://localhost:5000/author?author=${author}`
        fetch(
            author_query,
            {
                mode:'cors',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:5000'
                }
            }
        )
        .then(res=>{
            res.json()
        .then(data=>{
                console.log(data)
                if(data === 'ERROR')
                    this.setState({image:''})
                else
                    this.setState({image:data[0].image_path, isLoaded:true});
            });
        })

    }

    queryDB = () => {       
        this.getData(this.state.selected);
    }

    render(){
        const { data} = this.state;
        var book_ids = [];
        var author_name = this.state.author;

        for (var i in data) {
            book_ids.push(
                <div key={data[i]["title"]}>
                    <div className="card">
                        <div className="container">
                            <h4><b>{data[i]["title"]}</b></h4> 
                            <p>Edition: {data[i]["edition"]}</p>
                            <p>Year: {data[i]["year"]}</p> 
                        </div>
                    </div>
                    <br/>
                </div>
            )
        }
        
        
        return (
            <div className = "wrapper">
                <Form className="search-author"> 
                    <Form.Group>
                        <Form.Label 
                            style={{fontSize:'25px', fontWeight:'bold'}}
                        >Author Search</Form.Label>
                            <Typeahead
                                id='author-input'
                                className="typeahead-input"
                                multiple={false}
                                options={this.state.authors}
                                placeholder="Author Name"
                                style={{
                                    width:'250px',
                                    overflow:'hidden'
                                }} 
                                onChange={this.onChange}
                            />
                        <Form.Text>Enter the author you wish to search for<br/>last name first</Form.Text>
                    
                    </Form.Group>
                    <Form.Group className="author-search-button">
                        <Button variant="primary" type="submit" onClick={() => this.queryDB()}>
                            Submit
                        </Button>
                    </Form.Group>
                </Form>

                <div className="box" >
                    <h1>{author_name}</h1>
                    <img 
                        src={this.state.image === ''? book:this.state.image}
                        alt = "bookpic" 
                        className="container" 
                        style={{height:'350px', width:'400px', marginBottom: '20px'}}
                    />
                    {console.log('image:'+this.state.image)}
                    <div className = "scroll-wrapper2">
                        {book_ids}
                    </div>
                </div>
            </div>    
        );
    }
}