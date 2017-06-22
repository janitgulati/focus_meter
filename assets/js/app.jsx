var React = require('react')
var auth = require('./auth')

module.exports = React.createClass({
   getInitialState: function() {
        return {
        'user':[],
        'active_sprint_name': "",
        }
    },

    componentDidMount: function() {
        this.loadUserData()
        this.loadSprintsData()
    },
            
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/app/login/')
    },

    loadUserData: function() {
        $.ajax({
            method: 'GET',
            url: '/api/users/i/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                this.setState({user: res})
            }.bind(this)
        })
    },

    loadSprintsData: function() {
        $.ajax({
            method: 'GET',
            url: '/api/sprints/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                debugger;
                this.setState({active_sprint_name: res.active_sprint_name})
            }.bind(this)
        })
    },

    render: function() {
        return (
            <div>

      <div>
        <div className="choose-sprint-div text-center">
          <label htmlFor="choose-sprint"><span className="choose-sprint-span">Select Sprint: </span></label>
          <select id="choose-sprint" name="choose-sprint" className="selectpicker">
            <option value="2017-07-05">2017-07-05</option>&gt;
          </select>
        </div>
        <div className="container">
          <div className="row sprint-data-heading">
            <p className="sprint-data-heading">Data for sprint ending 2017-07-05:</p>
            <table className="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Issue Name</th>
                  <th>Issue Type</th>
                  <th>Assignee</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>MSXDEV-7500</td>
                  <td>Bug</td>
                  <td>Udit Porov</td>
                </tr>
                <tr>
                  <td>MSXDEV-7501</td>
                  <td>Support</td>
                  <td>Janit Gulati</td>
                </tr>
                <tr>
                  <td>MSXDEV-7502</td>
                  <td>New Feature</td>
                  <td>Nakul Sharma</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
        <h1>You are now logged in, {this.state.user.username}</h1>
        <div> {this.state.active_sprint_name} </div>
        <button onClick={this.logoutHandler}>Log out</button>
        </div>
        )        
    }
})
