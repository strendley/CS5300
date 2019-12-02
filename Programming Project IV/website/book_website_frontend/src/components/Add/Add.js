import React, { Component } from "react";
import "./Add.css";

const numbersOnly = RegExp(
    /^[0-9]*$/
  );

const formValid = ({ formErrors, ...rest }) => {
  let valid = true;

  // validate form errors being empty
  Object.values(formErrors).forEach(val => {
    val.length > 0 && (valid = false);
  });

  // validate the form was filled out
  Object.values(rest).forEach(val => {
    val === null && (valid = false);
  });

  return valid;
};

class Add extends Component {
  constructor(props) {
    super(props);

    this.state = {
      title: null,
      author: null,
      edition: null,
      isbn: null,
      pages: null,
      publish_year: null,
      notes: null,
      gutenberg_path: null,
      jacket_condition: null,
      binding_type: null,
      image_path: null,
      formErrors: {
        title: "",
        lastName: "",
        author: "",
        edition: "",
        isbn: "",
        pages: "",
        publish_year: "",
        notes: "",
        gutenberg_path: "",
        jacket_condition: "",
        binding_type: "",
        image_path: ""
      },
      response: '',
      error:''
    };
  }

  handleSubmit = e => {
      e.preventDefault();

      var {title,author,edition,isbn, pages, publish_year,notes,gutenberg_path, jacket_condition, binding_type, image_path} = this.state;

      title = title===null? '':`title=${title}`;
      author = author===null? '':`&author=${author}`;
      edition = edition===null? '':`&edition=${edition}`;
      isbn = isbn===null? '':`&isbn=${isbn}`;
      pages = pages===null? '':`&pages=${pages}`;
      publish_year = publish_year===null? '':`&publish_year=${publish_year}`;
      notes = notes===null? '':`&notes=${notes}`;
      gutenberg_path = gutenberg_path===null? '':`&gutenberg_path=${gutenberg_path}`;
      jacket_condition = jacket_condition===null? '':`&jacket_condition=${jacket_condition}`;
      binding_type = binding_type===null? '':`&binding_type=${binding_type}`;
      image_path = image_path===null? '':`&img_path=${image_path}`;
      
      var query_str = `http://localhost:5000/add_book?${title}${author}${edition}${isbn}${pages}${publish_year}${notes}${gutenberg_path}${jacket_condition}${binding_type}${image_path}`;

      fetch(
        query_str,
        {
          method:'post',
          mode:'cors',
          headers: {
            // "Content-Type": "text/plain",
            'Access-Control-Allow-Origin': 'http://localhost:5000'
          }
        }
      )
      .then(res=>{
          res.json()
      .then(response=>{
        console.log(response)
        if(response === 'ERROR')
            this.setState({error:true})
        else
            this.setState({error:false, response:response});
        });
      })
      if (formValid(this.state)) {
        console.log(`
          --SUBMITTING--
          Title: ${this.state.title}
          Author: ${this.state.author}
          Edition: ${this.state.edition}
        `);
      } else {
        console.error("FORM INVALID - DISPLAY ERROR MESSAGE");
      }
  };

  handleChange = e => {
    e.preventDefault();
    const { name, value } = e.target;
    let formErrors = { ...this.state.formErrors };

    switch (name) {
        case "title":
            formErrors.title =
            value.length < 1 ? "title is required" : "";
            break;
        case "author":
            formErrors.author =
            value.length < 1 ? "author is required" : "";
            break;
        case "edition":
            formErrors.edition =
            value.length < 1 ? "edition is required" : "";
            break;
        case "publish_year":
            formErrors.publish_year = numbersOnly.test(value)
            ? ""
            : "enter a valid year";
            break;
        case "pages":
            formErrors.pages = numbersOnly.test(value)
            ? ""
            : "enter a valid number of pages";
            break;
        case "gutenberg_path":
            break;
        case "image_path":
            break;
        default:
            break;
    }

    this.setState({ formErrors, [name]: value }, () => console.log(this.state));
  };

