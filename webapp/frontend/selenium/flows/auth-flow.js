module.exports = {
  'logging in': (client) => {
    var login = client.page.login()
    login
      .navigate(client.launchUrl)
      .standardLogin()
      .getText('h1', function(comp) {
        this.assert.equal(comp.value, 'Matching Tool - Test County')
      })

    login.assert.urlContains(client.launchUrl)
  },
  'logging out': (client) => {
    var homepage = client.page.homepage()
    homepage
      .click('@homeDrawer')
      .waitForElementVisible('@logoutButton', 1000)
      .click('@logoutButton')
      .waitForElementVisible('input[type=password]', 1000)

    client.end()
  },
}
