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
      .click('@uploadLink')
      .waitForElementVisible('h2', 1000)
  },
  'pick bad HMIS stays file ': (client) => {
    var upload = client.page.upload()
    upload
      .click('@hmisStays')
      .waitForElementVisible('@browseForFile', 1000)
      .uploadBadHMIS()
      .waitForElementVisible('@tryAgainButton', 1000)
    client.end()
  },
}
