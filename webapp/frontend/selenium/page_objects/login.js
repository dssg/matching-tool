var commands = {
  login: function(user, pass) {
    return this.waitForElementVisible('@userName', 1000)
      .setValue('@userName', user)
      .setValue('@password', pass)
      .click('@submit')
  },
  standardLogin: function() {
    return this.login('testuser@example.com', 'password')
  }
}
module.exports = {
  commands: [commands],
  elements: {
    userName: { 
      selector: 'input[type=text]' 
    },
    password: {
      selector: 'input[type=password]'
    },
    submit: {
      selector: 'input[type=submit]'
    }
  }
};
