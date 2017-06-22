var React = require('react')
var auth = require('./auth')

module.exports = React.createClass({
   getInitialState: function() {
        return {
        'user':[],
        'active_sprint_name': "",
        'active_sprint_id': "",
        'active_sprint_issue_count': "",
        'sprints': [],
        'active_sprint_issues': [],
        'loader': true
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

    onSelectLoadSprintData: function(event) {
        var sprint_id = event.target.value;

        this.setState({loader: true});
        $.ajax({
            method: 'GET',
            url: '/api/sprints/?sprint_id=' + sprint_id,
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                this.setState({active_sprint_name: res.active_sprint_name,
                               active_sprint_id: res.active_sprint_id,
                               active_sprint_issue_count: res.active_sprint_issue_count,
                               loader:false,
                               active_sprint_issues: res.active_sprint_issues});
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
                this.setState({active_sprint_name: res.active_sprint_name,
                               active_sprint_id: res.active_sprint_id,
                               active_sprint_issue_count: res.active_sprint_issue_count,
                               loader:false,
                               sprints: res.sprints,
                               active_sprint_issues: res.active_sprint_issues});
            }.bind(this)
        })
    },

    render: function() {
        var active_sprint_id = this.state.active_sprint_id;
        return (
            <div>
            <h1>You are now logged in, {this.state.user.username}</h1>
            <div style={{display: this.state.loader ? 'block' : 'none' }}> Loading...</div>

            <div style={{display: this.state.loader ? 'none' : 'block'}}>
                <div> {this.state.active_sprint_name}   </div>

                <select onChange={this.onSelectLoadSprintData}  >
                {this.state.sprints.map(function(sprint) {
                   var data = sprint.split('#-#');
                    return <option value={data[1]} selected={active_sprint_id == data[1]}> {data[0]}</option>;

                })}
                </select>


                <br/><br/>

                <h2 >Active Sprint Issues</h2>
                <ol >
                {this.state.active_sprint_issues.map(function(_issue) {
                    var data = _issue.split('#-#');
                    var issue = {'title': data[0], 'assignee': data[1], 'type': data[2]}
                   return <li >{data[0]}, {issue['assignee']}</li>
                })}
                </ol>
            </div>

            <button onClick={this.logoutHandler}>Log out</button>
            </div>
        )        
    }
})