  render() {
    const { formErrors } = this.state;

    return (
      <div className="wrapper">
        <div className="form-wrapper">
          <h1>Add Book</h1>
          <form onSubmit={this.handleSubmit} noValidate>
            <div className="title">
              <label htmlFor="title">Title</label>
              <input
                className={formErrors.title.length > 0 ? "error" : null}
                placeholder="Title"
                type="text"
                name="title"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.title.length > 0 && (
                <span className="errorMessage">{formErrors.title}</span>
              )}
            </div>
            <div className="author">
              <label htmlFor="author">Author</label>
              <input
                className={formErrors.author.length > 0 ? "error" : null}
                placeholder="Author"
                type="text"
                name="author"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.author.length > 0 && (
                <span className="errorMessage">{formErrors.author}</span>
              )}
            </div>
            <div className="edition">
              <label htmlFor="edition">Edition</label>
              <input
                className={formErrors.edition.length > 0 ? "error" : null}
                placeholder="Edition"
                type="text"
                name="edition"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.edition.length > 0 && (
                <span className="errorMessage">{formErrors.edition}</span>
              )}
            </div>
            <div className="publish_year">
              <label htmlFor="publish_year">Year Published</label>
              <input
                className={formErrors.publish_year.length > 0 ? "error" : null}
                placeholder="Year Published"
                type="text"
                name="publish_year"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.publish_year.length > 0 && (
                <span className="errorMessage">{formErrors.publish_year}</span>
              )}
            </div>
            
            <div className="pages">
              <label htmlFor="pages">Pages</label>
              <input
                className={formErrors.pages.length > 0 ? "error" : null}
                placeholder="Pages"
                type="text"
                name="pages"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.pages.length > 0 && (
                <span className="errorMessage">{formErrors.pages}</span>
              )}         
            </div>    

            <div className="isbn">
              <label htmlFor="isbn">ISBN</label>
              <input
                className={formErrors.isbn.length > 0 ? "error" : null}
                placeholder="ISBN"
                type="text"
                name="isbn"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.isbn.length > 0 && (
                <span className="errorMessage">{formErrors.isbn}</span>
              )}
            </div>

            <div className="gutenberg_path">
              <label htmlFor="gutenberg_path">Gutenberg Path URL</label>
              <input
                className={formErrors.gutenberg_path.length > 0 ? "error" : null}
                placeholder="Gutenberg Path"
                type="text"
                name="gutenberg_path"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.gutenberg_path.length > 0 && (
                <span className="errorMessage">{formErrors.gutenberg_path}</span>
              )}
            </div>

            <div className="jacket_condition">
              <label htmlFor="jacket_condition">Jacket Condition</label>
              <select id="jacket_condition">
                <option value="new">New</option>
                <option value="very_good">Very Good</option>
                <option value="good">Good</option>
                <option value="fair">Fair</option>
                <option value="poor">Poor</option>

              </select>
            </div>

            <div className="binding_type">
              <label htmlFor="binding_type">Binding Type</label>
              <select id="binding_type">
                <option value="case">Case</option>
                <option value="saddle">Saddle-Stitch</option>
                <option value="perfect">Perfect</option>
                <option value="spiral">Spiral</option>
                <option value="other">Other</option>

              </select>
            </div>

            <div className="image_path">
              <label htmlFor="image_path">Image Path URL</label>
              <input
                className={formErrors.image_path.length > 0 ? "error" : null}
                placeholder="Image Path"
                type="text"
                name="image_path"
                noValidate
                onChange={this.handleChange}
              />
              {formErrors.image_path.length > 0 && (
                <span className="errorMessage">{formErrors.image_path}</span>
              )}
            </div>

            <div className="notes">
            <label htmlFor="notes">Notes</label>    
            <textarea 
                placeholder="add any additional details about the book here ..."
                value={this.state.value} 
                onChange={this.handleChange} 
                cols={40} 
                rows={10} 
            />
            </div>
                   
            <div className="addBook">
              <button type="submit">Add Book To Database</button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}

export default Add;