module.exports = {
  'logging in': (client) => {
    var login = client.page.login()
    login
      .navigate(client.launchUrl)
      .standardLogin()
  },
  'loading the upload page': (client) => {
    var homepage = client.page.homepage()
    homepage
      .getText('h2', function(comp) {
        this.assert.equal(comp.value, 'Integrating HMIS and Criminal Justice Data')
      })
      .click('@uploadLink')
      .waitForElementVisible('h2', 1000)
      .getText('h2', function(comp) {
        this.assert.equal(comp.value, 'Upload')
      })
    client.assert.urlContains('upload')
  },
  'pick good jail bookings file': (client) => {
    var upload = client.page.upload()
    upload
      .click('@jailBookings')
      .waitForElementVisible('@browseForFile', 1000)
      .uploadGoodBookings()
      .waitForElementVisible('@uploadConfirmButton', 1000)
  },
  'confirm upload': (client) => {
    var upload = client.page.upload()
    upload
      .waitForElementVisible('@uploadConfirmButton', 1000)
      .click('@uploadConfirmButton')
      .waitForElementVisible('@backToHomeButton', 1000)
      .click('@backToHomeButton')
      .waitForElementNotPresent('@backToHomeButton', 1000)
      
    client.assert.urlEquals(client.launchUrl)
    client.end()
  }
}
