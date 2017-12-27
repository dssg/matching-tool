module.exports = {
  'logging in': (client) => {
    var login = client.page.login()
    login
      .navigate(client.launchUrl)
      .waitForElementVisible('@userName', 1000)
      .setValue('@userName', 'countyone@example.com')
      .setValue('@password', 'password')
      .click('@submit')
      .getText('h1', function(comp) {
        this.assert.equal(comp.value, 'Matching Tool - countyone')
      })

    login.assert.urlContains(client.launchUrl)
  },
  'loading the upload page': (client) => {
    var homepage = client.page.homepage()
    homepage
      .click('@uploadLink')
      .waitForElementVisible('h2', 1000)
      .getText('h1', function(comp) {
        this.assert.equal(comp.value, 'Matching Tool - countyone')
      })
    client.end()
  },
}
