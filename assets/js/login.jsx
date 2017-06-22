var React = require('react')
var auth = require('./auth')

module.exports = React.createClass({
    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    handleSubmit: function(e) {
        e.preventDefault()

        var username = this.refs.username.value
        var pass = this.refs.pass.value

        auth.login(username, pass, (loggedIn) => {
            this.context.router.replace('/app/')
        })
    },
    
    render: function() {
        return (
              <div className="container">
                <h1 className="welcome text-center">Welcome to Focus Meter </h1>
                <div className="card card-container">
                  <h2 className="login_title text-center">Login</h2>
                  <hr />
                  <form onSubmit={this.handleSubmit} className="form-signin">
                    <span id="reauth-email" className="reauth-email" />
                    <p className="input_title">Username</p>
                    <input type="text" ref="username" className="login_box" placeholder="username" required autofocus />
                    <p className="input_title">Password</p>
                    <input type="password" ref="pass" className="login_box" placeholder="password" required />
                    <div id="remember" className="checkbox">
                      <label>
                      </label>
                    </div>
                    <button className="btn btn-lg btn-primary" type="submit">Login</button>
                  </form>
                </div>
              </div>
            );
        }
    })
