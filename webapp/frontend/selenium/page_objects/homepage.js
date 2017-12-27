module.exports = {
  elements: {
    uploadLink: { 
      selector: "//span[text()='Upload']",
      locateStrategy: 'xpath'
    },
    homeDrawer: {
      selector: "//div[@id='app']//button",
      locateStrategy: 'xpath'
    },
    logoutButton: {
      selector: "//div[text()='Logout']",
      locateStrategy: 'xpath'
    }
  }
};
