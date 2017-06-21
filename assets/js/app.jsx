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
            <h1>You are now logged in, {this.state.user.username}</h1>
            <div> {this.state.active_sprint_name} </div>
            <button onClick={this.logoutHandler}>Log out</button>
            </div>
        )        
    }
})
